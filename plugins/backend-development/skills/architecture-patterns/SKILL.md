---
name: architecture-patterns
description: 实施经过验证的后端架构模式，包括整洁架构、六边形架构和领域驱动设计。在架构复杂后端系统或重构现有应用以提高可维护性时使用。
---

# 架构模式

掌握经过验证的后端架构模式，包括整洁架构、六边形架构和领域驱动设计，以构建可维护、可测试和可扩展的系统。

## 何时使用此技能

- 从头开始设计新的后端系统
- 重构单体应用以提高可维护性
- 为团队建立架构标准
- 从紧密耦合迁移到松散耦合架构
- 实施领域驱动设计原则
- 创建可测试和可模拟的代码库
- 规划微服务分解

## 核心概念

### 1. 整洁架构（Uncle Bob）

**层级（依赖向内流动）：**

- **实体**：核心业务模型
- **用例**：应用业务规则
- **接口适配器**：控制器、展示器、网关
- **框架和驱动**：UI、数据库、外部服务

**关键原则：**

- 依赖指向内部
- 内层不了解外层
- 业务逻辑独立于框架
- 可在没有 UI、数据库或外部服务的情况下测试

### 2. 六边形架构（端口和适配器）

**组件：**

- **领域核心**：业务逻辑
- **端口**：定义交互的接口
- **适配器**：端口的实现（数据库、REST、消息队列）

**优势：**

- 轻松交换实现（测试用模拟）
- 技术不可知的核心
- 清晰的关注点分离

### 3. 领域驱动设计（DDD）

**战略模式：**

- **限界上下文**：不同域的独立模型
- **上下文映射**：上下文如何关联
- **通用语言**：共享术语

**战术模式：**

- **实体**：具有身份的对象
- **值对象**：由属性定义的不可变对象
- **聚合**：一致性边界
- **仓储**：数据访问抽象
- **领域事件**：发生的事情

## 整洁架构模式

### 目录结构

```
app/
├── domain/           # 实体和业务规则
│   ├── entities/
│   │   ├── user.py
│   │   └── order.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── money.py
│   └── interfaces/   # 抽象接口
│       ├── user_repository.py
│       └── payment_gateway.py
├── use_cases/        # 应用业务规则
│   ├── create_user.py
│   ├── process_order.py
│   └── send_notification.py
├── adapters/         # 接口实现
│   ├── repositories/
│   │   ├── postgres_user_repository.py
│   │   └── redis_cache_repository.py
│   ├── controllers/
│   │   └── user_controller.py
│   └── gateways/
│       ├── stripe_payment_gateway.py
│       └── sendgrid_email_gateway.py
└── infrastructure/   # 框架和外部关注点
    ├── database.py
    ├── config.py
    └── logging.py
```

### 实施示例

```python
# domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """核心用户实体 - 无框架依赖。"""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """业务规则：停用用户。"""
        self.is_active = False

    def can_place_order(self) -> bool:
        """业务规则：活跃用户可以下单。"""
        return self.is_active

# domain/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.user import User

class IUserRepository(ABC):
    """端口：定义契约，无实现。"""

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

# use_cases/create_user.py
from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user: User
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """用例：编排业务逻辑。"""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # 业务验证
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(
                user=None,
                success=False,
                error="邮箱已存在"
            )

        # 创建实体
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now(),
            is_active=True
        )

        # 持久化
        saved_user = await self.user_repository.save(user)

        return CreateUserResponse(
            user=saved_user,
            success=True
        )

# adapters/repositories/postgres_user_repository.py
from domain.interfaces.user_repository import IUserRepository
from domain.entities.user import User
from typing import Optional
import asyncpg

class PostgresUserRepository(IUserRepository):
    """适配器：PostgreSQL 实现。"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None

    async def find_by_email(self, email: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )
            return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (id, email, name, created_at, is_active)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE
                SET email = $2, name = $3, is_active = $5
                """,
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user

    async def delete(self, user_id: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE id = $1", user_id
            )
            return result == "DELETE 1"

    def _to_entity(self, row) -> User:
        """将数据库行映射到实体。"""
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            created_at=row["created_at"],
            is_active=row["is_active"]
        )

# adapters/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from use_cases.create_user import CreateUserUseCase, CreateUserRequest
from pydantic import BaseModel

router = APIRouter()

class CreateUserDTO(BaseModel):
    email: str
    name: str

@router.post("/users")
async def create_user(
    dto: CreateUserDTO,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """控制器：仅处理 HTTP 关注点。"""
    request = CreateUserRequest(email=dto.email, name=dto.name)
    response = await use_case.execute(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)

    return {"user": response.user}
```

## 六边形架构模式

```python
# 核心领域（六边形中心）
class OrderService:
    """领域服务 - 无基础设施依赖。"""

    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        payment_gateway: PaymentGatewayPort,
        notification_service: NotificationPort
    ):
        self.orders = order_repository
        self.payments = payment_gateway
        self.notifications = notification_service

    async def place_order(self, order: Order) -> OrderResult:
        # 业务逻辑
        if not order.is_valid():
            return OrderResult(success=False, error="无效订单")

        # 使用端口（接口）
        payment = await self.payments.charge(
            amount=order.total,
            customer=order.customer_id
        )

        if not payment.success:
            return OrderResult(success=False, error="支付失败")

        order.mark_as_paid()
        saved_order = await self.orders.save(order)

        await self.notifications.send(
            to=order.customer_email,
            subject="订单已确认",
            body=f"订单 {order.id} 已确认"
        )

        return OrderResult(success=True, order=saved_order)

# 端口（接口）
class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order:
        pass

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        pass

class NotificationPort(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str):
        pass

# 适配器（实现）
class StripePaymentAdapter(PaymentGatewayPort):
    """主适配器：连接到 Stripe API。"""

    def __init__(self, api_key: str):
        self.stripe = stripe
        self.stripe.api_key = api_key

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        try:
            charge = self.stripe.Charge.create(
                amount=amount.cents,
                currency=amount.currency,
                customer=customer
            )
            return PaymentResult(success=True, transaction_id=charge.id)
        except stripe.error.CardError as e:
            return PaymentResult(success=False, error=str(e))

class MockPaymentAdapter(PaymentGatewayPort):
    """测试适配器：无外部依赖。"""

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

## 领域驱动设计模式

```python
# 值对象（不可变）
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Email:
    """值对象：已验证的邮箱。"""
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("无效邮箱")

@dataclass(frozen=True)
class Money:
    """值对象：带货币的金额。"""
    amount: int  # 分
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("货币不匹配")
        return Money(self.amount + other.amount, self.currency)

# 实体（具有身份）
class Order:
    """实体：具有身份、可变状态。"""

    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []

    def add_item(self, product: Product, quantity: int):
        """实体内的业务逻辑。"""
        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))

    def total(self) -> Money:
        """计算属性。"""
        return sum(item.subtotal() for item in self.items)

    def submit(self):
        """带业务规则的状态转换。"""
        if not self.items:
            raise ValueError("无法提交空订单")
        if self.status != OrderStatus.PENDING:
            raise ValueError("订单已提交")

        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))

# 聚合（一致性边界）
class Customer:
    """聚合根：控制对实体的访问。"""

    def __init__(self, id: str, email: Email):
        self.id = id
        self.email = email
        self._addresses: List[Address] = []
        self._orders: List[str] = []  # 订单 ID，不是完整对象

    def add_address(self, address: Address):
        """聚合强制执行不变量。"""
        if len(self._addresses) >= 5:
            raise ValueError("最多允许 5 个地址")
        self._addresses.append(address)

    @property
    def primary_address(self) -> Optional[Address]:
        return next((a for a in self._addresses if a.is_primary), None)

# 领域事件
@dataclass
class OrderSubmittedEvent:
    order_id: str
    occurred_at: datetime = field(default_factory=datetime.now)

# 仓储（聚合持久化）
class OrderRepository:
    """仓储：持久化/检索聚合。"""

    async def find_by_id(self, order_id: str) -> Optional[Order]:
        """从存储重新构建聚合。"""
        pass

    async def save(self, order: Order):
        """持久化聚合并发布事件。"""
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

## 资源

- **references/clean-architecture-guide.md**：详细的层级分解
- **references/hexagonal-architecture-guide.md**：端口和适配器模式
- **references/ddd-tactical-patterns.md**：实体、值对象、聚合
- **assets/clean-architecture-template/**：完整项目结构
- **assets/ddd-examples/**：领域建模示例

## 最佳实践

1. **依赖规则**：依赖始终指向内部
2. **接口隔离**：小而专注的接口
3. **领域内的业务逻辑**：将框架排除在核心之外
4. **测试独立性**：核心可无基础设施测试
5. **限界上下文**：清晰的领域边界
6. **通用语言**：一致的术语
7. **瘦控制器**：委托给用例
8. **丰富领域模型**：数据伴随行为

## 常见陷阱

- **贫血领域**：只有数据没有行为的实体
- **框架耦合**：业务逻辑依赖于框架
- **胖控制器**：控制器中的业务逻辑
- **仓储泄漏**：暴露 ORM 对象
- **缺少抽象**：核心中的具体依赖
- **过度设计**：为简单 CRUD 使用整洁架构