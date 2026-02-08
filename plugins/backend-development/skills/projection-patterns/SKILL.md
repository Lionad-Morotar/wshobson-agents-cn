---
name: projection-patterns
description: 从事件流构建读模型和投影。在实现 CQRS 读侧、构建物化视图或优化事件溯源系统中的查询性能时使用。
---

# 投影模式

为事件溯源系统构建投影和读模型的综合指南。

## 何时使用此技能

- 构建 CQRS 读模型
- 从事件创建物化视图
- 优化查询性能
- 实现实时仪表板
- 从事件构建搜索索引
- 跨流聚合数据

## 核心概念

### 1. 投影架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 事件存储    │────►│ 投影器      │────►│ 读模型      │
│             │     │             │     │ (数据库)    │
│ ┌─────────┐ │     │ ┌─────────┐ │     │ ┌─────────┐ │
│ │ 事件    │ │     │ │ 处理器  │ │     │ │ 表      │ │
│ └─────────┘ │     │ │ 逻辑    │ │     │ │ 视图    │ │
│             │     │ └─────────┘ │     │ │ 缓存    │ │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 2. 投影类型

| 类型           | 描述                 | 用例                   |
| -------------- | -------------------- | ---------------------- |
| **实时**       | 从订阅实时处理       | 当前状态查询           |
| **追赶**       | 处理历史事件         | 重建读模型             |
| **持久化**     | 存储检查点           | 重启后恢复             |
| **内联**       | 与写入在同一事务     | 强一致性               |

## 模板

### 模板 1：基本投影器

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Callable, List
import asyncpg

@dataclass
class Event:
    stream_id: str
    event_type: str
    data: dict
    version: int
    global_position: int


class Projection(ABC):
    """投影基类。"""

    @property
    @abstractmethod
    def name(self) -> str:
        """用于检查点的唯一投影名称。"""
        pass

    @abstractmethod
    def handles(self) -> List[str]:
        """此投影处理的事件类型列表。"""
        pass

    @abstractmethod
    async def apply(self, event: Event) -> None:
        """将事件应用到读模型。"""
        pass


class Projector:
    """从事件存储运行投影。"""

    def __init__(self, event_store, checkpoint_store):
        self.event_store = event_store
        self.checkpoint_store = checkpoint_store
        self.projections: List[Projection] = []

    def register(self, projection: Projection):
        self.projections.append(projection)

    async def run(self, batch_size: int = 100):
        """连续运行所有投影。"""
        while True:
            for projection in self.projections:
                await self._run_projection(projection, batch_size)
            await asyncio.sleep(0.1)

    async def _run_projection(self, projection: Projection, batch_size: int):
        checkpoint = await self.checkpoint_store.get(projection.name)
        position = checkpoint or 0

        events = await self.event_store.read_all(position, batch_size)

        for event in events:
            if event.event_type in projection.handles():
                await projection.apply(event)

            await self.checkpoint_store.save(
                projection.name,
                event.global_position
            )

    async def rebuild(self, projection: Projection):
        """从头重建投影。"""
        await self.checkpoint_store.delete(projection.name)
        # 可选地清除读模型表
        await self._run_projection(projection, batch_size=1000)
```

### 模板 2：订单摘要投影

```python
class OrderSummaryProjection(Projection):
    """将订单事件投影到摘要读模型。"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.pool = db_pool

    @property
    def name(self) -> str:
        return "order_summary"

    def handles(self) -> List[str]:
        return [
            "OrderCreated",
            "OrderItemAdded",
            "OrderItemRemoved",
            "OrderShipped",
            "OrderCompleted",
            "OrderCancelled"
        ]

    async def apply(self, event: Event) -> None:
        handlers = {
            "OrderCreated": self._handle_created,
            "OrderItemAdded": self._handle_item_added,
            "OrderItemRemoved": self._handle_item_removed,
            "OrderShipped": self._handle_shipped,
            "OrderCompleted": self._handle_completed,
            "OrderCancelled": self._handle_cancelled,
        }

        handler = handlers.get(event.event_type)
        if handler:
            await handler(event)

    async def _handle_created(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO order_summaries
                (order_id, customer_id, status, total_amount, item_count, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                event.data['order_id'],
                event.data['customer_id'],
                'pending',
                0,
                0,
                event.data['created_at']
            )

    async def _handle_item_added(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE order_summaries
                SET total_amount = total_amount + $2,
                    item_count = item_count + 1,
                    updated_at = NOW()
                WHERE order_id = $1
                """,
                event.data['order_id'],
                event.data['price'] * event.data['quantity']
            )

    async def _handle_item_removed(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE order_summaries
                SET total_amount = total_amount - $2,
                    item_count = item_count - 1,
                    updated_at = NOW()
                WHERE order_id = $1
                """,
                event.data['order_id'],
                event.data['price'] * event.data['quantity']
            )

    async def _handle_shipped(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE order_summaries
                SET status = 'shipped',
                    shipped_at = $2,
                    updated_at = NOW()
                WHERE order_id = $1
                """,
                event.data['order_id'],
                event.data['shipped_at']
            )

    async def _handle_completed(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE order_summaries
                SET status = 'completed',
                    completed_at = $2,
                    updated_at = NOW()
                WHERE order_id = $1
                """,
                event.data['order_id'],
                event.data['completed_at']
            )

    async def _handle_cancelled(self, event: Event):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE order_summaries
                SET status = 'cancelled',
                    cancelled_at = $2,
                    cancellation_reason = $3,
                    updated_at = NOW()
                WHERE order_id = $1
                """,
                event.data['order_id'],
                event.data['cancelled_at'],
                event.data.get('reason')
            )
```

### 模板 3：Elasticsearch 搜索投影

```python
from elasticsearch import AsyncElasticsearch

class ProductSearchProjection(Projection):
    """将产品事件投影到 Elasticsearch 进行全文搜索。"""

    def __init__(self, es_client: AsyncElasticsearch):
        self.es = es_client
        self.index = "products"

    @property
    def name(self) -> str:
        return "product_search"

    def handles(self) -> List[str]:
        return [
            "ProductCreated",
            "ProductUpdated",
            "ProductPriceChanged",
            "ProductDeleted"
        ]

    async def apply(self, event: Event) -> None:
        if event.event_type == "ProductCreated":
            await self.es.index(
                index=self.index,
                id=event.data['product_id'],
                document={
                    'name': event.data['name'],
                    'description': event.data['description'],
                    'category': event.data['category'],
                    'price': event.data['price'],
                    'tags': event.data.get('tags', []),
                    'created_at': event.data['created_at']
                }
            )

        elif event.event_type == "ProductUpdated":
            await self.es.update(
                index=self.index,
                id=event.data['product_id'],
                doc={
                    'name': event.data['name'],
                    'description': event.data['description'],
                    'category': event.data['category'],
                    'tags': event.data.get('tags', []),
                    'updated_at': event.data['updated_at']
                }
            )

        elif event.event_type == "ProductPriceChanged":
            await self.es.update(
                index=self.index,
                id=event.data['product_id'],
                doc={
                    'price': event.data['new_price'],
                    'price_updated_at': event.data['changed_at']
                }
            )

        elif event.event_type == "ProductDeleted":
            await self.es.delete(
                index=self.index,
                id=event.data['product_id']
            )
```

### 模板 4：聚合投影

```python
class DailySalesProjection(Projection):
    """按天聚合销售数据用于报告。"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.pool = db_pool

    @property
    def name(self) -> str:
        return "daily_sales"

    def handles(self) -> List[str]:
        return ["OrderCompleted", "OrderRefunded"]

    async def apply(self, event: Event) -> None:
        if event.event_type == "OrderCompleted":
            await self._increment_sales(event)
        elif event.event_type == "OrderRefunded":
            await self._decrement_sales(event)

    async def _increment_sales(self, event: Event):
        date = event.data['completed_at'][:10]  # YYYY-MM-DD
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO daily_sales (date, total_orders, total_revenue, total_items)
                VALUES ($1, 1, $2, $3)
                ON CONFLICT (date) DO UPDATE SET
                    total_orders = daily_sales.total_orders + 1,
                    total_revenue = daily_sales.total_revenue + $2,
                    total_items = daily_sales.total_items + $3,
                    updated_at = NOW()
                """,
                date,
                event.data['total_amount'],
                event.data['item_count']
            )

    async def _decrement_sales(self, event: Event):
        date = event.data['original_completed_at'][:10]
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE daily_sales SET
                    total_orders = total_orders - 1,
                    total_revenue = total_revenue - $2,
                    total_refunds = total_refunds + $2,
                    updated_at = NOW()
                WHERE date = $1
                """,
                date,
                event.data['refund_amount']
            )
```

### 模板 5：多表投影

```python
class CustomerActivityProjection(Projection):
    """跨多个表投影客户活动。"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.pool = db_pool

    @property
    def name(self) -> str:
        return "customer_activity"

    def handles(self) -> List[str]:
        return [
            "CustomerCreated",
            "OrderCompleted",
            "ReviewSubmitted",
            "CustomerTierChanged"
        ]

    async def apply(self, event: Event) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                if event.event_type == "CustomerCreated":
                    # 插入到客户表
                    await conn.execute(
                        """
                        INSERT INTO customers (customer_id, email, name, tier, created_at)
                        VALUES ($1, $2, $3, 'bronze', $4)
                        """,
                        event.data['customer_id'],
                        event.data['email'],
                        event.data['name'],
                        event.data['created_at']
                    )
                    # 初始化活动摘要
                    await conn.execute(
                        """
                        INSERT INTO customer_activity_summary
                        (customer_id, total_orders, total_spent, total_reviews)
                        VALUES ($1, 0, 0, 0)
                        """,
                        event.data['customer_id']
                    )

                elif event.event_type == "OrderCompleted":
                    # 更新活动摘要
                    await conn.execute(
                        """
                        UPDATE customer_activity_summary SET
                            total_orders = total_orders + 1,
                            total_spent = total_spent + $2,
                            last_order_at = $3
                        WHERE customer_id = $1
                        """,
                        event.data['customer_id'],
                        event.data['total_amount'],
                        event.data['completed_at']
                    )
                    # 插入到订单历史
                    await conn.execute(
                        """
                        INSERT INTO customer_order_history
                        (customer_id, order_id, amount, completed_at)
                        VALUES ($1, $2, $3, $4)
                        """,
                        event.data['customer_id'],
                        event.data['order_id'],
                        event.data['total_amount'],
                        event.data['completed_at']
                    )

                elif event.event_type == "ReviewSubmitted":
                    await conn.execute(
                        """
                        UPDATE customer_activity_summary SET
                            total_reviews = total_reviews + 1,
                            last_review_at = $2
                        WHERE customer_id = $1
                        """,
                        event.data['customer_id'],
                        event.data['submitted_at']
                    )

                elif event.event_type == "CustomerTierChanged":
                    await conn.execute(
                        """
                        UPDATE customers SET tier = $2, updated_at = NOW()
                        WHERE customer_id = $1
                        """,
                        event.data['customer_id'],
                        event.data['new_tier']
                    )
```

## 最佳实践

### 应该做

- **使投影幂等** - 可以安全地重放
- **使用事务** - 用于多表更新
- **存储检查点** - 故障后恢复
- **监控延迟** - 投影延迟时报警
- **规划重建** - 为重建而设计

### 不应该做

- **不要耦合投影** - 每个都是独立的
- **不要跳过错误处理** - 失败时记录日志和报警
- **不要忽略顺序** - 事件必须按顺序处理
- **不要过度规范化** - 为查询模式反规范化

## 资源

- [CQRS 模式](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [投影构建块](https://zimarev.com/blog/event-sourcing/projections/)
