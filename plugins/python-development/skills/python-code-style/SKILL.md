---
name: python-code-style
description: Python code style, linting, formatting, naming conventions, and documentation standards. Use when writing new code, reviewing style, configuring linters, writing docstrings, or establishing project standards.
---

# Python 代码风格与文档

一致的代码风格和清晰的文档使代码库更易于维护和协作。本技能涵盖现代 Python 工具链、命名约定和文档标准。

## 何时使用本技能

- 为新项目设置代码检查和格式化
- 编写或审查文档字符串
- 建立团队编码标准
- 配置 ruff、mypy 或 pyright
- 审查代码的风格一致性
- 创建项目文档

## 核心概念

### 1. 自动化格式化

让工具来处理格式化争议。一次配置，自动执行。

### 2. 一致的命名

遵循 PEP 8 规范，使用有意义、描述性的名称。

### 3. 文档即代码

文档字符串应与其描述的代码一同维护。

### 4. 类型注解

现代 Python 代码应为所有公共 API 包含类型提示。

## 快速开始

```bash
# 安装现代工具链
pip install ruff mypy

# 在 pyproject.toml 中配置
[tool.ruff]
line-length = 120
target-version = "py312"  # 根据项目的最低 Python 版本调整

[tool.mypy]
strict = true
```

## 基础模式

### 模式 1: 现代 Python 工具链

使用 `ruff` 作为一体化代码检查器和格式化工具。它用单个快速工具替代了 flake8、isort 和 black。

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py312"  # 根据项目的最低 Python 版本调整

[tool.ruff.lint]
select = [
    "E",    # pycodestyle 错误
    "W",    # pycodestyle 警告
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
]
ignore = ["E501"]  # 行长度由格式化工具处理

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

运行命令：

```bash
ruff check --fix .  # 检查并自动修复
ruff format .       # 格式化代码
```

### 模式 2: 类型检查配置

为生产代码配置严格类型检查。

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

替代方案：使用 `pyright` 进行更快的检查。

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

### 模式 3: 命名约定

遵循 PEP 8，强调清晰胜于简洁。

**文件和模块：**

```python
# 推荐：描述性的 snake_case
user_repository.py
order_processing.py
http_client.py

# 避免：缩写
usr_repo.py
ord_proc.py
http_cli.py
```

**类和函数：**

```python
# 类：PascalCase
class UserRepository:
    pass

class HTTPClientFactory:  # 缩写词保持大写
    pass

# 函数和变量：snake_case
def get_user_by_email(email: str) -> User | None:
    retry_count = 3
    max_connections = 100
```

**常量：**

```python
# 模块级常量：SCREAMING_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com"
```

### 模式 4: 导入组织

按一致的顺序组织导入：标准库、第三方包、本地导入。

```python
# 标准库
import os
from collections.abc import Callable
from typing import Any

# 第三方包
import httpx
from pydantic import BaseModel
from sqlalchemy import Column

# 本地导入
from myproject.models import User
from myproject.services import UserService
```

仅使用绝对导入：

```python
# 推荐
from myproject.utils import retry_decorator

# 避免相对导入
from ..utils import retry_decorator
```

## 高级模式

### 模式 5: Google 风格文档字符串

为所有公共类、方法和函数编写文档字符串。

**简单函数：**

```python
def get_user(user_id: str) -> User:
    """通过唯一标识符检索用户。"""
    ...
```

**复杂函数：**

```python
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """使用工作线程池并发处理项目。

    使用配置数量的工作线程处理批次中的每个项目。
    可以通过可选回调函数监控进度。

    Args:
        items: 要处理的项目。不能为空。
        max_workers: 最大并发工作线程数。默认为 4。
        on_progress: 可选回调函数，接收（已完成，总数）计数。

    Returns:
        BatchResult，包含成功项目和所有失败项目及其关联异常。

    Raises:
        ValueError: 如果 items 为空。
        ProcessingError: 如果无法处理批次。

    Example:
        >>> result = process_batch(items, max_workers=8)
        >>> print(f"Processed {len(result.succeeded)} items")
    """
    ...
```

**类文档字符串：**

```python
class UserService:
    """用于管理用户操作的服务。

    提供创建、检索、更新和删除用户的方法，具有适当的验证
    和错误处理。

    Attributes:
        repository: 用于用户持久化的数据访问层。
        logger: 用于操作跟踪的日志记录器实例。

    Example:
        >>> service = UserService(repository, logger)
        >>> user = service.create_user(CreateUserInput(...))
    """

    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        """初始化用户服务。

        Args:
            repository: 用户的数据访问层。
            logger: 用于跟踪操作的日志记录器。
        """
        self.repository = repository
        self.logger = logger
```

### 模式 6: 行长度和格式化

将行长度设置为 120 字符以适应现代显示器，同时保持可读性。

```python
# 推荐：可读的换行
def create_user(
    email: str,
    name: str,
    role: UserRole = UserRole.MEMBER,
    notify: bool = True,
) -> User:
    ...

# 推荐：清晰地链接方法调用
result = (
    db.query(User)
    .filter(User.active == True)
    .order_by(User.created_at.desc())
    .limit(10)
    .all()
)

# 推荐：格式化长字符串
error_message = (
    f"Failed to process user {user_id}: "
    f"received status {response.status_code} "
    f"with body {response.text[:100]}"
)
```

### 模式 7: 项目文档

**README 结构：**

```markdown
# 项目名称

对项目功能的简要描述。

## 安装

\`\`\`bash
pip install myproject
\`\`\`

## 快速开始

\`\`\`python
from myproject import Client

client = Client(api_key="...")
result = client.process(data)
\`\`\`

## 配置

记录环境变量和配置选项。

## 开发

\`\`\`bash
pip install -e ".[dev]"
pytest
\`\`\`
```

**CHANGELOG 格式（Keep a Changelog）：**

```markdown
# Changelog

## [Unreleased]

### Added
- 新功能 X

### Changed
- 修改了 Y 的行为

### Fixed
- 修复了 Z 的错误
```

## 最佳实践总结

1. **使用 ruff** - 代码检查和格式化的单一工具
2. **启用严格的 mypy** - 在运行前捕获类型错误
3. **120 字符行** - 可读性的现代标准
4. **描述性名称** - 清晰胜于简洁
5. **绝对导入** - 比相对导入更易维护
6. **Google 风格文档字符串** - 一致、可读的文档
7. **记录公共 API** - 每个公共函数都需要文档字符串
8. **保持文档更新** - 将文档视为代码
9. **在 CI 中自动化** - 在每次提交时运行代码检查工具
10. **面向 Python 3.10+** - 对于新项目，推荐 Python 3.12+ 以获得现代语言特性
