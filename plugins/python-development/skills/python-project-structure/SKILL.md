---
name: python-project-structure
description: Python project organization, module architecture, and public API design. Use when setting up new projects, organizing modules, defining public interfaces with __all__, or planning directory layouts.
---

# Python 项目结构与模块架构

设计组织良好的 Python 项目，具有清晰的模块边界、明确的公共接口和可维护的目录结构。良好的组织使代码可发现，且变更可预测。

## 何时使用此技能

- 从零开始新的 Python 项目
- 为清晰性重组现有代码库
- 使用 `__all__` 定义模块公共 API
- 决定使用扁平还是嵌套目录结构
- 确定测试文件放置策略
- 创建可重用的库包

## 核心概念

### 1. 模块内聚

将一起变化的相关代码分组。模块应具有单一、明确的目的。

### 2. 显式接口

使用 `__all__` 定义公开内容。未列出的所有内容都是内部实现细节。

### 3. 扁平层次结构

优先使用浅层目录结构。仅为真正的子域增加深度。

### 4. 一致约定

在整个项目中统一应用命名和组织模式。

## 快速开始

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── services/
│       ├── models/
│       └── api/
├── tests/
├── pyproject.toml
└── README.md
```

## 基础模式

### 模式 1：单文件单概念

每个文件应专注于单个概念或密切相关的一组函数。当文件出现以下情况时考虑拆分：

- 处理多个不相关的职责
- 增长超过 300-500 行（根据复杂度而异）
- 包含因不同原因而变化的类

```python
# 推荐：专注的文件
# user_service.py - 用户业务逻辑
# user_repository.py - 用户数据访问
# user_models.py - 用户数据结构

# 避免：大杂烩文件
# user.py - 包含服务、仓储、模型、工具...
```

### 模式 2：使用 `__all__` 定义显式公共 API

为每个模块定义公共接口。未列出的成员是内部实现细节。

```python
# mypackage/services/__init__.py
from .user_service import UserService
from .order_service import OrderService
from .exceptions import ServiceError, ValidationError

__all__ = [
    "UserService",
    "OrderService",
    "ServiceError",
    "ValidationError",
]

# 内部辅助函数通过省略保持私有
# from .internal_helpers import _validate_input  # 未导出
```

### 模式 3：扁平目录结构

优先使用最小嵌套。深层层次会使导入冗长，导航困难。

```
# 推荐：扁平结构
project/
├── api/
│   ├── routes.py
│   └── middleware.py
├── services/
│   ├── user_service.py
│   └── order_service.py
├── models/
│   ├── user.py
│   └── order.py
└── utils/
    └── validation.py

# 避免：深层嵌套
project/core/internal/services/impl/user/
```

仅在存在需要隔离的真正子域时才添加子包。

### 模式 4：测试文件组织

选择一种方法并在整个项目中一致应用。

**选项 A：并排测试**

```
src/
├── user_service.py
├── test_user_service.py
├── order_service.py
└── test_order_service.py
```

优势：测试位于它们验证的代码旁边。易于查看覆盖缺口。

**选项 B：并行测试目录**

```
src/
├── services/
│   ├── user_service.py
│   └── order_service.py
tests/
├── services/
│   ├── test_user_service.py
│   └── test_order_service.py
```

优势：生产代码和测试代码之间清晰分离。大型项目的标准。

## 高级模式

### 模式 5：包初始化

使用 `__init__.py` 为包使用者提供干净的公共接口。

```python
# mypackage/__init__.py
"""MyPackage - 用于做有用事情的库。"""

from .core import MainClass, HelperClass
from .exceptions import PackageError, ConfigError
from .config import Settings

__all__ = [
    "MainClass",
    "HelperClass",
    "PackageError",
    "ConfigError",
    "Settings",
]

__version__ = "1.0.0"
```

然后使用者可以直接从包导入：

```python
from mypackage import MainClass, Settings
```

### 模式 6：分层架构

按架构层组织代码，以清晰分离关注点。

```
myapp/
├── api/           # HTTP 处理器、请求/响应
│   ├── routes/
│   └── middleware/
├── services/      # 业务逻辑
├── repositories/  # 数据访问
├── models/        # 领域实体
├── schemas/       # API 模式（Pydantic）
└── config/        # 配置
```

每层应仅依赖于其下方的层，而非上方。

### 模式 7：领域驱动结构

对于复杂应用，按业务域而非技术层组织。

```
ecommerce/
├── users/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
├── orders/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
└── shared/
    ├── database.py
    └── exceptions.py
```

## 文件和模块命名

### 约定

- 所有文件和模块名使用 `snake_case`：`user_repository.py`
- 避免模糊含义的缩写：`user_repository.py` 而非 `usr_repo.py`
- 类名与文件名匹配：`user_service.py` 中的 `UserService`

### 导入风格

使用绝对导入以获得清晰性和可靠性：

```python
# 推荐：绝对导入
from myproject.services import UserService
from myproject.models import User

# 避免：相对导入
from ..services import UserService
from . import models
```

相对导入在模块移动或重组时可能中断。

## 最佳实践总结

1. **保持文件专注** - 单文件单概念，在 300-500 行时考虑拆分（根据复杂度而异）
2. **显式定义 `__all__`** - 使公共接口清晰
3. **优先扁平结构** - 仅为真正的子域增加深度
4. **使用绝对导入** - 更可靠、更清晰
5. **保持一致** - 在整个项目中统一应用模式
6. **名称与内容匹配** - 文件名应描述其用途
7. **分离关注点** - 保持层分明，依赖单向流动
8. **记录结构** - 包含解释组织的 README
