编排从需求到生产部署的端到端功能开发：

[扩展思考：此工作流通过综合功能开发阶段编排专业智能体——从发现和规划到实施、测试和部署。每个阶段都基于之前的输出，确保连贯的功能交付。工作流支持多种开发方法论（传统、TDD/BDD、DDD）、功能复杂度级别和现代部署策略，包括功能开关、渐进式推出和可观测性优先开发。智能体从之前阶段接收详细上下文，以在整个开发生命周期中保持一致性和质量。]

## 配置选项

### 开发方法论

- **traditional**: 实现后测试的顺序开发
- **tdd**: 使用红-绿-重构循环的测试驱动开发
- **bdd**: 使用基于场景测试的行为驱动开发
- **ddd**: 使用限界上下文和聚合的领域驱动设计

### 功能复杂度

- **simple**: 单一服务、最少集成（1-2 天）
- **medium**: 多个服务、中等集成（3-5 天）
- **complex**: 跨域、广泛集成（1-2 周）
- **epic**: 重大架构变更、多个团队（2+ 周）

### 部署策略

- **direct**: 立即向所有用户推出
- **canary**: 从 5% 流量开始的渐进式推出
- **feature-flag**: 通过功能开关控制激活
- **blue-green**: 零停机部署并支持即时回滚
- **a-b-test**: 分流流量进行实验和指标收集

## 阶段 1：发现和需求规划

1. **业务分析和需求**
   - 使用 Task 工具，subagent_type="business-analytics::business-analyst"
   - 提示："分析功能需求：$ARGUMENTS。定义用户故事、验收标准、成功指标和业务价值。识别利益相关者、依赖关系和风险。创建具有清晰范围边界的功能规格文档。"
   - 预期输出：包含用户故事、成功指标、风险评估的需求文档
   - 上下文：初始功能请求和业务上下文

2. **技术架构设计**
   - 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
   - 提示："为功能设计技术架构：$ARGUMENTS。使用需求：[包含步骤 1 的业务分析]。定义服务边界、API 契约、数据模型、集成点和技术栈。考虑可扩展性、性能和安全要求。"
   - 预期输出：包含架构图、API 规范、数据模型的技术设计文档
   - 上下文：业务需求、现有系统架构

3. **可行性和风险评估**
   - 使用 Task 工具，subagent_type="security-scanning::security-auditor"
   - 提示："评估功能的安全影响和风险：$ARGUMENTS。审查架构：[包含步骤 2 的技术设计]。识别安全要求、合规需求、数据隐私顾虑和潜在漏洞。"
   - 预期输出：包含风险矩阵、合规检查清单、缓解策略的安全评估
   - 上下文：技术设计、监管要求

## 阶段 2：实施和开发

4. **后端服务实施**
   - 使用 Task 工具，subagent_type="backend-architect"
   - 提示："为以下内容实施后端服务：$ARGUMENTS。遵循技术设计：[包含步骤 2 的架构]。构建 RESTful/GraphQL API，实施业务逻辑，与数据层集成，添加弹性模式（断路器、重试），实施缓存策略。包含渐进式推出的功能开关。"
   - 预期输出：具有 API、业务逻辑、数据库集成、功能开关的后端服务
   - 上下文：技术设计、API 契约、数据模型

5. **前端实施**
   - 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
   - 提示："为以下内容构建前端组件：$ARGUMENTS。与后端 API 集成：[包含步骤 4 的 API 端点]。实施响应式 UI、状态管理、错误处理、加载状态和分析跟踪。添加功能开关集成以支持 A/B 测试能力。"
   - 预期输出：具有 API 集成、状态管理、分析的前端组件
   - 上下文：后端 API、UI/UX 设计、用户故事

6. **数据管道和集成**
   - 使用 Task 工具，subagent_type="data-engineering::data-engineer"
   - 提示："为以下内容构建数据管道：$ARGUMENTS。设计 ETL/ELT 流程，实施数据验证，创建分析事件，设置数据质量监控。与产品分析平台集成以进行功能使用跟踪。"
   - 预期输出：数据管道、分析事件、数据质量检查
   - 上下文：数据需求、分析需求、现有数据基础设施

## 阶段 3：测试和质量保证

7. **自动化测试套件**
   - 使用 Task 工具，subagent_type="unit-testing::test-automator"
   - 提示："为以下内容创建全面的测试套件：$ARGUMENTS。为后端 [来自步骤 4] 和前端 [来自步骤 5] 编写单元测试。添加 API 端点的集成测试、关键用户旅程的端到端测试、可扩展性验证的性能测试。确保最低 80% 代码覆盖率。"
   - 预期输出：包含单元、集成、端到端和性能测试的测试套件
   - 上下文：实施代码、验收标准、测试要求

8. **安全验证**
   - 使用 Task 工具，subagent_type="security-scanning::security-auditor"
   - 提示："为以下内容执行安全测试：$ARGUMENTS。审查实施：[包含步骤 4-5 的后端和前端]。运行 OWASP 检查、渗透测试、依赖扫描和合规验证。验证数据加密、身份验证和授权。"
   - 预期输出：安全测试结果、漏洞报告、补救措施
   - 上下文：实施代码、安全要求

9. **性能优化**
   - 使用 Task 工具，subagent_type="application-performance::performance-engineer"
   - 提示："优化以下内容的性能：$ARGUMENTS。分析后端服务 [来自步骤 4] 和前端 [来自步骤 5]。分析代码、优化查询、实施缓存、减少捆绑包大小、改善加载时间。设置性能预算和监控。"
   - 预期输出：性能改进、优化报告、性能指标
   - 上下文：实施代码、性能要求

## 阶段 4：部署和监控

10. **部署策略和管道**
    - 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
    - 提示："为以下内容准备部署：$ARGUMENTS。创建具有自动化测试的 CI/CD 管道 [来自步骤 7]。配置渐进式推出的功能开关，实施蓝绿部署，设置回滚程序。创建部署运行手册和回滚计划。"
    - 预期输出：CI/CD 管道、部署配置、回滚程序
    - 上下文：测试套件、基础设施要求、部署策略

11. **可观测性和监控**
    - 使用 Task 工具，subagent_type="observability-monitoring::observability-engineer"
    - 提示："为以下内容设置可观测性：$ARGUMENTS。实施分布式追踪、自定义指标、错误跟踪和告警。创建功能使用、性能指标、错误率和业务 KPI 的仪表板。设置 SLO/SLI 和自动告警。"
    - 预期输出：监控仪表板、告警、SLO 定义、可观测性基础设施
    - 上下文：功能实施、成功指标、运维要求

12. **文档和知识转移**
    - 使用 Task 工具，subagent_type="documentation-generation::docs-architect"
    - 提示："为以下内容生成全面的文档：$ARGUMENTS。创建 API 文档、用户指南、部署指南、故障排除运行手册。包含架构图、数据流图和集成指南。从提交生成自动变更日志。"
    - 预期输出：API 文档、用户指南、运行手册、架构文档
    - 上下文：所有之前阶段的输出

## 执行参数

### 必需参数

- **--feature**: 功能名称和描述
- **--methodology**: 开发方法（traditional|tdd|bdd|ddd）
- **--complexity**: 功能复杂度级别（simple|medium|complex|epic）

### 可选参数

- **--deployment-strategy**: 部署方法（direct|canary|feature-flag|blue-green|a-b-test）
- **--test-coverage-min**: 最低测试覆盖率阈值（默认：80%）
- **--performance-budget**: 性能要求（例如，<200ms 响应时间）
- **--rollout-percentage**: 渐进式部署的初始推出百分比（默认：5%）
- **--feature-flag-service**: 功能开关提供商（launchdarkly|split|unleash|custom）
- **--analytics-platform**: 分析集成（segment|amplitude|mixpanel|custom）
- **--monitoring-stack**: 可观测性工具（datadog|newrelic|grafana|custom）

## 成功标准

- 满足业务需求中的所有验收标准
- 测试覆盖率超过最低阈值（默认 80%）
- 安全扫描显示无关键漏洞
- 性能满足定义的预算和 SLO
- 为控制推出配置了功能开关
- 监控和告警完全运行
- 文档完整并已批准
- 成功部署到生产环境并具有回滚能力
- 产品分析跟踪功能使用
- 配置了 A/B 测试指标（如适用）

## 回滚策略

如果在部署期间或部署后出现问题：

1. 立即禁用功能开关（< 1 分钟）
2. 蓝绿流量切换（< 5 分钟）
3. 通过 CI/CD 完整部署回滚（< 15 分钟）
4. 数据库迁移回滚（如需要）（与数据团队协调）
5. 事件事后分析和重新部署前的修复

功能描述：$ARGUMENTS