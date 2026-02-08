# 使用指南

使用代理、斜杠命令和多代理工作流的完整指南。

## 概述

插件生态系统提供两个主要接口：

1. **斜杠命令** - 直接调用工具和工作流
2. **自然语言** - Claude 推理使用哪些代理

## 斜杠命令

斜杠命令是与代理和工作流交互的主要接口。每个插件都提供可以直接运行的命名空间命令。

### 命令格式

```bash
/plugin-name:command-name [参数]
```

### 发现命令

列出已安装插件的所有可用斜杠命令：

```bash
/plugin
```

### 斜杠命令的优势

- **直接调用** - 无需用自然语言描述您想要的内容
- **结构化参数** - 显式传递参数以实现精确控制
- **可组合性** - 链接命令以实现复杂的工作流
- **可发现性** - 使用 `/plugin` 查看所有可用命令

## 自然语言

当您需要 Claude 推理使用哪个专家时，也可以通过自然语言调用代理：

```
"使用 backend-architect 设计身份验证 API"
"让 security-auditor 扫描 OWASP 漏洞"
"让 performance-engineer 优化此数据库查询"
```

Claude Code 会根据您的请求自动选择和协调适当的代理。

## 按类别分类的命令参考

### 开发和功能

| 命令                                        | 描述                                 |
| ---------------------------------------------- | ------------------------------------------- |
| `/backend-development:feature-development`     | 端到端后端功能开发      |
| `/full-stack-orchestration:full-stack-feature` | 完整的全栈功能实现  |
| `/multi-platform-apps:multi-platform`          | 跨平台应用开发协调 |

### 测试和质量

| 命令                       | 描述                           |
| ----------------------------- | ------------------------------------- |
| `/unit-testing:test-generate` | 生成全面的单元测试     |
| `/tdd-workflows:tdd-cycle`    | 完整的 TDD 红绿重构周期 |
| `/tdd-workflows:tdd-red`      | 首先编写失败的测试             |
| `/tdd-workflows:tdd-green`    | 实现代码以通过测试          |
| `/tdd-workflows:tdd-refactor` | 在测试通过时重构           |

### 代码质量和审查

| 命令                             | 描述                |
| ----------------------------------- | -------------------------- |
| `/code-review-ai:ai-review`         | AI 驱动的代码审查     |
| `/comprehensive-review:full-review` | 多视角分析 |
| `/comprehensive-review:pr-enhance`  | 增强拉取请求      |

### 调试和故障排除

| 命令                                | 描述                    |
| -------------------------------------- | ------------------------------ |
| `/debugging-toolkit:smart-debug`       | 交互式智能调试    |
| `/incident-response:incident-response` | 生产事件管理 |
| `/incident-response:smart-fix`         | 自动化事件解决  |
| `/error-debugging:error-analysis`      | 深度错误分析            |
| `/error-debugging:error-trace`         | 堆栈跟踪调试          |
| `/error-diagnostics:smart-debug`       | 智能诊断调试     |
| `/distributed-debugging:debug-trace`   | 分布式系统跟踪     |

### 安全

| 命令                                    | 描述                         |
| ------------------------------------------ | ----------------------------------- |
| `/security-scanning:security-hardening`    | 全面的安全加固    |
| `/security-scanning:security-sast`         | 静态应用安全测试 |
| `/security-scanning:security-dependencies` | 依赖漏洞扫描   |
| `/security-compliance:compliance-check`    | SOC2/HIPAA/GDPR 合规          |
| `/frontend-mobile-security:xss-scan`       | XSS 漏洞扫描          |

### 基础设施和部署

| 命令                                   | 描述                     |
| ----------------------------------------- | ------------------------------- |
| `/observability-monitoring:monitor-setup` | 设置监控基础设施 |
| `/observability-monitoring:slo-implement` | 实现 SLO/SLI 指标       |
| `/deployment-validation:config-validate`  | 部署前验证       |
| `/cicd-automation:workflow-automate`      | CI/CD 管道自动化       |

### 数据和 ML

| 命令                                 | 描述                        |
| --------------------------------------- | ---------------------------------- |
| `/machine-learning-ops:ml-pipeline`     | ML 训练管道编排 |
| `/data-engineering:data-pipeline`       | ETL/ELT 管道构建      |
| `/data-engineering:data-driven-feature` | 数据驱动的功能开发    |

### 文档

| 命令                                  | 描述                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| `/code-documentation:doc-generate`       | 生成全面的文档                                                       |
| `/code-documentation:code-explain`       | 解释代码功能                                                                 |
| `/documentation-generation:doc-generate` | OpenAPI 规范、图表、教程                                                         |
| `/c4-architecture:c4-architecture`       | 生成全面的 C4 架构文档（上下文、容器、组件、代码） |

### 重构和维护

| 命令                                 | 描述                  |
| --------------------------------------- | ---------------------------- |
| `/code-refactoring:refactor-clean`      | 代码清理和重构 |
| `/code-refactoring:tech-debt`           | 技术债务管理    |
| `/codebase-cleanup:deps-audit`          | 依赖审计          |
| `/codebase-cleanup:tech-debt`           | 技术债务减少     |
| `/framework-migration:legacy-modernize` | 遗留代码现代化    |
| `/framework-migration:code-migrate`     | 框架迁移          |
| `/framework-migration:deps-upgrade`     | 依赖升级          |

### 数据库

| 命令                                        | 描述                     |
| ---------------------------------------------- | ------------------------------- |
| `/database-migrations:sql-migrations`          | SQL 迁移自动化        |
| `/database-migrations:migration-observability` | 迁移监控            |
| `/database-cloud-optimization:cost-optimize`   | 数据库和云优化 |

### Git 和 PR 工作流

| 命令                          | 描述                  |
| -------------------------------- | ---------------------------- |
| `/git-pr-workflows:pr-enhance`   | 增强拉取请求质量 |
| `/git-pr-workflows:onboard`      | 团队入职自动化   |
| `/git-pr-workflows:git-workflow` | Git 工作流自动化      |

### 项目脚手架

| 命令                                      | 描述                  |
| -------------------------------------------- | ---------------------------- |
| `/python-development:python-scaffold`        | FastAPI/Django 项目设置 |
| `/javascript-typescript:typescript-scaffold` | Next.js/React + Vite 设置   |
| `/systems-programming:rust-project`          | Rust 项目脚手架     |

### AI 和 LLM 开发

| 命令                                     | 描述                     |
| ------------------------------------------- | ------------------------------- |
| `/llm-application-dev:langchain-agent`      | LangChain 代理开发     |
| `/llm-application-dev:ai-assistant`         | AI 助手实现     |
| `/llm-application-dev:prompt-optimize`      | 提示工程优化 |
| `/agent-orchestration:multi-agent-optimize` | 多代理优化        |
| `/agent-orchestration:improve-agent`        | 代理改进工作流     |

### 测试和性能

| 命令                                             | 描述          |
| --------------------------------------------------- | -------------------- |
| `/performance-testing-review:ai-review`             | 性能分析 |
| `/application-performance:performance-optimization` | 应用优化     |

### 团队协作

| 命令                             | 描述                 |
| ----------------------------------- | --------------------------- |
| `/team-collaboration:issue`         | 问题管理自动化 |
| `/team-collaboration:standup-notes` | 站会笔记生成    |

### 可访问性

| 命令                                         | 描述              |
| ----------------------------------------------- | ------------------------ |
| `/accessibility-compliance:accessibility-audit` | WCAG 合规审计 |

### API 开发

| 命令                               | 描述             |
| ------------------------------------- | ----------------------- |
| `/api-testing-observability:api-mock` | API 模拟和测试 |

### 上下文管理

| 命令                               | 描述               |
| ------------------------------------- | ------------------------- |
| `/context-management:context-save`    | 保存对话上下文 |
| `/context-management:context-restore` | 恢复以前的上下文  |

## 多代理工作流示例

插件提供可通过斜杠命令访问的预配置多代理工作流。

### 全栈开发

```bash
# 基于命令的工作流调用
/full-stack-orchestration:full-stack-feature "具有实时分析的用户仪表板"

# 自然语言替代方案
"实现具有实时分析的用户仪表板"
```

**编排：** backend-architect → database-architect → frontend-developer → test-automator → security-auditor → deployment-engineer → observability-engineer

**发生的过程：**

1. 具有迁移的数据库架构设计
2. 后端 API 实现（REST/GraphQL）
3. 具有状态管理的前端组件
4. 全面的测试套件（单元/集成/E2E）
5. 安全审计和加固
6. 具有功能标志的 CI/CD 管道设置
7. 可观察性和监控配置

### 安全加固

```bash
# 全面的安全评估和修复
/security-scanning:security-hardening --level comprehensive

# 自然语言替代方案
"执行安全审计并实施 OWASP 最佳实践"
```

**编排：** security-auditor → backend-security-coder → frontend-security-coder → mobile-security-coder → test-automator

### 数据/ML 管道

```bash
# 具有生产部署的 ML 功能开发
/machine-learning-ops:ml-pipeline "客户流失预测模型"

# 自然语言替代方案
"构建具有部署的客户流失预测模型"
```

**编排：** data-scientist → data-engineer → ml-engineer → mlops-engineer → performance-engineer

### 事件响应

```bash
# 具有根因分析的智能调试
/incident-response:smart-fix "支付服务中的生产内存泄漏"

# 自然语言替代方案
"调试生产内存泄漏并创建运行手册"
```

**编排：** incident-responder → devops-troubleshooter → debugger → error-detective → observability-engineer

### C4 架构文档

```bash
# 生成全面的 C4 架构文档
/c4-architecture:c4-architecture

# 自然语言替代方案
"为此代码库创建 C4 架构文档"
```

**编排：** c4-code → c4-component → c4-container → c4-context

**发生的过程：**

1. **代码级别**：自底向上分析所有子目录，创建具有函数签名和依赖关系的代码级文档
2. **组件级别**：将代码文档合成为具有接口和关系的逻辑组件
3. **容器级别**：将组件映射到具有 OpenAPI/Swagger API 规范的部署容器
4. **上下文级别**：创建具有人物角色、用户旅程和外部依赖关系的高级系统上下文

**输出：** `C4-Documentation/` 目录中的完整 C4 文档，包含所有级别的 Mermaid 图（上下文、容器、组件、代码）

## 命令参数和选项

许多斜杠命令支持参数以实现精确控制：

```bash
# 为特定文件生成测试
/unit-testing:test-generate src/api/users.py

# 具有方法规范的功能开发
/backend-development:feature-development OAuth2 integration with social login

# 安全依赖扫描
/security-scanning:security-dependencies

# 组件脚手架
/frontend-mobile-development:component-scaffold UserProfile component with hooks

# TDD 工作流周期
/tdd-workflows:tdd-red User can reset password
/tdd-workflows:tdd-green
/tdd-workflows:tdd-refactor

# 智能调试
/debugging-toolkit:smart-debug memory leak in checkout flow

# Python 项目脚手架
/python-development:python-scaffold fastapi-microservice

# C4 架构文档生成
/c4-architecture:c4-architecture
```

## 结合自然语言和命令

您可以混合使用两种方法以实现最佳灵活性：

```
# 从命令开始以进行结构化工作流
/full-stack-orchestration:full-stack-feature "支付处理"

# 然后提供自然语言指导
"确保 PCI-DSS 合规并与 Stripe 集成"
"为失败的事务添加重试逻辑"
"设置欺诈检测规则"
```

## 最佳实践

### 何时使用斜杠命令

- **结构化工作流** - 具有明确阶段的多步骤过程
- **重复性任务** - 您经常执行的操作
- **精确控制** - 当您需要特定参数时
- **发现** - 探索可用功能

### 何时使用自然语言

- **探索性工作** - 当您不确定使用哪个工具时
- **复杂推理** - 当 Claude 需要协调多个代理时
- **上下文决策** - 当正确方法取决于情况时
- **临时任务** - 不适合命令的一次性操作

### 工作流组合

为复杂场景组合多个插件：

```bash
# 1. 从功能开发开始
/backend-development:feature-development payment processing API

# 2. 添加安全加固
/security-scanning:security-hardening

# 3. 生成全面的测试
/unit-testing:test-generate

# 4. 审查实现
/code-review-ai:ai-review

# 5. 设置 CI/CD
/cicd-automation:workflow-automate

# 6. 添加监控
/observability-monitoring:monitor-setup
```

## 代理技能集成

代理技能与命令配合工作以提供深厚的专业知识：

```
用户："设置具有异步模式的 FastAPI 项目"
→ 激活：fastapi-templates 技能
→ 调用：/python-development:python-scaffold
→ 结果：具有最佳实践的生产就绪 FastAPI 项目

用户："使用 Helm 实现 Kubernetes 部署"
→ 激活：helm-chart-scaffolding、k8s-manifest-generator 技能
→ 指导：kubernetes-architect 代理
→ 结果：具有 Helm 图表的生产级 K8s 清单
```

有关 107 个专业技能的详细信息，请参阅[代理技能](./agent-skills.md)。

## 另请参阅

- [代理技能](./agent-skills.md) - 专业知识包
- [代理参考](./agents.md) - 完整的代理目录
- [插件参考](./plugins.md) - 所有 67 个插件
- [架构](./architecture.md) - 设计原则
