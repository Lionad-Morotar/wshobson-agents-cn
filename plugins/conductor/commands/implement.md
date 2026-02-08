---
description: "按照 TDD 工作流执行轨道实施计划中的任务"
argument-hint: "[track-id] [--task X.Y] [--phase N]"
---

# 实施轨道

执行轨道实施计划中的任务，遵循 `conductor/workflow.md` 中定义的工作流规则。

## 预检查

1. 验证 Conductor 已初始化：
   - 检查 `conductor/product.md` 存在
   - 检查 `conductor/workflow.md` 存在
   - 检查 `conductor/tracks.md` 存在
   - 如果缺失：显示错误并建议先运行 `/conductor:setup`

2. 加载工作流配置：
   - 读取 `conductor/workflow.md`
   - 解析 TDD 严格级别
   - 解析提交策略
   - 解析验证检查点规则

## 轨道选择

### 如果提供了参数：

- 验证轨道存在：`conductor/tracks/{argument}/plan.md`
- 如果未找到：搜索部分匹配，建议更正

### 如果没有参数：

1. 读取 `conductor/tracks.md`
2. 解析未完成的轨道（状态 `[ ]` 或 `[~]`）
3. 显示选择菜单：

   ```
   选择要实施的轨道：

   进行中：
   1. [~] auth_20250115 - 用户身份验证（阶段 2，任务 3）

   待处理：
   2. [ ] nav-fix_20250114 - 导航 Bug 修复
   3. [ ] dashboard_20250113 - 仪表板功能

   输入数字或轨道 ID：
   ```

## 上下文加载

加载实施的所有相关上下文：

1. 轨道文档：
   - `conductor/tracks/{trackId}/spec.md` - 需求
   - `conductor/tracks/{trackId}/plan.md` - 任务列表
   - `conductor/tracks/{trackId}/metadata.json` - 进度状态

2. 项目上下文：
   - `conductor/product.md` - 产品理解
   - `conductor/tech-stack.md` - 技术约束
   - `conductor/workflow.md` - 流程规则

3. 代码风格（如果存在）：
   - `conductor/code_styleguides/{language}.md`

## 轨道状态更新

更新轨道为进行中：

1. 在 `conductor/tracks.md` 中：
   - 将此轨道的 `[ ]` 更改为 `[~]`

2. 在 `conductor/tracks/{trackId}/metadata.json` 中：
   - 设置 `status: "in_progress"`
   - 更新 `updated` 时间戳

## 任务执行循环

对于 plan.md 中每个未完成的任务（标记为 `[ ]`）：

### 1. 任务识别

解析 plan.md 以查找下一个未完成的任务：

- 查找匹配 `- [ ] Task X.Y: {description}` 的行
- 从结构中跟踪当前阶段

### 2. 任务开始

标记任务为进行中：

- 更新 plan.md：将当前任务的 `[ ]` 更改为 `[~]`
- 宣布："正在开始任务 X.Y: {description}"

### 3. TDD 工作流（如果在 workflow.md 中启用 TDD）

**红色阶段 - 编写失败的测试：**

```
正在为任务 X.Y 遵循 TDD 工作流...

步骤 1：编写失败的测试
```

- 如需要，创建测试文件
- 为任务功能编写测试
- 运行测试以确认它们失败
- 如果测试意外通过：停止，调查

**绿色阶段 - 实施：**

```
步骤 2：实现通过测试的最小代码
```

- 编写使测试通过的最小代码
- 运行测试以确认它们通过
- 如果测试失败：调试并修复

**重构阶段：**

```
步骤 3：在保持测试通过的 同时进行重构
```

- 清理代码
- 运行测试以确保仍然通过

### 4. 非 TDD 工作流（如果 TDD 不严格）

- 直接实施任务
- 运行任何现有测试
- 根据需要进行手动验证

### 5. 任务完成

**提交更改**（遵循 workflow.md 中的提交策略）：

```bash
git add -A
git commit -m "{commit_prefix}: {task description} ({trackId})"
```

**更新 plan.md：**

- 将已完成任务的 `[~]` 更改为 `[x]`
- 提交计划更新：

```bash
git add conductor/tracks/{trackId}/plan.md
git commit -m "chore: 标记任务 X.Y 完成 ({trackId})"
```

**更新 metadata.json：**

- 增加 `tasks.completed`
- 更新 `updated` 时间戳

### 6. 阶段完成检查

每个任务后，检查阶段是否完成：

- 解析 plan.md 的阶段结构
- 如果当前阶段中的所有任务都是 `[x]`：

**运行阶段验证：**

```
阶段 {N} 完成。正在运行验证...
```

- 执行为阶段列出的验证任务
- 运行完整测试套件：`npm test` / `pytest` / 等

**报告并等待批准：**

```
阶段 {N} 验证结果：
- 所有阶段任务：完成
- 测试：{通过/失败}
- 验证：{通过/失败}

批准继续到阶段 {N+1}？
1. 是，继续
2. 不，有问题需要修复
3. 暂停实施
```

**关键：在继续到下一阶段之前等待明确的用户批准。**

## 实施期间的错误处理

### 工具失败

```
错误：{tool} 失败，原因：{error message}

选项：
1. 重试操作
2. 跳过此任务并继续
3. 暂停实施
4. 恢复当前任务更改
```

- 停止并显示选项
- 不要自动继续

### 测试失败

```
任务 X.Y 后测试失败

失败的测试：
- {test name}: {failure reason}

选项：
1. 尝试修复
2. 回滚任务更改
3. 暂停以进行手动干预
```

### Git 失败

```
GIT 错误：{error message}

这可能表示：
- 来自 Conductor 外部的未提交更改
- 合并冲突
- 权限问题

选项：
1. 显示 git 状态
2. 尝试解决
3. 暂停以进行手动干预
```

## 轨道完成

当所有阶段和任务都完成时：

### 1. 最终验证

```
所有任务完成。正在运行最终验证...
```

- 运行完整测试套件
- 检查 spec.md 中的所有验收标准
- 生成验证报告

### 2. 更新轨道状态

在 `conductor/tracks.md` 中：

- 将此轨道的 `[~]` 更改为 `[x]`
- 更新"更新时间"列

在 `conductor/tracks/{trackId}/metadata.json` 中：

- 设置 `status: "complete"`
- 设置 `phases.completed` 为总数
- 设置 `tasks.completed` 为总数
- 更新 `updated` 时间戳

在 `conductor/tracks/{trackId}/plan.md` 中：

- 更新标题状态为 `[x] 完成`

### 3. 文档同步提议

```
轨道完成！您想同步文档吗？

这将更新：
- conductor/product.md（如果添加了新功能）
- conductor/tech-stack.md（如果添加了新依赖）
- README.md（如果适用）

1. 是，同步文档
2. 不，跳过
```

### 4. 清理提议

```
轨道 {trackId} 已完成。

清理选项：
1. 归档 - 移动到 conductor/tracks/_archive/
2. 删除 - 移除轨道目录
3. 保留 - 保持原样
```

### 5. 完成摘要

```
轨道完成：{track title}

摘要：
- 轨道 ID：{trackId}
- 已完成阶段：{N}/{N}
- 已完成任务：{M}/{M}
- 创建的提交：{count}
- 测试：全部通过

后续步骤：
- 运行 /conductor:status 查看项目进度
- 运行 /conductor:new-track 创建下一个功能
```

## 进度跟踪

在整个过程中在 `metadata.json` 中维护进度：

```json
{
  "id": "auth_20250115",
  "title": "用户身份验证",
  "type": "feature",
  "status": "in_progress",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-15T14:30:00Z",
  "current_phase": 2,
  "current_task": "2.3",
  "phases": {
    "total": 3,
    "completed": 1
  },
  "tasks": {
    "total": 12,
    "completed": 7
  },
  "commits": [
    "abc1234: feat: 添加登录表单 (auth_20250115)",
    "def5678: feat: 添加密码验证 (auth_20250115)"
  ]
}
```

## 恢复

如果实施暂停并恢复：

1. 加载 `metadata.json` 以获取当前状态
2. 从 `current_task` 字段查找当前任务
3. 检查 plan.md 中的任务是否为 `[~]`
4. 询问用户：

   ```
   正在恢复轨道：{title}

   最后进行中的任务：任务 {X.Y}: {description}

   选项：
   1. 从我们停止的地方继续
   2. 重新开始当前任务
   3. 首先显示进度摘要
   ```

## 关键规则

1. **永不跳过验证检查点** - 始终在阶段之间等待用户批准
2. **任何失败时停止** - 不要尝试在错误后继续
3. **严格遵循 workflow.md** - TDD、提交策略和验证规则是强制性的
4. **保持 plan.md 更新** - 任务状态必须反映实际进度
5. **频繁提交** - 每个任务完成都应提交
6. **跟踪所有提交** - 在 metadata.json 中记录提交哈希以潜在恢复
