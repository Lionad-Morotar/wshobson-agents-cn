---
description: "启动具有专门审查维度的多审查者并行代码审查"
argument-hint: "<target> [--reviewers security,performance,architecture,testing,accessibility] [--base-branch main]"
---

# Team Review (团队审查)

编排多审查者并行代码审查,其中每个审查者专注于特定的质量维度。生成按严重程度组织的综合、去重报告。

## 预检查

1. 验证 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 已设置
2. 从 `$ARGUMENTS` 解析:
   - `<target>`:文件路径、目录、git diff 范围(例如 `main...HEAD`)或 PR 编号(例如 `#123`)
   - `--reviewers`:逗号分隔的维度(默认:`security,performance,architecture`)
   - `--base-branch`: diff 比较的基础分支(默认:`main`)

## 阶段 1:目标解析

1. 确定目标类型:
   - **文件/目录**: 原样用于审查范围
   - **Git diff 范围**: 使用 Bash 运行 `git diff {range} --name-only` 获取更改的文件
   - **PR 编号**: 使用 Bash 运行 `gh pr diff {number} --name-only` 获取更改的文件
2. 收集完整的 diff 内容以分发给审查者
3. 向用户显示审查范围:"{N} 个文件在 {M} 个维度上审查"

## 阶段 2:团队生成

1. 使用 `Teammate` 工具和 `operation: "spawnTeam"`,团队名称:`review-{timestamp}`
2. 对于每个请求的维度,使用 `Task` 工具生成队友:
   - `name`: `{dimension}-reviewer`(例如 "security-reviewer")
   - `subagent_type`: "agent-teams:team-reviewer"
   - `prompt`: 包括维度分配、目标文件和 diff 内容
3. 为每个审查者的任务使用 `TaskCreate`:
   - 主题:"审查 {target} 的 {dimension} 问题"
   - 描述:包括文件列表、diff 内容和维度特定检查清单

## 阶段 3:监控和收集

1. 等待所有审查任务完成(定期检查 `TaskList`)
2. 随着每个审查者完成,收集他们的结构化发现
3. 跟踪进度:"{completed}/{total} 个审查完成"

## 阶段 4:整合

1. **去重**: 合并引用相同 file:line 位置的发现
2. **解决冲突**: 如果审查者在严重程度上有分歧,使用较高的评级
3. **按严重程度组织**: 将发现分组为严重、高、中、低
4. **交叉引用**: 注意在多个维度中出现的发现

## 阶段 5:报告和清理

1. 展示综合报告:

   ```
   ## 代码审查报告: {target}

   审查者: {dimensions}
   已审查文件: {count}

   ### 严重 ({count})
   [发现...]

   ### 高 ({count})
   [发现...]

   ### 中 ({count})
   [发现...]

   ### 低 ({count})
   [发现...]

   ### 摘要
   总发现: {count} (严重: N, 高: N, 中: N, 低: N)
   ```

2. 向所有审查者发送 `shutdown_request`
3. 调用 `Teammate` cleanup 删除团队资源
