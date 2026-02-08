# 架构和设计原则

此市场遵循行业最佳实践，重点关注细粒度、可组合性和最小 token 使用。

## 核心理念

### 单一职责原则

- 每个插件都做好**一件事**（Unix 哲学）
- 清晰、专注的目的（可用 5-10 个词描述）
- 平均插件大小：**3.4 个组件**（遵循 Anthropic 的 2-8 模式）
- **零臃肿插件** - 所有插件都专注且有意义

### 可组合性优于捆绑

- 根据需求混合和匹配插件
- 工作流编排器组合专注的插件
- 没有强制功能捆绑
- 插件之间有清晰的边界

### 上下文效率

- 更小的工具 = 更快的处理
- 更好地适应 LLM 上下文窗口
- 更准确、专注的响应
- 只安装您需要的内容

### 可维护性

- 单一用途 = 更容易更新
- 清晰的边界 = 隔离的更改
- 更少的重复 = 更简单的维护
- 隔离的依赖

## 细粒度插件架构

### 插件分布

- **67 个专注的插件**，针对特定用例进行了优化
- **23 个清晰的类别**，每个类别 1-6 个插件，易于发现
- 按领域组织：
  - **开发**：4 个插件（调试、后端、前端、多平台）
  - **安全**：4 个插件（扫描、合规、后端 API、前端/移动）
  - **运维**：4 个插件（事件、诊断、分布式、可观察性）
  - **语言**：7 个插件（Python、JS/TS、系统、JVM、脚本、函数式、嵌入式）
  - **基础设施**：5 个插件（部署、验证、K8s、云、CI/CD）
  - 以及 18 个更多专业类别

### 组件细分

**99 个专业代理**

- 在架构、语言、基础设施、质量、数据/AI、文档、业务和 SEO 方面拥有深厚知识的领域专家
- 使用三层策略（Opus、Sonnet、Haiku）进行模型优化，以提高性能和降低成本

**15 个工作流编排器**

- 多代理协调系统
- 复杂操作，如全栈开发、安全加固、ML 流程、事件响应
- 预配置的代理工作流

**71 个开发工具**

- 优化的实用程序，包括：
  - 项目脚手架（Python、TypeScript、Rust）
  - 安全扫描（SAST、依赖审计、XSS）
  - 测试生成（pytest、Jest）
  - 组件脚手架（React、React Native）
  - 基础设施设置（Terraform、Kubernetes）

**107 个代理技能**

- 模块化知识包
- 渐进式披露架构
- 跨 18 个插件的领域特定专业知识
- 符合规范（Anthropic 代理技能规范）

## 仓库结构

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # 市场目录（67 个插件）
├── plugins/                       # 隔离的插件目录
│   ├── python-development/
│   │   ├── agents/               # Python 语言代理
│   │   │   ├── python-pro.md
│   │   │   ├── django-pro.md
│   │   │   └── fastapi-pro.md
│   │   ├── commands/             # Python 工具
│   │   │   └── python-scaffold.md
│   │   └── skills/               # Python 技能（共 5 个）
│   │       ├── async-python-patterns/
│   │       ├── python-testing-patterns/
│   │       ├── python-packaging/
│   │       ├── python-performance-optimization/
│   │       └── uv-package-manager/
│   ├── backend-development/
│   │   ├── agents/
│   │   │   ├── backend-architect.md
│   │   │   ├── graphql-architect.md
│   │   │   └── tdd-orchestrator.md
│   │   ├── commands/
│   │   │   └── feature-development.md
│   │   └── skills/               # 后端技能（共 3 个）
│   │       ├── api-design-principles/
│   │       ├── architecture-patterns/
│   │       └── microservices-patterns/
│   ├── security-scanning/
│   │   ├── agents/
│   │   │   └── security-auditor.md
│   │   ├── commands/
│   │   │   ├── security-hardening.md
│   │   │   ├── security-sast.md
│   │   │   └── security-dependencies.md
│   │   └── skills/               # 安全技能（共 1 个）
│   │       └── sast-configuration/
│   ├── c4-architecture/
│   │   ├── agents/               # C4 架构代理
│   │   │   ├── c4-code.md
│   │   │   ├── c4-component.md
│   │   │   ├── c4-container.md
│   │   │   └── c4-context.md
│   │   └── commands/
│   │       └── c4-architecture.md
│   └── ... (62 个更多隔离插件)
├── docs/                          # 文档
│   ├── agent-skills.md           # 代理技能指南
│   ├── agents.md                 # 代理参考
│   ├── plugins.md                # 插件目录
│   ├── usage.md                  # 使用指南
│   └── architecture.md           # 此文件
└── README.md                      # 快速开始
```

## 插件结构

每个插件包含：

- **agents/** - 该领域的专业代理（可选）
- **commands/** - 该插件特有的工具和工作流（可选）
- **skills/** - 具有渐进式披露的模块化知识包（可选）

### 最低要求

- 至少一个代理或一个命令
- 清晰、专注的目的
- 所有文件中的正确前置元数据
- marketplace.json 中的条目

### 示例插件

```
plugins/kubernetes-operations/
├── agents/
│   └── kubernetes-architect.md   # K8s 架构和设计
├── commands/
│   └── k8s-deploy.md            # 部署自动化
└── skills/
    ├── k8s-manifest-generator/   # 清单创建技能
    ├── helm-chart-scaffolding/   # Helm 图表技能
    ├── gitops-workflow/          # GitOps 自动化技能
    └── k8s-security-policies/    # 安全策略技能
```

## 代理技能架构

### 渐进式披露

技能使用三层架构来实现 token 效率：

1. **元数据**（前置元数据）：名称和激活标准（始终加载）
2. **指令**：核心指导和模式（激活时加载）
3. **资源**：示例和模板（按需加载）

### 规范合规性

所有技能都遵循[代理技能规范](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)：

```yaml
---
name: skill-name # 必需：连字符大小写
description: 技能的作用。在[触发器]时使用。# 必需：< 1024 个字符
---
# 具有渐进式披露的技能内容
```

### 优势

- **Token 效率**：仅在需要时加载相关知识
- **专业知识**：深厚的领域知识，无臃肿
- **清晰激活**：显式触发器防止意外调用
- **可组合性**：跨工作流混合和匹配技能
- **可维护性**：隔离的更新不影响其他技能

有关 107 个技能的完整详细信息，请参阅[代理技能](./agent-skills.md)。

## 模型配置策略

### 两层架构

系统战略性地使用 Claude Opus 和 Sonnet 模型：

| 模型  | 数量     | 用例                                     |
| ------ | --------- | -------------------------------------------- |
| Opus   | 42 个代理 | 关键架构、安全、代码审查 |
| Sonnet | 39 个代理 | 复杂任务、智能支持     |
| Haiku  | 18 个代理 | 快速运营任务                       |

### 选择标准

**Haiku - 快速执行和确定性任务**

- 根据明确定义的规范生成代码
- 按照既定模式创建测试
- 使用清晰的模板编写文档
- 执行基础设施操作
- 执行数据库查询优化
- 处理客户支持响应
- 处理 SEO 优化任务
- 管理部署管道

**Sonnet - 复杂推理和架构**

- 设计系统架构
- 做出技术选择决策
- 执行安全审计
- 审查架构模式的代码
- 创建复杂的 AI/ML 流程
- 提供特定语言的专业知识
- 编排多代理工作流
- 处理业务关键的法律/HR 事务

### 混合编排

组合模型以实现最佳性能和成本：

```
规划阶段 (Sonnet) → 执行阶段 (Haiku) → 审查阶段 (Sonnet)

示例：
backend-architect (Sonnet) 设计 API
  ↓
Generate endpoints (Haiku) 实现规范
  ↓
test-automator (Haiku) 创建测试
  ↓
code-reviewer (Sonnet) 验证架构
```

## 性能和质量

### 优化的 Token 使用

- **隔离的插件**只加载您需要的内容
- **细粒度架构**减少不必要的上下文
- **渐进式披露**（技能）按需加载知识
- **清晰的边界**防止上下文污染

### 组件覆盖

- **100% 代理覆盖** - 所有插件至少包含一个代理
- **100% 组件可用性** - 所有 99 个代理都可跨插件访问
- **高效分布** - 平均每个插件 3.4 个组件

### 可发现性

- **清晰的插件名称**立即传达目的
- **逻辑分类**，包含 23 个明确定义的类别
- **可搜索的文档**，带有交叉引用
- **易于找到**适合工作的正确工具

## 设计模式

### 模式 1：单一目的插件

每个插件专注于一个领域：

```
python-development/
├── agents/           # Python 语言专家
├── commands/         # Python 项目脚手架
└── skills/           # Python 特定知识
```

**优势：**

- 清晰的职责
- 易于维护
- 最小 token 使用
- 可与其他插件组合

### 模式 2：工作流编排

编排器插件协调多个代理：

```
full-stack-orchestration/
└── commands/
    └── full-stack-feature.md    # 协调 7+ 个代理
```

**编排：**

1. backend-architect（设计 API）
2. database-architect（设计架构）
3. frontend-developer（构建 UI）
4. test-automator（创建测试）
5. security-auditor（安全审查）
6. deployment-engineer（CI/CD）
7. observability-engineer（监控）

### 模式 3：代理 + 技能集成

代理提供推理，技能提供知识：

```
用户："构建具有异步模式的 FastAPI 项目"
  ↓
fastapi-pro 代理（编排）
  ↓
fastapi-templates 技能（提供模式）
  ↓
python-scaffold 命令（生成项目）
```

### 模式 4：多插件组合

复杂工作流使用多个插件：

```
功能开发工作流：
1. backend-development:feature-development
2. security-scanning:security-hardening
3. unit-testing:test-generate
4. code-review-ai:ai-review
5. cicd-automation:workflow-automate
6. observability-monitoring:monitor-setup
```

## 版本控制和更新

### 市场更新

- `.claude-plugin/marketplace.json` 中的市场目录
- 插件的语义版本控制
- 维护向后兼容性
- 针对重大更改的清晰迁移指南

### 插件更新

- 单个插件更新不影响其他插件
- 技能可以独立更新
- 代理可以添加/删除而不会破坏工作流
- 命令保持稳定的接口

## 贡献指南

### 添加插件

1. 创建插件目录：`plugins/{plugin-name}/`
2. 添加代理和/或命令
3. 可选地添加技能
4. 更新 marketplace.json
5. 在适当的类别中记录

### 添加代理

1. 创建 `plugins/{plugin-name}/agents/{agent-name}.md`
2. 添加前置元数据（名称、描述、模型）
3. 编写全面的系统提示
4. 更新插件定义

### 添加技能

1. 创建 `plugins/{plugin-name}/skills/{skill-name}/SKILL.md`
2. 添加 YAML 前置元数据（名称、带有"Use when"的描述）
3. 编写具有渐进式披露的技能内容
4. 添加到 marketplace.json 中插件的技能数组

### 质量标准

- **清晰的命名** - 连字符大小写，描述性
- **专注的范围** - 单一职责
- **完整的文档** - 内容、时间、方式
- **经过测试的功能** - 提交前验证
- **规范合规** - 遵循 Anthropic 指南

## 另请参阅

- [代理技能](./agent-skills.md) - 模块化知识包
- [代理参考](./agents.md) - 完整的代理目录
- [插件参考](./plugins.md) - 所有 67 个插件
- [使用指南](./usage.md) - 命令和工作流
