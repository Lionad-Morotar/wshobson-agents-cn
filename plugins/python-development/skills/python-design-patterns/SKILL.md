---
name: python-design-patterns
description: Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance. Use when making architecture decisions, refactoring code structure, or evaluating when abstractions are appropriate.
---

# Python 设计模式

使用基本的设计原则编写可维护的 Python 代码。这些模式帮助你构建易于理解、测试和修改的系统。

## 何时使用此技能

- 设计新的组件或服务
- 重构复杂或混乱的代码
- 决定是否创建抽象
- 在继承和组合之间做出选择
- 评估代码复杂度和耦合度
- 规划模块化架构

## 核心概念

### 1. KISS（保持简单）

选择可行的最简单解决方案。复杂度必须由具体需求来证明其合理性。

### 2. 单一职责（SRP）

每个单元应该只有一个变更原因。将关注点分离到专注的组件中。

### 3. 组合优于继承

通过组合对象来构建行为，而不是扩展类。

### 4. 三次法则

在拥有三个实例之前，不要进行抽象。重复通常比过早抽象更好。

## 快速开始

```python
# 简单胜过巧妙
# 不使用工厂/注册表模式：
FORMATTERS = {"json": JsonFormatter, "csv": CsvFormatter}

def get_formatter(name: str) -> Formatter:
    return FORMATTERS[name]()
```

## 基础模式

### 模式 1：KISS - 保持简单

在添加复杂性之前，先问：有更简单的解决方案吗？

```python
# 过度工程：带注册功能的工厂
class OutputFormatterFactory:
    _formatters: dict[str, type[Formatter]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(formatter_cls):
            cls._formatters[name] = formatter_cls
            return formatter_cls
        return decorator

    @classmethod
    def create(cls, name: str) -> Formatter:
        return cls._formatters[name]()

@OutputFormatterFactory.register("json")
class JsonFormatter(Formatter):
    ...

# 简单：直接使用字典
FORMATTERS = {
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "xml": XmlFormatter,
}

def get_formatter(name: str) -> Formatter:
    """按名称获取格式化器。"""
    if name not in FORMATTERS:
        raise ValueError(f"Unknown format: {name}")
    return FORMATTERS[name]()
```

在这里，工厂模式增加了代码但没有增加价值。把模式留给解决真正问题的时候使用。

### 模式 2：单一职责原则

每个类或函数应该只有一个变更原因。

```python
# 糟糕：处理器包揽一切
class UserHandler:
    async def create_user(self, request: Request) -> Response:
        # HTTP 解析
        data = await request.json()

        # 验证
        if not data.get("email"):
            return Response({"error": "email required"}, status=400)

        # 数据库访问
        user = await db.execute(
            "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
            data["email"], data["name"]
        )

        # 响应格式化
        return Response({"id": user.id, "email": user.email}, status=201)

# 良好：分离关注点
class UserService:
    """仅包含业务逻辑。"""

    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def create_user(self, data: CreateUserInput) -> User:
        # 这里只处理业务规则
        user = User(email=data.email, name=data.name)
        return await self._repo.save(user)

class UserHandler:
    """仅处理 HTTP 相关事务。"""

    def __init__(self, service: UserService) -> None:
        self._service = service

    async def create_user(self, request: Request) -> Response:
        data = CreateUserInput(**(await request.json()))
        user = await self._service.create_user(data)
        return Response(user.to_dict(), status=201)
```

现在 HTTP 变更不会影响业务逻辑，反之亦然。

### 模式 3：关注点分离

将代码组织成具有明确职责的不同层。

```
┌─────────────────────────────────────────────────────┐
│  API 层（处理器）                                     │
│  - 解析请求                                          │
│  - 调用服务                                          │
│  - 格式化响应                                        │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  服务层（业务逻辑）                                   │
│  - 领域规则和验证                                    │
│  - 编排操作                                          │
│  - 尽可能使用纯函数                                  │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│  仓储层（数据访问）                                   │
│  - SQL 查询                                          │
│  - 外部 API 调用                                     │
│  - 缓存操作                                          │
└─────────────────────────────────────────────────────┘
```

每一层仅依赖于其下方的层：

```python
# 仓储：数据访问
class UserRepository:
    async def get_by_id(self, user_id: str) -> User | None:
        row = await self._db.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**row) if row else None

# 服务：业务逻辑
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def get_user(self, user_id: str) -> User:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

# 处理器：HTTP 相关事务
@app.get("/users/{user_id}")
async def get_user(user_id: str) -> UserResponse:
    user = await user_service.get_user(user_id)
    return UserResponse.from_user(user)
```

### 模式 4：组合优于继承

通过组合对象而非继承来构建行为。

```python
# 继承：僵化且难以测试
class EmailNotificationService(NotificationService):
    def __init__(self):
        super().__init__()
        self._smtp = SmtpClient()  # 难以模拟

    def notify(self, user: User, message: str) -> None:
        self._smtp.send(user.email, message)

# 组合：灵活且可测试
class NotificationService:
    """通过多个渠道发送通知。"""

    def __init__(
        self,
        email_sender: EmailSender,
        sms_sender: SmsSender | None = None,
        push_sender: PushSender | None = None,
    ) -> None:
        self._email = email_sender
        self._sms = sms_sender
        self._push = push_sender

    async def notify(
        self,
        user: User,
        message: str,
        channels: set[str] | None = None,
    ) -> None:
        channels = channels or {"email"}

        if "email" in channels:
            await self._email.send(user.email, message)

        if "sms" in channels and self._sms and user.phone:
            await self._sms.send(user.phone, message)

        if "push" in channels and self._push and user.device_token:
            await self._push.send(user.device_token, message)

# 易于使用假对象进行测试
service = NotificationService(
    email_sender=FakeEmailSender(),
    sms_sender=FakeSmsSender(),
)
```

## 高级模式

### 模式 5：三次法则

在拥有三个实例之前，不要进行抽象。

```python
# 两个相似的函数？暂时不要抽象
def process_orders(orders: list[Order]) -> list[Result]:
    results = []
    for order in orders:
        validated = validate_order(order)
        result = process_validated_order(validated)
        results.append(result)
    return results

def process_returns(returns: list[Return]) -> list[Result]:
    results = []
    for ret in returns:
        validated = validate_return(ret)
        result = process_validated_return(validated)
        results.append(result)
    return results

# 这些看起来很相似，但是等等！它们真的相同吗？
# 不同的验证、不同的处理、不同的错误...
# 重复通常比错误的抽象更好

# 只有在出现第三种情况后，才考虑是否真的存在模式
# 但即使那样，有时显式比抽象更好
```

### 模式 6：函数大小指南

保持函数专注。当函数出现以下情况时进行提取：

- 超过 20-50 行（因复杂度而异）
- 服务于多个不同的目的
- 有深度嵌套的逻辑（3 层以上）

```python
# 太长，混合了多个关注点
def process_order(order: Order) -> Result:
    # 50 行验证...
    # 30 行库存检查...
    # 40 行支付处理...
    # 20 行通知...
    pass

# 更好：由专注的函数组合而成
def process_order(order: Order) -> Result:
    """通过完整工作流程处理客户订单。"""
    validate_order(order)
    reserve_inventory(order)
    payment_result = charge_payment(order)
    send_confirmation(order, payment_result)
    return Result(success=True, order_id=order.id)
```

### 模式 7：依赖注入

通过构造函数传递依赖以提高可测试性。

```python
from typing import Protocol

class Logger(Protocol):
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...

class Cache(Protocol):
    async def get(self, key: str) -> str | None: ...
    async def set(self, key: str, value: str, ttl: int) -> None: ...

class UserService:
    """带有注入依赖的服务。"""

    def __init__(
        self,
        repository: UserRepository,
        cache: Cache,
        logger: Logger,
    ) -> None:
        self._repo = repository
        self._cache = cache
        self._logger = logger

    async def get_user(self, user_id: str) -> User:
        # 首先检查缓存
        cached = await self._cache.get(f"user:{user_id}")
        if cached:
            self._logger.info("Cache hit", user_id=user_id)
            return User.from_json(cached)

        # 从数据库获取
        user = await self._repo.get_by_id(user_id)
        if user:
            await self._cache.set(f"user:{user_id}", user.to_json(), ttl=300)

        return user

# 生产环境
service = UserService(
    repository=PostgresUserRepository(db),
    cache=RedisCache(redis),
    logger=StructlogLogger(),
)

# 测试
service = UserService(
    repository=InMemoryUserRepository(),
    cache=FakeCache(),
    logger=NullLogger(),
)
```

### 模式 8：避免常见反模式

**不要暴露内部类型：**

```python
# 糟糕：将 ORM 模型暴露给 API
@app.get("/users/{id}")
def get_user(id: str) -> UserModel:  # SQLAlchemy 模型
    return db.query(UserModel).get(id)

# 良好：使用响应模式
@app.get("/users/{id}")
def get_user(id: str) -> UserResponse:
    user = db.query(UserModel).get(id)
    return UserResponse.from_orm(user)
```

**不要将 I/O 与业务逻辑混合：**

```python
# 糟糕：SQL 嵌入在业务逻辑中
def calculate_discount(user_id: str) -> float:
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    # 业务逻辑与数据访问混合

# 良好：仓储模式
def calculate_discount(user: User, order_history: list[Order]) -> float:
    # 纯业务逻辑，易于测试
    if len(order_history) > 10:
        return 0.15
    return 0.0
```

## 最佳实践总结

1. **保持简单** - 选择可行的最简单解决方案
2. **单一职责** - 每个单元只有一个变更原因
3. **分离关注点** - 具有明确目的的不同层
4. **组合，不要继承** - 组合对象以获得灵活性
5. **三次法则** - 抽象之前先等待
6. **保持函数短小** - 20-50 行（因复杂度而异），单一目的
7. **注入依赖** - 构造函数注入以提高可测试性
8. **先删除再抽象** - 删除死代码，然后考虑模式
9. **测试每一层** - 为每个关注点进行隔离测试
10. **显式胜过巧妙** - 可读的代码胜过优雅的代码
