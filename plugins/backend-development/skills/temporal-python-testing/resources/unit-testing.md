# Temporal 工作流和活动单元测试

使用 WorkflowEnvironment 和 ActivityEnvironment 单独测试工作流和活动的专注指南。

## 使用时间跳过的 WorkflowEnvironment

**目的**：单独测试工作流，时间瞬间推进（月度工作流 → 秒级）

### 基本设置模式

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    """可重用的时间跳过测试环境"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow_execution(workflow_env):
    """使用时间跳过测试工作流"""
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            "test-input",
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == "expected-output"
```

**关键优势**：

- `workflow.sleep(timedelta(days=30))` 瞬间完成
- 快速反馈循环（毫秒级而非小时级）
- 确定性测试执行

### 时间跳过示例

**睡眠推进**：

```python
@pytest.mark.asyncio
async def test_workflow_with_delays(workflow_env):
    """在时间跳过模式下工作流睡眠是瞬间的"""

    @workflow.defn
    class DelayedWorkflow:
        @workflow.run
        async def run(self) -> str:
            await workflow.sleep(timedelta(hours=24))  # 测试中瞬间
            return "completed"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DelayedWorkflow],
    ):
        result = await workflow_env.client.execute_workflow(
            DelayedWorkflow.run,
            id="delayed-wf",
            task_queue="test",
        )
        assert result == "completed"
```

**手动时间控制**：

```python
@pytest.mark.asyncio
async def test_workflow_manual_time(workflow_env):
    """手动推进时间以实现精确控制"""

    handle = await workflow_env.client.start_workflow(
        TimeBasedWorkflow.run,
        id="time-wf",
        task_queue="test",
    )

    # 推进特定时间量
    await workflow_env.sleep(timedelta(hours=1))

    # 通过查询验证中间状态
    state = await handle.query(TimeBasedWorkflow.get_state)
    assert state == "processing"

    # 推进到完成
    await workflow_env.sleep(timedelta(hours=23))
    result = await handle.result()
    assert result == "completed"
```

### 测试工作流逻辑

**决策测试**：

```python
@pytest.mark.asyncio
async def test_workflow_branching(workflow_env):
    """测试不同的执行路径"""

    @workflow.defn
    class ConditionalWorkflow:
        @workflow.run
        async def run(self, condition: bool) -> str:
            if condition:
                return "path-a"
            return "path-b"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ConditionalWorkflow],
    ):
        # 测试 true 路径
        result_a = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            True,
            id="cond-wf-true",
            task_queue="test",
        )
        assert result_a == "path-a"

        # 测试 false 路径
        result_b = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            False,
            id="cond-wf-false",
            task_queue="test",
        )
        assert result_b == "path-b"
```

## ActivityEnvironment 测试

**目的**：单独测试活动，无需工作流或 Temporal 服务器

### 基本活动测试

```python
from temporalio.testing import ActivityEnvironment

async def test_activity_basic():
    """在没有工作流上下文的情况下测试活动"""

    @activity.defn
    async def process_data(input: str) -> str:
        return input.upper()

    env = ActivityEnvironment()
    result = await env.run(process_data, "test")
    assert result == "TEST"
```

### 测试活动上下文

**心跳测试**：

```python
async def test_activity_heartbeat():
    """验证心跳调用"""

    @activity.defn
    async def long_running_activity(total_items: int) -> int:
        for i in range(total_items):
            activity.heartbeat(i)  # 报告进度
            await asyncio.sleep(0.1)
        return total_items

    env = ActivityEnvironment()
    result = await env.run(long_running_activity, 10)
    assert result == 10
```

**取消测试**：

```python
async def test_activity_cancellation():
    """测试活动取消处理"""

    @activity.defn
    async def cancellable_activity() -> str:
        try:
            while True:
                if activity.is_cancelled():
                    return "cancelled"
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            return "cancelled"

    env = ActivityEnvironment(cancellation_reason="test-cancel")
    result = await env.run(cancellable_activity)
    assert result == "cancelled"
```

### 测试错误处理

**异常传播**：

```python
async def test_activity_error():
    """测试活动错误处理"""

    @activity.defn
    async def failing_activity(should_fail: bool) -> str:
        if should_fail:
            raise ApplicationError("验证失败", non_retryable=True)
        return "success"

    env = ActivityEnvironment()

    # 测试成功路径
    result = await env.run(failing_activity, False)
    assert result == "success"

    # 测试错误路径
    with pytest.raises(ApplicationError) as exc_info:
        await env.run(failing_activity, True)
    assert "验证失败" in str(exc_info.value)
```

## Pytest 集成模式

### 共享 Fixture

```python
# conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture(scope="module")
async def workflow_env():
    """模块范围环境（跨测试重用）"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """函数范围环境（每个测试全新）"""
    return ActivityEnvironment()
```

### 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
    ("123", "123"),
])
async def test_activity_parameterized(activity_env, input, expected):
    """测试多个输入场景"""
    result = await activity_env.run(process_data, input)
    assert result == expected
```

## 最佳实践

1. **快速执行**：所有工作流测试使用时间跳过
2. **隔离**：分别测试工作流和活动
3. **共享 Fixture**：在相关测试中重用 WorkflowEnvironment
4. **覆盖率目标**：工作流逻辑 ≥80%
5. **模拟活动**：使用 ActivityEnvironment 测试活动特定逻辑
6. **确定性**：确保测试结果在运行之间一致
7. **错误案例**：测试成功和失败场景

## 常见模式

**测试重试逻辑**：

```python
@pytest.mark.asyncio
async def test_workflow_with_retries(workflow_env):
    """测试活动重试行为"""

    call_count = 0

    @activity.defn
    async def flaky_activity() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("瞬态错误")
        return "success"

    @workflow.defn
    class RetryWorkflow:
        @workflow.run
        async def run(self) -> str:
            return await workflow.execute_activity(
                flaky_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=1),
                    maximum_attempts=5,
                ),
            )

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[flaky_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success"
        assert call_count == 3  # 验证重试尝试
```

## 其他资源

- Python SDK 测试：docs.temporal.io/develop/python/testing-suite
- pytest 文档：docs.pytest.org
- Temporal 示例：github.com/temporalio/samples-python
