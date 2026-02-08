# 使用模拟活动的集成测试

使用模拟外部依赖、错误注入和复杂场景测试工作流的综合模式。

## 活动模拟策略

**目的**：测试工作流编排逻辑而不调用真实的外部服务

### 基本模拟模式

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_workflow_with_mocked_activity(workflow_env):
    """模拟活动以测试工作流逻辑"""

    # 创建模拟活动
    mock_activity = Mock(return_value="mocked-result")

    @workflow.defn
    class WorkflowWithActivity:
        @workflow.run
        async def run(self, input: str) -> str:
            result = await workflow.execute_activity(
                process_external_data,
                input,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return f"processed: {result}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[WorkflowWithActivity],
        activities=[mock_activity],  # 使用模拟而不是真实活动
    ):
        result = await workflow_env.client.execute_workflow(
            WorkflowWithActivity.run,
            "test-input",
            id="wf-mock",
            task_queue="test",
        )
        assert result == "processed: mocked-result"
        mock_activity.assert_called_once()
```

### 动态模拟响应

**基于场景的模拟**：

```python
@pytest.mark.asyncio
async def test_workflow_multiple_mock_scenarios(workflow_env):
    """使用动态模拟测试不同的工作流路径"""

    # 根据输入模拟返回不同的值
    def dynamic_activity(input: str) -> str:
        if input == "error-case":
            raise ApplicationError("验证失败", non_retryable=True)
        return f"processed-{input}"

    @workflow.defn
    class DynamicWorkflow:
        @workflow.run
        async def run(self, input: str) -> str:
            try:
                result = await workflow.execute_activity(
                    dynamic_activity,
                    input,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                return f"success: {result}"
            except ApplicationError as e:
                return f"error: {e.message}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DynamicWorkflow],
        activities=[dynamic_activity],
    ):
        # 测试成功路径
        result_success = await workflow_env.client.execute_workflow(
            DynamicWorkflow.run,
            "valid-input",
            id="wf-success",
            task_queue="test",
        )
        assert result_success == "success: processed-valid-input"

        # 测试错误路径
        result_error = await workflow_env.client.execute_workflow(
            DynamicWorkflow.run,
            "error-case",
            id="wf-error",
            task_queue="test",
        )
        assert "验证失败" in result_error
```

## 错误注入模式

### 测试瞬态故障

**重试行为**：

```python
@pytest.mark.asyncio
async def test_workflow_transient_errors(workflow_env):
    """使用受控故障测试重试逻辑"""

    attempt_count = 0

    @activity.defn
    async def transient_activity() -> str:
        nonlocal attempt_count
        attempt_count += 1

        if attempt_count < 3:
            raise Exception(f"瞬态错误 {attempt_count}")
        return "success-after-retries"

    @workflow.defn
    class RetryWorkflow:
        @workflow.run
        async def run(self) -> str:
            return await workflow.execute_activity(
                transient_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=10),
                    maximum_attempts=5,
                    backoff_coefficient=1.0,
                ),
            )

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[transient_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success-after-retries"
        assert attempt_count == 3
```

### 测试不可重试错误

**业务验证失败**：

```python
@pytest.mark.asyncio
async def test_workflow_non_retryable_error(workflow_env):
    """测试永久故障的处理"""

    @activity.defn
    async def validation_activity(input: dict) -> str:
        if not input.get("valid"):
            raise ApplicationError(
                "无效输入",
                non_retryable=True,  # 不重试验证错误
            )
        return "validated"

    @workflow.defn
    class ValidationWorkflow:
        @workflow.run
        async def run(self, input: dict) -> str:
            try:
                return await workflow.execute_activity(
                    validation_activity,
                    input,
                    start_to_close_timeout=timedelta(seconds=10),
                )
            except ApplicationError as e:
                return f"validation-failed: {e.message}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ValidationWorkflow],
        activities=[validation_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            ValidationWorkflow.run,
            {"valid": False},
            id="validation-wf",
            task_queue="test",
        )
        assert "validation-failed" in result
```

## 多活动工作流测试

### 顺序活动模式

```python
@pytest.mark.asyncio
async def test_workflow_sequential_activities(workflow_env):
    """测试编排多个活动的工作流"""

    activity_calls = []

    @activity.defn
    async def step_1(input: str) -> str:
        activity_calls.append("step_1")
        return f"{input}-step1"

    @activity.defn
    async def step_2(input: str) -> str:
        activity_calls.append("step_2")
        return f"{input}-step2"

    @activity.defn
    async def step_3(input: str) -> str:
        activity_calls.append("step_3")
        return f"{input}-step3"

    @workflow.defn
    class SequentialWorkflow:
        @workflow.run
        async def run(self, input: str) -> str:
            result_1 = await workflow.execute_activity(
                step_1,
                input,
                start_to_close_timeout=timedelta(seconds=10),
            )
            result_2 = await workflow.execute_activity(
                step_2,
                result_1,
                start_to_close_timeout=timedelta(seconds=10),
            )
            result_3 = await workflow.execute_activity(
                step_3,
                result_2,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return result_3

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SequentialWorkflow],
        activities=[step_1, step_2, step_3],
    ):
        result = await workflow_env.client.execute_workflow(
            SequentialWorkflow.run,
            "start",
            id="seq-wf",
            task_queue="test",
        )
        assert result == "start-step1-step2-step3"
        assert activity_calls == ["step_1", "step_2", "step_3"]
```

### 并行活动模式

```python
@pytest.mark.asyncio
async def test_workflow_parallel_activities(workflow_env):
    """测试并发活动执行"""

    @activity.defn
    async def parallel_task(task_id: int) -> str:
        return f"task-{task_id}"

    @workflow.defn
    class ParallelWorkflow:
        @workflow.run
        async def run(self, task_count: int) -> list[str]:
            # 并行执行活动
            tasks = [
                workflow.execute_activity(
                    parallel_task,
                    i,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                for i in range(task_count)
            ]
            return await asyncio.gather(*tasks)

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ParallelWorkflow],
        activities=[parallel_task],
    ):
        result = await workflow_env.client.execute_workflow(
            ParallelWorkflow.run,
            3,
            id="parallel-wf",
            task_queue="test",
        )
        assert result == ["task-0", "task-1", "task-2"]
```

## 信号和查询测试

### 信号处理器

```python
@pytest.mark.asyncio
async def test_workflow_signals(workflow_env):
    """测试工作流信号处理"""

    @workflow.defn
    class SignalWorkflow:
        def __init__(self) -> None:
            self._status = "initialized"

        @workflow.run
        async def run(self) -> str:
            # 等待完成信号
            await workflow.wait_condition(lambda: self._status == "completed")
            return self._status

        @workflow.signal
        async def update_status(self, new_status: str) -> None:
            self._status = new_status

        @workflow.query
        def get_status(self) -> str:
            return self._status

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SignalWorkflow],
    ):
        # 启动工作流
        handle = await workflow_env.client.start_workflow(
            SignalWorkflow.run,
            id="signal-wf",
            task_queue="test",
        )

        # 通过查询验证初始状态
        initial_status = await handle.query(SignalWorkflow.get_status)
        assert initial_status == "initialized"

        # 发送信号
        await handle.signal(SignalWorkflow.update_status, "processing")

        # 验证更新后的状态
        updated_status = await handle.query(SignalWorkflow.get_status)
        assert updated_status == "processing"

        # 完成工作流
        await handle.signal(SignalWorkflow.update_status, "completed")
        result = await handle.result()
        assert result == "completed"
```

## 覆盖率策略

### 工作流逻辑覆盖率

**目标**：≥80% 的工作流决策逻辑覆盖率

```python
# 测试所有分支
@pytest.mark.parametrize("condition,expected", [
    (True, "branch-a"),
    (False, "branch-b"),
])
async def test_workflow_branches(workflow_env, condition, expected):
    """确保测试所有代码路径"""
    # 测试实现
    pass
```

### 活动覆盖率

**目标**：≥80% 的活动逻辑覆盖率

```python
# 测试活动边缘情况
@pytest.mark.parametrize("input,expected", [
    ("valid", "success"),
    ("", "empty-input-error"),
    (None, "null-input-error"),
])
async def test_activity_edge_cases(activity_env, input, expected):
    """测试活动错误处理"""
    # 测试实现
    pass
```

## 集成测试组织

### 测试结构

```
tests/
├── integration/
│   ├── conftest.py              # 共享夹具
│   ├── test_order_workflow.py   # 订单处理测试
│   ├── test_payment_workflow.py # 支付测试
│   └── test_fulfillment_workflow.py
├── unit/
│   ├── test_order_activities.py
│   └── test_payment_activities.py
└── fixtures/
    └── test_data.py             # 测试数据构建器
```

### 共享夹具

```python
# conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture(scope="session")
async def workflow_env():
    """集成测试的会话范围环境"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def mock_payment_service():
    """模拟外部支付服务"""
    return Mock()

@pytest.fixture
def mock_inventory_service():
    """模拟外部库存服务"""
    return Mock()
```

## 最佳实践

1. **模拟外部依赖**：切勿在测试中调用真实 API
2. **测试错误场景**：验证补偿和重试逻辑
3. **并行测试**：使用 pytest-xdist 加快测试运行
4. **隔离测试**：每个测试应该独立
5. **清晰的断言**：验证结果和副作用
6. **覆盖率目标**：关键工作流 ≥80%
7. **快速执行**：使用时间跳跃，避免真实延迟

## 额外资源

- 模拟策略：docs.temporal.io/develop/python/testing-suite
- pytest 最佳实践：docs.pytest.org/en/stable/goodpractices.html
- Python SDK 示例：github.com/temporalio/samples-python