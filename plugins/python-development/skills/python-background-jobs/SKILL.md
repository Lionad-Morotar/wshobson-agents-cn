---
name: python-background-jobs
description: Python background job patterns including task queues, workers, and event-driven architecture. Use when implementing async task processing, job queues, long-running operations, or decoupling work from request/response cycles.
---

# Python 后台任务与任务队列

将长时间运行或不可靠的工作从请求/响应周期中解耦。立即向用户返回响应，同时后台工作器异步处理繁重的工作。

## 何时使用此技能

- 处理耗时超过几秒的任务
- 发送电子邮件、通知或 Webhook
- 生成报告或导出数据
- 处理上传或媒体转换
- 与不可靠的外部服务集成
- 构建事件驱动架构

## 核心概念

### 1. 任务队列模式

API 接受请求，将任务加入队列，并立即返回任务 ID。工作器异步处理任务。

### 2. 幂等性

任务失败时可能会重试。设计时需考虑安全重执行。

### 3. 任务状态机

任务在状态之间转换：pending（待处理）→ running（运行中）→ succeeded/failed（成功/失败）。

### 4. 至少一次投递

大多数队列保证至少一次投递。你的代码必须处理重复。

## 快速开始

此技能使用 Celery 作为示例，它是一个广泛采用的任务队列。RQ、Dramatiq 和云原生解决方案（AWS SQS、GCP Tasks）同样是合理的选择。

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

@app.task
def send_email(to: str, subject: str, body: str) -> None:
    # 这在后台工作器中运行
    email_client.send(to, subject, body)

# 在你的 API 处理器中
send_email.delay("user@example.com", "Welcome!", "Thanks for signing up")
```

## 基础模式

### 模式 1：立即返回任务 ID

对于超过几秒的操作，返回任务 ID 并异步处理。

```python
from uuid import uuid4
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

@dataclass
class Job:
    id: str
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None
    error: str | None = None

# API 端点
async def start_export(request: ExportRequest) -> JobResponse:
    """启动导出任务并返回任务 ID。"""
    job_id = str(uuid4())

    # 持久化任务记录
    await jobs_repo.create(Job(
        id=job_id,
        status=JobStatus.PENDING,
        created_at=datetime.utcnow(),
    ))

    # 将任务加入队列以进行后台处理
    await task_queue.enqueue(
        "export_data",
        job_id=job_id,
        params=request.model_dump(),
    )

    # 立即返回任务 ID
    return JobResponse(
        job_id=job_id,
        status="pending",
        poll_url=f"/jobs/{job_id}",
    )
```

### 模式 2：Celery 任务配置

配置 Celery 任务的重试和超时设置。

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

# 全局配置
app.conf.update(
    task_time_limit=3600,          # 硬限制：1 小时
    task_soft_time_limit=3000,      # 软限制：50 分钟
    task_acks_late=True,            # 完成后确认
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,   # 不要预取太多任务
)

@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
)
def process_payment(self, payment_id: str) -> dict:
    """处理支付，在瞬态错误时自动重试。"""
    try:
        result = payment_gateway.charge(payment_id)
        return {"status": "success", "transaction_id": result.id}
    except PaymentDeclinedError as e:
        # 不要重试永久性失败
        return {"status": "declined", "reason": str(e)}
    except TransientError as e:
        # 使用指数退避重试
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
```

### 模式 3：使任务具有幂等性

工作器可能在崩溃或超时时重试。设计时需考虑安全重执行。

```python
@app.task(bind=True)
def process_order(self, order_id: str) -> None:
    """幂等地处理订单。"""
    order = orders_repo.get(order_id)

    # 已处理？提前返回
    if order.status == OrderStatus.COMPLETED:
        logger.info("Order already processed", order_id=order_id)
        return

    # 正在处理？检查是否应该继续
    if order.status == OrderStatus.PROCESSING:
        # 使用幂等键避免重复收费
        pass

    # 使用幂等键处理
    result = payment_provider.charge(
        amount=order.total,
        idempotency_key=f"order-{order_id}",  # 关键！
    )

    orders_repo.update(order_id, status=OrderStatus.COMPLETED)
```

**幂等性策略：**

1. **写入前检查**：在操作前验证状态
2. **幂等键**：与外部服务使用唯一令牌
3. **Upsert 模式**：`INSERT ... ON CONFLICT UPDATE`
4. **去重窗口**：跟踪已处理的 ID N 小时

### 模式 4：任务状态管理

持久化任务状态转换以实现可见性和调试。

```python
class JobRepository:
    """用于管理任务状态的仓库。"""

    async def create(self, job: Job) -> Job:
        """创建新任务记录。"""
        await self._db.execute(
            """INSERT INTO jobs (id, status, created_at)
               VALUES ($1, $2, $3)""",
            job.id, job.status.value, job.created_at,
        )
        return job

    async def update_status(
        self,
        job_id: str,
        status: JobStatus,
        **fields,
    ) -> None:
        """更新任务状态并带时间戳。"""
        updates = {"status": status.value, **fields}

        if status == JobStatus.RUNNING:
            updates["started_at"] = datetime.utcnow()
        elif status in (JobStatus.SUCCEEDED, JobStatus.FAILED):
            updates["completed_at"] = datetime.utcnow()

        await self._db.execute(
            "UPDATE jobs SET status = $1, ... WHERE id = $2",
            updates, job_id,
        )

        logger.info(
            "Job status updated",
            job_id=job_id,
            status=status.value,
        )
```

## 高级模式

### 模式 5：死信队列

处理永久失败的任务以供人工检查。

```python
@app.task(bind=True, max_retries=3)
def process_webhook(self, webhook_id: str, payload: dict) -> None:
    """处理 webhook，失败时使用 DLQ。"""
    try:
        result = send_webhook(payload)
        if not result.success:
            raise WebhookFailedError(result.error)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            # 移至死信队列以供人工检查
            dead_letter_queue.send({
                "task": "process_webhook",
                "webhook_id": webhook_id,
                "payload": payload,
                "error": str(e),
                "attempts": self.request.retries + 1,
                "failed_at": datetime.utcnow().isoformat(),
            })
            logger.error(
                "Webhook moved to DLQ after max retries",
                webhook_id=webhook_id,
                error=str(e),
            )
            return

        # 指数退避重试
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
```

### 模式 6：状态轮询端点

为客户端提供检查任务状态的端点。

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str) -> JobStatusResponse:
    """获取后台任务的当前状态。"""
    job = await jobs_repo.get(job_id)

    if job is None:
        raise HTTPException(404, f"Job {job_id} not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        result=job.result if job.status == JobStatus.SUCCEEDED else None,
        error=job.error if job.status == JobStatus.FAILED else None,
        # 对客户端有帮助
        is_terminal=job.status in (JobStatus.SUCCEEDED, JobStatus.FAILED),
    )
```

### 模式 7：任务链与工作流

从简单任务组合复杂工作流。

```python
from celery import chain, group, chord

# 简单链：A → B → C
workflow = chain(
    extract_data.s(source_id),
    transform_data.s(),
    load_data.s(destination_id),
)

# 并行执行：A, B, C 同时进行
parallel = group(
    send_email.s(user_email),
    send_sms.s(user_phone),
    update_analytics.s(event_data),
)

# Chord：并行运行任务，然后执行回调
# 处理所有项目，然后发送完成通知
workflow = chord(
    [process_item.s(item_id) for item_id in item_ids],
    send_completion_notification.s(batch_id),
)

workflow.apply_async()
```

### 模式 8：替代任务队列

根据需求选择合适的工具。

**RQ（Redis Queue）**：简单、基于 Redis
```python
from rq import Queue
from redis import Redis

queue = Queue(connection=Redis())
job = queue.enqueue(send_email, "user@example.com", "Subject", "Body")
```

**Dramatiq**：现代的 Celery 替代方案
```python
import dramatiq
from dramatiq.brokers.redis import RedisBroker

dramatiq.set_broker(RedisBroker())

@dramatiq.actor
def send_email(to: str, subject: str, body: str) -> None:
    email_client.send(to, subject, body)
```

**云原生选项：**
- AWS SQS + Lambda
- Google Cloud Tasks
- Azure Functions

## 最佳实践总结

1. **立即返回** - 不要长时间阻塞请求
2. **持久化任务状态** - 启用状态轮询和调试
3. **使任务具有幂等性** - 任何失败都可以安全重试
4. **使用幂等键** - 用于外部服务调用
5. **设置超时** - 包括软限制和硬限制
6. **实现 DLQ** - 捕获永久失败的任务
7. **记录状态转换** - 跟踪任务状态变化
8. **适当重试** - 对瞬态错误使用指数退避
9. **不要重试永久性失败** - 验证错误、无效凭据
10. **监控队列深度** - 在积压增长时发出警报
