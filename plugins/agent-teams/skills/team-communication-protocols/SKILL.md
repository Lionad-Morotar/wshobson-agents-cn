---
name: team-communication-protocols
description: 智能体团队通信的结构化消息协议,包括消息类型选择、计划批准、关闭程序和避免的反模式。在建立团队通信规范、处理计划批准或管理团队关闭时使用此技能。
version: 1.0.2
---

# 团队通信协议

智能体队友之间有效通信的协议,包括消息类型选择、计划批准工作流、关闭程序和要避免的常见反模式。

## 何时使用此技能

- 为新团队建立通信规范
- 在消息类型之间选择(message、broadcast、shutdown_request)
- 处理计划批准工作流
- 管理优雅的团队关闭
- 发现队友身份和能力

## 消息类型选择

### `message`(直接消息) — 默认选择

发送给单个特定队友:

```json
{
  "type": "message",
  "recipient": "implementer-1",
  "content": "你的 API 端点已准备就绪。你现在可以构建前端表单。",
  "summary": "API 端点已准备好供前端使用"
}
```

**用于**: 任务更新、协调、问题、集成通知。

### `broadcast` — 谨慎使用

同时发送给所有队友:

```json
{
  "type": "broadcast",
  "content": "关键:共享类型文件已更新。在继续之前请拉取最新版本。",
  "summary": "共享类型已更新"
}
```

**仅用于**: 影响所有人的关键阻塞、共享资源的重大更改。

**为什么谨慎?**: 每个广播发送 N 条单独消息(每个队友一条),消耗与团队规模成比例的 API 资源。

### `shutdown_request` — 优雅终止

请求队友关闭:

```json
{
  "type": "shutdown_request",
  "recipient": "reviewer-1",
  "content": "审查完成,正在关闭团队。"
}
```

队友以 `shutdown_response` 响应(批准或拒绝并说明原因)。

## 通信反模式

| 反模式                          | 问题                                  | 更好的方法                              |
| ---------------------------------| -------------------------------------| -------------------------------------- |
| 广播例行更新                     | 浪费资源、噪音                        | 向受影响的队友发送直接消息              |
| 发送 JSON 状态消息               | 不是为结构化数据设计的                | 使用 TaskUpdate 更新任务状态            |
| 不在集成点通信                   | 队友针对过时的接口构建                | 当你的接口准备好时发送消息              |
| 通过消息进行微观管理             | 使队友不知所措,减慢工作               | 在里程碑检查,而不是每一步               |
| 使用 UUID 而不是名称             | 难以阅读、容易出错                    | 始终使用队友名称                       |
| 忽略空闲的队友                   | 浪费容量                              | 分配新工作或关闭                       |

## 计划批准工作流

当使用 `plan_mode_required` 生成队友时:

1. 队友使用只读探索工具创建计划
2. 队友调用 `ExitPlanMode`,向领导者发送 `plan_approval_request`
3. 领导者审查计划
4. 领导者以 `plan_approval_response` 响应:

**批准**:

```json
{
  "type": "plan_approval_response",
  "request_id": "abc-123",
  "recipient": "implementer-1",
  "approve": true
}
```

**拒绝并反馈**:

```json
{
  "type": "plan_approval_response",
  "request_id": "abc-123",
  "recipient": "implementer-1",
  "approve": false,
  "feedback": "考虑边缘情况:如果认证服务不可用怎么办?"
}
```

## 关闭协议

### 优雅关闭步骤

1. **预关闭检查**
   - 检查进行中的任务
   - 向用户警告未完成的工作
   - 询问确认

2. **发送关闭请求**
   - 向每个队友发送 `shutdown_request`
   - 包含内容:"团队关闭请求。请完成当前工作并保存状态。"

3. **等待响应**
   - 队友以 `shutdown_response` 响应
   - 批准:队友准备关闭
   - 拒绝:队友需要更多时间,提供原因

4. **强制关闭(可选)**
   - 如果用户强制关闭,跳过等待
   - 直接调用清理

5. **清理**
   - 调用 `Teammate` 工具与 `operation: "cleanup"`
   - 删除团队配置和任务目录
   - 向用户显示关闭摘要

## 队友发现

### 读取团队配置

从 `~/.claude/teams/{team-name}/config.json` 读取以获取队友列表:

```json
{
  "teammates": [
    {
      "id": "uuid-1",
      "name": "implementer-1",
      "status": "working"
    },
    {
      "id": "uuid-2",
      "name": "implementer-2",
      "status": "idle"
    }
  ]
}
```

### 引用队友

- **始终使用名称**,而不是 UUID
- 名称是人类可读的,不太容易出错
- UUID 在消息上下文中不可见
