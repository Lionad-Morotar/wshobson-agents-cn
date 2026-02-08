---
description: "使用竞争假设和多个智能体的并行调查来调试问题"
argument-hint: "<error-description-or-file> [--hypotheses N] [--scope files|module|project]"
---

# Team Debug (团队调试)

使用竞争假设分析(ACH)方法调试复杂问题。多个调试器智能体并行调查不同的假设,收集证据以确认或证伪每个假设。

## 预检查

1. 验证 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 已设置
2. 从 `$ARGUMENTS` 解析:
   - `<error-description-or-file>`:bug 描述、错误消息或显示问题的文件路径
   - `--hypotheses N`: 要生成的假设数量(默认:3)
   - `--scope`: 调查范围 — `files`(特定文件)、`module`(模块/包)、`project`(整个项目)

## 阶段 1:初始分类

1. 分析错误描述或文件:
   - 如果是文件路径:读取文件,查找明显问题,收集错误上下文
   - 如果是错误描述:搜索代码库中的相关代码、错误消息、堆栈跟踪
2. 清楚地识别症状:什么失败,何时以及如何
3. 收集初始上下文:最近的 git 更改、相关测试、配置

## 阶段 2:假设生成

生成 N 个关于根本原因的假设,涵盖不同的失败模式类别:

1. **逻辑错误** — 错误的算法、错误条件、差一错误、缺失边缘情况
2. **数据问题** — 无效输入、类型不匹配、null/undefined、编码问题
3. **状态问题** — 竞态条件、陈旧缓存、错误初始化、变异 bug
4. **集成失败** — API 契约违反、版本不匹配、配置错误
5. **资源问题** — 内存泄漏、连接耗尽、超时、磁盘空间
6. **环境** — 缺失依赖、错误版本、平台特定行为

向用户展示假设:"已生成 {N} 个假设。正在生成调查者..."

## 阶段 3:调查

1. 使用 `Teammate` 工具和 `operation: "spawnTeam"`,团队名称:`debug-{timestamp}`
2. 对于每个假设,使用 `Task` 工具生成队友:
   - `name`: `investigator-{n}`(例如 "investigator-1")
   - `subagent_type`: "agent-teams:team-debugger"
   - `prompt`: 包括假设、调查范围和相关上下文
3. 为每个调查者的任务使用 `TaskCreate`:
   - 主题:"调查假设:{hypothesis summary}"
   - 描述:完整假设陈述、范围边界、证据标准

## 阶段 4:证据收集

1. 监控 TaskList 完成情况
2. 调查者完成时,收集他们的证据报告
3. 跟踪:"{completed}/{total} 个调查完成"

## 阶段 5:仲裁

1. 比较所有调查者的发现:
   - 哪些假设已确认(高置信度)?
   - 哪些已证伪(矛盾证据)?
   - 哪些无结论(证据不足)?

2. 对已确认的假设进行排名:
   - 置信度水平(高 > 中 > 低)
   - 因果链强度
   - 支持证据数量
   - 缺乏矛盾证据

3. 展示根本原因分析:

   ```
   ## 调试报告: {error description}

   ### 根本原因(最可能)
   **假设**: {description}
   **置信度**: {High/Medium/Low}
   **证据**: {summary with file:line citations}
   **因果链**: {step-by-step from cause to symptom}

   ### 建议修复
   {specific fix with code changes}

   ### 其他假设
   - {hypothesis 2}: {status} — {brief evidence summary}
   - {hypothesis 3}: {status} — {brief evidence summary}
   ```

## 阶段 6:清理

1. 向所有调查者发送 `shutdown_request`
2. 调用 `Teammate` cleanup 删除团队资源
