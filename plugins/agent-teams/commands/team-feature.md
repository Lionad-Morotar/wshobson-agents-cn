---
description: "使用文件所有权边界和依赖管理与多个智能体并行开发功能"
argument-hint: "<feature-description> [--team-size N] [--branch feature/name] [--plan-first]"
---

# Team Feature (团队功能)

编排多个实现者智能体的并行功能开发。将功能分解为具有严格文件所有权的工作流,管理依赖关系并验证集成。

## 预检查

1. 验证 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 已设置
2. 从 `$ARGUMENTS` 解析:
   - `<feature-description>`: 要构建的功能描述
   - `--team-size N`: 实现者数量(默认:2)
   - `--branch`: git 分支名称(默认:从功能描述自动生成)
   - `--plan-first`: 在生成前分解并获得用户批准

## 阶段 1:分析

1. 分析功能描述以了解范围
2. 探索代码库以识别:
   - 需要修改的文件
   - 要遵循的现有模式和约定
   - 与现有代码的集成点
   - 需要更新的测试文件

## 阶段 2:分解

1. 将功能分解为工作流:
   - 每个工作流获得独占文件所有权(无重叠文件)
   - 在工作流之间定义接口契约
   - 识别工作流之间的依赖关系(blockedBy/blocks)
   - 跨工作流平衡工作负载

2. 如果设置了 `--plan-first`:
   - 向用户展示分解:

     ```
     ## 功能分解: {feature}

     ### 工作流 1: {name}
     所有者: implementer-1
     文件: {list}
     依赖: 无

     ### 工作流 2: {name}
     所有者: implementer-2
     文件: {list}
     依赖: 被工作流 1 阻塞(需要来自 {file} 的接口)

     ### 集成契约
     {shared types/interfaces}
     ```

   - 继续前等待用户批准
   - 如果用户请求更改,调整分解

## 阶段 3:团队生成

1. 如果指定了 `--branch`,使用 Bash 创建并检出分支:
   ```
   git checkout -b {branch-name}
   ```
2. 使用 `Teammate` 工具和 `operation: "spawnTeam"`,团队名称:`feature-{timestamp}`
3. 生成一个 `team-lead` 智能体进行协调
4. 对于每个工作流,使用 `Task` 工具生成 `team-implementer`:
   - `name`: `implementer-{n}`
   - `subagent_type`: "agent-teams:team-implementer"
   - `prompt`: 包括拥有的文件、接口契约和实现要求

## 阶段 4:任务创建

1. 为每个工作流使用 `TaskCreate`:
   - 主题:"{stream name}"
   - 描述:拥有的文件、要求、接口契约、验收标准
2. 使用 `TaskUpdate` 为依赖工作流设置 `blockedBy` 关系
3. 使用 `TaskUpdate` 将任务分配给实现者(设置 `owner`)

## 阶段 5:监控和协调

1. 监控 `TaskList` 进度
2. 实现者完成任务时:
   - 检查集成问题
   - 解除依赖任务的阻塞
   - 如需要重新平衡
3. 处理集成点协调:
   - 当实现者完成接口时,通知依赖实现者

## 阶段 6:集成验证

所有任务完成后:

1. 使用 Bash 验证代码编译/构建:运行适当的构建命令
2. 使用 Bash 运行测试:运行适当的测试命令
3. 如果发现问题,创建修复任务并分配给适当的实现者
4. 向用户报告集成状态

## 阶段 7:清理

1. 展示功能摘要:

   ```
   ## 功能完成: {feature}

   已修改文件: {count}
   已完成工作流: {count}/{total}
   测试: {pass/fail}

   更改在分支上: {branch-name}
   ```

2. 向所有队友发送 `shutdown_request`
3. 调用 `Teammate` cleanup
