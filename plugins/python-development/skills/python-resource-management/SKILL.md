---
name: python-resource-management
description: 使用上下文管理器、清理模式和流式处理进行 Python 资源管理。在管理连接、文件句柄、实现清理逻辑或构建带累积状态的流式响应时使用。
---

# Python 资源管理

使用上下文管理器以确定性的方式管理资源。数据库连接、文件句柄和网络套接字等资源应该可靠地释放，即使在发生异常时也是如此。

## 何时使用此技能

- 管理数据库连接和连接池
- 处理文件句柄和 I/O 操作
- 实现自定义上下文管理器
- 构建带状态的流式响应
- 处理嵌套资源清理
- 创建异步上下文管理器

## 核心概念

### 1. 上下文管理器

`with` 语句确保资源自动释放，即使发生异常也是如此。

### 2. 协议方法

`__enter__`/`__exit__` 用于同步资源管理，`__aenter__`/`__aexit__` 用于异步资源管理。

### 3. 无条件清理

`__exit__` 始终会运行，无论是否发生异常。

### 4. 异常处理

从 `__exit__` 返回 `True` 来抑制异常，返回 `False` 来传播异常。

## 快速开始

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        resource.cleanup()

with managed_resource() as r:
    r.do_work()
```

## 基本模式

### 模式 1: 基于类的上下文管理器

为复杂资源实现上下文管理器协议。

```python
class DatabaseConnection:
    """带自动清理的数据库连接。"""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._conn: Connection | None = None

    def connect(self) -> None:
        """建立数据库连接。"""
        self._conn = psycopg.connect(self._dsn)

    def close(self) -> None:
        """如果连接打开则关闭。"""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "DatabaseConnection":
        """进入上下文：连接并返回 self。"""
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """退出上下文：始终关闭连接。"""
        self.close()

# 使用上下文管理器（推荐）
with DatabaseConnection(dsn) as db:
    result = db.execute(query)

# 需要时手动管理
db = DatabaseConnection(dsn)
db.connect()
try:
    result = db.execute(query)
finally:
    db.close()
```

### 模式 2: 异步上下文管理器

对于异步资源，实现异步协议。

```python
class AsyncDatabasePool:
    """异步数据库连接池。"""

    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10) -> None:
        self._dsn = dsn
        self._min_size = min_size
        self._max_size = max_size
        self._pool: asyncpg.Pool | None = None

    async def __aenter__(self) -> "AsyncDatabasePool":
        """创建连接池。"""
        self._pool = await asyncpg.create_pool(
            self._dsn,
            min_size=self._min_size,
            max_size=self._max_size,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """关闭池中的所有连接。"""
        if self._pool is not None:
            await self._pool.close()

    async def execute(self, query: str, *args) -> list[dict]:
        """使用池连接执行查询。"""
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

# 使用
async with AsyncDatabasePool(dsn) as pool:
    users = await pool.execute("SELECT * FROM users WHERE active = $1", True)
```

### 模式 3: 使用 @contextmanager 装饰器

使用装饰器简化简单场景的上下文管理器。

```python
from contextlib import contextmanager, asynccontextmanager
import time
import structlog

logger = structlog.get_logger()

@contextmanager
def timed_block(name: str):
    """计时代码块。"""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} completed", duration_seconds=round(elapsed, 3))

# 使用
with timed_block("data_processing"):
    process_large_dataset()

@asynccontextmanager
async def database_transaction(conn: AsyncConnection):
    """管理数据库事务。"""
    await conn.execute("BEGIN")
    try:
        yield conn
        await conn.execute("COMMIT")
    except Exception:
        await conn.execute("ROLLBACK")
        raise

# 使用
async with database_transaction(conn) as tx:
    await tx.execute("INSERT INTO users ...")
    await tx.execute("INSERT INTO audit_log ...")
```

### 模式 4: 无条件资源释放

无论是否发生异常，始终在 `__exit__` 中清理资源。

```python
class FileProcessor:
    """保证清理的文件处理器。"""

    def __init__(self, path: str) -> None:
        self._path = path
        self._file: IO | None = None
        self._temp_files: list[Path] = []

    def __enter__(self) -> "FileProcessor":
        self._file = open(self._path, "r")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """无条件清理所有资源。"""
        # 关闭主文件
        if self._file is not None:
            self._file.close()

        # 清理所有临时文件
        for temp_file in self._temp_files:
            try:
                temp_file.unlink()
            except OSError:
                pass  # 尽力清理

        # 返回 None/False 以传播任何异常
```

## 高级模式

### 模式 5: 选择性异常抑制

仅抑制特定的、文档化的异常。

```python
class StreamWriter:
    """优雅处理管道断开的写入器。"""

    def __init__(self, stream) -> None:
        self._stream = stream

    def __enter__(self) -> "StreamWriter":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """清理，在关闭时抑制 BrokenPipeError。"""
        self._stream.close()

        # 抑制 BrokenPipeError（客户端断开连接）
        # 这是预期行为，不是错误
        if exc_type is BrokenPipeError:
            return True  # 异常被抑制

        return False  # 传播所有其他异常
```

### 模式 6: 带累积状态的流式处理

在流式传输期间维护增量块和累积状态。

```python
from collections.abc import Generator
from dataclasses import dataclass, field

@dataclass
class StreamingResult:
    """累积的流式结果。"""

    chunks: list[str] = field(default_factory=list)
    _finalized: bool = False

    @property
    def content(self) -> str:
        """获取累积的内容。"""
        return "".join(self.chunks)

    def add_chunk(self, chunk: str) -> None:
        """添加块到累加器。"""
        if self._finalized:
            raise RuntimeError("无法添加到已完成的结果")
        self.chunks.append(chunk)

    def finalize(self) -> str:
        """标记流完成并返回内容。"""
        self._finalized = True
        return self.content

def stream_with_accumulation(
    response: StreamingResponse,
) -> Generator[tuple[str, str], None, str]:
    """流式传输响应同时累积内容。

    Yields:
        每个块的 (累积内容, 新块) 元组。

    Returns:
        最终累积的内容。
    """
    result = StreamingResult()

    for chunk in response.iter_content():
        result.add_chunk(chunk)
        yield result.content, chunk

    return result.finalize()
```

### 模式 7: 高效字符串累积

累积时避免 O(n²) 字符串拼接。

```python
def accumulate_stream(stream) -> str:
    """高效累积流内容。"""
    # 错误：O(n²)，因为字符串不可变
    # content = ""
    # for chunk in stream:
    #     content += chunk  # 每次都创建新字符串

    # 正确：O(n)，使用列表和 join
    chunks: list[str] = []
    for chunk in stream:
        chunks.append(chunk)
    return "".join(chunks)  # 单次分配
```

### 模式 8: 跟踪流指标

测量首字节时间和总流式传输时间。

```python
import time
from collections.abc import Generator

def stream_with_metrics(
    response: StreamingResponse,
) -> Generator[str, None, dict]:
    """流式传输响应同时收集指标。

    Yields:
        内容块。

    Returns:
        指标字典。
    """
    start = time.perf_counter()
    first_chunk_time: float | None = None
    chunk_count = 0
    total_bytes = 0

    for chunk in response.iter_content():
        if first_chunk_time is None:
            first_chunk_time = time.perf_counter() - start

        chunk_count += 1
        total_bytes += len(chunk.encode())
        yield chunk

    total_time = time.perf_counter() - start

    return {
        "time_to_first_byte_ms": round((first_chunk_time or 0) * 1000, 2),
        "total_time_ms": round(total_time * 1000, 2),
        "chunk_count": chunk_count,
        "total_bytes": total_bytes,
    }
```

### 模式 9: 使用 ExitStack 管理多个资源

干净地处理动态数量的资源。

```python
from contextlib import ExitStack, AsyncExitStack
from pathlib import Path

def process_files(paths: list[Path]) -> list[str]:
    """处理多个文件并自动清理。"""
    results = []

    with ExitStack() as stack:
        # 打开所有文件 - 当块退出时它们都会被关闭
        files = [stack.enter_context(open(p)) for p in paths]

        for f in files:
            results.append(f.read())

    return results

async def process_connections(hosts: list[str]) -> list[dict]:
    """处理多个异步连接。"""
    results = []

    async with AsyncExitStack() as stack:
        connections = [
            await stack.enter_async_context(connect_to_host(host))
            for host in hosts
        ]

        for conn in connections:
            results.append(await conn.fetch_data())

    return results
```

## 最佳实践总结

1. **始终使用上下文管理器** - 对于任何需要清理的资源
2. **无条件清理** - 即使发生异常 `__exit__` 也会运行
3. **不要意外抑制异常** - 除非有意抑制，否则返回 `False`
4. **使用 @contextmanager** - 用于简单的资源模式
5. **实现两种协议** - 支持 `with` 和手动管理
6. **使用 ExitStack** - 用于动态数量的资源
7. **高效累积** - 列表 + join，而不是字符串拼接
8. **跟踪指标** - 首字节时间对流式传输很重要
9. **文档化行为** - 特别是异常抑制
10. **测试清理路径** - 验证错误时资源被释放
