# Agent Teams 插件

使用 Claude Code 实验性的 [Agent Teams](https://code.claude.com/docs/en/agent-teams) 功能编排多智能体团队,进行并行代码审查、假设驱动调试和协调功能开发。

## 设置

### 前置要求

1. 启用实验性的 Agent Teams 功能:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

2. 在你的 `~/.claude/settings.json` 中配置队友显示模式:

```json
{
  "teammateMode": "tmux"
}
```

可用的显示模式:

- `"tmux"` — 每个队友在一个 tmux 窗格中运行(推荐)
- `"iterm2"` — 每个队友获得一个 iTerm2 标签页(仅 macOS)
- `"in-process"` — 队友在同一进程中运行(默认)

### 安装

首先,添加市场源(如果尚未添加):

```
/plugin marketplace add wshobson/agents
```

然后安装插件:

```
/plugin install agent-teams@claude-code-workflows
```

## 功能特性

- **预设团队** — 为常见工作流程生成预配置的团队(审查、调试、功能、全栈、研究、安全、迁移)
- **多维度代码审查** — 跨安全、性能、架构、测试和可访问性维度的并行审查
- **假设驱动调试** — 竞争假设调查与基于证据的根因分析
- **并行功能开发** — 具有文件所有权边界的协调多智能体实现
- **并行研究** — 多个 Explore 智能体同时调查不同的问题或代码库区域
- **安全审计** — 跨 OWASP、认证、依赖和配置的综合并行安全审查
- **迁移支持** — 协调的代码库迁移,具有并行实现流和正确性验证
- **任务协调** — 具有工作负载平衡的依赖感知任务管理
- **团队通信** — 高效智能体协作的结构化消息协议

## 命令

| 命令              | 描述                                                      |
| ----------------- | --------------------------------------------------------- |
| `/team-spawn`     | 使用预设或自定义组合生成一个团队                           |
| `/team-status`    | 显示团队成员、任务和进度                                   |
| `/team-shutdown`  | 优雅地关闭一个团队并清理资源                              |
| `/team-review`    | 多审查者并行代码审查                                       |
| `/team-debug`     | 竞争假设调试与并行调查                                    |
| `/team-feature`   | 具有文件所有权的并行功能开发                               |
| `/team-delegate`  | 任务委托仪表盘和工作负载管理                               |

## 智能体

| 智能体            | 角色                                                            | 颜色  |
| ----------------- | --------------------------------------------------------------- | ----- |
| `team-lead`       | 团队编排者 — 分解工作、管理生命周期、综合结果                   | 蓝色  |
| `team-reviewer`   | 多维度代码审查者 — 在指定的审查维度上工作                       | 绿色  |
| `team-debugger`   | 假设调查者 — 收集证据以确认/证伪指定的假设                      | 红色  |
| `team-implementer` | 并行构建者 — 在严格的文件所有权边界内实现                       | 黄色  |

## 技能

| 技能                           | 描述                                                        |
| ------------------------------ | ----------------------------------------------------------- |
| `team-composition-patterns`    | 团队规模启发式、预设组合、智能体类型选择                     |
| `task-coordination-strategies` | 任务分解、依赖图、工作负载监控                               |
| `parallel-debugging`           | 假设生成、证据收集、结果仲裁                                 |
| `multi-reviewer-patterns`      | 审查维度分配、发现去重、严重程度校准                         |
| `parallel-feature-development` | 文件所有权策略、冲突避免、集成模式                           |
| `team-communication-protocols` | 消息类型选择、计划批准工作流、关闭协议                       |

## 快速开始

### 多维度代码审查

```
/team-review src/ --reviewers security,performance,architecture
```

生成 3 个审查者,每个从其指定的维度分析代码库,然后将发现整合到优先级报告中。

### 假设驱动调试

```
/team-debug "API returns 500 on POST /users with valid payload" --hypotheses 3
```

生成 3 个竞争假设,为每个假设生成调查者,收集证据,并展示最可能的根本原因及其修复方案。

### 并行功能开发

```
/team-feature "Add user authentication with OAuth2" --team-size 3 --plan-first
```

将功能分解为具有文件所有权边界的工作流,获得你的批准,然后生成实现者并行构建。

### 并行研究

```
/team-spawn research --name codebase-research
```

生成 3 个研究人员并行调查不同方面 — 跨越你的代码库(Grep/Read)和网络(WebSearch/WebFetch)。每个都报告带有引用的发现。

### 安全审计

```
/team-spawn security
```

生成 4 个安全审查者,覆盖 OWASP 漏洞、认证/访问控制、依赖供应链和机密/配置。生成综合安全报告。

### 代码库迁移

```
/team-spawn migration --name react-hooks-migration
```

生成一个领导者来规划迁移,2 个实现者来并行迁移代码,以及一个审查者来验证迁移代码的正确性。

### 自定义团队

```
/team-spawn custom --name my-team --members 4
```

交互式地配置团队组合,具有自定义角色和智能体类型。

## 最佳实践

1. **从预设开始** — 在构建自定义团队之前,先使用 `/team-spawn review`、`/team-spawn debug` 或 `/team-spawn feature`
2. **使用 `--plan-first`** — 对于功能开发,在生成实现者之前始终审查分解方案
3. **文件所有权至关重要** — 永远不要将同一文件分配给多个实现者;在边界处使用接口契约
4. **使用 `/team-status` 监控** — 定期检查进度,如果工作不均,使用 `/team-delegate --rebalance`
5. **优雅关闭** — 始终使用 `/team-shutdown` 而不是手动终止进程
6. **保持小团队** — 2-4 个队友是最佳的;更大的团队会增加协调开销
7. **使用 Shift+Tab** — Claude Code 内置的委托模式(Shift+Tab)与这些命令互补,用于临时委托
