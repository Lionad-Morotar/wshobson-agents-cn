使用现代 API 优先方法，协调跨后端、前端和基础设施层的全栈功能开发：

[扩展思考：此工作流协调多个专业代理，从架构到部署交付完整的全栈功能。它遵循 API 优先开发原则，确保契约驱动开发，其中 API 规范驱动后端实现和前端消费。每个阶段构建先前的输出，创建具有适当关注点分离、全面测试和生产就绪部署的内聚系统。工作流强调现代实践，如组件驱动的 UI 开发、功能标志、可观察性和渐进式推出策略。]

## 第一阶段：架构与设计基础

### 1. 数据库架构设计

- 使用 Task 工具，设置 subagent_type="database-design::database-architect"
- 提示："为以下内容设计数据库架构和数据模型：$ARGUMENTS。考虑可扩展性、查询模式、索引策略和数据一致性要求。如果修改现有架构，请包含迁移策略。提供逻辑和物理数据模型。"
- 预期输出：实体关系图、表架构、索引策略、迁移脚本、数据访问模式
- 上下文：初始需求和业务领域模型

### 2. 后端服务架构

- 使用 Task 工具，设置 subagent_type="backend-development::backend-architect"
- 提示："为以下内容设计后端服务架构：$ARGUMENTS。使用上一步的数据库设计，创建服务边界，定义 API 契约（OpenAPI/GraphQL），设计身份验证/授权策略，并指定服务间通信模式。包含弹性模式（断路器、重试）和缓存策略。"
- 预期输出：服务架构图、OpenAPI 规范、身份验证流程、缓存架构、消息队列设计（如适用）
- 上下文：步骤 1 的数据库架构、非功能性需求

### 3. 前端组件架构

- 使用 Task 工具，设置 subagent_type="frontend-mobile-development::frontend-developer"
- 提示："为以下内容设计前端架构和组件结构：$ARGUMENTS。基于上一步的 API 契约，设计组件层次结构、状态管理方法（Redux/Zustand/Context）、路由结构和数据获取模式。包含可访问性要求和响应式设计策略。规划 Storybook 组件文档。"
- 预期输出：组件树图、状态管理设计、路由配置、设计系统集成计划、可访问性检查清单
- 上下文：步骤 2 的 API 规范、UI/UX 需求

## 第二阶段：并行实现

### 4. 后端服务实现

- 使用 Task 工具，设置 subagent_type="python-development::python-pro"（或根据技术栈选择 "golang-pro"/"nodejs-expert"）
- 提示："为以下内容实现后端服务：$ARGUMENTS。使用第一阶段的架构和 API 规范，构建具有适当验证、错误处理和日志的 RESTful/GraphQL 端点。实现业务逻辑、数据访问层、身份验证中间件和与外部服务的集成。包含可观察性（结构化日志、指标、追踪）。"
- 预期输出：后端服务代码、API 端点、中间件、后台作业、单元测试、集成测试
- 上下文：第一阶段的架构设计、数据库架构

### 5. 前端实现

- 使用 Task 工具，设置 subagent_type="frontend-mobile-development::frontend-developer"
- 提示："为以下内容实现前端应用：$ARGUMENTS。使用第一阶段的组件架构构建 React/Next.js 组件。实现状态管理、API 集成（具有适当的错误处理和加载状态）、表单验证和响应式布局。为组件创建 Storybook 故事。确保可访问性（WCAG 2.1 AA 合规）。"
- 预期输出：React 组件、状态管理实现、API 客户端代码、Storybook 故事、响应式样式、可访问性实现
- 上下文：步骤 3 的组件架构、API 契约

### 6. 数据库实现与优化

- 使用 Task 工具，设置 subagent_type="database-design::sql-pro"
- 提示："为以下内容实现和优化数据库层：$ARGUMENTS。创建迁移脚本、存储过程（如需要）、优化后端实现识别的查询、设置适当的索引，并实现数据验证约束。包含数据库级安全措施和备份策略。"
- 预期输出：迁移脚本、优化查询、存储过程、索引定义、数据库安全配置
- 上下文：步骤 1 的数据库设计、后端实现的查询模式

## 第三阶段：集成与测试

### 7. API 契约测试

- 使用 Task 工具，设置 subagent_type="test-automator"
- 提示："为以下内容创建契约测试：$ARGUMENTS。实现 Pact/Dredd 测试以验证后端和前端之间的 API 契约。为所有 API 端点创建集成测试，测试身份验证流程，验证错误响应，并确保正确的 CORS 配置。包含负载测试场景。"
- 预期输出：契约测试套件、集成测试、负载测试场景、API 文档验证
- 上下文：第二阶段的 API 实现

### 8. 端到端测试

- 使用 Task 工具，设置 subagent_type="test-automator"
- 提示："为以下内容实现 E2E 测试：$ARGUMENTS。创建覆盖关键用户旅程、跨浏览器兼容性、移动响应式和错误场景的 Playwright/Cypress 测试。测试功能标志集成、分析跟踪和性能指标。包含视觉回归测试。"
- 预期输出：E2E 测试套件、视觉回归基准、性能基准、测试报告
- 上下文：第二阶段的前端和后端实现

### 9. 安全审计与加固

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示："为以下内容执行安全审计：$ARGUMENTS。审查 API 安全（身份验证、授权、速率限制），检查 OWASP Top 10 漏洞，审计前端的 XSS/CSRF 风险，验证输入清理，并审查密钥管理。提供渗透测试结果和修复步骤。"
- 预期输出：安全审计报告、漏洞评估、修复建议、安全头配置
- 上下文：第二阶段的所有实现

## 第四阶段：部署与运营

### 10. 基础设施与 CI/CD 设置

- 使用 Task 工具，设置 subagent_type="deployment-engineer"
- 提示："为以下内容设置部署基础设施：$ARGUMENTS。创建 Docker 容器、Kubernetes 清单（或云特定配置），实现具有自动测试门控的 CI/CD 流水线，设置功能标志（LaunchDarkly/Unleash），并配置监控/告警。包含蓝绿部署策略和回滚程序。"
- 预期输出：Dockerfile、K8s 清单、CI/CD 流水线配置、功能标志设置、IaC 模板（Terraform/CloudFormation）
- 上下文：前面阶段的所有实现和测试

### 11. 可观察性与监控

- 使用 Task 工具，设置 subagent_type="deployment-engineer"
- 提示："为以下内容实现可观察性堆栈：$ARGUMENTS。设置分布式追踪（OpenTelemetry），配置应用指标（Prometheus/DataDog），实现集中式日志（ELK/Splunk），为关键指标创建仪表板，并定义 SLI/SLO。包含告警规则和待命程序。"
- 预期输出：可观察性配置、仪表板定义、告警规则、运维手册、SLI/SLO 定义
- 上下文：步骤 10 的基础设施设置

### 12. 性能优化

- 使用 Task 工具，设置 subagent_type="performance-engineer"
- 提示："为以下内容优化跨栈性能：$ARGUMENTS。分析和优化数据库查询，实现缓存策略（Redis/CDN），优化前端 bundle 大小和加载性能，设置懒加载和代码分割，并调优后端服务性能。包含优化前后的指标。"
- 预期输出：性能改进、缓存配置、CDN 设置、优化后的 bundle、性能指标报告
- 上下文：步骤 11 的监控数据、负载测试结果

## 配置选项

- `stack`：指定技术栈（例如，"React/FastAPI/PostgreSQL"、"Next.js/Django/MongoDB"）
- `deployment_target`：云平台（AWS/GCP/Azure）或本地部署
- `feature_flags`：启用/禁用功能标志集成
- `api_style`：REST 或 GraphQL
- `testing_depth`：全面或基本
- `compliance`：特定合规要求（GDPR、HIPAA、SOC2）

## 成功标准

- 所有 API 契约通过契约测试验证
- 前端和后端集成测试通过
- E2E 测试覆盖关键用户旅程
- 安全审计通过，无关键漏洞
- 性能指标满足定义的 SLO
- 可观察性堆栈捕获所有关键指标
- 功能标志配置用于渐进式推出
- 所有组件的文档完成
- 具有自动质量门控的 CI/CD 流水线
- 验证零停机部署能力

## 协调说明

- 每个阶段构建前一阶段的输出
- 第二阶段的并行任务可以同时运行，但必须为第三阶段汇聚
- 保持需求和实现之间的可追溯性
- 在所有服务中使用相关 ID 进行分布式追踪
- 在 ADR 中记录所有架构决策
- 确保服务间一致的错误处理和 API 响应

要实现的功能：$ARGUMENTS
