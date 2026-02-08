---
description: "使用预设(review、debug、feature、fullstack、research、security、migration)或自定义组合生成智能体团队"
argument-hint: "<preset|custom> [--name team-name] [--members N] [--delegate]"
---

# Team Spawn (团队生成)

使用预设配置或自定义组合生成多智能体团队。处理团队创建、队友生成和初始任务设置。

## 预检查

1. 验证 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 已设置:
   - 如果未设置,通知用户:"Agent Teams 需要实验性功能标志。在环境中设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。"
   - 如果未启用,停止执行

2. 从 `$ARGUMENTS` 解析参数:
   - 第一个位置参数:预设名称或 "custom"
   - `--name`: 团队名称(默认:从预设自动生成)
   - `--members N`: 覆盖默认成员数量
   - `--delegate`: 生成后进入委托模式

## 阶段 1:团队配置

### 预设团队

如果指定了预设,使用这些配置:

**`review`** — 多维度代码审查(默认:3 个成员)

- 生成 3 个具有维度的 `team-reviewer` 智能体:安全、性能、架构
- 团队名称默认:`review-team`

**`debug`** — 竞争假设调试(默认:3 个成员)

- 生成 3 个 `team-debugger` 智能体,每个分配不同的假设
- 团队名称默认:`debug-team`

**`feature`** — 并行功能开发(默认:3 个成员)

- 生成 1 个 `team-lead` 智能体 + 2 个 `team-implementer` 智能体
- 团队名称默认:`feature-team`

**`fullstack`** — 全栈开发(默认:4 个成员)

- 生成 1 个 `team-implementer`(前端)、1 个 `team-implementer`(后端)、1 个 `team-implementer`(测试)、1 个 `team-lead`
- 团队名称默认:`fullstack-team`

**`research`** — 并行代码库、网络和文档研究(默认:3 个成员)

- 生成 3 个 `general-purpose` 智能体,每个分配不同的研究问题或区域
- 智能体有权访问代码库搜索(Grep、Glob、Read)和网络搜索(WebSearch、WebFetch)
- 团队名称默认:`research-team`

**`security`** — 综合安全审计(默认:4 个成员)

- 生成 1 个 `team-reviewer`(OWASP/漏洞)、1 个 `team-reviewer`(认证/访问控制)、1 个 `team-reviewer`(依赖/供应链)、1 个 `team-reviewer`(机密/配置)
- 团队名称默认:`security-team`

**`migration`** — 代码库迁移或大型重构(默认:4 个成员)

- 生成 1 个 `team-lead`(协调 + 迁移计划)、2 个 `team-implementer`(并行迁移流)、1 个 `team-reviewer`(验证迁移正确性)
- 团队名称默认:`migration-team`

### 自定义组合

如果指定了 "custom":

1. 使用 AskUserQuestion 提示团队规模(2-5 个成员)
2. 对于每个成员,询问角色选择:team-lead、team-reviewer、team-debugger、team-implementer
3. 如果未通过 `--name` 提供,询问团队名称

## 阶段 2:团队创建

1. 使用 `Teammate` 工具和 `operation: "spawnTeam"` 创建团队
2. 对于每个团队成员,使用 `Task` 工具:
   - `team_name`: 团队名称
   - `name`: 描述性成员名称(例如 "security-reviewer"、"hypothesis-1")
   - `subagent_type`: "general-purpose"(队友需要完整的工具访问)
   - `prompt`: 引用相应智能体定义的角色特定指令

## 阶段 3:初始设置

1. 使用 `TaskCreate` 为每个队友创建初始占位符任务
2. 显示团队摘要:
   - 团队名称
   - 成员名称和角色
   - 显示模式(tmux/iTerm2/in-process)
3. 如果设置了 `--delegate` 标志,转换到委托模式

## 输出

显示格式化的团队摘要:

```
团队 "{team-name}" 生成成功!

成员:
  - {member-1-name} ({role})
  - {member-2-name} ({role})
  - {member-3-name} ({role})

使用 /team-status 监控进度
使用 /team-delegate 分配任务
使用 /team-shutdown 清理资源
```
