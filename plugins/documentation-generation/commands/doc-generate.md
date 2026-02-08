# 自动化文档生成

你是一位文档专家，专长于从代码创建全面的、可维护的文档。使用 AI 驱动的分析和行业最佳实践生成 API 文档、架构图、用户指南和技术参考。

## 上下文

用户需要自动化文档生成，从代码中提取信息、创建清晰的解释，并在文档类型之间保持一致性。专注于创建与代码保持同步的活文档。

## 需求

$ARGUMENTS

## 如何使用此工具

此工具同时提供**简明指令**（创建什么）和**详细参考示例**（如何创建）。结构：

- **指令**：高级指导和要生成的文档类型
- **参考示例**：完整的实现模式，可作为模板调整和使用

## 指令

通过分析代码库并创建以下工件来生成全面文档：

### 1. **API 文档**

- 从代码中提取端点定义、参数和响应
- 生成 OpenAPI/Swagger 规范
- 创建交互式 API 文档（Swagger UI、Redoc）
- 包含身份验证、速率限制和错误处理细节

### 2. **架构文档**

- 创建系统架构图（Mermaid、PlantUML）
- 记录组件关系和数据流
- 解释服务依赖和通信模式
- 包含可扩展性和可靠性考虑

### 3. **代码文档**

- 生成内联文档和文档字符串
- 创建包含设置、使用和贡献指南的 README 文件
- 记录配置选项和环境变量
- 提供故障排除指南和代码示例

### 4. **用户文档**

- 编写分步用户指南
- 创建入门教程
- 记录常见工作流和用例
- 包含可访问性和本地化说明

### 5. **文档自动化**

- 配置 CI/CD 管道以自动生成文档
- 设置文档检查和验证
- 实施文档覆盖检查
- 自动部署到托管平台

### 质量标准

确保所有生成的文档：

- 准确并与当前代码同步
- 使用一致的术语和格式
- 包含实用的示例和用例
- 可搜索且组织良好
- 遵循可访问性最佳实践

## 参考示例

### 示例 1：文档的代码分析

**API 文档提取**

```python
import ast
from typing import Dict, List

class APIDocExtractor:
    def extract_endpoints(self, code_path):
        """提取 API 端点及其文档"""
        endpoints = []

        with open(code_path, 'r') as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if self._is_route_decorator(decorator):
                        endpoint = {
                            'method': self._extract_method(decorator),
                            'path': self._extract_path(decorator),
                            'function': node.name,
                            'docstring': ast.get_docstring(node),
                            'parameters': self._extract_parameters(node),
                            'returns': self._extract_returns(node)
                        }
                        endpoints.append(endpoint)
        return endpoints

    def _extract_parameters(self, func_node):
        """提取带类型的函数参数"""
        params = []
        for arg in func_node.args.args:
            param = {
                'name': arg.arg,
                'type': ast.unparse(arg.annotation) if arg.annotation else None,
                'required': True
            }
            params.append(param)
        return params
```

**模式提取**

```python
def extract_pydantic_schemas(file_path):
    """为 API 文档提取 Pydantic 模型定义"""
    schemas = []

    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(base.id == 'BaseModel' for base in node.bases if hasattr(base, 'id')):
                schema = {
                    'name': node.name,
                    'description': ast.get_docstring(node),
                    'fields': []
                }

                for item in node.body:
                    if isinstance(item, ast.AnnAssign):
                        field = {
                            'name': item.target.id,
                            'type': ast.unparse(item.annotation),
                            'required': item.value is None
                        }
                        schema['fields'].append(field)
                schemas.append(schema)
    return schemas
```

### 示例 2：OpenAPI 规范生成

**OpenAPI 模板**

```yaml
openapi: 3.0.0
info:
  title: ${API_TITLE}
  version: ${VERSION}
  description: |
    ${DESCRIPTION}

    ## 身份验证
    ${AUTH_DESCRIPTION}

servers:
  - url: https://api.example.com/v1
    description: 生产服务器

security:
  - bearerAuth: []

paths:
  /users:
    get:
      summary: 列出所有用户
      operationId: listUsers
      tags:
        - 用户
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/User"
                  pagination:
                    $ref: "#/components/schemas/Pagination"
        "401":
          $ref: "#/components/responses/Unauthorized"

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
```

### 示例 3：架构图

**系统架构（Mermaid）**

```mermaid
graph TB
    subgraph "前端"
        UI[React UI]
        Mobile[移动应用]
    end

    subgraph "API 网关"
        Gateway[Kong/nginx]
        Auth[身份验证服务]
    end

    subgraph "微服务"
        UserService[用户服务]
        OrderService[订单服务]
        PaymentService[支付服务]
    end

    subgraph "数据层"
        PostgresMain[(PostgreSQL)]
        Redis[(Redis 缓存)]
        S3[S3 存储]
    end

    UI --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> UserService
    Gateway --> OrderService
    OrderService --> PaymentService
    UserService --> PostgresMain
    UserService --> Redis
    OrderService --> PostgresMain
```

**组件文档**

````markdown
## 用户服务

**目的**：管理用户账户、身份验证和配置文件

**技术栈**：

- 语言：Python 3.11
- 框架：FastAPI
- 数据库：PostgreSQL
- 缓存：Redis
- 身份验证：JWT

**API 端点**：

- `POST /users` - 创建新用户
- `GET /users/{id}` - 获取用户详细信息
- `PUT /users/{id}` - 更新用户
- `POST /auth/login` - 用户登录

**配置**：

```yaml
user_service:
  port: 8001
  database:
    host: postgres.internal
    name: users_db
  jwt:
    secret: ${JWT_SECRET}
    expiry: 3600
```
````

````

### 示例 4：README 生成

**README 模板**
```markdown
# ${PROJECT_NAME}

${BADGES}

${SHORT_DESCRIPTION}

## 功能

${FEATURES_LIST}

## 安装

### 前置要求

- Python 3.8+
- PostgreSQL 12+
- Redis 6+

### 使用 pip

```bash
pip install ${PACKAGE_NAME}
````

### 从源码安装

```bash
git clone https://github.com/${GITHUB_ORG}/${REPO_NAME}.git
cd ${REPO_NAME}
pip install -e .
```

## 快速开始

```python
${QUICK_START_CODE}
```

## 配置

### 环境变量

| 变量         | 描述                   | 默认值 | 必需   |
| ------------ | ---------------------- | ------ | ------ |
| DATABASE_URL | PostgreSQL 连接字符串  | -      | 是     |
| REDIS_URL    | Redis 连接字符串       | -      | 是     |
| SECRET_KEY   | 应用程序密钥           | -      | 是     |

## 开发

```bash
# 克隆和设置
git clone https://github.com/${GITHUB_ORG}/${REPO_NAME}.git
cd ${REPO_NAME}
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements-dev.txt

# 运行测试
pytest

# 启动开发服务器
python manage.py runserver
```

## 测试

```bash
# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=your_package
```

## 贡献

1. Fork 存储库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 打开 Pull Request

## 许可证

本项目在 ${LICENSE} 许可证下发布 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

````

### 示例 5：函数文档生成器

```python
import inspect

def generate_function_docs(func):
    """为函数生成全面的文档"""
    sig = inspect.signature(func)
    params = []
    args_doc = []

    for param_name, param in sig.parameters.items():
        param_str = param_name
        if param.annotation != param.empty:
            param_str += f": {param.annotation.__name__}"
        if param.default != param.empty:
            param_str += f" = {param.default}"
        params.append(param_str)
        args_doc.append(f"{param_name}: {param_name} 的描述")

    return_type = ""
    if sig.return_annotation != sig.empty:
        return_type = f" -> {sig.return_annotation.__name__}"

    doc_template = f'''
def {func.__name__}({", ".join(params)}){return_type}:
    """
    {func.__name__} 的简短描述

    参数：
        {chr(10).join(f"        {arg}" for arg in args_doc)}

    返回：
        返回值的描述

    示例：
        >>> {func.__name__}(example_input)
        expected_output
    """
'''
    return doc_template
`````

### 示例 6：用户指南模板

```markdown
# 用户指南

## 入门

### 创建您的第一个 ${FEATURE}

1. **导航到仪表板**

   在主导航菜单中点击 ${FEATURE} 选项卡。

2. **点击"创建新"**

   您会在右上角找到"创建新"按钮。

3. **填写详细信息**
   - **名称**：输入描述性名称
   - **描述**：添加可选的详细信息
   - **设置**：根据需要配置

4. **保存您的更改**

   点击"保存"创建您的 ${FEATURE}。

### 常见任务

#### 编辑 ${FEATURE}

1. 在列表中找到您的 ${FEATURE}
2. 点击"编辑"按钮
3. 进行更改
4. 点击"保存"

#### 删除 ${FEATURE}

> ⚠️ **警告**：删除是永久性的，无法撤消。

1. 在列表中找到您的 ${FEATURE}
2. 点击"删除"按钮
3. 确认删除

### 故障排除

| 错误                | 含义                   | 解决方案       |
| ------------------- | ---------------------- | -------------- |
| "Name required"     | 名称字段为空           | 输入名称       |
| "Permission denied" | 您没有访问权限         | 联系管理员     |
| "Server error"      | 技术问题               | 稍后再试       |
```

### 示例 7：交互式 API 游乐场

**Swagger UI 设置**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>API 文档</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui.css"
    />
  </head>
  <body>
    <div id="swagger-ui"></div>

    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js"></script>
    <script>
      window.onload = function () {
        SwaggerUIBundle({
          url: "/api/openapi.json",
          dom_id: "#swagger-ui",
          deepLinking: true,
          presets: [SwaggerUIBundle.presets.apis],
          layout: "StandaloneLayout",
        });
      };
    </script>
  </body>
</html>
```

**代码示例生成器**

```python
def generate_code_examples(endpoint):
    """以多种语言为 API 端点生成代码示例"""
    examples = {}

    # Python
    examples['python'] = f'''
import requests

url = "https://api.example.com{endpoint['path']}"
headers = {{"Authorization": "Bearer YOUR_API_KEY"}}

response = requests.{endpoint['method'].lower()}(url, headers=headers)
print(response.json())
'''

    # JavaScript
    examples['javascript'] = f'''
const response = await fetch('https://api.example.com{endpoint['path']}', {{
    method: '{endpoint['method']}',
    headers: {{'Authorization': 'Bearer YOUR_API_KEY'}}
}});

const data = await response.json();
console.log(data);
'''

    # cURL
    examples['curl'] = f'''
curl -X {endpoint['method']} https://api.example.com{endpoint['path']} \\
    -H "Authorization: Bearer YOUR_API_KEY"
'''

    return examples
```

### 示例 8：文档 CI/CD

**GitHub Actions 工作流**

```yaml
name: 生成文档

on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "api/**"

jobs:
  generate-docs:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: 设置 Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 安装依赖
        run: |
          pip install -r requirements-docs.txt
          npm install -g @redocly/cli

      - name: 生成 API 文档
        run: |
          python scripts/generate_openapi.py > docs/api/openapi.json
          redocly build-docs docs/api/openapi.json -o docs/api/index.html

      - name: 生成代码文档
        run: sphinx-build -b html docs/source docs/build

      - name: 部署到 GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build
```

### 示例 9：文档覆盖验证

```python
import ast
import glob

class DocCoverage:
    def check_coverage(self, codebase_path):
        """检查代码库的文档覆盖"""
        results = {
            'total_functions': 0,
            'documented_functions': 0,
            'total_classes': 0,
            'documented_classes': 0,
            'missing_docs': []
        }

        for file_path in glob.glob(f"{codebase_path}/**/*.py", recursive=True):
            module = ast.parse(open(file_path).read())

            for node in ast.walk(module):
                if isinstance(node, ast.FunctionDef):
                    results['total_functions'] += 1
                    if ast.get_docstring(node):
                        results['documented_functions'] += 1
                    else:
                        results['missing_docs'].append({
                            'type': 'function',
                            'name': node.name,
                            'file': file_path,
                            'line': node.lineno
                        })

                elif isinstance(node, ast.ClassDef):
                    results['total_classes'] += 1
                    if ast.get_docstring(node):
                        results['documented_classes'] += 1
                    else:
                        results['missing_docs'].append({
                            'type': 'class',
                            'name': node.name,
                            'file': file_path,
                            'line': node.lineno
                        })

        # 计算覆盖百分比
        results['function_coverage'] = (
            results['documented_functions'] / results['total_functions'] * 100
            if results['total_functions'] > 0 else 100
        )
        results['class_coverage'] = (
            results['documented_classes'] / results['total_classes'] * 100
            if results['total_classes'] > 0 else 100
        )

        return results
```

## 输出格式

1. **API 文档**：带交互式游乐场的 OpenAPI 规范
2. **架构图**：系统、序列和组件图
3. **代码文档**：内联文档、文档字符串和类型提示
4. **用户指南**：分步教程
5. **开发者指南**：设置、贡献和 API 使用指南
6. **参考文档**：带示例的完整 API 参考
7. **文档站点**：具有搜索功能的已部署静态站点

专注于创建准确、全面且易于与代码更改一起维护的文档。
