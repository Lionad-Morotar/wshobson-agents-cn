# Temporal Python 测试的本地开发设置

使用 pytest 集成和覆盖率跟踪设置本地 Temporal 开发环境的综合指南。

## 使用 Docker Compose 设置 Temporal Server

### 基本 Docker Compose 配置

```yaml
# docker-compose.yml
version: "3.8"

services:
  temporal:
    image: temporalio/auto-setup:latest
    container_name: temporal-dev
    ports:
      - "7233:7233" # Temporal 服务器
      - "8233:8233" # Web UI
    environment:
      - DB=postgresql
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgresql
      - DYNAMIC_CONFIG_FILE_PATH=config/dynamicconfig/development-sql.yaml
    depends_on:
      - postgresql

  postgresql:
    image: postgres:14-alpine
    container_name: temporal-postgres
    environment:
      - POSTGRES_USER=temporal
      - POSTGRES_PASSWORD=temporal
      - POSTGRES_DB=temporal
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  temporal-ui:
    image: temporalio/ui:latest
    container_name: temporal-ui
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - TEMPORAL_CORS_ORIGINS=http://localhost:3000
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

### 启动本地服务器

```bash
# 启动 Temporal 服务器
docker-compose up -d

# 验证服务器正在运行
docker-compose ps

# 查看日志
docker-compose logs -f temporal

# 访问 Temporal Web UI
open http://localhost:8080

# 停止服务器
docker-compose down

# 重置数据（清空）
docker-compose down -v
```

### 健康检查脚本

```python
# scripts/health_check.py
import asyncio
from temporalio.client import Client

async def check_temporal_health():
    """验证 Temporal 服务器可访问"""
    try:
        client = await Client.connect("localhost:7233")
        print("✓ 已连接到 Temporal 服务器")

        # 测试工作流执行
        from temporalio.worker import Worker

        @workflow.defn
        class HealthCheckWorkflow:
            @workflow.run
            async def run(self) -> str:
                return "healthy"

        async with Worker(
            client,
            task_queue="health-check",
            workflows=[HealthCheckWorkflow],
        ):
            result = await client.execute_workflow(
                HealthCheckWorkflow.run,
                id="health-check",
                task_queue="health-check",
            )
            print(f"✓ 工作流执行成功: {result}")

        return True

    except Exception as e:
        print(f"✗ 健康检查失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_temporal_health())
```

## pytest 配置

### 项目结构

```
temporal-project/
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── src/
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── order_workflow.py
│   │   └── payment_workflow.py
│   └── activities/
│       ├── __init__.py
│       ├── payment_activities.py
│       └── inventory_activities.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_workflows.py
│   │   └── test_activities.py
│   ├── integration/
│   │   └── test_order_flow.py
│   └── replay/
│       └── test_workflow_replay.py
└── scripts/
    ├── health_check.py
    └── export_histories.py
```

### pytest 配置

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 用于测试分类的标记
markers =
    unit: 单元测试（快速、隔离）
    integration: 集成测试（需要 Temporal 服务器）
    replay: 重放测试（需要生产历史）
    slow: 慢速运行测试

# 覆盖率设置
addopts =
    --verbose
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

# 异步测试超时
asyncio_default_fixture_loop_scope = function
```

### 共享测试夹具

```python
# tests/conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.client import Client

@pytest.fixture(scope="session")
def event_loop():
    """为异步夹具提供事件循环"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def temporal_client():
    """提供连接到本地服务器的 Temporal 客户端"""
    client = await Client.connect("localhost:7233")
    yield client
    await client.close()

@pytest.fixture(scope="module")
async def workflow_env():
    """模块范围的时间跳跃环境"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """函数范围的活动环境"""
    from temporalio.testing import ActivityEnvironment
    return ActivityEnvironment()

@pytest.fixture
async def test_worker(temporal_client, workflow_env):
    """预配置的测试 Worker"""
    from temporalio.worker import Worker
    from src.workflows import OrderWorkflow, PaymentWorkflow
    from src.activities import process_payment, update_inventory

    return Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[OrderWorkflow, PaymentWorkflow],
        activities=[process_payment, update_inventory],
    )
```

### 依赖项

```txt
# requirements.txt
temporalio>=1.5.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-xdist>=3.3.0  # 并行测试执行
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_backend"

[project]
name = "temporal-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "temporalio>=1.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## 覆盖率配置

### 覆盖率设置

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    # 排除类型检查块
    if TYPE_CHECKING:
    # 排除调试代码
    def __repr__
    # 排除抽象方法
    @abstractmethod
    # 排除 pass 语句
    pass

[html]
directory = htmlcov
```

### 使用覆盖率运行测试

```bash
# 运行所有测试并生成覆盖率
pytest --cov=src --cov-report=term-missing

# 生成 HTML 覆盖率报告
pytest --cov=src --cov-report=html
open htmlcov/index.html

# 运行特定测试类别
pytest -m unit  # 仅单元测试
pytest -m integration  # 仅集成测试
pytest -m "not slow"  # 跳过慢速测试

# 并行执行（更快）
pytest -n auto  # 使用所有 CPU 核心

# 覆盖率低于阈值时失败
pytest --cov=src --cov-fail-under=80
```

### 覆盖率报告示例

```
---------- coverage: platform darwin, python 3.11.5 -----------
名称                                语句   缺失   覆盖率   缺失行
-----------------------------------------------------------------
src/__init__.py                         0      0   100%
src/activities/__init__.py              2      0   100%
src/activities/inventory.py            45      3    93%   78-80
src/activities/payment.py              38      0   100%
src/workflows/__init__.py               2      0   100%
src/workflows/order_workflow.py        67      5    93%   45-49
src/workflows/payment_workflow.py      52      0   100%
-----------------------------------------------------------------
总计                                 206      8    96%

10 个文件因完全覆盖率而跳过。
```

## 开发工作流

### 日常开发流程

```bash
# 1. 启动 Temporal 服务器
docker-compose up -d

# 2. 验证服务器健康
python scripts/health_check.py

# 3. 开发期间运行测试
pytest tests/unit/ --verbose

# 4. 提交前运行完整测试套件
pytest --cov=src --cov-report=term-missing

# 5. 检查覆盖率
open htmlcov/index.html

# 6. 停止服务器
docker-compose down
```

### 预提交钩子

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "运行测试..."
pytest --cov=src --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo "测试失败。提交已中止。"
    exit 1
fi

echo "所有测试通过！"
```

### 常见任务的 Makefile

```makefile
# Makefile
.PHONY: setup test test-unit test-integration coverage clean

setup:
	docker-compose up -d
	pip install -r requirements.txt
	python scripts/health_check.py

test:
	pytest --cov=src --cov-report=term-missing

test-unit:
	pytest -m unit --verbose

test-integration:
	pytest -m integration --verbose

test-replay:
	pytest -m replay --verbose

test-parallel:
	pytest -n auto --cov=src

coverage:
	pytest --cov=src --cov-report=html
	open htmlcov/index.html

clean:
	docker-compose down -v
	rm -rf .pytest_cache htmlcov .coverage

ci:
	docker-compose up -d
	sleep 10  # 等待 Temporal 启动
	pytest --cov=src --cov-fail-under=80
	docker-compose down
```

### CI/CD 示例

```yaml
# .github/workflows/test.yml
name: 测试

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: 设置 Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 启动 Temporal 服务器
        run: docker-compose up -d

      - name: 等待 Temporal
        run: sleep 10

      - name: 安装依赖
        run: |
          pip install -r requirements.txt

      - name: 运行测试并生成覆盖率
        run: |
          pytest --cov=src --cov-report=xml --cov-fail-under=80

      - name: 上传覆盖率
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

      - name: 清理
        if: always()
        run: docker-compose down
```

## 调试技巧

### 启用 Temporal SDK 日志

```python
import logging

# 为 Temporal SDK 启用调试日志
logging.basicConfig(level=logging.DEBUG)
temporal_logger = logging.getLogger("temporalio")
temporal_logger.setLevel(logging.DEBUG)
```

### 交互式调试

```python
# 在测试中添加断点
@pytest.mark.asyncio
async def test_workflow_with_breakpoint(workflow_env):
    import pdb; pdb.set_trace()  # 在此处调试

    async with Worker(...):
        result = await workflow_env.client.execute_workflow(...)
```

### Temporal Web UI

```bash
# 在 http://localhost:8080 访问 Web UI
# - 查看工作流执行
# - 检查事件历史
# - 重放工作流
# - 监控 Worker
```

## 最佳实践

1. **隔离环境**：使用 Docker Compose 实现可重现的本地设置
2. **健康检查**：运行测试前始终验证 Temporal 服务器
3. **快速反馈**：使用 pytest 标记快速运行单元测试
4. **覆盖率目标**：保持 ≥80% 代码覆盖率
5. **并行测试**：使用 pytest-xdist 加快测试运行
6. **CI/CD 集成**：每次提交时自动测试
7. **清理**：如需要在测试运行之间清除 Docker 卷

## 故障排除

**问题：Temporal 服务器未启动**

```bash
# 检查日志
docker-compose logs temporal

# 重置数据库
docker-compose down -v
docker-compose up -d
```

**问题：测试超时**

```python
# 在 pytest.ini 中增加超时
asyncio_default_timeout = 30
```

**问题：端口已被使用**

```bash
# 查找使用端口 7233 的进程
lsof -i :7233

# 终止进程或在 docker-compose.yml 中更改端口
```

## 额外资源

- Temporal 本地开发：docs.temporal.io/develop/python/local-dev
- pytest 文档：docs.pytest.org
- Docker Compose：docs.docker.com/compose
- pytest-asyncio：github.com/pytest-dev/pytest-asyncio