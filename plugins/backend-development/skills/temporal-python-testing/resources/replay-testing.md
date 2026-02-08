# 确定性和兼容性重放测试

验证工作流确定性并确保代码更改安全的综合指南，使用重放测试。

## 什么是重放测试？

**目的**：验证工作流代码更改与现有工作流执行向后兼容

**工作原理**：

1. Temporal 将每个工作流决策记录为事件历史
2. 重放测试根据记录的历史重新执行工作流代码
3. 如果新代码做出相同决策 → 确定性（可安全部署）
4. 如果决策不同 → 非确定性（破坏性更改）

**关键用例**：

- 将工作流代码更改部署到生产环境
- 验证重构不会破坏正在运行的工作流
- CI/CD 自动化兼容性检查
- 版本迁移验证

## 基本重放测试

### 重放器设置

```python
from temporalio.worker import Replayer
from temporalio.client import Client

async def test_workflow_replay():
    """针对生产历史测试工作流"""

    # 连接到 Temporal 服务器
    client = await Client.connect("localhost:7233")

    # 使用当前工作流代码创建重放器
    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # 从生产环境获取工作流历史
    handle = client.get_workflow_handle("order-123")
    history = await handle.fetch_history()

    # 使用当前代码重放历史
    await replayer.replay_workflow(history)
    # 成功 = 确定性，异常 = 破坏性更改
```

### 测试多个历史

```python
import pytest
from temporalio.worker import Replayer

@pytest.mark.asyncio
async def test_replay_multiple_workflows():
    """针对多个生产历史重放"""

    replayer = Replayer(workflows=[OrderWorkflow])

    # 测试不同的工作流执行
    workflow_ids = [
        "order-success-123",
        "order-cancelled-456",
        "order-retry-789",
    ]

    for workflow_id in workflow_ids:
        handle = client.get_workflow_handle(workflow_id)
        history = await handle.fetch_history()

        # 重放应对所有变体成功
        await replayer.replay_workflow(history)
```

## 确定性验证

### 常见非确定性模式

**问题：随机数生成**

```python
# ❌ 非确定性（破坏重放）
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> int:
        return random.randint(1, 100)  # 重放时不同！

# ✅ 确定性（对重放安全）
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> int:
        return workflow.random().randint(1, 100)  # 确定性随机
```

**问题：当前时间**

```python
# ❌ 非确定性
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = datetime.now()  # 重放时不同！
        return now.isoformat()

# ✅ 确定性
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = workflow.now()  # 确定性时间
        return now.isoformat()
```

**问题：直接外部调用**

```python
# ❌ 非确定性
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> dict:
        response = requests.get("https://api.example.com/data")  # 外部调用！
        return response.json()

# ✅ 确定性
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # 使用活动进行外部调用
        return await workflow.execute_activity(
            fetch_external_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
```

### 测试确定性

```python
@pytest.mark.asyncio
async def test_workflow_determinism():
    """验证工作流在多次运行中产生相同输出"""

    @workflow.defn
    class DeterministicWorkflow:
        @workflow.run
        async def run(self, seed: int) -> list[int]:
            # 使用 workflow.random() 实现确定性
            rng = workflow.random()
            rng.seed(seed)
            return [rng.randint(1, 100) for _ in range(10)]

    env = await WorkflowEnvironment.start_time_skipping()

    # 使用相同输入运行工作流两次
    results = []
    for i in range(2):
        async with Worker(
            env.client,
            task_queue="test",
            workflows=[DeterministicWorkflow],
        ):
            result = await env.client.execute_workflow(
                DeterministicWorkflow.run,
                42,  # 相同种子
                id=f"determinism-test-{i}",
                task_queue="test",
            )
            results.append(result)

    await env.shutdown()

    # 验证相同输出
    assert results[0] == results[1]
```

## 生产历史重放

### 导出工作流历史

```python
from temporalio.client import Client

async def export_workflow_history(workflow_id: str, output_file: str):
    """导出工作流历史用于重放测试"""

    client = await Client.connect("production.temporal.io:7233")

    # 获取工作流历史
    handle = client.get_workflow_handle(workflow_id)
    history = await handle.fetch_history()

    # 保存到文件用于重放测试
    with open(output_file, "wb") as f:
        f.write(history.SerializeToString())

    print(f"已导出历史到 {output_file}")
```

### 从文件重放

```python
from temporalio.worker import Replayer
from temporalio.api.history.v1 import History

async def test_replay_from_file():
    """从导出的历史文件重放工作流"""

    # 从文件加载历史
    with open("workflow_histories/order-123.pb", "rb") as f:
        history = History.FromString(f.read())

    # 使用当前工作流代码重放
    replayer = Replayer(workflows=[OrderWorkflow])
    await replayer.replay_workflow(history)
    # 成功 = 可安全部署
```

## CI/CD 集成模式

### GitHub Actions 示例

```yaml
# .github/workflows/replay-tests.yml
name: 重放测试

on:
  pull_request:
    branches: [main]

jobs:
  replay-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: 设置 Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 安装依赖
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: 下载生产历史
        run: |
          # 从生产环境获取最近的工作流历史
          python scripts/export_histories.py

      - name: 运行重放测试
        run: |
          pytest tests/replay/ --verbose

      - name: 上传结果
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: replay-failures
          path: replay-failures/
```

### 自动化历史导出

```python
# scripts/export_histories.py
import asyncio
from temporalio.client import Client
from datetime import datetime, timedelta

async def export_recent_histories():
    """导出最近的生产工作流历史"""

    client = await Client.connect("production.temporal.io:7233")

    # 查询最近完成的工作流
    workflows = client.list_workflows(
        query="WorkflowType='OrderWorkflow' AND CloseTime > '7 days ago'"
    )

    count = 0
    async for workflow in workflows:
        # 导出历史
        history = await workflow.fetch_history()

        # 保存到文件
        filename = f"workflow_histories/{workflow.id}.pb"
        with open(filename, "wb") as f:
            f.write(history.SerializeToString())

        count += 1
        if count >= 100:  # 限制为最近 100 个
            break

    print(f"已导出 {count} 个工作流历史")

if __name__ == "__main__":
    asyncio.run(export_recent_histories())
```

### 重放测试套件

```python
# tests/replay/test_workflow_replay.py
import pytest
import glob
from temporalio.worker import Replayer
from temporalio.api.history.v1 import History
from workflows import OrderWorkflow, PaymentWorkflow

@pytest.mark.asyncio
async def test_replay_all_histories():
    """重放所有生产历史"""

    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # 加载所有历史文件
    history_files = glob.glob("workflow_histories/*.pb")

    failures = []
    for history_file in history_files:
        try:
            with open(history_file, "rb") as f:
                history = History.FromString(f.read())

            await replayer.replay_workflow(history)
            print(f"✓ {history_file}")

        except Exception as e:
            failures.append((history_file, str(e)))
            print(f"✗ {history_file}: {e}")

    # 报告失败
    if failures:
        pytest.fail(
            f"重放失败 {len(failures)} 个工作流：\n"
            + "\n".join(f"  {file}: {error}" for file, error in failures)
        )
```

## 版本兼容性测试

### 测试代码演进

```python
@pytest.mark.asyncio
async def test_workflow_version_compatibility():
    """测试版本变化的工作流"""

    @workflow.defn
    class EvolvingWorkflow:
        @workflow.run
        async def run(self) -> str:
            # 使用版本控制实现安全代码演进
            version = workflow.get_version("feature-flag", 1, 2)

            if version == 1:
                # 旧行为
                return "version-1"
            else:
                # 新行为
                return "version-2"

    env = await WorkflowEnvironment.start_time_skipping()

    # 测试版本 1 行为
    async with Worker(
        env.client,
        task_queue="test",
        workflows=[EvolvingWorkflow],
    ):
        result_v1 = await env.client.execute_workflow(
            EvolvingWorkflow.run,
            id="evolving-v1",
            task_queue="test",
        )
        assert result_v1 == "version-1"

        # 模拟工作流使用版本 2 再次执行
        result_v2 = await env.client.execute_workflow(
            EvolvingWorkflow.run,
            id="evolving-v2",
            task_queue="test",
        )
        # 新工作流使用版本 2
        assert result_v2 == "version-2"

    await env.shutdown()
```

### 迁移策略

```python
# 阶段 1：添加版本检查
@workflow.defn
class MigratingWorkflow:
    @workflow.run
    async def run(self) -> dict:
        version = workflow.get_version("new-logic", 1, 2)

        if version == 1:
            # 旧逻辑（现有工作流）
            return await self._old_implementation()
        else:
            # 新逻辑（新工作流）
            return await self._new_implementation()

# 阶段 2：所有旧工作流完成后，删除旧代码
@workflow.defn
class MigratedWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # 仅保留新逻辑
        return await self._new_implementation()
```

## 最佳实践

1. **部署前重放**：部署工作流更改前始终运行重放测试
2. **定期导出**：持续导出生产历史用于测试
3. **CI/CD 集成**：在拉取请求检查中自动重放测试
4. **版本跟踪**：使用 workflow.get_version() 实现安全代码演进
5. **历史保留**：保留代表性工作流历史用于回归测试
6. **确定性**：永不使用 random()、datetime.now() 或直接外部调用
7. **全面测试**：测试各种工作流执行路径

## 常见重放错误

**非确定性错误**：

```
WorkflowNonDeterministicError: 工作流命令在位置 5 不匹配
预期：ScheduleActivityTask(activity_id='activity-1')
实际：ScheduleActivityTask(activity_id='activity-2')
```

**解决方案**：代码更改改变了工作流决策序列

**版本不匹配错误**：

```
WorkflowVersionError: 工作流版本从 1 变为 2，未使用 get_version()
```

**解决方案**：使用 workflow.get_version() 进行向后兼容更改

## 其他资源

- 重放测试：docs.temporal.io/develop/python/testing-suite#replay-testing
- 工作流版本控制：docs.temporal.io/workflows#versioning
- 确定性指南：docs.temporal.io/workflows#deterministic-constraints
- CI/CD 集成：github.com/temporalio/samples-python/tree/main/.github/workflows
