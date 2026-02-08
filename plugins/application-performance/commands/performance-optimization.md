---
description: "编排端到端的应用程序性能优化，从性能分析到监控"
argument-hint: "<application or service> [--focus latency|throughput|cost|balanced] [--depth quick-wins|comprehensive|enterprise]"
---

# 性能优化编排器

## 关键行为规则

你必须完全遵守这些规则。违反任何一条都视为失败。

1. **按顺序执行步骤。** 不要跳过、重新排序或合并步骤。
2. **写入输出文件。** 每个步骤必须在下一步开始前在 `.performance-optimization/` 中生成其输出文件。从之前的步骤文件中读取 — 不要依赖上下文窗口内存。
3. **在检查点停止。** 当你到达 `PHASE CHECKPOINT` 时，你必须停止并等待用户明确批准后才能继续。使用 AskUserQuestion 工具并提供清晰的选项。
4. **遇到失败时停止。** 如果任何步骤失败（代理错误、测试失败、缺少依赖项），立即停止。显示错误并询问用户如何继续。不要静默继续。
5. **仅使用本地代理。** 所有 `subagent_type` 引用使用此插件捆绑的代理或 `general-purpose`。无跨插件依赖。
6. **不要自主进入计划模式。** 不要使用 EnterPlanMode。此命令本身就是计划 — 执行它。

## 飞行前检查

在开始之前，执行这些检查：

### 1. 检查现有会话

检查 `.performance-optimization/state.json` 是否存在：

- 如果存在且 `status` 为 `"in_progress"`：读取它，显示当前步骤，并询问用户：

  ```
  发现一个进行中的性能优化会话：
  目标：[来自 state 的名称]
  当前步骤：[来自 state 的步骤]

  1. 从我们停止的地方继续
  2. 重新开始（归档现有会话）
  ```

- 如果存在且 `status` 为 `"complete"`：询问是否归档并重新开始。

### 2. 初始化状态

创建 `.performance-optimization/` 目录和 `state.json`：

```json
{
  "target": "$ARGUMENTS",
  "status": "in_progress",
  "focus": "balanced",
  "depth": "comprehensive",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

解析 `$ARGUMENTS` 中的 `--focus` 和 `--depth` 标志。如果未指定，使用默认值。

### 3. 解析目标描述

从 `$ARGUMENTS` 中提取目标描述（标志之前的所有内容）。这在下面的提示中引用为 `$TARGET`。

---

## 第 1 阶段：性能分析和基线（步骤 1-3）

### 步骤 1：全面性能分析

使用 Task 工具启动性能工程师：

```
Task:
  subagent_type: "performance-engineer"
  description: "分析 $TARGET 的应用程序性能"
  prompt: |
    全面分析以下内容的性能：$TARGET。

    生成 CPU 使用率的火焰图、内存分析的堆转储、跟踪 I/O 操作
    并识别热路径。如果可用，使用 DataDog 或 New Relic 等 APM 工具。包括数据库
    查询分析、API 响应时间和前端渲染指标。为所有关键用户旅程建立性能基线。

    ## 交付成果
    1. 包含火焰图和内存分析的性能分析
    2. 按影响排序的瓶颈识别
    3. 关键用户旅程的基线指标
    4. 数据库查询分析结果
    5. API 响应时间测量

    将你的完整分析报告作为单个 markdown 文档编写。
```

将代理的输出保存到 `.performance-optimization/01-profiling.md`。

更新 `state.json`：将 `current_step` 设置为 2，将步骤 1 添加到 `completed_steps`。

### 步骤 2：可观测性技术栈评估

读取 `.performance-optimization/01-profiling.md` 以加载分析上下文。

使用 Task 工具：

```
Task:
  subagent_type: "observability-engineer"
  description: "评估 $TARGET 的可观测性设置"
  prompt: |
    评估以下内容的当前可观测性设置：$TARGET。

    ## 性能分析
    [插入 .performance-optimization/01-profiling.md 的完整内容]

    审查现有监控、使用 OpenTelemetry 的分布式追踪、日志聚合
    和指标收集。识别可见性差距、缺失指标以及需要更好检测的领域。
    推荐针对业务关键操作的 APM 工具集成和自定义指标。

    ## 交付成果
    1. 当前可观测性评估
    2. 已识别的检测差距
    3. 监控建议
    4. 推荐的指标和仪表板

    将你的完整评估作为单个 markdown 文档编写。
```

将代理的输出保存到 `.performance-optimization/02-observability.md`。

更新 `state.json`：将 `current_step` 设置为 3，将步骤 2 添加到 `completed_steps`。

### 步骤 3：用户体验分析

读取 `.performance-optimization/01-profiling.md`。

使用 Task 工具：

```
Task:
  subagent_type: "performance-engineer"
  description: "分析 $TARGET 的用户体验指标"
  prompt: |
    分析以下内容的用户体验指标：$TARGET。

    ## 性能基线
    [插入 .performance-optimization/01-profiling.md 的内容]

    测量核心 Web 指标（LCP、FID、CLS）、页面加载时间、可交互时间
    和感知性能。如果可用，使用真实用户监控（RUM）数据。
    识别性能较差的用户旅程及其业务影响。

    ## 交付成果
    1. 核心 Web 指标分析
    2. 用户旅程性能报告
    3. 业务影响评估
    4. 优先排序的改进机会

    将你的完整分析作为单个 markdown 文档编写。
```

将代理的输出保存到 `.performance-optimization/03-ux-analysis.md`。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-1"，将步骤 3 添加到 `completed_steps`。

---

## 阶段检查点 1 — 需要用户批准

你必须在此停止并展示分析结果以供审查。

显示来自 `.performance-optimization/01-profiling.md`、`.performance-optimization/02-observability.md` 和 `.performance-optimization/03-ux-analysis.md` 的摘要（关键瓶颈、可观测性差距、UX 发现）并询问：

```
性能分析完成。请审查：
- .performance-optimization/01-profiling.md
- .performance-optimization/02-observability.md
- .performance-optimization/03-ux-analysis.md

关键瓶颈：[摘要]
可观测性差距：[摘要]
UX 发现：[摘要]

1. 批准 — 继续进行优化
2. 请求更改 — 告诉我需要调整什么
3. 暂停 — 保存进度并在此停止
```

在用户选择选项 1 之前，不要进入第 2 阶段。如果他们选择选项 2，修改并重新检查点。如果选择选项 3，更新 `state.json` 状态并停止。

---

## 第 2 阶段：数据库和后端优化（步骤 4-6）

### 步骤 4：数据库性能优化

读取 `.performance-optimization/01-profiling.md` 和 `.performance-optimization/03-ux-analysis.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "优化 $TARGET 的数据库性能"
  prompt: |
    你是数据库优化专家。优化以下内容的数据库性能：$TARGET。

    ## 分析数据
    [插入 .performance-optimization/01-profiling.md 的内容]

    ## UX 分析
    [插入 .performance-optimization/03-ux-analysis.md 的内容]

    分析慢查询日志、创建缺失的索引、优化执行计划、使用
    Redis/Memcached 实现查询结果缓存。审查连接池、预处理语句
    和批处理机会。如果需要，考虑只读副本和数据库分片。

    ## 交付成果
    1. 优化的查询及其前后性能
    2. 新索引及其理由
    3. 缓存策略建议
    4. 连接池配置
    5. 按优先顺序的实施计划

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/04-database.md`。

更新 `state.json`：将 `current_step` 设置为 5，将步骤 4 添加到 `completed_steps`。

### 步骤 5：后端代码和 API 优化

读取 `.performance-optimization/01-profiling.md` 和 `.performance-optimization/04-database.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "优化 $TARGET 的后端服务"
  prompt: |
    你是后端性能架构师。优化以下内容的后端服务：$TARGET。

    ## 分析数据
    [插入 .performance-optimization/01-profiling.md 的内容]

    ## 数据库优化
    [插入 .performance-optimization/04-database.md 的内容]

    实现高效算法、添加应用级缓存、优化 N+1 查询、
    有效使用 async/await 模式。实现分页、响应压缩、
    GraphQL 查询优化和批量 API 操作。添加断路器和隔板以提高弹性。

    ## 交付成果
    1. 优化的后端代码及其前后指标
    2. 缓存实施计划
    3. API 改进及其预期影响
    4. 添加的弹性模式
    5. 实施优先顺序

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/05-backend.md`。

更新 `state.json`：将 `current_step` 设置为 6，将步骤 5 添加到 `completed_steps`。

### 步骤 6：微服务和分布式系统优化

读取 `.performance-optimization/01-profiling.md` 和 `.performance-optimization/05-backend.md`。

使用 Task 工具：

```
Task:
  subagent_type: "performance-engineer"
  description: "优化 $TARGET 的分布式系统性能"
  prompt: |
    优化以下内容的分布式系统性能：$TARGET。

    ## 分析数据
    [插入 .performance-optimization/01-profiling.md 的内容]

    ## 后端优化
    [插入 .performance-optimization/05-backend.md 的内容]

    分析服务间通信、实现服务网格优化、
    优化消息队列性能（Kafka/RabbitMQ）、减少网络跳数。实现
    分布式缓存策略并优化序列化/反序列化。

    ## 交付成果
    1. 服务通信改进
    2. 消息队列优化计划
    3. 分布式缓存设置
    4. 网络优化建议
    5. 预期的延迟改进

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/06-distributed.md`。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-2"，将步骤 6 添加到 `completed_steps`。

---

## 阶段检查点 2 — 需要用户批准

显示步骤 4-6 的优化计划摘要并询问：

```
后端优化计划完成。请审查：
- .performance-optimization/04-database.md
- .performance-optimization/05-backend.md
- .performance-optimization/06-distributed.md

1. 批准 — 继续进行前端和 CDN 优化
2. 请求更改 — 告诉我需要调整什么
3. 暂停 — 保存进度并在此停止
```

在用户批准之前，不要进入第 3 阶段。

---

## 第 3 阶段：前端和 CDN 优化（步骤 7-9）

### 步骤 7：前端打包和加载优化

读取 `.performance-optimization/03-ux-analysis.md` 和 `.performance-optimization/05-backend.md`。

使用 Task 工具：

```
Task:
  subagent_type: "frontend-developer"
  description: "优化 $TARGET 的前端性能"
  prompt: |
    优化以下内容的前端性能：$TARGET，针对核心 Web 指标的改进。

    ## UX 分析
    [插入 .performance-optimization/03-ux-analysis.md 的内容]

    ## 后端优化
    [插入 .performance-optimization/05-backend.md 的内容]

    实现代码分割、tree shaking、懒加载和动态导入。使用 webpack/rollup 分析优化打包大小。
    实现资源提示（prefetch、preconnect、preload）。
    优化关键渲染路径并消除渲染阻塞资源。

    ## 交付成果
    1. 打包优化及其大小减少
    2. 懒加载实施计划
    3. 资源提示配置
    4. 关键渲染路径优化
    5. 预期的核心 Web 指标改进

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/07-frontend.md`。

更新 `state.json`：将 `current_step` 设置为 8，将步骤 7 添加到 `completed_steps`。

### 步骤 8：CDN 和边缘优化

读取 `.performance-optimization/07-frontend.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "优化 $TARGET 的 CDN 和边缘性能"
  prompt: |
    你是云基础设施和 CDN 优化专家。优化以下内容的 CDN 和边缘
    性能：$TARGET。

    ## 前端优化
    [插入 .performance-optimization/07-frontend.md 的内容]

    配置 CloudFlare/CloudFront 以实现最佳缓存、为动态内容实施边缘功能、
    设置响应式图片和 WebP/AVIF 格式的图片优化。
    配置 HTTP/2 和 HTTP/3、实施 Brotli 压缩。为全球用户设置地理分布。

    ## 交付成果
    1. CDN 配置建议
    2. 边缘缓存规则
    3. 图片优化策略
    4. 压缩设置
    5. 地理分布计划

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/08-cdn.md`。

更新 `state.json`：将 `current_step` 设置为 9，将步骤 8 添加到 `completed_steps`。

### 步骤 9：移动端和渐进式 Web 应用优化

读取 `.performance-optimization/07-frontend.md` 和 `.performance-optimization/08-cdn.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "优化 $TARGET 的移动端体验"
  prompt: |
    你是移动端性能优化专家。优化以下内容的移动端体验：$TARGET。

    ## 前端优化
    [插入 .performance-optimization/07-frontend.md 的内容]

    ## CDN 优化
    [插入 .performance-optimization/08-cdn.md 的内容]

    实施 service workers 以提供离线功能、通过自适应加载优化慢网络。
    减少移动端 CPU 的 JavaScript 执行时间。为长列表实现虚拟滚动。
    优化触摸响应和流畅动画。如果适用，考虑 React Native/Flutter 特定优化。

    ## 交付成果
    1. 移动端优化代码建议
    2. PWA 实施计划
    3. 离线功能策略
    4. 自适应加载配置
    5. 预期的移动端性能改进

    将你的完整优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/09-mobile.md`。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-3"，将步骤 9 添加到 `completed_steps`。

---

## 阶段检查点 3 — 需要用户批准

显示前端/CDN/移动端优化计划摘要并询问：

```
前端优化计划完成。请审查：
- .performance-optimization/07-frontend.md
- .performance-optimization/08-cdn.md
- .performance-optimization/09-mobile.md

1. 批准 — 继续进行负载测试和验证
2. 请求更改 — 告诉我需要调整什么
3. 暂停 — 保存进度并在此停止
```

在用户批准之前，不要进入第 4 阶段。

---

## 第 4 阶段：负载测试和验证（步骤 10-11）

### 步骤 10：全面负载测试

读取 `.performance-optimization/01-profiling.md`。

使用 Task 工具：

```
Task:
  subagent_type: "performance-engineer"
  description: "对 $TARGET 进行全面负载测试"
  prompt: |
    使用 k6/Gatling/Artillery 对以下内容进行全面负载测试：$TARGET。

    ## 原始基线
    [插入 .performance-optimization/01-profiling.md 的内容]

    基于生产流量模式设计真实的负载场景。测试正常负载、峰值负载
    和压力场景。包括 API 测试、基于浏览器的测试（如果适用）
    和 WebSocket 测试。测量各种负载级别的响应时间、吞吐量、错误率和资源利用率。

    ## 交付成果
    1. 负载测试脚本和配置
    2. 正常、峰值和压力负载下的结果
    3. 响应时间和吞吐量测量
    4. 崩溃点和可扩展性分析
    5. 与原始基线的对比

    将你的完整负载测试报告作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/10-load-testing.md`。

更新 `state.json`：将 `current_step` 设置为 11，将步骤 10 添加到 `completed_steps`。

### 步骤 11：性能回归测试

读取 `.performance-optimization/10-load-testing.md` 和 `.performance-optimization/01-profiling.md`。

使用 Task 工具：

```
Task:
  subagent_type: "general-purpose"
  description: "为 $TARGET 创建性能回归测试"
  prompt: |
    你是专门从事性能测试的测试自动化专家。为以下内容创建
    自动化性能回归测试：$TARGET。

    ## 负载测试结果
    [插入 .performance-optimization/10-load-testing.md 的内容]

    ## 原始基线
    [插入 .performance-optimization/01-profiling.md 的内容]

    为关键指标设置性能预算、使用 GitHub Actions 或类似工具集成到 CI/CD 管道。
    为前端创建 Lighthouse CI 测试、使用 Artillery 进行 API 性能测试
    以及数据库性能基准测试。为性能回归实施自动回滚触发器。

    ## 交付成果
    1. 包含脚本的性能测试套件
    2. CI/CD 集成配置
    3. 性能预算和阈值
    4. 回归检测规则
    5. 自动回滚触发器

    将你的完整回归测试计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/11-regression-testing.md`。

更新 `state.json`：将 `current_step` 设置为 "checkpoint-4"，将步骤 11 添加到 `completed_steps`。

---

## 阶段检查点 4 — 需要用户批准

显示测试结果摘要并询问：

```
负载测试和验证完成。请审查：
- .performance-optimization/10-load-testing.md
- .performance-optimization/11-regression-testing.md

1. 批准 — 继续进行监控和持续优化
2. 请求更改 — 告诉我需要调整什么
3. 暂停 — 保存进度并在此停止
```

在用户批准之前，不要进入第 5 阶段。

---

## 第 5 阶段：监控和持续优化（步骤 12-13）

### 步骤 12：生产监控设置

读取 `.performance-optimization/02-observability.md` 和 `.performance-optimization/10-load-testing.md`。

使用 Task 工具：

```
Task:
  subagent_type: "observability-engineer"
  description: "为 $TARGET 实施生产性能监控"
  prompt: |
    为以下内容实施生产性能监控：$TARGET。

    ## 可观测性评估
    [插入 .performance-optimization/02-observability.md 的内容]

    ## 负载测试结果
    [插入 .performance-optimization/10-load-testing.md 的内容]

    使用 DataDog/New Relic/Dynatrace 设置 APM、使用 OpenTelemetry 配置分布式追踪、
    实施自定义业务指标。为关键指标创建 Grafana 仪表板、
    为性能下降设置 PagerDuty 告警。为关键服务定义 SLI/SLO 以及错误预算。

    ## 交付成果
    1. 监控仪表板配置
    2. 告警规则和阈值
    3. SLI/SLO 定义
    4. 常见性能问题的运行手册
    5. 错误预算跟踪设置

    将你的完整监控计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/12-monitoring.md`。

更新 `state.json`：将 `current_step` 设置为 13，将步骤 12 添加到 `completed_steps`。

### 步骤 13：持续性能优化

读取所有之前的 `.performance-optimization/*.md` 文件。

使用 Task 工具：

```
Task:
  subagent_type: "performance-engineer"
  description: "为 $TARGET 建立持续优化流程"
  prompt: |
    为以下内容建立持续优化流程：$TARGET。

    ## 监控设置
    [插入 .performance-optimization/12-monitoring.md 的内容]

    ## 所有之前的优化工作
    [插入所有之前步骤的关键发现摘要]

    创建性能预算跟踪、为性能变更实施 A/B 测试、
    在生产环境中设置持续分析。记录优化机会待办事项、
    创建容量规划模型并建立定期性能审查周期。

    ## 交付成果
    1. 性能预算跟踪系统
    2. 包含优先级的优化待办事项
    3. 容量规划模型
    4. 审查周期计划和流程
    5. 性能变更的 A/B 测试框架

    将你的完整持续优化计划作为单个 markdown 文档编写。
```

将输出保存到 `.performance-optimization/13-continuous.md`。

更新 `state.json`：将 `current_step` 设置为 "complete"，将步骤 13 添加到 `completed_steps`。

---

## 完成

更新 `state.json`：

- 将 `status` 设置为 `"complete"`
- 将 `last_updated` 设置为当前时间戳

展示最终摘要：

```
性能优化完成：$TARGET

## 创建的文件
[列出所有 .performance-optimization/ 输出文件]

## 优化摘要
- 性能分析：.performance-optimization/01-profiling.md
- 可观测性：.performance-optimization/02-observability.md
- UX 分析：.performance-optimization/03-ux-analysis.md
- 数据库：.performance-optimization/04-database.md
- 后端：.performance-optimization/05-backend.md
- 分布式：.performance-optimization/06-distributed.md
- 前端：.performance-optimization/07-frontend.md
- CDN：.performance-optimization/08-cdn.md
- 移动端：.performance-optimization/09-mobile.md
- 负载测试：.performance-optimization/10-load-testing.md
- 回归测试：.performance-optimization/11-regression-testing.md
- 监控：.performance-optimization/12-monitoring.md
- 持续：.performance-optimization/13-continuous.md

## 成功标准
- 响应时间：关键端点的 P50 < 200ms、P95 < 1s、P99 < 2s
- 核心 Web 指标：LCP < 2.5s、FID < 100ms、CLS < 0.1
- 吞吐量：支持 2 倍当前峰值负载，错误率 < 1%
- 数据库性能：查询 P95 < 100ms，无查询 > 1s
- 资源利用率：正常负载下 CPU < 70%、内存 < 80%
- 成本效率：每美元性能至少提高 30%
- 监控覆盖率：100% 的关键路径配备告警检测

## 后续步骤
1. 按每个阶段的优先顺序实施优化
2. 每次优化后运行回归测试
3. 根据基线监控生产指标
4. 每周审查性能预算
```
