# Claude Code 插件：编排与自动化

> **⚡ 已针对 Opus 4.5、Sonnet 4.5 和 Haiku 4.5 更新** — 三层模型策略以实现最佳性能

[![Run in Smithery](https://smithery.ai/badge/skills/wshobson)](https://smithery.ai/skills?ns=wshobson&utm_source=github&utm_medium=badge)

> **🎯 代理技能已启用** — 129 个专业技能通过渐进式披露扩展了 Claude 在各插件中的能力

一个综合的生产就绪系统，结合了 **108 个专业 AI 代理**、**15 个多代理工作流编排器**、**129 个代理技能** 和 **72 个开发工具**，组织成 **72 个专注的、单一用途的插件**，用于 [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)。

## 概述

这个统一的仓库提供了现代软件开发中智能自动化和多代理编排所需的一切：

- **72 个专注的插件** - 细粒度的、单一用途的插件，针对最小 token 使用和可组合性进行了优化
- **108 个专业代理** - 在架构、语言、基础设施、质量、数据/AI、文档、业务运营和 SEO 方面拥有深厚知识的领域专家
- **129 个代理技能** - 模块化知识包，通过渐进式披露提供专业专业知识
- **15 个工作流编排器** - 多代理协调系统，用于全栈开发、安全加固、ML 流程和事件响应等复杂操作
- **72 个开发工具** - 优化的实用程序，包括项目脚手架、安全扫描、测试自动化和基础设施设置

### 主要特性

- **细粒度插件架构**：72 个专注的插件，针对最小 token 使用进行了优化
- **全面的工具**：72 个开发工具，包括测试生成、脚手架和安全扫描
- **100% 代理覆盖**：所有插件都包括专业代理
- **代理技能**：129 个专业技能，遵循渐进式披露和 token 效率原则
- **清晰的组织**：23 个类别，每个类别 1-6 个插件，易于发现
- **高效设计**：平均每个插件 3.4 个组件（遵循 Anthropic 的 2-8 模式）

### 工作原理

每个插件都完全独立，拥有自己的代理、命令和技能：

- **只安装你需要的内容** - 每个插件只加载其特定的代理、命令和技能
- **最小 token 使用** - 不会将不必要的资源加载到上下文中
- **混合搭配** - 组合多个插件用于复杂的工作流
- **清晰的边界** - 每个插件都有单一的、专注的目的
- **渐进式披露** - 技能仅在激活时加载知识

**示例**：安装 `python-development` 会加载 3 个 Python 代理、1 个脚手架工具，并提供 16 个技能（约 1000 个 token），而不是整个市场。

## 快速开始

### 步骤 1：添加市场

将此市场添加到 Claude Code：

```bash
/plugin marketplace add wshobson/agents
```

这使得所有 72 个插件都可以安装，但**不会将任何代理或工具加载到您的上下文中**。

### 步骤 2：安装插件

浏览可用的插件：

```bash
/plugin
```

安装您需要的插件：

```bash
# 核心开发插件
/plugin install python-development          # Python 带 16 个专业技能
/plugin install javascript-typescript       # JS/TS 带 4 个专业技能
/plugin install backend-development         # 后端 API 带 3 个架构技能

# 基础设施和运维
/plugin install kubernetes-operations       # K8s 带 4 个部署技能
/plugin install cloud-infrastructure        # AWS/Azure/GCP 带 4 个云技能

# 安全和质量
/plugin install security-scanning           # SAST 带安全技能
/plugin install code-review-ai             # AI 驱动的代码审查

# 全栈编排
/plugin install full-stack-orchestration   # 多代理工作流
```

每个安装的插件只将**其特定的代理、命令和技能**加载到 Claude 的上下文中。

### 插件 vs 代理

您安装**插件**，它捆绑了代理：

| 插件                  | 代理                                            |
| ----------------------- | ------------------------------------------------- |
| `comprehensive-review`  | architect-review, code-reviewer, security-auditor |
| `javascript-typescript` | javascript-pro, typescript-pro                    |
| `python-development`    | python-pro, django-pro, fastapi-pro               |
| `blockchain-web3`       | blockchain-developer                              |

```bash
# ❌ 错误 - 不能直接安装代理
/plugin install typescript-pro

# ✅ 正确 - 安装插件
/plugin install javascript-typescript@claude-code-workflows
```

### 故障排除

**"Plugin not found"** → 使用插件名称，而不是代理名称。添加 `@claude-code-workflows` 后缀。

**插件未加载** → 清除缓存并重新安装：

```bash
rm -rf ~/.claude/plugins/cache/claude-code-workflows && rm ~/.claude/plugins/installed_plugins.json
```

## 文档

### 核心指南

- **[插件参考](docs/plugins.md)** - 所有 72 个插件的完整目录
- **[代理参考](docs/agents.md)** - 按类别组织的所有 108 个代理
- **[代理技能](docs/agent-skills.md)** - 129 个具有渐进式披露的专业技能
- **[使用指南](docs/usage.md)** - 命令、工作流和最佳实践
- **[架构](docs/architecture.md)** - 设计原则和模式

### 快速链接

- [安装](#quick-start) - 2 步入门
- [核心插件](docs/plugins.md#quick-start---essential-plugins) - 立即提高生产力的顶级插件
- [命令参考](docs/usage.md#command-reference-by-category) - 按类别组织的所有斜杠命令
- [多代理工作流](docs/usage.md#multi-agent-workflow-examples) - 预配置的编排示例
- [模型配置](docs/agents.md#model-configuration) - Haiku/Sonnet 混合编排

## 新增功能

### 代理技能（跨 20 个插件的 140 个技能）

遵循 Anthropic 渐进式披露架构的专业知识包：

**语言开发：**

- **Python**（5 个技能）：异步模式、测试、打包、性能、UV 包管理器
- **JavaScript/TypeScript**（4 个技能）：高级类型、Node.js 模式、测试、现代 ES6+

**基础设施和 DevOps：**

- **Kubernetes**（4 个技能）：清单、Helm 图表、GitOps、安全策略
- **云基础设施**（4 个技能）：Terraform、多云、混合网络、成本优化
- **CI/CD**（4 个技能）：管道设计、GitHub Actions、GitLab CI、密钥管理

**开发和架构：**

- **后端**（3 个技能）：API 设计、架构模式、微服务
- **LLM 应用**（8 个技能）：LangGraph、提示工程、RAG、评估、嵌入、相似性搜索、向量调优、混合搜索

**区块链和 Web3**（4 个技能）：DeFi 协议、NFT 标准、Solidity 安全、Web3 测试

**项目管理：**

- **Conductor**（3 个技能）：上下文驱动开发、轨道管理、工作流模式

**以及更多**：框架迁移、可观察性、支付处理、ML 运营、安全扫描

[→ 查看完整的技能文档](docs/agent-skills.md)

### 三层模型策略

为最佳性能和成本进行的战略模型分配：

| 层级       | 模型    | 代理 | 用例                                                                                        |
| ---------- | -------- | ------ | ----------------------------------------------------------------------------------------------- |
| **第 1 层** | Opus 4.5 | 42     | 关键架构、安全、所有代码审查、生产编码（语言专家、框架） |
| **第 2 层** | 继承  | 42     | 复杂任务 - 用户选择模型（AI/ML、后端、前端/移动、专业化）               |
| **第 3 层** | Sonnet   | 51     | 智能支持（文档、测试、调试、网络、API 文档、DX、遗留、支付）   |
| **第 4 层** | Haiku    | 18     | 快速运营任务（SEO、部署、简单文档、销售、内容、搜索）                   |

**为什么关键代理使用 Opus 4.5？**

- SWE-bench 上 80.9% 的分数（业界领先）
- 复杂任务减少 65% 的 token
- 最适合架构决策和安全审计

**第 2 层灵活性（`inherit`）：**
标记为 `inherit` 的代理使用您会话的默认模型，让您平衡成本和性能：

- 通过 `claude --model opus` 或 `claude --model sonnet` 启动会话时设置
- 如果未指定默认值，则回退到 Sonnet 4.5
- 非常适合希望控制成本的前端/移动开发者
- AI/ML 工程师可以为复杂的模型工作选择 Opus

**成本考虑：**

- **Opus 4.5**：每百万输入/输出 token $5/$25 - 关键工作的 premium
- **Sonnet 4.5**：每百万 token $3/$15 - 平衡的性能/成本
- **Haiku 4.5**：每百万 token $1/$5 - 快速、经济高效的运营
- Opus 在复杂任务上减少 65% 的 token 通常可以抵消更高的费率
- 使用 `inherit` 层来控制大批量使用情况的成本

编排模式组合模型以提高效率：

```
Opus (架构) → Sonnet (开发) → Haiku (部署)
```

[→ 查看模型配置详细信息](docs/agents.md#model-configuration)

## 流行的用例

### 全栈功能开发

```bash
/full-stack-orchestration:full-stack-feature "使用 OAuth2 的用户身份验证"
```

协调 7+ 个代理：backend-architect → database-architect → frontend-developer → test-automator → security-auditor → deployment-engineer → observability-engineer

[→ 查看所有工作流示例](docs/usage.md#multi-agent-workflow-examples)

### 安全加固

```bash
/security-scanning:security-hardening --level comprehensive
```

多代理安全评估，包括 SAST、依赖扫描和代码审查。

### 使用现代工具的 Python 开发

```bash
/python-development:python-scaffold fastapi-microservice
```

创建具有异步模式的生产就绪 FastAPI 项目，激活技能：

- `async-python-patterns` - AsyncIO 和并发
- `python-testing-patterns` - pytest 和 fixtures
- `uv-package-manager` - 快速依赖管理

### Kubernetes 部署

```bash
# 自动激活 k8s 技能
"使用 Helm 图表和 GitOps 创建生产 Kubernetes 部署"
```

使用 kubernetes-architect 代理和 4 个专业技能生成生产级配置。

[→ 查看完整的使用指南](docs/usage.md)

## 插件类别

**23 个类别，72 个插件：**

- 🎨 **开发**（4）- 调试、后端、前端、多平台
- 📚 **文档**（3）- 代码文档、API 规范、图表、C4 架构
- 🔄 **工作流**（4）- git、全栈、TDD、**Conductor**（上下文驱动开发）
- ✅ **测试**（2）- 单元测试、TDD 工作流
- 🔍 **质量**（3）- 代码审查、综合审查、性能
- 🤖 **AI 和 ML**（4）- LLM 应用、代理编排、上下文、MLOps
- 📊 **数据**（2）- 数据工程、数据验证
- 🗄️ **数据库**（2）- 数据库设计、迁移
- 🚨 **运维**（4）- 事件响应、诊断、分布式调试、可观察性
- ⚡ **性能**（2）- 应用性能、数据库/云优化
- ☁️ **基础设施**（5）- 部署、验证、Kubernetes、云、CI/CD
- 🔒 **安全**（4）- 扫描、合规、后端/API、前端/移动
- 💻 **语言**（7）- Python、JS/TS、系统、JVM、脚本、函数式、嵌入式
- 🔗 **区块链**（1）- 智能合约、DeFi、Web3
- 💰 **金融**（1）- 量化交易、风险管理
- 💳 **支付**（1）- Stripe、PayPal、账单
- 🎮 **游戏**（1）- Unity、Minecraft 插件
- 📢 **营销**（4）- SEO 内容、技术 SEO、SEO 分析、内容营销
- 💼 **业务**（3）- 分析、HR/法律、客户/销售
- 以及更多...

[→ 查看完整的插件目录](docs/plugins.md)

## 架构亮点

### 细粒度设计

- **单一职责** - 每个插件做好一件事
- **最小 token 使用** - 平均每个插件 3.4 个组件
- **可组合** - 混合搭配用于复杂的工作流
- **100% 覆盖** - 所有 108 个代理都可跨插件访问

### 渐进式披露（技能）

token 效率的三层架构：

1. **元数据** - 名称和激活标准（始终加载）
2. **指令** - 核心指导（激活时加载）
3. **资源** - 示例和模板（按需加载）

### 仓库结构

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # 72 个插件
├── plugins/
│   ├── python-development/
│   │   ├── agents/               # 3 个 Python 专家
│   │   ├── commands/             # 脚手架工具
│   │   └── skills/               # 5 个专业技能
│   ├── kubernetes-operations/
│   │   ├── agents/               # K8s 架构师
│   │   ├── commands/             # 部署工具
│   │   └── skills/               # 4 个 K8s 技能
│   └── ... (65 个更多插件)
├── docs/                          # 全面的文档
└── README.md                      # 此文件
```

[→ 查看架构详细信息](docs/architecture.md)

## 贡献

要添加新的代理、技能或命令：

1. 在 `plugins/` 中识别或创建适当的插件目录
2. 在适当的子目录中创建 `.md` 文件：
   - `agents/` - 用于专业代理
   - `commands/` - 用于工具和工作流
   - `skills/` - 用于模块化知识包
3. 遵循命名约定（小写、连字符分隔）
4. 编写清晰的激活标准和全面的内容
5. 更新 `.claude-plugin/marketplace.json` 中的插件定义

有关详细指南，请参阅[架构文档](docs/architecture.md)。

## 资源

### 文档

- [Claude Code 文档](https://docs.claude.com/en/docs/claude-code/overview)
- [插件指南](https://docs.claude.com/en/docs/claude-code/plugins)
- [子代理指南](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [代理技能指南](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [斜杠命令参考](https://docs.claude.com/en/docs/claude-code/slash-commands)

### 此仓库

- [插件参考](docs/plugins.md)
- [代理参考](docs/agents.md)
- [代理技能指南](docs/agent-skills.md)
- [使用指南](docs/usage.md)
- [架构](docs/architecture.md)

## 许可证

MIT 许可证 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=wshobson/agents&type=date&legend=top-left)](https://www.star-history.com/#wshobson/agents&type=date&legend=top-left)
