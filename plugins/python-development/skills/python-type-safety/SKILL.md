---
name: python-type-safety
description: Python 类型安全，包括类型注解、泛型、协议和严格类型检查。当添加类型注解、实现泛型类、定义结构化接口或配置 mypy/pyright 时使用。
---

# Python 类型安全

利用 Python 的类型系统在静态分析时捕获错误。类型注解作为强制性的文档，由工具自动验证。

## 何时使用本技能

- 为现有代码添加类型注解
- 创建可复用的泛型类
- 使用协议定义结构化接口
- 配置 mypy 或 pyright 进行严格检查
- 理解类型收窄和守卫
- 构建类型安全的 API 和库

## 核心概念

### 1. 类型注解

为函数参数、返回值和变量声明预期类型。

### 2. 泛型

编写可复用的代码，同时在不同类型间保留类型信息。

### 3. 协议

定义结构化接口而无需继承（具备类型安全的鸭子类型）。

### 4. 类型收窄

使用守卫和条件语句在代码块内收窄类型。

## 快速开始

```python
def get_user(user_id: str) -> User | None:
    """返回类型使'可能不存在'变得明确。"""
    ...

# 类型检查器强制要求处理 None 情况
user = get_user("123")
if user is None:
    raise UserNotFoundError("123")
print(user.name)  # 类型检查器知道这里的 user 是 User 类型
```

## 基础模式

### 模式 1：为所有公共签名添加注解

每个公共函数、方法和类都应该有类型注解。

```python
def get_user(user_id: str) -> User:
    """通过 ID 获取用户。"""
    ...

def process_batch(
    items: list[Item],
    max_workers: int = 4,
) -> BatchResult[ProcessedItem]:
    """并发处理项目。"""
    ...

class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def find_by_id(self, user_id: str) -> User | None:
        """如果找到则返回 User，否则返回 None。"""
        ...

    async def find_by_email(self, email: str) -> User | None:
        ...

    async def save(self, user: User) -> User:
        """保存用户并返回包含生成 ID 的用户。"""
        ...
```

在 CI 中使用 `mypy --strict` 或 `pyright` 以尽早发现类型错误。对于现有项目，可以使用按模块覆盖的方式增量启用严格模式。

### 模式 2：使用现代联合类型语法

Python 3.10+ 提供了更简洁的联合类型语法。

```python
# 推荐方式（3.10+）
def find_user(user_id: str) -> User | None:
    ...

def parse_value(v: str) -> int | float | str:
    ...

# 旧式写法（仍然有效，3.9 版本需要）
from typing import Optional, Union

def find_user(user_id: str) -> Optional[User]:
    ...
```

### 模式 3：使用守卫进行类型收窄

使用条件语句帮助类型检查器收窄类型。

```python
def process_user(user_id: str) -> UserData:
    user = find_user(user_id)

    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")

    # 类型检查器知道这里的 user 是 User 类型，而不是 User | None
    return UserData(
        name=user.name,
        email=user.email,
    )

def process_items(items: list[Item | None]) -> list[ProcessedItem]:
    # 过滤并收窄类型
    valid_items = [item for item in items if item is not None]
    # valid_items 现在是 list[Item] 类型
    return [process(item) for item in valid_items]
```

### 模式 4：泛型类

创建类型安全的可复用容器。

```python
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Result(Generic[T, E]):
    """表示成功值或错误之一。"""

    def __init__(
        self,
        value: T | None = None,
        error: E | None = None,
    ) -> None:
        if (value is None) == (error is None):
            raise ValueError("Exactly one of value or error must be set")
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        """获取值或抛出错误。"""
        if self._error is not None:
            raise self._error
        return self._value  # type: ignore[return-value]

    def unwrap_or(self, default: T) -> T:
        """获取值或返回默认值。"""
        if self._error is not None:
            return default
        return self._value  # type: ignore[return-value]

# 使用时保留类型信息
def parse_config(path: str) -> Result[Config, ConfigError]:
    try:
        return Result(value=Config.from_file(path))
    except ConfigError as e:
        return Result(error=e)

result = parse_config("config.yaml")
if result.is_success:
    config = result.unwrap()  # 类型：Config
```

## 高级模式

### 模式 5：泛型仓储

创建类型安全的数据访问模式。

```python
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):
    """泛型仓储接口。"""

    @abstractmethod
    async def get(self, id: ID) -> T | None:
        """通过 ID 获取实体。"""
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        """保存并返回实体。"""
        ...

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        """删除实体，如果存在则返回 True。"""
        ...

class UserRepository(Repository[User, str]):
    """使用字符串 ID 的 User 具体仓储。"""

    async def get(self, id: str) -> User | None:
        row = await self._db.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        return User(**row) if row else None

    async def save(self, entity: User) -> User:
        ...

    async def delete(self, id: str) -> bool:
        ...
```

### 模式 6：带边界的 TypeVar

将泛型参数限制为特定类型。

```python
from typing import TypeVar
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

def validate_and_create(model_cls: type[ModelT], data: dict) -> ModelT:
    """从字典创建已验证的 Pydantic 模型。"""
    return model_cls.model_validate(data)

# 适用于任何 BaseModel 子类
class User(BaseModel):
    name: str
    email: str

user = validate_and_create(User, {"name": "Alice", "email": "a@b.com"})
# user 的类型为 User

# 类型错误：str 不是 BaseModel 子类
result = validate_and_create(str, {"name": "Alice"})  # 错误！
```

### 模式 7：用于结构化类型的协议

定义接口而无需继承。

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """任何可以与字典相互序列化的类。"""

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> "Serializable":
        ...

# User 无需继承 Serializable 即可满足其要求
class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(id=data["id"], name=data["name"])

def serialize(obj: Serializable) -> str:
    """适用于任何 Serializable 对象。"""
    return json.dumps(obj.to_dict())

# 可以使用 - User 符合协议
serialize(User("1", "Alice"))

# 使用 @runtime_checkable 进行运行时检查
isinstance(User("1", "Alice"), Serializable)  # True
```

### 模式 8：常用协议模式

定义可复用的结构化接口。

```python
from typing import Protocol

class Closeable(Protocol):
    """可以关闭的资源。"""
    def close(self) -> None: ...

class AsyncCloseable(Protocol):
    """可以关闭的异步资源。"""
    async def close(self) -> None: ...

class Readable(Protocol):
    """可以从中读取的对象。"""
    def read(self, n: int = -1) -> bytes: ...

class HasId(Protocol):
    """具有 ID 属性的对象。"""
    @property
    def id(self) -> str: ...

class Comparable(Protocol):
    """支持比较的对象。"""
    def __lt__(self, other: "Comparable") -> bool: ...
    def __le__(self, other: "Comparable") -> bool: ...
```

### 模式 9：类型别名

创建有意义的类型名称。

**注意：** `type` 语句是在 Python 3.10 中引入的，用于简单别名。泛型类型语句需要 Python 3.12+。

```python
# Python 3.10+ 用于简单别名的 type 语句
type UserId = str
type UserDict = dict[str, Any]

# Python 3.12+ 带泛型的 type 语句
type Handler[T] = Callable[[Request], T]
type AsyncHandler[T] = Callable[[Request], Awaitable[T]]

# Python 3.9-3.11 风格（需要更广泛的兼容性）
from typing import TypeAlias
from collections.abc import Callable, Awaitable

UserId: TypeAlias = str
Handler: TypeAlias = Callable[[Request], Response]

# 使用
def register_handler(path: str, handler: Handler[Response]) -> None:
    ...
```

### 模式 10：可调用类型

为函数参数和回调添加类型。

```python
from collections.abc import Callable, Awaitable

# 同步回调
ProgressCallback = Callable[[int, int], None]  # (current, total)

# 异步回调
AsyncHandler = Callable[[Request], Awaitable[Response]]

# 带命名参数（使用 Protocol）
class OnProgress(Protocol):
    def __call__(
        self,
        current: int,
        total: int,
        *,
        message: str = "",
    ) -> None: ...

def process_items(
    items: list[Item],
    on_progress: ProgressCallback | None = None,
) -> list[Result]:
    for i, item in enumerate(items):
        if on_progress:
            on_progress(i, len(items))
        ...
```

## 配置

### 严格模式检查清单

符合 `mypy --strict` 要求：

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
```

增量采用目标：
- 所有函数参数都已添加注解
- 所有返回类型都已添加注解
- 类属性都已添加注解
- 最小化 `Any` 的使用（对于真正的动态数据是可以接受的）
- 泛型集合使用类型参数（`list[str]` 而非 `list`）

对于现有代码库，可以使用 `# mypy: strict` 按模块启用严格模式，或在 `pyproject.toml` 中配置按模块覆盖。

## 最佳实践总结

1. **为所有公共 API 添加注解** - 函数、方法、类属性
2. **使用 `T | None`** - 现代联合类型语法优于 `Optional[T]`
3. **运行严格类型检查** - 在 CI 中使用 `mypy --strict`
4. **使用泛型** - 在可复用代码中保留类型信息
5. **定义协议** - 使用结构化类型定义接口
6. **收窄类型** - 使用守卫帮助类型检查器
7. **限制类型变量** - 将泛型限制为有意义的类型
8. **创建类型别名** - 为复杂类型使用有意义的名称
9. **最小化 `Any`** - 使用具体类型或泛型。`Any` 仅对于真正的动态数据或与无类型的第三方代码交互时可以接受
10. **用类型文档化** - 类型是可执行的文档
