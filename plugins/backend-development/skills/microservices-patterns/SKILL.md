---
name: microservices-patterns
description: 设计具有服务边界、事件驱动通信和弹性模式的微服务架构。在构建分布式系统、拆解单体或实现微服务时使用。
---

# 微服务模式

掌握微服务架构模式，包括服务边界、服务间通信、数据管理和弹性模式，用于构建分布式系统。

## 何时使用此技能

- 将单体应用拆解为微服务
- 设计服务边界和契约
- 实现服务间通信
- 管理分布式数据和事务
- 构建弹性分布式系统
- 实现服务发现和负载均衡
- 设计事件驱动架构

## 核心概念

### 1. 服务拆解策略

**按业务能力**

- 围绕业务功能组织服务
- 每个服务拥有自己的领域
- 示例：OrderService、PaymentService、InventoryService

**按子领域（DDD）**

- 核心领域、支撑子领域
- 限界上下文映射到服务
- 明确的所有权和责任

**绞杀者模式**

- 逐步从单体中提取
- 新功能作为微服务
- 代理路由到旧/新系统

### 2. 通信模式

**同步（请求/响应）**

- REST API
- gRPC
- GraphQL

**异步（事件/消息）**

- 事件流（Kafka）
- 消息队列（RabbitMQ、SQS）
- 发布/订阅模式

### 3. 数据管理

**每服务一数据库**

- 每个服务拥有自己的数据
- 无共享数据库
- 松耦合

**Saga 模式**

- 分布式事务
- 补偿操作
- 最终一致性

### 4. 弹性模式

**熔断器**

- 重复错误时快速失败
- 防止级联故障

**带退避的重试**

- 瞬态故障处理
- 指数退避

**舱壁隔离**

- 隔离资源
- 限制故障影响

## 服务拆解模式

### 模式 1：按业务能力

```python
# 电子商务示例

# 订单服务
class OrderService:
    """处理订单生命周期。"""

    async def create_order(self, order_data: dict) -> Order:
        order = Order.create(order_data)

        # 发布事件给其他服务
        await self.event_bus.publish(
            OrderCreatedEvent(
                order_id=order.id,
                customer_id=order.customer_id,
                items=order.items,
                total=order.total
            )
        )

        return order

# 支付服务（独立服务）
class PaymentService:
    """处理支付处理。"""

    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        # 处理支付
        result = await self.payment_gateway.charge(
            amount=payment_request.amount,
            customer=payment_request.customer_id
        )

        if result.success:
            await self.event_bus.publish(
                PaymentCompletedEvent(
                    order_id=payment_request.order_id,
                    transaction_id=result.transaction_id
                )
            )

        return result

# 库存服务（独立服务）
class InventoryService:
    """处理库存管理。"""

    async def reserve_items(self, order_id: str, items: List[OrderItem]) -> ReservationResult:
        # 检查可用性
        for item in items:
            available = await self.inventory_repo.get_available(item.product_id)
            if available < item.quantity:
                return ReservationResult(
                    success=False,
                    error=f"Insufficient inventory for {item.product_id}"
                )

        # 预留商品
        reservation = await self.create_reservation(order_id, items)

        await self.event_bus.publish(
            InventoryReservedEvent(
                order_id=order_id,
                reservation_id=reservation.id
            )
        )

        return ReservationResult(success=True, reservation=reservation)
```

### 模式 2：API 网关

```python
from fastapi import FastAPI, HTTPException, Depends
import httpx
from circuitbreaker import circuit

app = FastAPI()

class APIGateway:
    """所有客户端请求的中央入口点。"""

    def __init__(self):
        self.order_service_url = "http://order-service:8000"
        self.payment_service_url = "http://payment-service:8001"
        self.inventory_service_url = "http://inventory-service:8002"
        self.http_client = httpx.AsyncClient(timeout=5.0)

    @circuit(failure_threshold=5, recovery_timeout=30)
    async def call_order_service(self, path: str, method: str = "GET", **kwargs):
        """使用熔断器调用订单服务。"""
        response = await self.http_client.request(
            method,
            f"{self.order_service_url}{path}",
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    async def create_order_aggregate(self, order_id: str) -> dict:
        """从多个服务聚合数据。"""
        # 并行请求
        order, payment, inventory = await asyncio.gather(
            self.call_order_service(f"/orders/{order_id}"),
            self.call_payment_service(f"/payments/order/{order_id}"),
            self.call_inventory_service(f"/reservations/order/{order_id}"),
            return_exceptions=True
        )

        # 处理部分故障
        result = {"order": order}
        if not isinstance(payment, Exception):
            result["payment"] = payment
        if not isinstance(inventory, Exception):
            result["inventory"] = inventory

        return result

@app.post("/api/orders")
async def create_order(
    order_data: dict,
    gateway: APIGateway = Depends()
):
    """API 网关端点。"""
    try:
        # 路由到订单服务
        order = await gateway.call_order_service(
            "/orders",
            method="POST",
            json=order_data
        )
        return {"order": order}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail="Order service unavailable")
```

## 通信模式

### 模式 1：同步 REST 通信

```python
# 服务 A 调用服务 B
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    """带重试和超时的 HTTP 客户端。"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(5.0, connect=2.0),
            limits=httpx.Limits(max_keepalive_connections=20)
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get(self, path: str, **kwargs):
        """带自动重试的 GET 请求。"""
        response = await self.client.get(f"{self.base_url}{path}", **kwargs)
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, **kwargs):
        """POST 请求。"""
        response = await self.client.post(f"{self.base_url}{path}", **kwargs)
        response.raise_for_status()
        return response.json()

# 使用
payment_client = ServiceClient("http://payment-service:8001")
result = await payment_client.post("/payments", json=payment_data)
```

### 模式 2：异步事件驱动

```python
# 使用 Kafka 的事件驱动通信
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class DomainEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    occurred_at: datetime
    data: dict

class EventBus:
    """事件发布和订阅。"""

    def __init__(self, bootstrap_servers: List[str]):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
        await self.producer.start()

    async def publish(self, event: DomainEvent):
        """发布事件到 Kafka 主题。"""
        topic = event.event_type
        await self.producer.send_and_wait(
            topic,
            value=asdict(event),
            key=event.aggregate_id.encode()
        )

    async def subscribe(self, topic: str, handler: callable):
        """订阅事件。"""
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode()),
            group_id="my-service"
        )
        await consumer.start()

        try:
            async for message in consumer:
                event_data = message.value
                await handler(event_data)
        finally:
            await consumer.stop()

# 订单服务发布事件
async def create_order(order_data: dict):
    order = await save_order(order_data)

    event = DomainEvent(
        event_id=str(uuid.uuid4()),
        event_type="OrderCreated",
        aggregate_id=order.id,
        occurred_at=datetime.now(),
        data={
            "order_id": order.id,
            "customer_id": order.customer_id,
            "total": order.total
        }
    )

    await event_bus.publish(event)

# 库存服务监听 OrderCreated
async def handle_order_created(event_data: dict):
    """响应订单创建。"""
    order_id = event_data["data"]["order_id"]
    items = event_data["data"]["items"]

    # 预留库存
    await reserve_inventory(order_id, items)
```

### 模式 3：Saga 模式（分布式事务）

```python
# 订单履行的 Saga 编排
from enum import Enum
from typing import List, Callable

class SagaStep:
    """Saga 中的单个步骤。"""

    def __init__(
        self,
        name: str,
        action: Callable,
        compensation: Callable
    ):
        self.name = name
        self.action = action
        self.compensation = compensation

class SagaStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

class OrderFulfillmentSaga:
    """订单履行的编排 Saga。"""

    def __init__(self):
        self.steps: List[SagaStep] = [
            SagaStep(
                "create_order",
                action=self.create_order,
                compensation=self.cancel_order
            ),
            SagaStep(
                "reserve_inventory",
                action=self.reserve_inventory,
                compensation=self.release_inventory
            ),
            SagaStep(
                "process_payment",
                action=self.process_payment,
                compensation=self.refund_payment
            ),
            SagaStep(
                "confirm_order",
                action=self.confirm_order,
                compensation=self.cancel_order_confirmation
            )
        ]

    async def execute(self, order_data: dict) -> SagaResult:
        """执行 Saga 步骤。"""
        completed_steps = []
        context = {"order_data": order_data}

        try:
            for step in self.steps:
                # 执行步骤
                result = await step.action(context)
                if not result.success:
                    # 补偿
                    await self.compensate(completed_steps, context)
                    return SagaResult(
                        status=SagaStatus.FAILED,
                        error=result.error
                    )

                completed_steps.append(step)
                context.update(result.data)

            return SagaResult(status=SagaStatus.COMPLETED, data=context)

        except Exception as e:
            # 错误时补偿
            await self.compensate(completed_steps, context)
            return SagaResult(status=SagaStatus.FAILED, error=str(e))

    async def compensate(self, completed_steps: List[SagaStep], context: dict):
        """按相反顺序执行补偿操作。"""
        for step in reversed(completed_steps):
            try:
                await step.compensation(context)
            except Exception as e:
                # 记录补偿失败
                print(f"Compensation failed for {step.name}: {e}")

    # 步骤实现
    async def create_order(self, context: dict) -> StepResult:
        order = await order_service.create(context["order_data"])
        return StepResult(success=True, data={"order_id": order.id})

    async def cancel_order(self, context: dict):
        await order_service.cancel(context["order_id"])

    async def reserve_inventory(self, context: dict) -> StepResult:
        result = await inventory_service.reserve(
            context["order_id"],
            context["order_data"]["items"]
        )
        return StepResult(
            success=result.success,
            data={"reservation_id": result.reservation_id}
        )

    async def release_inventory(self, context: dict):
        await inventory_service.release(context["reservation_id"])

    async def process_payment(self, context: dict) -> StepResult:
        result = await payment_service.charge(
            context["order_id"],
            context["order_data"]["total"]
        )
        return StepResult(
            success=result.success,
            data={"transaction_id": result.transaction_id},
            error=result.error
        )

    async def refund_payment(self, context: dict):
        await payment_service.refund(context["transaction_id"])
```

## 弹性模式

### 熔断器模式

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"  # 正常运行
    OPEN = "open"      # 故障中，拒绝请求
    HALF_OPEN = "half_open"  # 测试是否恢复

class CircuitBreaker:
    """服务调用的熔断器。"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """使用熔断器执行函数。"""

        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """处理成功调用。"""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def _on_failure(self):
        """处理失败调用。"""
        self.failure_count += 1

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()

    def _should_attempt_reset(self) -> bool:
        """检查是否经过足够时间可以重试。"""
        return (
            datetime.now() - self.opened_at
            > timedelta(seconds=self.recovery_timeout)
        )

# 使用
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

async def call_payment_service(payment_data: dict):
    return await breaker.call(
        payment_client.process_payment,
        payment_data
    )
```

## 资源

- **references/service-decomposition-guide.md**：拆解单体
- **references/communication-patterns.md**：同步与异步模式
- **references/saga-implementation.md**：分布式事务
- **assets/circuit-breaker.py**：生产级熔断器
- **assets/event-bus-template.py**：Kafka 事件总线实现
- **assets/api-gateway-template.py**：完整的 API 网关

## 最佳实践

1. **服务边界**：与业务能力对齐
2. **每服务一数据库**：无共享数据库
3. **API 契约**：版本化、向后兼容
4. **尽可能异步**：事件优于直接调用
5. **熔断器**：服务故障时快速失败
6. **分布式追踪**：跨服务跟踪请求
7. **服务注册表**：动态服务发现
8. **健康检查**：存活和就绪探针

## 常见陷阱

- **分布式单体**：紧密耦合的服务
- **啰嗦的服务**：过多的服务间调用
- **共享数据库**：通过数据紧密耦合
- **无熔断器**：级联故障
- **全部同步**：紧密耦合、弹性差
- **过早微服务**：从微服务开始
- **忽略网络故障**：假设网络可靠
- **无补偿逻辑**：无法撤消失败的事务
