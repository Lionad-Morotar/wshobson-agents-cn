# Agent 参考

按类别组织的所有 **100 个专业 AI 代理** 的完整参考，包含模型分配。

## Agent 类别

### 架构与系统设计

#### 核心架构

| Agent                                                                                         | Model  | 描述                                                            |
| --------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------- |
| [backend-architect](../plugins/backend-development/agents/backend-architect.md)               | opus   | RESTful API 设计、微服务边界、数据库模式          |
| [frontend-developer](../plugins/multi-platform-apps/agents/frontend-developer.md)             | sonnet | React 组件、响应式布局、客户端状态管理     |
| [graphql-architect](../plugins/backend-development/agents/graphql-architect.md)               | opus   | GraphQL 模式、解析器、联合架构                    |
| [architect-reviewer](../plugins/comprehensive-review/agents/architect-review.md)              | opus   | 架构一致性分析和模式验证              |
| [cloud-architect](../plugins/cloud-infrastructure/agents/cloud-architect.md)                  | opus   | AWS/Azure/GCP 基础设施设计和成本优化              |
| [hybrid-cloud-architect](../plugins/cloud-infrastructure/agents/hybrid-cloud-architect.md)    | opus   | 跨云和本地环境的多云策略       |
| [kubernetes-architect](../plugins/kubernetes-operations/agents/kubernetes-architect.md)       | opus   | 使用 Kubernetes 和 GitOps 的云原生基础设施                 |
| [service-mesh-expert](../plugins/cloud-infrastructure/agents/service-mesh-expert.md)          | opus   | Istio/Linkerd 服务网格架构、mTLS 和流量管理  |
| [event-sourcing-architect](../plugins/backend-development/agents/event-sourcing-architect.md) | opus   | 事件溯源、CQRS 模式、事件存储和 Saga 编排    |
| [monorepo-architect](../plugins/developer-essentials/agents/monorepo-architect.md)            | opus   | 使用 Nx、Turborepo、Bazel 的 Monorepo 工具和工作空间优化 |

#### UI/UX 与移动端

| Agent                                                                                    | Model  | 描述                                             |
| ---------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [ui-designer](../plugins/ui-design/agents/ui-designer.md)                                | opus   | 面向移动端和 Web 的 UI/UX 设计，采用现代模式    |
| [accessibility-expert](../plugins/ui-design/agents/accessibility-expert.md)              | opus   | WCAG 合规、可访问性审计、包容性设计 |
| [design-system-architect](../plugins/ui-design/agents/design-system-architect.md)        | opus   | 设计令牌、组件库、主题系统     |
| [ui-ux-designer](../plugins/multi-platform-apps/agents/ui-ux-designer.md)                | sonnet | 界面设计、线框图、设计系统            |
| [ui-visual-validator](../plugins/accessibility-compliance/agents/ui-visual-validator.md) | sonnet | 视觉回归测试和 UI 验证           |
| [mobile-developer](../plugins/multi-platform-apps/agents/mobile-developer.md)            | sonnet | React Native 和 Flutter 应用开发        |
| [ios-developer](../plugins/multi-platform-apps/agents/ios-developer.md)                  | sonnet | 使用 Swift/SwiftUI 的原生 iOS 开发               |
| [flutter-expert](../plugins/multi-platform-apps/agents/flutter-expert.md)                | sonnet | 高级 Flutter 开发和状态管理      |

### 编程语言

#### 系统与底层

| Agent                                                             | Model  | 描述                                                 |
| ----------------------------------------------------------------- | ------ | ----------------------------------------------------------- |
| [c-pro](../plugins/systems-programming/agents/c-pro.md)           | sonnet | 系统编程，包含内存管理和 OS 接口 |
| [cpp-pro](../plugins/systems-programming/agents/cpp-pro.md)       | sonnet | 现代 C++，包含 RAII、智能指针、STL 算法        |
| [rust-pro](../plugins/systems-programming/agents/rust-pro.md)     | sonnet | 内存安全的系统编程和所有权模式     |
| [golang-pro](../plugins/systems-programming/agents/golang-pro.md) | sonnet | 使用 goroutine 和 channel 的并发编程         |

#### Web 与应用

| Agent                                                                               | Model  | 描述                                                                       |
| ----------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------- |
| [javascript-pro](../plugins/javascript-typescript/agents/javascript-pro.md)         | sonnet | 现代 JavaScript，包含 ES6+、异步模式、Node.js                              |
| [typescript-pro](../plugins/javascript-typescript/agents/typescript-pro.md)         | sonnet | 高级 TypeScript，包含类型系统和泛型                                |
| [python-pro](../plugins/python-development/agents/python-pro.md)                    | sonnet | Python 开发，包含高级特性和优化                        |
| [temporal-python-pro](../plugins/backend-development/agents/temporal-python-pro.md) | sonnet | 使用 Python SDK 的 Temporal 工作流编排、持久化工作流、Saga 模式 |
| [ruby-pro](../plugins/web-scripting/agents/ruby-pro.md)                             | sonnet | Ruby，包含元编程、Rails 模式、gem 开发                        |
| [php-pro](../plugins/web-scripting/agents/php-pro.md)                               | sonnet | 现代 PHP，包含框架和性能优化                           |

#### 企业与 JVM

| Agent                                                       | Model  | 描述                                                          |
| ----------------------------------------------------------- | ------ | -------------------------------------------------------------------- |
| [java-pro](../plugins/jvm-languages/agents/java-pro.md)     | sonnet | 现代 Java，包含流、并发、JVM 优化              |
| [scala-pro](../plugins/jvm-languages/agents/scala-pro.md)   | sonnet | 企业级 Scala，包含函数式编程和分布式系统 |
| [csharp-pro](../plugins/jvm-languages/agents/csharp-pro.md) | sonnet | C# 开发，包含 .NET 框架和模式                     |

#### 专业平台

| Agent                                                                              | Model  | 描述                                                                               |
| ---------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| [elixir-pro](../plugins/functional-programming/agents/elixir-pro.md)               | sonnet | Elixir，包含 OTP 模式和 Phoenix 框架                                           |
| [django-pro](../plugins/api-scaffolding/agents/django-pro.md)                      | sonnet | Django 开发，包含 ORM 和异步视图                                               |
| [fastapi-pro](../plugins/api-scaffolding/agents/fastapi-pro.md)                    | sonnet | FastAPI，包含异步模式和 Pydantic                                                  |
| [haskell-pro](../plugins/functional-programming/agents/haskell-pro.md)             | sonnet | 强类型函数式编程，包含纯度、高级类型系统和并发 |
| [unity-developer](../plugins/game-development/agents/unity-developer.md)           | sonnet | Unity 游戏开发和优化                                                   |
| [minecraft-bukkit-pro](../plugins/game-development/agents/minecraft-bukkit-pro.md) | sonnet | Minecraft 服务器插件开发                                                       |
| [sql-pro](../plugins/database-design/agents/sql-pro.md)                            | sonnet | 复杂 SQL 查询和数据库优化                                             |

### 基础设施与运维

#### DevOps 与部署

| Agent                                                                                  | Model  | 描述                                                        |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------ |
| [devops-troubleshooter](../plugins/incident-response/agents/devops-troubleshooter.md)  | sonnet | 生产调试、日志分析、部署故障排除     |
| [deployment-engineer](../plugins/cloud-infrastructure/agents/deployment-engineer.md)   | sonnet | CI/CD 管道、容器化、云部署               |
| [terraform-specialist](../plugins/cloud-infrastructure/agents/terraform-specialist.md) | sonnet | 使用 Terraform 模块和状态管理的基础设施即代码 |
| [dx-optimizer](../plugins/team-collaboration/agents/dx-optimizer.md)                   | sonnet | 开发体验优化和工具改进         |

#### 数据库管理

| Agent                                                                                  | Model  | 描述                                                         |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------- |
| [database-optimizer](../plugins/observability-monitoring/agents/database-optimizer.md) | sonnet | 查询优化、索引设计、迁移策略              |
| [database-admin](../plugins/database-migrations/agents/database-admin.md)              | sonnet | 数据库运维、备份、复制、监控                |
| [database-architect](../plugins/database-design/agents/database-architect.md)          | opus   | 从零开始的数据库设计、技术选型、模式建模 |

#### 事件响应与网络

| Agent                                                                              | Model  | 描述                                         |
| ---------------------------------------------------------------------------------- | ------ | --------------------------------------------------- |
| [incident-responder](../plugins/incident-response/agents/incident-responder.md)    | opus   | 生产事件管理和解决       |
| [network-engineer](../plugins/observability-monitoring/agents/network-engineer.md) | sonnet | 网络调试、负载均衡、流量分析 |

#### 项目管理

| Agent                                                             | Model | 描述                                                                          |
| ----------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------ |
| [conductor-validator](../conductor/agents/conductor-validator.md) | opus  | 验证 Conductor 项目工件的完整性、一致性和正确性 |

### 质量保证与安全

#### 代码质量与审查

| Agent                                                                                            | Model | 描述                                                     |
| ------------------------------------------------------------------------------------------------ | ----- | --------------------------------------------------------------- |
| [code-reviewer](../plugins/comprehensive-review/agents/code-reviewer.md)                         | opus  | 代码审查，专注于安全和生产可靠性      |
| [security-auditor](../plugins/comprehensive-review/agents/security-auditor.md)                   | opus  | 漏洞评估和 OWASP 合规                   |
| [backend-security-coder](../plugins/data-validation-suite/agents/backend-security-coder.md)      | opus  | 安全后端编码实践、API 安全实现    |
| [frontend-security-coder](../plugins/frontend-mobile-security/agents/frontend-security-coder.md) | opus  | XSS 防护、CSP 实现、客户端安全        |
| [mobile-security-coder](../plugins/frontend-mobile-security/agents/mobile-security-coder.md)     | opus  | 移动安全模式、WebView 安全、生物认证      |
| [threat-modeling-expert](../plugins/security-scanning/agents/threat-modeling-expert.md)          | opus  | STRIDE 威胁建模、攻击树和安全需求 |

#### 测试与调试

| Agent                                                                         | Model  | 描述                                                |
| ----------------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [test-automator](../plugins/codebase-cleanup/agents/test-automator.md)        | sonnet | 全面测试套件创建（单元、集成、e2e） |
| [tdd-orchestrator](../plugins/backend-development/agents/tdd-orchestrator.md) | sonnet | 测试驱动开发方法论指导               |
| [debugger](../plugins/error-debugging/agents/debugger.md)                     | sonnet | 错误解决和测试失败分析                 |
| [error-detective](../plugins/error-debugging/agents/error-detective.md)       | sonnet | 日志分析和错误模式识别                 |

#### 性能与可观测性

| Agent                                                                                          | Model | 描述                                                    |
| ---------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------- |
| [performance-engineer](../plugins/observability-monitoring/agents/performance-engineer.md)     | opus  | 应用性能分析和优化                         |
| [observability-engineer](../plugins/observability-monitoring/agents/observability-engineer.md) | opus  | 生产监控、分布式跟踪、SLI/SLO 管理 |
| [search-specialist](../plugins/content-marketing/agents/search-specialist.md)                  | haiku | 高级网络研究和信息综合                |

### 数据与 AI

#### 数据工程与分析

| Agent                                                                      | Model  | 描述                                             |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [data-scientist](../plugins/machine-learning-ops/agents/data-scientist.md) | opus   | 数据分析、SQL 查询、BigQuery 操作         |
| [data-engineer](../plugins/data-engineering/agents/data-engineer.md)       | sonnet | ETL 管道、数据仓库、流式架构 |

#### 机器学习与 AI

| Agent                                                                                         | Model | 描述                                                           |
| --------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------- |
| [ai-engineer](../plugins/llm-application-dev/agents/ai-engineer.md)                           | opus  | LLM 应用、RAG 系统、提示管道                       |
| [ml-engineer](../plugins/machine-learning-ops/agents/ml-engineer.md)                          | opus  | ML 管道、模型服务、特征工程                      |
| [mlops-engineer](../plugins/machine-learning-ops/agents/mlops-engineer.md)                    | opus  | ML 基础设施、实验跟踪、模型注册表              |
| [prompt-engineer](../plugins/llm-application-dev/agents/prompt-engineer.md)                   | opus  | LLM 提示优化和工程                               |
| [vector-database-engineer](../plugins/llm-application-dev/agents/vector-database-engineer.md) | opus  | 向量数据库、嵌入、相似性搜索和混合检索 |

### 文档与技术写作

| Agent                                                                                | Model  | 描述                                                           |
| ------------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------------- |
| [docs-architect](../plugins/code-documentation/agents/docs-architect.md)             | opus   | 全面技术文档生成                      |
| [api-documenter](../plugins/api-testing-observability/agents/api-documenter.md)      | sonnet | OpenAPI/Swagger 规范和开发文档                     |
| [reference-builder](../plugins/documentation-generation/agents/reference-builder.md) | haiku  | 技术参考和 API 文档                            |
| [tutorial-engineer](../plugins/code-documentation/agents/tutorial-engineer.md)       | sonnet | 分步教程和教育内容                        |
| [mermaid-expert](../plugins/documentation-generation/agents/mermaid-expert.md)       | sonnet | 图表创建（流程图、序列图、ERD）                        |
| [c4-code](../plugins/c4-architecture/agents/c4-code.md)                              | haiku  | C4 代码级文档，包含函数签名和依赖 |
| [c4-component](../plugins/c4-architecture/agents/c4-component.md)                    | sonnet | C4 组件级架构综合和文档           |
| [c4-container](../plugins/c4-architecture/agents/c4-container.md)                    | sonnet | C4 容器级架构和 API 文档                |
| [c4-context](../plugins/c4-architecture/agents/c4-context.md)                        | sonnet | C4 上下文级系统文档，包含角色和用户旅程 |

### 业务与运营

#### 业务分析与金融

| Agent                                                                        | Model  | 描述                                             |
| ---------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [business-analyst](../plugins/business-analytics/agents/business-analyst.md) | sonnet | 指标分析、报告、KPI 跟踪               |
| [quant-analyst](../plugins/quantitative-trading/agents/quant-analyst.md)     | opus   | 金融建模、交易策略、市场分析 |
| [risk-manager](../plugins/quantitative-trading/agents/risk-manager.md)       | sonnet | 投资组合风险监控和管理                |

#### 营销与销售

| Agent                                                                             | Model  | 描述                                  |
| --------------------------------------------------------------------------------- | ------ | -------------------------------------------- |
| [content-marketer](../plugins/content-marketing/agents/content-marketer.md)       | sonnet | 博客文章、社交媒体、邮件活动    |
| [sales-automator](../plugins/customer-sales-automation/agents/sales-automator.md) | haiku  | 冷邮件、跟进、提案生成 |

#### 支持与法务

| Agent                                                                               | Model  | 描述                                             |
| ----------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [customer-support](../plugins/customer-sales-automation/agents/customer-support.md) | sonnet | 支持工单、FAQ 响应、客户沟通  |
| [hr-pro](../plugins/hr-legal-compliance/agents/hr-pro.md)                           | opus   | HR 运营、政策、员工关系             |
| [legal-advisor](../plugins/hr-legal-compliance/agents/legal-advisor.md)             | opus   | 隐私政策、服务条款、法律文档 |

### SEO 与内容优化

| Agent                                                                                                     | Model  | 描述                                          |
| --------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------- |
| [seo-content-auditor](../plugins/seo-content-creation/agents/seo-content-auditor.md)                      | sonnet | 内容质量分析、E-E-A-T 信号评估 |
| [seo-meta-optimizer](../plugins/seo-technical-optimization/agents/seo-meta-optimizer.md)                  | haiku  | 元标题和描述优化              |
| [seo-keyword-strategist](../plugins/seo-technical-optimization/agents/seo-keyword-strategist.md)          | haiku  | 关键词分析和语义变体             |
| [seo-structure-architect](../plugins/seo-technical-optimization/agents/seo-structure-architect.md)        | haiku  | 内容结构和模式标记                  |
| [seo-snippet-hunter](../plugins/seo-technical-optimization/agents/seo-snippet-hunter.md)                  | haiku  | 精选摘要格式                          |
| [seo-content-refresher](../plugins/seo-analysis-monitoring/agents/seo-content-refresher.md)               | haiku  | 内容新鲜度分析                           |
| [seo-cannibalization-detector](../plugins/seo-analysis-monitoring/agents/seo-cannibalization-detector.md) | haiku  | 关键词重叠检测                            |
| [seo-authority-builder](../plugins/seo-analysis-monitoring/agents/seo-authority-builder.md)               | sonnet | E-E-A-T 信号分析                              |
| [seo-content-writer](../plugins/seo-content-creation/agents/seo-content-writer.md)                        | sonnet | SEO 优化内容创建                       |
| [seo-content-planner](../plugins/seo-content-creation/agents/seo-content-planner.md)                      | haiku  | 内容规划和主题集群                  |

### 专业领域

| Agent                                                                                   | Model  | 描述                                             |
| --------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [arm-cortex-expert](../plugins/arm-cortex-microcontrollers/agents/arm-cortex-expert.md) | sonnet | ARM Cortex-M 固件和外设驱动开发 |
| [blockchain-developer](../plugins/blockchain-web3/agents/blockchain-developer.md)       | sonnet | Web3 应用、智能合约、DeFi 协议              |
| [payment-integration](../plugins/payment-processing/agents/payment-integration.md)      | sonnet | 支付处理器集成（Stripe、PayPal）          |
| [legacy-modernizer](../plugins/framework-migration/agents/legacy-modernizer.md)         | sonnet | 遗留代码重构和现代化               |
| [context-manager](../plugins/agent-orchestration/agents/context-manager.md)             | haiku  | 多代理上下文管理                          |

## 模型配置

根据任务复杂性和计算要求，Agent 被分配到特定的 Claude 模型。

### 模型分布概览

| Model  | Agent 数量 | 用途                                                        |
| ------ | ----------- | --------------------------------------------------------------- |
| Opus   | 42          | 关键架构、安全、代码审查、生产编码 |
| Sonnet | 39          | 复杂任务、智能支持                        |
| Haiku  | 18          | 快速操作任务                                          |

### 模型选择标准

#### Haiku - 快速执行与确定性任务

**适用于：**

- 根据明确定义的规范生成代码
- 按照既定模式创建测试
- 使用清晰模板编写文档
- 执行基础设施操作
- 进行数据库查询优化
- 处理客户支持响应
- 处理 SEO 优化任务
- 管理部署管道

#### Sonnet - 复杂推理与架构

**适用于：**

- 设计系统架构
- 做出技术选型决策
- 执行安全审计
- 审查架构模式代码
- 创建复杂的 AI/ML 管道
- 提供特定语言的专业知识
- 编排多代理工作流
- 处理业务关键的法律/HR 事务

### 混合编排模式

插件生态系统利用 Sonnet + Haiku 编排以实现最佳性能和成本效率：

#### 模式 1：规划 → 执行

```
Sonnet: backend-architect (设计 API 架构)
  ↓
Haiku: 按规范生成 API 端点
  ↓
Haiku: test-automator (生成全面测试)
  ↓
Sonnet: code-reviewer (架构审查)
```

#### 模式 2：推理 → 操作（事件响应）

```
Sonnet: incident-responder (诊断问题、制定策略)
  ↓
Haiku: devops-troubleshooter (执行修复)
  ↓
Haiku: deployment-engineer (部署热修复)
  ↓
Haiku: 实现监控告警
```

#### 模式 3：复杂 → 简单（数据库设计）

```
Sonnet: database-architect (模式设计、技术选型)
  ↓
Haiku: sql-pro (生成迁移脚本)
  ↓
Haiku: database-admin (执行迁移)
  ↓
Haiku: database-optimizer (优化查询性能)
```

#### 模式 4：多代理工作流

```
全栈功能开发：
Sonnet: backend-architect + frontend-developer (设计组件)
  ↓
Haiku: 按设计生成代码
  ↓
Haiku: test-automator (单元 + 集成测试)
  ↓
Sonnet: security-auditor (安全审查)
  ↓
Haiku: deployment-engineer (CI/CD 设置)
  ↓
Haiku: 设置可观测性堆栈
```

## Agent 调用

### 自然语言

当您需要 Claude 推理使用哪个专家时，可以通过自然语言调用 Agent：

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

### 斜杠命令

许多 Agent 可通过插件斜杠命令直接调用：

```bash
/backend-development:feature-development user authentication
/security-scanning:security-sast
/incident-response:smart-fix "memory leak in payment service"
```

## 贡献

添加新 Agent：

1. 创建 `plugins/{plugin-name}/agents/{agent-name}.md`
2. 添加包含名称、描述和模型分配的 frontmatter
3. 编写全面的系统提示
4. 更新 `.claude-plugin/marketplace.json` 中的插件定义

详情请参阅[贡献指南](../CONTRIBUTING.md)。
