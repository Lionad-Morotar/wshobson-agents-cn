使用专业的性能优化智能体，端到端地优化应用程序性能：

[扩展思考：此工作流程协调整个应用程序技术栈的全面性能优化过程。从深度性能分析和基线建立开始，工作流程逐步推进每个系统层的针对性优化，通过负载测试验证改进，并建立持续监控以维持性能。每个阶段都基于前一阶段的洞察，构建数据驱动的优化策略，解决实际瓶颈而非理论改进。该工作流程强调现代可观测性实践、以用户为中心的性能指标以及具有成本效益的优化策略。]

## 第1阶段：性能分析与基线建立

### 1. 全面性能分析

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示词："对以下内容进行全面性能分析：$ARGUMENTS。生成 CPU 使用率的火焰图、内存分析的堆转储、跟踪 I/O 操作并识别热路径。如果可用，使用 DataDog 或 New Relic 等 APM 工具。包括数据库查询分析、API 响应时间和前端渲染指标。为所有关键用户旅程建立性能基线。"
- 上下文：初始性能调查
- 输出：详细的性能分析报告，包括火焰图、内存分析、瓶颈识别、基线指标

### 2. 可观测性技术栈评估

- 使用 Task 工具，设置 subagent_type="observability-engineer"
- 提示词："评估以下内容的当前可观测性设置：$ARGUMENTS。审查现有监控、使用 OpenTelemetry 的分布式追踪、日志聚合和指标收集。识别可见性差距、缺失指标以及需要更好检测的领域。推荐 APM 工具集成和针对业务关键操作的自定义指标。"
- 上下文：第1步的性能分析
- 输出：可观测性评估报告、检测差距、监控建议

### 3. 用户体验分析

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示词："分析以下内容的用户体验指标：$ARGUMENTS。测量核心 Web 指标（LCP、FID、CLS）、页面加载时间、可交互时间和感知性能。如果可用，使用真实用户监控（RUM）数据。识别性能较差的用户旅程及其业务影响。"
- 上下文：第1步的性能基线
- 输出：UX 性能报告、核心 Web 指标分析、用户影响评估

## 第2阶段：数据库与后端优化

### 4. 数据库性能优化

- 使用 Task 工具，设置 subagent_type="database-cloud-optimization::database-optimizer"
- 提示词："基于分析数据优化以下内容的数据库性能：$ARGUMENTS，分析数据来自：{context_from_phase_1}。分析慢查询日志、创建缺失的索引、优化执行计划、使用 Redis/Memcached 实现查询结果缓存。审查连接池、预处理语句和批处理机会。如果需要，考虑只读副本和数据库分片。"
- 上下文：第1阶段的性能瓶颈
- 输出：优化的查询、新索引、缓存策略、连接池配置

### 5. 后端代码与 API 优化

- 使用 Task 工具，设置 subagent_type="backend-development::backend-architect"
- 提示词："针对以下瓶颈优化后端服务：$ARGUMENTS，目标瓶颈：{context_from_phase_1}。实现高效算法、添加应用级缓存、优化 N+1 查询、有效使用 async/await 模式。实现分页、响应压缩、GraphQL 查询优化和批量 API 操作。添加断路器和隔离机制以提高弹性。"
- 上下文：第4步的数据库优化、第1阶段的分析数据
- 输出：优化的后端代码、缓存实现、API 改进、弹性模式

### 6. 微服务与分布式系统优化

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示词："优化以下内容的分布式系统性能：$ARGUMENTS。分析服务间通信、实现服务网格优化、优化消息队列性能（Kafka/RabbitMQ）、减少网络跳数。实现分布式缓存策略并优化序列化/反序列化。"
- 上下文：第5步的后端优化
- 输出：服务通信改进、消息队列优化、分布式缓存设置

## 第3阶段：前端与 CDN 优化

### 7. 前端打包与加载优化

- 使用 Task 工具，设置 subagent_type="frontend-developer"
- 提示词："针对核心 Web 指标优化以下内容的前端性能：$ARGUMENTS，目标指标：{context_from_phase_1}。实现代码分割、tree shaking、懒加载和动态导入。通过 webpack/rollup 分析优化打包大小。实现资源提示（prefetch、preconnect、preload）。优化关键渲染路径并消除渲染阻塞资源。"
- 上下文：第1阶段的 UX 分析、第2阶段的后端优化
- 输出：优化的打包文件、懒加载实现、改进的核心 Web 指标

### 8. CDN 与边缘优化

- 使用 Task 工具，设置 subagent_type="cloud-infrastructure::cloud-architect"
- 提示词："优化以下内容的 CDN 和边缘性能：$ARGUMENTS。配置 CloudFlare/CloudFront 以实现最佳缓存、为动态内容实现边缘功能、设置响应式图片和 WebP/AVIF 格式的图片优化。配置 HTTP/2 和 HTTP/3、实现 Brotli 压缩。为全球用户设置地理分布。"
- 上下文：第7步的前端优化
- 输出：CDN 配置、边缘缓存规则、压缩设置、地理优化

### 9. 移动端与渐进式 Web 应用优化

- 使用 Task 工具，设置 subagent_type="frontend-mobile-development::mobile-developer"
- 提示词："优化以下内容的移动端体验：$ARGUMENTS。实现 service workers 以提供离线功能、通过自适应加载优化慢网络。减少移动端 CPU 的 JavaScript 执行时间。为长列表实现虚拟滚动。优化触摸响应和流畅动画。如果适用，考虑 React Native/Flutter 特定优化。"
- 上下文：第7-8步的前端优化
- 输出：移动端优化的代码、PWA 实现、离线功能

## 第4阶段：负载测试与验证

### 10. 全面负载测试

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示词："使用 k6/Gatling/Artillery 对以下内容进行全面负载测试：$ARGUMENTS。基于生产流量模式设计真实的负载场景。测试正常负载、峰值负载和压力场景。包括 API 测试、基于浏览器的测试（如果适用）以及 WebSocket 测试。测量各种负载级别的响应时间、吞吐量、错误率和资源利用率。"
- 上下文：第1-3阶段的所有优化
- 输出：负载测试结果、负载下的性能、崩溃点、可扩展性分析

### 11. 性能回归测试

- 使用 Task 工具，设置 subagent_type="performance-testing-review::test-automator"
- 提示词："为以下内容创建自动化性能回归测试：$ARGUMENTS。为关键指标设置性能预算、使用 GitHub Actions 或类似工具集成到 CI/CD 管道。创建前端 Lighthouse CI 测试、使用 Artillery 进行 API 性能测试以及数据库性能基准测试。为性能回归实现自动回滚触发器。"
- 上下文：第10步的负载测试结果、第1阶段的基线指标
- 输出：性能测试套件、CI/CD 集成、回归预防系统

## 第5阶段：监控与持续优化

### 12. 生产环境监控设置

- 使用 Task 工具，设置 subagent_type="observability-engineer"
- 提示词："为以下内容实现生产性能监控：$ARGUMENTS。使用 DataDog/New Relic/Dynatrace 设置 APM、使用 OpenTelemetry 配置分布式追踪、实现自定义业务指标。为关键指标创建 Grafana 仪表板、为性能下降设置 PagerDuty 告警。定义关键服务的 SLI/SLO 以及错误预算。"
- 上下文：之前所有阶段的性能改进
- 输出：监控仪表板、告警规则、SLI/SLO 定义、运行手册

### 13. 持续性能优化

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示词："为以下内容建立持续优化流程：$ARGUMENTS。创建性能预算跟踪、为性能变更实现 A/B 测试、在生产环境中设置持续分析。记录优化机会待办事项、创建容量规划模型并建立定期性能审查周期。"
- 上下文：第12步的监控设置、所有之前的优化工作
- 输出：性能预算跟踪、优化待办事项、容量规划、审查流程

## 配置选项

- **performance_focus**: "latency" | "throughput" | "cost" | "balanced"（默认："balanced"）
- **optimization_depth**: "quick-wins" | "comprehensive" | "enterprise"（默认："comprehensive"）
- **tools_available**: ["datadog", "newrelic", "prometheus", "grafana", "k6", "gatling"]
- **budget_constraints**: 设置基础设施变更的最大可接受成本
- **user_impact_tolerance**: "zero-downtime" | "maintenance-window" | "gradual-rollout"

## 成功标准

- **响应时间**：关键端点的 P50 < 200ms，P95 < 1s，P99 < 2s
- **核心 Web 指标**：LCP < 2.5s，FID < 100ms，CLS < 0.1
- **吞吐量**：支持 2 倍当前峰值负载，错误率 < 1%
- **数据库性能**：查询 P95 < 100ms，无查询 > 1s
- **资源利用率**：正常负载下 CPU < 70%，内存 < 80%
- **成本效率**：每美元性能至少提升 30%
- **监控覆盖率**：100% 的关键路径配备告警检测

性能优化目标：$ARGUMENTS
