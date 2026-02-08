---
description: "用于管理工作负载、任务分配和重新平衡的任务委托仪表盘"
argument-hint: "[team-name] [--assign task-id=member-name] [--message member-name 'content'] [--rebalance]"
---

# Team Delegate (团队委托)

管理任务分配和团队工作负载。提供委托仪表盘,显示未分配的任务、成员工作负载、阻塞的任务和重新平衡建议。

## 预检查

1. 从 `$ARGUMENTS` 解析团队名称和操作标志:
   - `--assign task-id=member-name`: 将特定任务分配给成员
   - `--message member-name 'content'`: 向特定成员发送消息
   - `--rebalance`: 分析并重新平衡工作负载分布

2. 使用 Read 工具从 `~/.claude/teams/{team-name}/config.json` 读取团队配置
3. 调用 `TaskList` 获取当前状态

## 操作:分配任务

如果提供了 `--assign` 标志:

1. 从 `task-id=member-name` 格式解析任务 ID 和成员名称
2. 使用 `TaskUpdate` 设置任务所有者
3. 使用 `SendMessage` 和 `type: "message"` 通知成员:
   - recipient: 成员名称
   - content: "你已被分配任务 #{id}: {subject}。{task description}"
4. 确认:"任务 #{id} 已分配给 {member-name}"

## 操作:发送消息

如果提供了 `--message` 标志:

1. 解析成员名称和消息内容
2. 使用 `SendMessage` 和 `type: "message"`:
   - recipient: 成员名称
   - content: 消息内容
3. 确认:"消息已发送给 {member-name}"

## 操作:重新平衡

如果提供了 `--rebalance` 标志:

1. 分析当前工作负载分布:
   - 计算每个成员的任务数(in_progress + pending assigned)
   - 识别有 0 个任务的成员(空闲)
   - 识别有 3+ 个任务的成员(过载)
   - 检查可以解除阻塞的阻塞任务

2. 生成重新平衡建议:

   ```
   ## 工作负载分析

   成员          任务    状态
   ─────────────────────────────────
   implementer-1   3        过载
   implementer-2   1        平衡
   implementer-3   0        空闲

   建议:
   1. 将任务 #5 从 implementer-1 移到 implementer-3
   2. 将未分配任务 #7 分配给 implementer-3
   ```

3. 在执行重新平衡前询问用户确认
4. 使用 `TaskUpdate` 和 `SendMessage` 执行已批准的移动

## 默认:委托仪表盘

如果没有提供操作标志,显示完整的委托仪表盘:

```
## 委托仪表盘: {team-name}

### 未分配任务
  #5  审查错误处理模式
  #7  添加集成测试

### 成员工作负载
  implementer-1   3 个任务 (1 个进行中, 2 个待处理)
  implementer-2   1 个任务  (1 个进行中)
  implementer-3   0 个任务 (空闲)

### 阻塞任务
  #6  被 #4 阻塞(进行中,所有者: implementer-1)

### 建议
  - 将 #5 分配给 implementer-3(空闲)
  - 将 #7 分配给 implementer-2(低工作负载)
```

**提示**: 使用 Shift+Tab 进入 Claude Code 内置的委托模式进行临时任务委托。
