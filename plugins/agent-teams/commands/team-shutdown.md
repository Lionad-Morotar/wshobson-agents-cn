---
description: "优雅地关闭智能体团队,收集最终结果并清理资源"
argument-hint: "[team-name] [--force] [--keep-tasks]"
---

# Team Shutdown (团队关闭)

通过向所有队友发送关闭请求、收集最终结果并清理团队资源来优雅地关闭活动智能体团队。

## 阶段 1:关闭前

1. 从 `$ARGUMENTS` 解析团队名称和标志:
   - 如果没有团队名称,检查活动团队(与 team-status 相同的发现)
   - `--force`: 跳过等待优雅关闭响应
   - `--keep-tasks`: 清理后保留任务列表

2. 使用 Read 工具从 `~/.claude/teams/{team-name}/config.json` 读取团队配置
3. 调用 `TaskList` 检查进行中的任务

4. 如果有进行中的任务且未设置 `--force`:
   - 显示警告:"警告:{N} 个任务仍在进行中"
   - 列出进行中的任务
   - 询问用户:"继续关闭? 进行中的工作可能会丢失。"

## 阶段 2:优雅关闭

对于团队中的每个队友:

1. 使用 `SendMessage` 和 `type: "shutdown_request"` 请求优雅关闭
   - 包含内容:"团队关闭请求。请完成当前工作并保存状态。"
2. 等待关闭响应
   - 如果队友批准:标记为已关闭
   - 如果队友拒绝:向用户报告原因
   - 如果 `--force`: 不等待响应

## 阶段 3:清理

1. 显示关闭摘要:

   ```
   团队 "{team-name}" 关闭完成。

   已关闭成员: {N}/{total}
   已完成任务: {completed}/{total}
   剩余任务: {remaining}
   ```

2. 除非设置了 `--keep-tasks`,否则调用 `Teammate` 工具和 `operation: "cleanup"` 删除团队和任务目录

3. 如果设置了 `--keep-tasks`,通知用户:"任务列表已保存在 ~/.claude/tasks/{team-name}/"
