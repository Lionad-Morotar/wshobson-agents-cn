---
name: python-observability
description: Python observability patterns including structured logging, metrics, and distributed tracing. Use when adding logging, implementing metrics collection, setting up tracing, or debugging production systems.
---

# Python 可观测性

为 Python 应用添加结构化日志、指标和追踪的 instrumentation。当生产环境出现问题时,你无需部署新代码就能回答"什么、哪里、为什么"。

## 何时使用此技能

- 为应用添加结构化日志
- 使用 Prometheus 实现指标采集
- 跨服务设置分布式追踪
- 在请求链中传播关联 ID
- 调试生产环境问题
- 构建可观测性仪表板

## 核心概念

### 1. 结构化日志

在生产环境中以 JSON 格式输出具有一致性字段的日志。机器可读的日志能够实现强大的查询和告警。对于本地开发,可考虑使用人类可读的格式。

### 2. 四大黄金信号

在每个服务边界上跟踪延迟、流量、错误和饱和度。

### 3. 关联 ID

为单个请求在所有日志和 span 中串联一个唯一 ID,实现端到端追踪。

### 4. 有界基数

保持指标标签值的范围有限。无界标签(如用户 ID)会导致存储成本激增。

## 快速开始

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()
logger.info("Request processed", user_id="123", duration_ms=45)
```

## 基础模式

### 模式 1: 使用 Structlog 的结构化日志

配置 structlog 以输出具有一致性字段的 JSON 格式日志。

```python
import logging
import structlog

def configure_logging(log_level: str = "INFO") -> None:
    """为应用配置结构化日志。"""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# 在应用启动时初始化
configure_logging("INFO")
logger = structlog.get_logger()
```

### 模式 2: 一致的日志字段

每条日志条目都应包含用于过滤和关联的标准字段。

```python
import structlog
from contextvars import ContextVar

# 在上下文中存储关联 ID
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

logger = structlog.get_logger()

def process_request(request: Request) -> Response:
    """处理请求并记录结构化日志。"""
    logger.info(
        "Request received",
        correlation_id=correlation_id.get(),
        method=request.method,
        path=request.path,
        user_id=request.user_id,
    )

    try:
        result = handle_request(request)
        logger.info(
            "Request completed",
            correlation_id=correlation_id.get(),
            status_code=200,
            duration_ms=elapsed,
        )
        return result
    except Exception as e:
        logger.error(
            "Request failed",
            correlation_id=correlation_id.get(),
            error_type=type(e).__name__,
            error_message=str(e),
        )
        raise
```

### 模式 3: 语义化日志级别

在整个应用中一致地使用日志级别。

| 级别 | 用途 | 示例 |
|-------|---------|----------|
| `DEBUG` | 开发诊断 | 变量值、内部状态 |
| `INFO` | 请求生命周期、操作 | 请求开始/结束、任务完成 |
| `WARNING` | 可恢复的异常 | 重试尝试、使用降级方案 |
| `ERROR` | 需要关注的失败 | 异常、服务不可用 |

```python
# DEBUG: 详细的内部信息
logger.debug("Cache lookup", key=cache_key, hit=cache_hit)

# INFO: 正常的操作事件
logger.info("Order created", order_id=order.id, total=order.total)

# WARNING: 异常但已处理的情况
logger.warning(
    "Rate limit approaching",
    current_rate=950,
    limit=1000,
    reset_seconds=30,
)

# ERROR: 需要调查的失败
logger.error(
    "Payment processing failed",
    order_id=order.id,
    error=str(e),
    payment_provider="stripe",
)
```

切勿将预期行为记录为 `ERROR`。用户输入错误密码是 `INFO`,不是 `ERROR`。

### 模式 4: 关联 ID 传播

在入口处生成唯一 ID,并在所有操作中串联它。

```python
from contextvars import ContextVar
import uuid
import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def set_correlation_id(cid: str | None = None) -> str:
    """为当前上下文设置关联 ID。"""
    cid = cid or str(uuid.uuid4())
    correlation_id.set(cid)
    structlog.contextvars.bind_contextvars(correlation_id=cid)
    return cid

# FastAPI 中间件示例
from fastapi import Request

async def correlation_middleware(request: Request, call_next):
    """设置和传播关联 ID 的中间件。"""
    # 使用传入的 header 或生成新的
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    set_correlation_id(cid)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response
```

传播到出站请求:

```python
import httpx

async def call_downstream_service(endpoint: str, data: dict) -> dict:
    """调用下游服务并携带关联 ID。"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            json=data,
            headers={"X-Correlation-ID": correlation_id.get()},
        )
        return response.json()
```

## 高级模式

### 模式 5: 使用 Prometheus 的四大黄金信号

为每个服务边界跟踪这些指标:

```python
from prometheus_client import Counter, Histogram, Gauge

# 延迟: 请求耗时
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint", "status"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

# 流量: 请求速率
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

# 错误: 错误率
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["method", "endpoint", "error_type"],
)

# 饱和度: 资源利用率
DB_POOL_USAGE = Gauge(
    "db_connection_pool_used",
    "Number of database connections in use",
)
```

为你的端点添加 instrumentation:

```python
import time
from functools import wraps

def track_request(func):
    """跟踪请求指标的装饰器。"""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        method = request.method
        endpoint = request.url.path
        start = time.perf_counter()

        try:
            response = await func(request, *args, **kwargs)
            status = str(response.status_code)
            return response
        except Exception as e:
            status = "500"
            ERROR_COUNT.labels(
                method=method,
                endpoint=endpoint,
                error_type=type(e).__name__,
            ).inc()
            raise
        finally:
            duration = time.perf_counter() - start
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint, status=status).observe(duration)

    return wrapper
```

### 模式 6: 有界基数

避免使用无界值的标签以防止指标爆炸。

```python
# 错误: 用户 ID 可能有数百万个值
REQUEST_COUNT.labels(method="GET", user_id=user.id)  # 不要这样做!

# 正确: 仅使用有界值
REQUEST_COUNT.labels(method="GET", endpoint="/users", status="200")

# 如果需要每个用户的指标,使用不同的方法:
# - 记录 user_id 并查询日志
# - 使用独立的分析系统
# - 按类型/层级对用户进行分桶
REQUEST_COUNT.labels(
    method="GET",
    endpoint="/users",
    user_tier="premium",  # 有界的值集合
)
```

### 模式 7: 使用上下文管理器的定时操作

创建可重用的定时上下文管理器来跟踪操作。

```python
from contextlib import contextmanager
import time
import structlog

logger = structlog.get_logger()

@contextmanager
def timed_operation(name: str, **extra_fields):
    """用于定时和记录操作的上下文管理器。"""
    start = time.perf_counter()
    logger.debug("Operation started", operation=name, **extra_fields)

    try:
        yield
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.error(
            "Operation failed",
            operation=name,
            duration_ms=round(elapsed_ms, 2),
            error=str(e),
            **extra_fields,
        )
        raise
    else:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Operation completed",
            operation=name,
            duration_ms=round(elapsed_ms, 2),
            **extra_fields,
        )

# 使用示例
with timed_operation("fetch_user_orders", user_id=user.id):
    orders = await order_repository.get_by_user(user.id)
```

### 模式 8: OpenTelemetry 追踪

使用 OpenTelemetry 设置分布式追踪。

**注意:** OpenTelemetry 正在积极演进。请查阅 [官方 Python 文档](https://opentelemetry.io/docs/languages/python/) 获取最新的 API 模式和最佳实践。

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def configure_tracing(service_name: str, otlp_endpoint: str) -> None:
    """配置 OpenTelemetry 追踪。"""
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

async def process_order(order_id: str) -> Order:
    """处理订单并记录追踪。"""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        with tracer.start_as_current_span("validate_order"):
            validate_order(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge_payment(order_id)

        with tracer.start_as_current_span("send_confirmation"):
            send_confirmation(order_id)

        return order
```

## 最佳实践总结

1. **使用结构化日志** - 带有一致字段的 JSON 日志
2. **传播关联 ID** - 在所有请求和日志中串联
3. **跟踪四大黄金信号** - 延迟、流量、错误、饱和度
4. **限制标签基数** - 永远不要使用无界值作为指标标签
5. **使用适当的日志级别** - 不要滥用 ERROR 级别
6. **包含上下文** - 在日志中包含用户 ID、请求 ID、操作名称
7. **使用上下文管理器** - 一致的定时和错误处理
8. **分离关注点** - 可观测性代码不应污染业务逻辑
9. **测试可观测性** - 在集成测试中验证日志和指标
10. **设置告警** - 没有告警的指标毫无用处
