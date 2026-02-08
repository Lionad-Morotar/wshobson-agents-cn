---
description: "从需求到部署的端到端功能开发协调"
argument-hint: "<功能描述> [--methodology tdd|bdd|ddd] [--complexity simple|medium|complex]"
---

# 功能开发协调器

## 关键行为规则

你必须完全遵循这些规则。违反其中任何一条即为失败。

1. **按顺序执行步骤。** 不要跳过、重新排序或合并步骤。
2. **写入输出文件。** 每个步骤必须在下一步开始之前在 `.feature-dev/` 中生成其输出文件。从上一步骤的文件读取——不要依赖上下文窗口记忆。
3. **在检查点停止。** 当你到达 `PHASE CHECKPOINT` 时，必须停止并等待用户明确批准后才能继续。使用 AskUserQuestion 工具并提供清晰的选项。
4. **失败时停止。** 如果任何步骤失败（代理错误、测试失败、缺少依赖），立即停止。展示错误并询问用户如何继续。不要默默继续。
5. **仅使用本地代理。** 所有 `subagent_type` 引用使用由此插件捆绑的代理或 `general-purpose`。无跨插件依赖。
6.** 从不自主进入计划模式。** 不要使用 EnterPlanMode。此命令就是计划——执行它。

## 启动前检查

在开始之前，执行这些检查：

### 1. 检查现有会话

检查 `.feature-dev/state.json` 是否存在：

- 如果存在且 `status` 为 `"in_progress"`：读取它，显示当前步骤，并询问用户：

  ```
  发现一个进行中的功能开发会话：
  功能：[来自状态的名称]
  当前步骤：[来自状态的步骤]

  1. 从我们离开的地方恢复
  2. 重新开始（归档现有会话）
  ```

- 如果存在且 `status` 为 `"complete"`：询问是否归档并重新开始。

### 2. 初始化状态

创建 `.feature-dev/` 目录和 `state.json`：

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "methodology": "traditional",
  "complexity": "medium",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

从 `$ARGUMENTS` 中解析 `--methodology` 和 `--complexity` 标志。如果未指定则使用默认值。

### 3. 解析功能描述

从 `$ARGUMENTS` 中提取功能描述（标志之前的所有内容）。这在下面的提示中被引用为 `$FEATURE`。

---

## 第一阶段：发现（步骤 1-2）— 交互式

### 步骤 1：需求收集

通过交互式问答收集需求。一次使用 AskUserQuestion 工具问一个问题。不要一次问所有问题。

**要问的问题（按顺序）：**

1. **问题陈述**："此功能解决什么问题？谁是用户，他们的痛点是什么？"
2. **验收标准**："关键验收标准是什么？此功能何时才算'完成'？"
3. **范围边界**："此功能明确排除什么？"
4. **技术约束**："有任何技术约束吗？（例如，必须使用现有的身份验证系统、特定数据库、延迟要求）"
5. **依赖关系**："此功能是否依赖或影响其他功能/服务？"

收集答案后，编写需求文档：

**输出文件：** `.feature-dev/01-requirements.md`

```markdown
# 需求：$FEATURE

## 问题陈述

[来自 Q1]

## 验收标准

[来自 Q2 — 格式化为复选框]

## 范围

### 包含范围

[从答案推导]

### 排除范围

[来自 Q3]

## 技术约束

[来自 Q4]

## 依赖关系

[来自 Q5]

## 方法论：[tdd|bdd|ddd|traditional]

## 复杂度：[simple|medium|complex]
```

更新 `state.json`：将 `current_step` 设置为 2，将 `"01-requirements.md"` 添加到 `files_created`，将步骤 1 添加到 `completed_steps`。

### 步骤 2：架构和安全设计

读取 `.feature-dev/01-requirements.md` 以加载需求上下文。

使用 Task 工具启动架构代理：

```
Task:
  subagent_type: "backend-architect"
  description: "为 $FEATURE 设计架构"
  prompt: |
    为此功能设计技术架构。

    ## 需求
    [插入 .feature-dev/01-requirements.md 的完整内容]

    ## 交付物
    1. **服务/组件设计**：需要哪些组件、它们的职责和边界
    2. **API 设计**：端点、请求/响应架构、错误处理
    3. **数据模型**：数据库表/集合、关系、所需的迁移
    4. **安全考虑**：身份验证要求、输入验证、数据保护、OWASP 关注点
    5. **集成点**：如何连接到现有服务/系统
    6. **风险评估**：技术风险和缓解策略

    将你的完整架构设计编写为单个 markdown 文档。
```

将代理的输出保存到 `.feature-dev/02-architecture.md`。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-1"，将步骤 2 添加到 `completed_steps`。

---

## 阶段检查点 1 — 需要用户批准

你必须在这里停止并展示架构以供审查。

显示 `.feature-dev/02-architecture.md` 中架构的摘要（关键组件、API 端点、数据模型概述）并询问：

```
架构设计已完成。请查看 .feature-dev/02-architecture.md

1. 批准 — 继续实施
2. 请求更改 — 告诉我需要调整什么
3. 暂停 — 保存进度并在此停止
```

在用户选择选项 1 之前，不要继续进行第二阶段。如果他们选择选项 2，修订架构并重新检查点。如果选择选项 3，更新 `state.json` 状态并停止。

---

## 第二阶段：实施（步骤 3-5）

### 步骤 3：后端实施

读取 `.feature-dev/01-requirements.md` 和 `.feature-dev/02-architecture.md`。

使用 Task 工具启动后端架构师进行实施：

```
Task:
  subagent_type: "backend-architect"
  description: "为 $FEATURE 实施后端"
  prompt: |
    根据批准的架构为此功能实施后端。

    ## 需求
    [插入 .feature-dev/01-requirements.md 的内容]

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 指示
    1. 按照设计实施 API 端点、业务逻辑和数据访问层
    2. 包括架构中指定的数据层组件（模型、迁移、存储库）
    3. 添加输入验证和错误处理
    4. 遵循项目现有的代码模式和约定
    5. 如果方法论是 TDD：先编写失败的测试，然后实施
    6. 仅在逻辑非显而易见的地方添加内联注释

    编写所有代码文件。报告创建/修改了哪些文件。
```

将实施内容的摘要保存到 `.feature-dev/03-backend.md`（创建/修改的文件列表、关键决策、与架构的任何偏差）。

更新 `state.json`：将 `current_step` 设置为 4，将步骤 3 添加到 `completed_steps`。

### 步骤 4：前端实施

读取 `.feature-dev/01-requirements.md`、`.feature-dev/02-architecture.md` 和 `.feature-dev/03-backend.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "为 $FEATURE 实施前端"
  prompt: |
    你是一名前端开发人员。为此功能实施前端组件。

    ## 需求
    [插入 .feature-dev/01-requirements.md 的内容]

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 后端实施
    [插入 .feature-dev/03-backend.md 的内容]

    ## 指示
    1. 构建与后端 API 端点集成的 UI 组件
    2. 实施状态管理、表单处理和错误状态
    3. 在适当的地方添加加载状态和乐观更新
    4. 遵循项目现有的前端模式和组件约定
    5. 确保响应式设计和基本的可访问性（语义化 HTML、ARIA 标签、键盘导航）

    编写所有代码文件。报告创建/修改了哪些文件。
```

将摘要保存到 `.feature-dev/04-frontend.md`。

**注意：** 如果该功能没有前端组件（纯后端/API），请跳过此步骤 — 在 `04-frontend.md` 中写一个简短的注释说明跳过的原因，然后继续。

更新 `state.json`：将 `current_step` 设置为 5，将步骤 4 添加到 `completed_steps`。

### 步骤 5：测试和验证

读取 `.feature-dev/03-backend.md` 和 `.feature-dev/04-frontend.md`。

在单个响应中使用多个 Task 工具调用并行启动三个代理：

**5a. 测试套件创建：**

```
Task:
  subagent_type: "test-automator"
  description: "为 $FEATURE 创建测试套件"
  prompt: |
    为此功能创建全面的测试套件。

    ## 已实施的内容
    ### 后端
    [插入 .feature-dev/03-backend.md 的内容]

    ### 前端
    [插入 .feature-dev/04-frontend.md 的内容]

    ## 指示
    1. 为所有新的后端函数/方法编写单元测试
    2. 为 API 端点编写集成测试
    3. 如适用，编写前端组件测试
    4. 覆盖：快乐路径、边缘情况、错误处理、边界条件
    5. 遵循项目中现有的测试模式和框架
    6. 新代码的目标覆盖率为 80% 以上

    编写所有测试文件。报告创建了哪些测试文件以及它们覆盖的内容。
```

**5b. 安全审查：**

```
Task:
  subagent_type: "security-auditor"
  description: "对 $FEATURE 进行安全审查"
  prompt: |
    对此功能实施进行安全审查。

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 后端实施
    [插入 .feature-dev/03-backend.md 的内容]

    ## 前端实施
    [插入 .feature-dev/04-frontend.md 的内容]

    审查：OWASP Top 10、身份验证/授权缺陷、输入验证差距、
    数据保护问题、依赖漏洞以及任何安全反模式。

    提供带有严重性、位置和具体修复建议的发现。
```

**5c. 性能审查：**

```
Task:
  subagent_type: "performance-engineer"
  description: "对 $FEATURE 进行性能审查"
  prompt: |
    审查此功能实施的性能。

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 后端实施
    [插入 .feature-dev/03-backend.md 的内容]

    ## 前端实施
    [插入 .feature-dev/04-frontend.md 的内容]

    审查：N+1 查询、缺少索引、未优化的查询、内存泄漏、
    缺少缓存机会、大负载、慢速渲染路径。

    提供带有影响估计和具体优化建议的发现。
```

所有三个完成后，将结果合并到 `.feature-dev/05-testing.md`：

```markdown
# 测试和验证：$FEATURE

## 测试套件

[来自 5a 的摘要 — 创建的文件、覆盖区域]

## 安全发现

[来自 5b 的摘要 — 按严重性分类的发现]

## 性能发现

[来自 5c 的摘要 — 按影响分类的发现]

## 行动项

[列出在交付前需要解决的任何关键/高严重性发现]
```

如果安全或性能审查中有关键或高严重性的发现，请在继续之前立即解决它们。应用修复并重新验证。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-2"，将步骤 5 添加到 `completed_steps`。

---

## 阶段检查点 2 — 需要用户批准

显示 `.feature-dev/05-testing.md` 中的测试和验证结果摘要并询问：

```
测试和验证已完成。请查看 .feature-dev/05-testing.md

测试覆盖率：[摘要]
安全发现：[X 个关键，Y 个高，Z 个中等]
性能发现：[X 个关键，Y 个高，Z 个中等]

1. 批准 — 继续部署和文档
2. 请求更改 — 告诉我需要修复什么
3. 暂停 — 保存进度并在此停止
```

在用户批准之前，不要继续进行第三阶段。

---

## 第三阶段：交付（步骤 6-7）

### 步骤 6：部署和监控

读取 `.feature-dev/02-architecture.md` 和 `.feature-dev/05-testing.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "为 $FEATURE 创建部署配置"
  prompt: |
    你是一名部署工程师。为此功能创建部署和监控配置。

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 测试结果
    [插入 .feature-dev/05-testing.md 的内容]

    ## 指示
    1. 为新代码创建或更新 CI/CD 管道配置
    2. 如果功能应逐步推出，则添加功能标志配置
    3. 为新服务/端点定义健康检查和就绪探针
    4. 为关键指标创建监控警报（错误率、延迟、吞吐量）
    5. 编写带有回滚步骤的部署运行手册
    6. 遵循项目中现有的部署模式

    编写所有配置文件。报告创建/修改了什么。
```

将输出保存到 `.feature-dev/06-deployment.md`。

更新 `state.json`：将 `current_step` 设置为 7，将步骤 6 添加到 `completed_steps`。

### 步骤 7：文档和交接

读取所有之前的 `.feature-dev/*.md` 文件。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "为 $FEATURE 编写文档"
  prompt: |
    你是一名技术文档编写者。为此功能创建文档。

    ## 功能上下文
    [插入 .feature-dev/01-requirements.md 的内容]

    ## 架构
    [插入 .feature-dev/02-architecture.md 的内容]

    ## 实施摘要
    ### 后端：[插入 .feature-dev/03-backend.md 的内容]
    ### 前端：[插入 .feature-dev/04-frontend.md 的内容]

    ## 部署
    [插入 .feature-dev/06-deployment.md 的内容]

    ## 指示
    1. 为新端点编写 API 文档（请求/响应示例）
    2. 如适用，更新或创建面向用户的文档
    3. 编写简短的架构决策记录（ADR）以解释关键设计选择
    4. 创建交接摘要：构建了什么、如何测试它、已知限制

    编写文档文件。报告创建/修改了什么。
```

将输出保存到 `.feature-dev/07-documentation.md`。

更新 `state.json`：将 `current_step` 设置为 "complete"，将步骤 7 添加到 `completed_steps`。

---

## 完成

更新 `state.json`：

- 将 `status` 设置为 `"complete"`
- 将 `last_updated` 设置为当前时间戳

展示最终摘要：

```
功能开发已完成：$FEATURE

## 已创建文件
[列出所有 .feature-dev/ 输出文件]

## 实施摘要
- 需求：.feature-dev/01-requirements.md
- 架构：.feature-dev/02-architecture.md
- 后端：.feature-dev/03-backend.md
- 前端：.feature-dev/04-frontend.md
- 测试：.feature-dev/05-testing.md
- 部署：.feature-dev/06-deployment.md
- 文档：.feature-dev/07-documentation.md

## 后续步骤
1. 审查所有生成的代码和文档
2. 运行完整的测试套件以验证一切通过
3. 使用实施创建拉取请求
4. 使用 .feature-dev/06-deployment.md 中的运行手册进行部署
```
