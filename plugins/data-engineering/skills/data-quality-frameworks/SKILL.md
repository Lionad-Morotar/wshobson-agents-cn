---
name: data-quality-frameworks
description: 使用 Great Expectations、dbt 测试、data contracts 和自动化质量检查实施数据质量的框架和模式。涵盖 expectation suites、checkpoints、自定义测试和质量指标。
---

# 数据质量框架

使用 Great Expectations、dbt 测试、data contracts 和自动化质量检查实施可靠数据质量框架的综合模式。这些模式确保数据可靠性、及早发现问题，并在整个数据管道中维护数据标准。

## 简介

数据质量框架提供结构化的方法来验证、监控和维护整个数据管道中的数据质量。这包括：

- **Great Expectations**：基于 Python 的数据文档、质量期望和验证框架
- **dbt Tests**：dbt 模型中基于 SQL 的测试，用于确保数据完整性和业务逻辑
- **Data Contracts**：定义服务之间数据模式、类型和质量标准的形式化协议
- **Automated Quality Checks**：对数据质量指标的持续监控和告警

这些框架共同工作，创建全面的数据质量保证，在问题影响下游系统之前捕获它们。

## 模式

### 1. Expectation Suites

**目标**：使用 Great Expectations suites 定义全面的数据质量期望。

**描述**：创建可重用的 expectation suites，根据定义的质量规则验证数据，包括类型检查、值范围和自定义业务逻辑。

**Implementation**:

```python
import great_expectations as ge
from great_expectations.core.batch import RuntimeBatchRequest

# 创建数据上下文
context = ge.get_context()

# 定义 expectation suite
suite = context.add_or_update_expectation_suite("user_data_suite")

# 添加期望
expectations = [
    # 列存在性和类型
    {
        "expectation_type": "expect_table_columns_to_match_ordered_list",
        "kwargs": {"column_list": ["user_id", "email", "created_at"]}
    },
    {
        "expectation_type": "expect_column_values_to_be_of_type",
        "kwargs": {"column": "user_id", "type_": "integer"}
    },
    
    # 值约束
    {
        "expectation_type": "expect_column_values_to_be_between",
        "kwargs": {"column": "age", "min_value": 18, "max_value": 120}
    },
    {
        "expectation_type": "expect_column_values_to_be_in_set",
        "kwargs": {"column": "status", "value_set": ["active", "inactive", "pending"]}
    },
    
    # 唯一性和完整性
    {
        "expectation_type": "expect_column_values_to_be_unique",
        "kwargs": {"column": "user_id"}
    },
    {
        "expectation_type": "expect_column_values_to_not_be_null",
        "kwargs": {"column": "email"}
    },
    
    # 字符串模式
    {
        "expectation_type": "expect_column_values_to_match_regex",
        "kwargs": {"column": "email", "regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"}
    },
    
    # 自定义业务逻辑
    {
        "expectation_type": "expect_column_values_to_be_increasing",
        "kwargs": {"column": "created_at"}
    }
]

for exp in expectations:
    suite.add_expectation(**exp)

# 保存 suite
context.save_expectation_suite(suite)
```

**关键特性**：
- **列验证**：检查列存在性、类型和顺序
- **值约束**：验证范围、集合和模式
- **业务逻辑**：实现自定义验证规则
- **可重用性**：跨环境共享 expectation suites

### 2. Checkpoints 和验证

**目标**：使用 Great Expectations checkpoints 自动化数据验证。

**描述**：创建 checkpoints，对数据批次运行 expectation suites，生成验证报告，并在失败时触发告警。

**Implementation**:

```yaml
# great_expectations.yml
config_variables_file_name: config_variables.yml

stores:
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: expectations/
  
  validations_store:
    class_name: ValidationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/validations/
  
  evaluation_parameter_store:
    class_name: EvaluationParameterStore

expectations_store_name: expectations_store
validations_store_name: validations_store
evaluation_parameter_store_name: evaluation_parameter_store

data_docs_sites:
  local_site:
    class_name: SiteBuilder
    show_how_to_buttons: true
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/data_docs/local_site
    site_index_builder:
      class_name: DefaultSiteIndexBuilder

checkpoint_config:
  class_name: SimpleCheckpoint
```

```python
# 创建 checkpoint
checkpoint_config = {
    "name": "user_data_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "run_name_template": "%Y%m%d-%H%M%S-user-data-validation",
    "expectation_suite_name": "user_data_suite",
    "action_list": [
        {
            "name": "store_validation_result",
            "action": {
                "class_name": "StoreValidationResultAction"
            }
        },
        {
            "name": "store_evaluation_params",
            "action": {
                "class_name": "StoreEvaluationParametersAction"
            }
        },
        {
            "name": "update_data_docs",
            "action": {
                "class_name": "UpdateDataDocsAction",
                "site_name": "local_site"
            }
        }
    ]
}

checkpoint = context.add_or_update_checkpoint(**checkpoint_config)

# 运行 checkpoint
batch_request = RuntimeBatchRequest(
    datasource_name="my_datasource",
    data_connector_name="runtime_data_connector",
    data_asset_name="user_data",
    batch_identifiers={"batch_id": "latest"},
    runtime_parameters={"batch_data": user_data_df}
)

validation_result = checkpoint.run(batch_request=batch_request)

# 检查结果
if validation_result["success"]:
    print("✓ All expectations passed")
else:
    print("✗ Validation failed")
    for result in validation_result["results"]:
        if not result["success"]:
            print(f"  - {result['expectation_config']['expectation_type']}: {result['expectation_config']['kwargs']}")
```

**关键特性**：
- **自动化验证**：按计划或事件触发运行检查
- **丰富的报告**：生成详细的验证报告和数据文档
- **告警**：在验证失败时触发通知
- **集成**：与 Airflow 等编排工具集成

### 3. dbt 测试

**目标**：在 dbt 模型中实现基于 SQL 的测试以确保数据完整性。

**描述**：创建 dbt 测试，直接在转换层验证数据质量，确保数据完整性和业务逻辑合规性。

**Implementation**:

```sql
-- models/schema.yml

version: 2

models:
  - name: users
    description: "包含全面属性的用户维度表"
    columns:
      - name: user_id
        description: "每个用户的唯一标识符"
        tests:
          - unique
          - not_null
      
      - name: email
        description: "用户电子邮件地址"
        tests:
          - unique
          - not_null
      
      - name: age
        description: "用户年龄"
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: "age >= 18"
      
      - name: status
        description: "用户账户状态"
        tests:
          - not_null
          - dbt_utils.relationships_where:
              to: ref('status_lookup')
              field: status_code
              from_condition: status IS NOT NULL
      
      - name: country
        description: "用户所在国家"
        tests:
          - dbt_utils.is_in_reasonable_unit:
              reason: "ISO 3166-1 alpha-2 国家代码"
              values: ['US', 'CA', 'GB', 'FR', 'DE', 'JP', 'AU']
```

```sql
-- tests/generic/user_email_format.sql

{% test user_email_format(model) %}

SELECT *
FROM {{ model }}
WHERE email NOT REGEXP '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

{% endtest %}
```

```sql
-- tests/generic/user_has_recent_activity.sql

{% test user_has_recent_activity(model, date_column, days) %}

WITH latest_activity AS (
    SELECT MAX({{ date_column }}) as last_activity
    FROM {{ model }}
)

SELECT 1
FROM {{ model }}, latest_activity
WHERE {{ date_column }} < DATEADD(day, -{{ days }}, CURRENT_DATE)
HAVING COUNT(*) > 0

{% endtest %}
```

```sql
-- models/users.yml (续)

models:
  - name: users
    columns:
      - name: email
        tests:
          - user_email_format
      
      - name: last_activity_date
        tests:
          - user_has_recent_activity:
              date_column: last_activity_date
              days: 30
```

**关键特性**：
- **内置测试**：使用标准测试如 unique、not_null、relationships
- **自定义测试**：创建特定领域的测试逻辑
- **集成**：测试随 dbt run 自动运行
- **文档**：测试作为活文档

### 4. 自定义 dbt 测试

**目标**：创建高级的、特定领域的 dbt 测试以进行复杂验证。

**描述**：实现自定义 dbt 测试，用于复杂业务逻辑、多表验证和高级数据质量检查。

**Implementation**:

```sql
-- tests/generic/range_check.sql

{% test range_check(model, column, min_value, max_value) %}

SELECT *
FROM {{ model }}
WHERE {{ column }} < {{ min_value }} OR {{ column }} > {{ max_value }}

{% endtest %}
```

```sql
-- tests/generic/multi_column_reference.sql

{% test multi_column_reference(model, column_list, reference_model, reference_column_list) %}

WITH model_values AS (
    SELECT {{ column_list|join(', ') }}
    FROM {{ model }}
    GROUP BY {{ column_list|join(', ') }}
),

reference_values AS (
    SELECT {{ reference_column_list|join(', ') }}
    FROM {{ reference_model }}
    GROUP BY {{ reference_column_list|join(', ') }}
)

SELECT mv.*
FROM model_values mv
LEFT JOIN reference_values rv
  ON mv.{{ column_list[0] }} = rv.{{ reference_column_list[0] }}
WHERE rv.{{ reference_column_list[0] }} IS NULL

{% endtest %}
```

```sql
-- tests/generic/business_rule.sql

{% test business_rule(model, rule_description, rule_sql) %}

{{ rule_description }}:
此测试验证自定义业务规则。

规则 SQL: {{ rule_sql }}

SELECT *
FROM {{ model }}
WHERE NOT ({{ rule_sql }})

{% endtest %}
```

```sql
-- models/schema.yml (使用方法)

models:
  - name: orders
    columns:
      - name: order_amount
        tests:
          - range_check:
              min_value: 0
              max_value: 1000000
      
      - name: user_id
        tests:
          - multi_column_reference:
              column_list: ['user_id', 'region']
              reference_model: ref('users')
              reference_column_list: ['user_id', 'region']
      
      - name: discount_percentage
        tests:
          - business_rule:
              rule_description: "普通客户的折扣不应超过 50%"
              rule_sql: "customer_type = 'premium' OR discount_percentage <= 50"
```

**关键特性**：
- **可重用逻辑**：创建参数化的测试宏
- **业务规则**：将复杂业务逻辑编码为测试
- **跨表验证**：验证表之间的关系
- **可维护性**：在宏中集中测试逻辑

### 5. Data Contracts

**目标**：定义和强制执行服务之间的 data contracts。

**描述**：创建形式化的 data contracts，指定服务之间数据交换的模式、数据类型、约束和质量标准。

**Implementation**:

```python
# data_contract.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class FieldDefinition:
    name: str
    type: str
    nullable: bool = False
    unique: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[str]] = None
    pattern: Optional[str] = None

@dataclass
class DataContract:
    name: str
    version: str
    description: str
    fields: List[FieldDefinition]
    owner: str
    created_at: datetime
    updated_at: datetime
    sla: Optional[dict] = None

# 定义 contract
user_contract = DataContract(
    name="user_data_contract",
    version="1.0.0",
    description="服务之间交换的用户数据 contract",
    owner="data-team@company.com",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    sla={
        "freshness": "1 hour",
        "completeness": "99.9%",
        "accuracy": "99.5%"
    },
    fields=[
        FieldDefinition(
            name="user_id",
            type="integer",
            nullable=False,
            unique=True
        ),
        FieldDefinition(
            name="email",
            type="string",
            nullable=False,
            unique=True,
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        ),
        FieldDefinition(
            name="age",
            type="integer",
            nullable=False,
            min_value=18,
            max_value=120
        ),
        FieldDefinition(
            name="status",
            type="string",
            nullable=False,
            allowed_values=["active", "inactive", "pending"]
        ),
        FieldDefinition(
            name="created_at",
            type="timestamp",
            nullable=False
        )
    ]
)

# 根据 contract 验证数据
def validate_contract(data: pd.DataFrame, contract: DataContract) -> dict:
    results = {
        "valid": True,
        "errors": []
    }
    
    for field in contract.fields:
        # 检查空值
        if not field.nullable and data[field.name].isnull().any():
            results["valid"] = False
            results["errors"].append(f"字段 '{field.name}' 包含空值")
        
        # 检查唯一性
        if field.unique and data[field.name].duplicated().any():
            results["valid"] = False
            results["errors"].append(f"字段 '{field.name}' 包含重复值")
        
        # 检查值范围
        if field.min_value is not None and (data[field.name] < field.min_value).any():
            results["valid"] = False
            results["errors"].append(f"字段 '{field.name}' 包含低于最小值的值")
        
        if field.max_value is not None and (data[field.name] > field.max_value).any():
            results["valid"] = False
            results["errors"].append(f"字段 '{field.name}' 包含高于最大值的值")
        
        # 检查允许的值
        if field.allowed_values:
            invalid = ~data[field.name].isin(field.allowed_values)
            if invalid.any():
                results["valid"] = False
                results["errors"].append(f"字段 '{field.name}' 包含无效值")
    
    return results

# 使用方法
validation_result = validate_contract(user_data_df, user_contract)
print(validation_result)
```

**关键特性**：
- **模式定义**：形式化的模式规范
- **类型安全**：强制执行数据类型和约束
- **SLA 强制执行**：定义和监控服务级别协议
- **版本控制**：跟踪 contract 随时间的变化

### 6. 自动化质量管道

**目标**：构建自动化管道以持续监控数据质量。

**描述**：创建自动化管道，运行质量检查、生成报告、触发告警，并维护数据质量仪表板。

**Implementation**:

```python
# quality_pipeline.py
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack import SlackAPIPostOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-quality',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_quality_pipeline',
    default_args=default_args,
    description='自动化数据质量监控管道',
    schedule_interval='0 */6 * * *',  # 每 6 小时
    catchup=False,
    tags=['data-quality', 'monitoring']
)

def run_great_expectations_checkpoint():
    context = ge.get_context()
    checkpoint = context.get_checkpoint("user_data_checkpoint")
    result = checkpoint.run()
    
    if not result["success"]:
        raise Exception("Great Expectations 验证失败")
    
    return result

def run_dbt_tests():
    import subprocess
    result = subprocess.run(
        ['dbt', 'test', '--select', 'users'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"dbt 测试失败: {result.stderr}")
    
    return result.stdout

def check_data_freshness():
    query = """
        SELECT 
            MAX(created_at) as latest_record,
            TIMESTAMPDIFF(HOUR, MAX(created_at), NOW()) as hours_since_latest
        FROM users
    """
    
    df = pd.read_sql(query, engine)
    
    if df['hours_since_latest'].iloc[0] > 2:
        raise Exception(f"数据新鲜度告警: 距离最新记录 {df['hours_since_latest'].iloc[0]} 小时")
    
    return df.to_dict()

def generate_quality_report():
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "total_records": len(user_data_df),
        "null_counts": user_data_df.isnull().sum().to_dict(),
        "duplicate_count": user_data_df.duplicated().sum(),
        "data_freshness": check_data_freshness()
    }
    
    # 保存报告
    with open(f"reports/quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(metrics, f, indent=2)
    
    return metrics

def send_slack_alert(context):
    task_instance = context['task_instance']
    error_message = task_instance.xcom_pull(task_ids=context['task'].upstream_task_ids[-1])
    
    SlackAPIPostOperator(
        task_id='slack_alert',
        slack_conn_id='slack',
        channel='#data-quality',
        text=f"""
🚨 *数据质量告警*

*任务*: {context['task'].task_id}
*DAG*: {context['dag'].dag_id}
*错误*: {str(error_message)}
*时间*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """,
        username='Data Quality Bot'
    ).execute(context=context)

# 定义任务
ge_task = PythonOperator(
    task_id='run_great_expectations',
    python_callable=run_great_expectations_checkpoint,
    dag=dag
)

dbt_task = PythonOperator(
    task_id='run_dbt_tests',
    python_callable=run_dbt_tests,
    dag=dag
)

freshness_task = PythonOperator(
    task_id='check_data_freshness',
    python_callable=check_data_freshness,
    dag=dag
)

report_task = PythonOperator(
    task_id='generate_quality_report',
    python_callable=generate_quality_report,
    dag=dag
)

alert_task = SlackAPIPostOperator(
    task_id='send_slack_alert',
    slack_conn_id='slack',
    channel='#data-quality',
    text="""
🚨 *数据质量告警*

一个或多个质量检查失败。请进行调查。
    """,
    trigger_rule='one_failed',
    dag=dag
)

# 设置任务依赖
[ge_task, dbt_task, freshness_task] >> report_task >> alert_task
```

**关键特性**：
- **自动化检查**：自动计划并运行质量检查
- **告警**：在质量失败时触发告警
- **报告**：生成全面的质量报告
- **集成**：与编排平台集成

## 最佳实践

1. **从简单开始**：从基本验证开始，逐步增加复杂性
2. **具体明确**：为关键数据质量规则创建有针对性的测试
3. **自动化**：自动化质量检查以尽早发现问题
4. **监控**：持续监控质量指标和趋势
5. **文档**：记录质量规则及其业务依据
6. **版本控制**：将质量定义存储在版本控制中
7. **定期审查**：随着数据需求的发展审查和更新测试

## 资源

- [Great Expectations 文档](https://docs.greatexpectations.io/)
- [dbt 测试指南](https://docs.getdbt.com/docs/build/tests)
- [Data Contract 规范](https://www.datacontract.com/)
- [数据质量最佳实践](https://www.datamesh-architecture.com/data-quality)
