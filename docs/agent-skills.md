# Agent 技能

Agent 技能是模块化包，通过专业领域知识扩展 Claude 的能力，遵循 Anthropic 的 [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)。该插件生态系统包含跨 27 个插件的 **129 种专业技能**，实现渐进式披露和高效的 token 使用。

## 概述

技能为 Claude 提供特定领域的深度专业知识，而无需预先将所有内容加载到上下文中。每个技能包括：

- **YAML Frontmatter**：名称和激活标准
- **渐进式披露**：元数据 → 指令 → 资源
- **激活触发器**：清晰的"适用于"子句用于自动调用

## 按插件分类的技能

### Kubernetes 运维 (4 个技能)

| 技能                      | 描述                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **k8s-manifest-generator** | 按照最佳实践创建生产就绪的 Kubernetes 清单，用于 Deployment、Service、ConfigMap 和 Secret |
| **helm-chart-scaffolding** | 设计、组织和管理 Helm 图表，用于模板化和打包 Kubernetes 应用                            |
| **gitops-workflow**        | 使用 ArgoCD 和 Flux 实现 GitOps 工作流，实现自动化、声明式部署                                   |
| **k8s-security-policies**  | 实现包括 NetworkPolicy、PodSecurityPolicy 和 RBAC 的 Kubernetes 安全策略                              |

### LLM 应用开发 (8 个技能)

| 技能                            | 描述                                                                                 |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| **langchain-architecture**       | 使用 LangChain 框架设计 LLM 应用，包含代理、记忆和工具集成 |
| **prompt-engineering-patterns**  | 掌握高级提示工程技术，提升 LLM 性能和可靠性           |
| **rag-implementation**           | 使用向量数据库和语义搜索构建检索增强生成系统      |
| **llm-evaluation**               | 通过自动化指标和基准测试实现全面评估策略       |
| **embedding-strategies**         | 设计文本、图像和多模态内容的嵌入管道，实现最优分块   |
| **similarity-search-patterns**   | 使用 ANN 算法和距离度量实现高效相似性搜索              |
| **vector-index-tuning**          | 通过 HNSW、IVF 和混合配置优化向量索引性能                 |
| **hybrid-search-implementation** | 结合向量和关键词搜索以提高检索准确性                           |

### 后端开发 (9 个技能)

| 技能                               | 描述                                                                                           |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **api-design-principles**           | 掌握 REST 和 GraphQL API 设计，构建直观、可扩展且可维护的 API                     |
| **architecture-patterns**           | 实现整洁架构、六边形架构和领域驱动设计                        |
| **microservices-patterns**          | 设计微服务，包含服务边界、事件驱动通信和弹性              |
| **workflow-orchestration-patterns** | 使用 Temporal 设计持久化工作流，用于分布式系统、Saga 模式和状态管理   |
| **temporal-python-testing**         | 使用 pytest、时间跳过和模拟策略测试 Temporal 工作流，实现全面覆盖 |
| **event-store-design**              | 设计优化的模式、快照和流分区的事件存储                        |
| **cqrs-implementation**             | 实现使用分离读/写模型的 CQRS 和最终一致性模式                      |
| **projection-patterns**             | 从事件流构建高效投影，用于读优化视图                               |
| **saga-orchestration**              | 设计包含补偿逻辑和故障处理的分布式 Saga                                 |

### 开发者必备 (11 个技能)

| 技能                            | 描述                                                                                     |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| **git-advanced-workflows**       | 掌握高级 Git 工作流，包括变基、精选、二分、工作树和 reflog |
| **sql-optimization-patterns**    | 优化 SQL 查询、索引策略和 EXPLAIN 分析以提升数据库性能        |
| **error-handling-patterns**      | 实现健壮的错误处理，包含异常、Result 类型和优雅降级         |
| **code-review-excellence**       | 提供有效的代码审查，包含建设性反馈和系统分析               |
| **e2e-testing-patterns**         | 使用 Playwright 和 Cypress 为关键用户工作流构建可靠的 E2E 测试套件          |
| **auth-implementation-patterns** | 使用 JWT、OAuth2、会话和 RBAC 实现认证和授权                 |
| **debugging-strategies**         | 掌握系统化调试技术、分析工具和根本原因分析                |
| **monorepo-management**          | 使用 Turborepo、Nx 和 pnpm 工作区管理 monorepo，实现可扩展的多包项目    |
| **nx-workspace-patterns**        | 使用计算缓存和影响命令配置 Nx 工作区                          |
| **turborepo-caching**            | 通过远程缓存和管道配置优化 Turborepo 构建                        |
| **bazel-build-optimization**     | 使用隔离操作和远程执行设计 Bazel 构建                                  |

### 区块链与 Web3 (4 个技能)

| 技能                       | 描述                                                                             |
| --------------------------- | --------------------------------------------------------------------------------------- |
| **defi-protocol-templates** | 使用质押、AMM、治理和借贷模板实现 DeFi 协议      |
| **nft-standards**           | 实现包含元数据和市场集成的 NFT 标准 (ERC-721, ERC-1155)   |
| **solidity-security**       | 掌握智能合约安全以防止漏洞并实现安全模式 |
| **web3-testing**            | 使用 Hardhat 和 Foundry 测试智能合约，包含单元测试和主网分叉      |

### CI/CD 自动化 (4 个技能)

| 技能                          | 描述                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| **deployment-pipeline-design** | 设计包含审批门和安全检查的多阶段 CI/CD 管道                |
| **github-actions-templates**   | 创建用于测试、构建和部署的生产就绪 GitHub Actions 工作流     |
| **gitlab-ci-patterns**         | 使用多阶段工作流和分布式运行器构建 GitLab CI/CD 管道           |
| **secrets-management**         | 使用 Vault、AWS Secrets Manager 或原生解决方案实现安全密钥管理         |

### 云基础设施 (8 个技能)

| 技能                          | 描述                                                               |
| ------------------------------ | ------------------------------------------------------------------------- |
| **terraform-module-library**   | 为 AWS、Azure 和 GCP 基础设施构建可重用的 Terraform 模块   |
| **multi-cloud-architecture**   | 设计避免供应商锁定的多云架构                  |
| **hybrid-cloud-networking**    | 配置本地和云平台之间的安全连接     |
| **cost-optimization**          | 通过合理调整大小、标记和预留实例优化云成本          |
| **istio-traffic-management**   | 配置 Istio 流量路由、负载均衡和金丝雀部署   |
| **linkerd-patterns**           | 使用自动 mTLS 和流量拆分实现 Linkerd 服务网格  |
| **mtls-configuration**         | 使用证书管理设计零信任 mTLS 架构          |
| **service-mesh-observability** | 使用分布式跟踪和指标构建全面的可观测性    |

### 框架迁移 (4 个技能)

| 技能                   | 描述                                                                   |
| ----------------------- | ----------------------------------------------------------------------------- |
| **react-modernization** | 升级 React 应用，迁移到 hooks，采用并发特性           |
| **angular-migration**   | 使用混合模式和增量重写从 AngularJS 迁移到 Angular |
| **database-migration**  | 使用零停机策略和转换执行数据库迁移  |
| **dependency-upgrade**  | 通过兼容性分析和测试管理主要依赖升级      |

### 可观测性与监控 (4 个技能)

| 技能                        | 描述                                                             |
| ---------------------------- | ----------------------------------------------------------------------- |
| **prometheus-configuration** | 设置 Prometheus 以实现全面的指标收集和监控    |
| **grafana-dashboards**       | 创建生产 Grafana 仪表板以实现实时系统可视化 |
| **distributed-tracing**      | 使用 Jaeger 和 Tempo 实现分布式跟踪以跟踪请求   |
| **slo-implementation**       | 使用错误预算和告警定义 SLI 和 SLO                    |

### 支付处理 (4 个技能)

| 技能                  | 描述                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| **stripe-integration** | 实现 Stripe 支付处理，包含结账、订阅和 Webhook |
| **paypal-integration** | 集成 PayPal 支付处理，包含快速结账和订阅   |
| **pci-compliance**     | 实现 PCI DSS 合规以安全处理支付卡数据            |
| **billing-automation** | 构建自动计费系统以处理周期性支付和发票          |

### Python 开发 (5 个技能)

| 技能                               | 描述                                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------- |
| **async-python-patterns**           | 掌握 Python asyncio、并发编程和 async/await 模式               |
| **python-testing-patterns**         | 使用 pytest、fixture 和 mock 实现全面测试                    |
| **python-packaging**                | 创建可分发的 Python 包，包含正确的结构和 PyPI 发布        |
| **python-performance-optimization** | 使用 cProfile 和性能最佳实践分析和优化 Python 代码        |
| **uv-package-manager**              | 掌握 uv 包管理器以实现快速依赖管理和虚拟环境              |

### JavaScript/TypeScript (4 个技能)

| 技能                           | 描述                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| **typescript-advanced-types**   | 掌握 TypeScript 高级类型系统，包含泛型和条件类型     |
| **nodejs-backend-patterns**     | 使用 Express/Fastify 和最佳实践构建生产就绪的 Node.js 服务       |
| **javascript-testing-patterns** | 使用 Jest、Vitest 和 Testing Library 实现全面测试                |
| **modern-javascript-patterns**  | 掌握 ES6+ 特性，包含 async/await、解构和函数式编程 |

### API 脚手架 (1 个技能)

| 技能                 | 描述                                                                     |
| --------------------- | ------------------------------------------------------------------------------- |
| **fastapi-templates** | 创建包含异步模式和错误处理的生产就绪 FastAPI 项目 |

### 机器学习运维 (1 个技能)

| 技能                    | 描述                                                               |
| ------------------------ | ------------------------------------------------------------------------- |
| **ml-pipeline-workflow** | 构建从数据准备到部署的端到端 MLOps 管道 |

### 安全扫描 (5 个技能)

| 技能                               | 描述                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------- |
| **sast-configuration**              | 配置静态应用安全测试工具以检测漏洞 |
| **stride-analysis-patterns**        | 应用 STRIDE 方法论识别欺骗、篡改和其他威胁     |
| **attack-tree-construction**        | 构建将威胁场景映射到漏洞的攻击树                  |
| **security-requirement-extraction** | 从威胁模型导出安全需求及验收标准        |
| **threat-mitigation-mapping**       | 将威胁映射到缓解措施及优先修复计划                   |

### 可访问性合规 (2 个技能)

| 技能                     | 描述                                                             |
| ------------------------- | ----------------------------------------------------------------------- |
| **wcag-audit-patterns**   | 使用自动化和手动测试进行 WCAG 2.2 可访问性审计 |
| **screen-reader-testing** | 在 NVDA、JAWS 和 VoiceOver 上测试屏幕阅读器兼容性       |

### 业务分析 (2 个技能)

| 技能                    | 描述                                                                  |
| ------------------------ | ---------------------------------------------------------------------------- |
| **kpi-dashboard-design** | 设计包含可操作 KPI 和下钻功能的高管仪表板 |
| **data-storytelling**    | 将数据洞察转化为面向利益相关者的引人入胜的叙述          |

### 数据工程 (4 个技能)

| 技能                           | 描述                                                                 |
| ------------------------------- | --------------------------------------------------------------------------- |
| **spark-optimization**          | 通过分区、缓存和广播连接优化 Apache Spark 作业  |
| **dbt-transformation-patterns** | 使用增量策略和测试构建 dbt 模型                    |
| **airflow-dag-patterns**        | 设计具有适当依赖和错误处理的 Airflow DAG             |
| **data-quality-frameworks**     | 使用 Great Expectations 和自定义验证器实现数据质量检查     |

### 文档生成 (3 个技能)

| 技能                             | 描述                                                         |
| --------------------------------- | ------------------------------------------------------------------- |
| **openapi-spec-generation**       | 从代码生成包含完整模式的 OpenAPI 3.1 规范 |
| **changelog-automation**          | 从约定提交自动生成变更日志             |
| **architecture-decision-records** | 编写记录架构决策和权衡的 ADR       |

### 前端移动开发 (4 个技能)

| 技能                          | 描述                                                     |
| ------------------------------ | --------------------------------------------------------------- |
| **react-state-management**     | 使用 Zustand、Jotai 和 React Query 实现状态管理 |
| **nextjs-app-router-patterns** | 使用 App Router、RSC 和流式构建 Next.js 14+ 应用      |
| **tailwind-design-system**     | 使用 Tailwind CSS 和组件库创建设计系统     |
| **react-native-architecture**  | 架构包含导航和原生模块的 React Native 应用  |

### UI 设计 (9 个技能)

| 技能                         | 描述                                                         |
| ----------------------------- | ------------------------------------------------------------------- |
| **design-system-patterns**    | 使用令牌、组件和主题构建可扩展的设计系统  |
| **accessibility-compliance**  | 使用适当的 ARIA 和键盘导航实现 WCAG 2.1/2.2 合规  |
| **responsive-design**         | 使用 CSS Grid、Flexbox 和容器查询创建流体布局  |
| **mobile-ios-design**         | 遵循人机界面指南设计 iOS 应用                |
| **mobile-android-design**     | 遵循 Material Design 3 指南设计 Android 应用          |
| **react-native-design**       | React Native 应用的跨平台设计模式        |
| **web-component-design**      | 使用 Shadow DOM 构建可访问、可重用的 Web 组件           |
| **interaction-design**        | 创建微交互、动画和基于手势的界面        |
| **visual-design-foundations** | 应用排版、色彩理论、间距和视觉层次       |

### 游戏开发 (2 个技能)

| 技能                       | 描述                                                          |
| --------------------------- | -------------------------------------------------------------------- |
| **unity-ecs-patterns**      | 实现 Unity ECS 以构建高性能游戏系统                |
| **godot-gdscript-patterns** | 使用 GDScript 最佳实践和场景组合构建 Godot 游戏 |

### HR 法务合规 (2 个技能)

| 技能                             | 描述                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| **gdpr-data-handling**            | 实现符合 GDPR 的数据处理及同意管理 |
| **employment-contract-templates** | 生成包含特定司法管辖区条款的雇佣合同 |

### 事件响应 (3 个技能)

| 技能                          | 描述                                                           |
| ------------------------------ | --------------------------------------------------------------------- |
| **postmortem-writing**         | 编写包含根本原因分析和行动项的无责事后回顾         |
| **incident-runbook-templates** | 为常见事件场景创建包含升级路径的运行手册   |
| **on-call-handoff-patterns**   | 设计包含上下文保留和告警路由的值班交接   |

### 量化交易 (2 个技能)

| 技能                        | 描述                                                             |
| ---------------------------- | ----------------------------------------------------------------------- |
| **backtesting-frameworks**   | 构建包含真实滑点和交易成本的回测系统 |
| **risk-metrics-calculation** | 计算投资组合的 VaR、夏普比率和回撤指标        |

### 系统编程 (3 个技能)

| 技能                       | 描述                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| **rust-async-patterns**     | 使用 Tokio、futures 和适当的错误处理实现异步 Rust         |
| **go-concurrency-patterns** | 使用 channel、工作池和上下文取消设计 Go 并发 |
| **memory-safety-patterns**  | 使用所有权、边界检查和清理程序编写内存安全代码      |

### Conductor - 项目管理 (3 个技能)

| 技能                          | 描述                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **context-driven-development** | 应用上下文驱动开发方法论，包含产品上下文、规范和分阶段规划  |
| **track-management**           | 管理功能、错误、杂项和重构的开发跟踪，包含规范和实施计划 |
| **workflow-patterns**          | 实现 TDD 工作流、提交策略和验证检查点，实现系统化开发     |

## 技能工作原理

### 激活

当 Claude 在您的请求中检测到匹配模式时，技能会自动激活：

```
用户: "Set up Kubernetes deployment with Helm chart"
→ 激活: helm-chart-scaffolding, k8s-manifest-generator

用户: "Build a RAG system for document Q&A"
→ 激活: rag-implementation, prompt-engineering-patterns

用户: "Optimize Python async performance"
→ 激活: async-python-patterns, python-performance-optimization
```

### 渐进式披露

技能使用三层架构实现 token 效率：

1. **元数据**（Frontmatter）：名称和激活标准（始终加载）
2. **指令**：核心指导和模式（激活时加载）
3. **资源**：示例和模板（按需加载）

### 与 Agent 集成

技能与 Agent 协同工作以提供深度领域专业知识：

- **Agent**：高级推理和编排
- **技能**：专业知识和实施模式

示例工作流：

```
backend-architect agent → 规划 API 架构
  ↓
api-design-principles skill → 提供 REST/GraphQL 最佳实践
  ↓
fastapi-templates skill → 提供生产就绪模板
```

## 规范合规性

所有 107 个技能遵循 [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)：

- ✓ 必需的 `name` 字段（连字符命名）
- ✓ �必需的 `description` 字段，包含"适用于"子句
- ✓ 描述少于 1024 个字符
- ✓ 完整、非截断的描述
- ✓ 正确的 YAML frontmatter 格式

## 创建新技能

向插件添加技能：

1. 创建 `plugins/{plugin-name}/skills/{skill-name}/SKILL.md`
2. 添加 YAML frontmatter：
   ```yaml
   ---
   name: skill-name
   description: 技能的功能。适用于 [激活触发器]。
   ---
   ```
3. 使用渐进式披露编写全面的技能内容
4. 将技能路径添加到 `marketplace.json`：
   ```json
   {
     "name": "plugin-name",
     "skills": ["./skills/skill-name"]
   }
   ```

### 技能结构

```
plugins/{plugin-name}/
└── skills/
    └── {skill-name}/
        └── SKILL.md        # Frontmatter + 内容
```

## 优势

- **Token 效率**：仅在需要时加载相关知识
- **专业专业知识**：深度领域知识，无冗余
- **清晰激活**：明确触发器防止意外调用
- **可组合性**：跨工作流混合搭配技能
- **可维护性**：隔离更新不影响其他技能

## 资源

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
