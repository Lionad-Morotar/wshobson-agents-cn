# 多智能体编排的智能问题解决

[扩展思考：此工作流程实现了一个复杂的调试和解决流水线，利用 AI 辅助的调试工具和可观测性平台来系统地诊断和解决生产问题。智能调试策略将自动化根因分析与人类专业知识相结合，使用 2024/2025 年的现代实践，包括 AI 代码助手（GitHub Copilot、Claude Code）、可观测性平台（Sentry、DataDog、OpenTelemetry）、用于回归跟踪的 git bisect 自动化，以及分布式追踪和结构化日志记录等生产安全调试技术。该流程遵循严格的四阶段方法：(1) 问题分析阶段 - error-detective 和 debugger 智能体分析错误追踪、日志、复现步骤和可观测性数据，以了解故障的完整上下文，包括上游/下游影响，(2) 根因调查阶段 - debugger 和 code-reviewer 智能体执行深度代码分析、自动化 git bisect 以识别引入提交、依赖兼容性检查和状态检查以隔离确切的故障机制，(3) 修复实施阶段 - 领域特定智能体（python-pro、typescript-pro、rust-expert 等）实施最小修复，包括单元、集成和边缘情况测试的全面测试覆盖，同时遵循生产安全实践，(4) 验证阶段 - test-automator 和 performance-engineer 智能体运行回归套件、性能基准测试、安全扫描，并验证没有引入新问题。跨越多个系统的复杂问题需要在专家智能体之间进行编排协调（database-optimizer → performance-engineer → devops-troubleshooter），并明确传递上下文和共享状态。该工作流程强调理解根本原因而非治疗症状、实施持久的架构改进、通过增强的监控和警报自动化检测，以及通过类型系统和静态分析防止未来发生。]

## 阶段 1：问题分析 - 错误检测和上下文收集

使用 Task 工具，首先使用 subagent_type="error-debugging::error-detective"，然后使用 subagent_type="error-debugging::debugger"：

**首先：错误侦探分析**

**提示词：**

```
分析以下内容的错误追踪、日志和可观测性数据：$ARGUMENTS

交付成果：
1. 错误签名分析：异常类型、消息模式、频率、首次出现
2. 堆栈追踪深入分析：故障位置、调用链、涉及的组件
3. 复现步骤：最小测试用例、环境要求、所需数据固件
4. 可观测性上下文：
   - Sentry/DataDog 错误组和趋势
   - 显示请求流的分布式追踪（OpenTelemetry/Jaeger）
   - 结构化日志（带关联 ID 的 JSON 日志）
   - APM 指标：延迟峰值、错误率、资源使用情况
5. 用户影响评估：受影响的用户细分、错误率、业务指标影响
6. 时间线分析：何时开始、与部署/配置更改的相关性
7. 相关症状：类似错误、级联故障、上游/下游影响

使用的现代调试技术：
- AI 辅助日志分析（模式检测、异常识别）
- 跨微服务的分布式追踪关联
- 生产安全调试（无代码更改，使用可观测性数据）
- 用于去重和跟踪的错误指纹识别
```

**预期输出：**

```
ERROR_SIGNATURE: {异常类型 + 关键消息模式}
FREQUENCY: {计数、速率、趋势}
FIRST_SEEN: {时间戳或 git 提交}
STACK_TRACE: {突出显示关键帧的格式化追踪}
REPRODUCTION: {最小步骤 + 示例数据}
OBSERVABILITY_LINKS: [Sentry URL、DataDog 仪表板、追踪 ID]
USER_IMPACT: {受影响用户、严重程度、业务影响}
TIMELINE: {开始时间、与更改的相关性}
RELATED_ISSUES: [类似错误、级联故障]
```

**其次：调试器根因识别**

**提示词：**

```
使用错误侦探的输出执行根因调查：

来自错误侦探的上下文：
- 错误签名：{ERROR_SIGNATURE}
- 堆栈追踪：{STACK_TRACE}
- 复现：{REPRODUCTION}
- 可观测性：{OBSERVABILITY_LINKS}

交付成果：
1. 带有支持证据的根因假设
2. 代码级分析：变量状态、控制流、时序问题
3. Git bisect 分析：识别引入提交（使用 git bisect run 自动化）
4. 依赖分析：版本冲突、API 更改、配置漂移
5. 状态检查：数据库状态、缓存状态、外部 API 响应
6. 故障机制：为什么代码在这些特定条件下失败
7. 带有权衡的修复策略选项（快速修复 vs 正确修复）

下一阶段所需的上下文：
- 需要更改的确切文件路径和行号
- 受影响的数据结构或 API 契约
- 可能需要更新的依赖项
- 用于验证修复的测试场景
- 要维持的性能特征
```

**预期输出：**

```
ROOT_CAUSE: {带有证据的技术解释}
INTRODUCING_COMMIT: {git SHA + 通过 bisect 找到的摘要（如有）}
AFFECTED_FILES: [带有特定行号的文件路径]
FAILURE_MECHANISM: {失败原因 - 竞态条件、空检查、类型不匹配等}
DEPENDENCIES: [相关系统、库、外部 API]
FIX_STRATEGY: {带有推理的推荐方法}
QUICK_FIX_OPTION: {临时缓解措施（如适用）}
PROPER_FIX_OPTION: {长期解决方案}
TESTING_REQUIREMENTS: [必须覆盖的场景]
```

## 阶段 2：根因调查 - 深度代码分析

使用 Task 工具，配合 subagent_type="error-debugging::debugger" 和 subagent_type="comprehensive-review::code-reviewer" 进行系统调查：

**首先：调试器代码分析**

**提示词：**

````
执行深度代码分析和 bisect 调查：

来自阶段 1 的上下文：
- 根因：{ROOT_CAUSE}
- 受影响的文件：{AFFECTED_FILES}
- 故障机制：{FAILURE_MECHANISM}
- 引入提交：{INTRODUCING_COMMIT}

交付成果：
1. 代码路径分析：从入口点到失败的执行跟踪
2. 变量状态跟踪：关键决策点的值
3. 控制流分析：采取的分支、循环、异步操作
4. Git bisect 自动化：创建 bisect 脚本以识别确切的破坏性提交
   ```bash
   git bisect start HEAD v1.2.3
   git bisect run ./test_reproduction.sh
   ````

5. 依赖兼容性矩阵：工作/失败的版本组合
6. 配置分析：环境变量、功能标志、部署配置
7. 时序和竞态条件分析：异步操作、事件排序、锁
8. 内存和资源分析：泄漏、耗尽、争用

现代调查技术：

- AI 辅助代码解释（Claude/Copilot 理解复杂逻辑）
- 使用复现测试的自动化 git bisect
- 依赖关系图分析（npm ls、go mod graph、pip show）
- 配置漂移检测（比较 staging 与 production）
- 使用生产追踪的时间旅行调试

```

**预期输出：**

```

CODE_PATH: {带有关键变量的入口 → ... → 故障位置}
STATE_AT_FAILURE: {变量值、对象状态、数据库状态}
BISECT_RESULT: {引入 bug 的确切提交 + diff}
DEPENDENCY_ISSUES: [版本冲突、破坏性更改、CVE]
CONFIGURATION_DRIFT: {环境之间的差异}
RACE_CONDITIONS: {异步问题、事件排序问题}
ISOLATION_VERIFICATION: {确认单一根因 vs 多个问题}

```

**其次：代码审查员深入分析**

**提示词：**
```

审查代码逻辑并识别设计问题：

来自调试器的上下文：

- 代码路径：{CODE_PATH}
- 失败时的状态：{STATE_AT_FAILURE}
- Bisect 结果：{BISECT_RESULT}

交付成果：

1. 逻辑缺陷分析：错误假设、缺失的边缘情况、错误算法
2. 类型安全差距：更强的类型可以在哪里防止问题
3. 错误处理审查：缺失的 try-catch、未处理的 promise、panic 场景
4. 契约验证：输入验证差距、未满足的输出保证
5. 架构问题：紧耦合、缺失的抽象、层违规
6. 类似模式：具有相同漏洞的其他代码位置
7. 修复设计：最小更改 vs 重构 vs 架构改进

审查清单：

- 是否正确处理了 null/undefined 值？
- 异步操作是否正确等待/链接？
- 错误情况是否显式处理？
- 类型断言是否安全？
- 是否尊重 API 契约？
- 副作用是否隔离？

```

**预期输出：**

```

LOGIC_FLAWS: [具体的错误假设或算法]
TYPE_SAFETY_GAPS: [类型可以防止问题的地方]
ERROR_HANDLING_GAPS: [未处理的错误路径]
SIMILAR_VULNERABILITIES: [具有相同模式的其他代码]
FIX_DESIGN: {最小更改方法}
REFACTORING_OPPORTUNITIES: {如果需要更大的改进}
ARCHITECTURAL_CONCERNS: {如果存在系统性问题}

```

## 阶段 3：修复实施 - 领域特定智能体执行

基于阶段 2 的输出，使用 Task 工具路由到相应的领域智能体：

**路由逻辑：**
- Python 问题 → subagent_type="python-development::python-pro"
- TypeScript/JavaScript → subagent_type="javascript-typescript::typescript-pro"
- Go → subagent_type="systems-programming::golang-pro"
- Rust → subagent_type="systems-programming::rust-pro"
- SQL/数据库 → subagent_type="database-cloud-optimization::database-optimizer"
- 性能 → subagent_type="application-performance::performance-engineer"
- 安全 → subagent_type="security-scanning::security-auditor"

**提示词模板（针对语言调整）：**
```

实施具有全面测试覆盖的生产安全修复：

来自阶段 2 的上下文：

- 根因：{ROOT_CAUSE}
- 逻辑缺陷：{LOGIC_FLAWS}
- 修复设计：{FIX_DESIGN}
- 类型安全差距：{TYPE_SAFETY_GAPS}
- 类似漏洞：{SIMILAR_VULNERABILITIES}

交付成果：

1. 解决根因（而非症状）的最小修复实施
2. 单元测试：
   - 特定失败案例复现
   - 边缘情况（边界值、null/空、溢出）
   - 错误路径覆盖
3. 集成测试：
   - 具有真实依赖项的端到端场景
   - 适当的外部 API 模拟
   - 数据库状态验证
4. 回归测试：
   - 类似漏洞的测试
   - 覆盖相关代码路径的测试
5. 性能验证：
   - 显示无下降的基准测试
   - 负载测试（如适用）
6. 生产安全实践：
   - 用于逐步推出的功能标志
   - 修复失败时的优雅降级
   - 用于修复验证的监控挂钩
   - 用于调试的结构化日志记录

现代实施技术（2024/2025）：

- AI 结对编程（GitHub Copilot、Claude Code）用于测试生成
- 类型驱动开发（利用 TypeScript、mypy、clippy）
- 契约优先的 API（OpenAPI、gRPC 架构）
- 可观测性优先（结构化日志、指标、追踪）
- 防御性编程（显式错误处理、验证）

实施要求：

- 遵循现有的代码模式和约定
- 添加战略性调试日志记录（JSON 结构化日志）
- 包含全面的类型注解
- 更新错误消息以使其可操作（包括上下文、建议）
- 维持向后兼容性（如果破坏性更改，则对 API 进行版本控制）
- 添加 OpenTelemetry 跨度用于分布式追踪
- 包含用于监控的指标计数器（成功率/失败率）

```

**预期输出：**

```

FIX_SUMMARY: {更改了什么以及为什么 - 根因 vs 症状}
CHANGED_FILES: [
{path: "..."，changes: "..."，reasoning: "..."}
]
NEW_FILES: [{path: "..."，purpose: "..."}]
TEST_COVERAGE: {
unit: "X 个场景",
integration: "Y 个场景",
edge_cases: "Z 个场景",
regression: "W 个场景"
}
TEST_RESULTS: {all_passed: true/false，details: "..."}
BREAKING_CHANGES: {none | 带有迁移路径的 API 更改}
OBSERVABILITY_ADDITIONS: [
{type: "log"，location: "..."，purpose: "..."}，
{type: "metric"，name: "..."，purpose: "..."}，
{type: "trace"，span: "..."，purpose: "..."}
]
FEATURE_FLAGS: [{flag: "..."，rollout_strategy: "..."}]
BACKWARD_COMPATIBILITY: {maintained | 带有缓解措施的破坏性更改}

```

## 阶段 4：验证 - 自动化测试和性能验证

使用 Task 工具，配合 subagent_type="unit-testing::test-automator" 和 subagent_type="application-performance::performance-engineer"：

**首先：测试自动化器回归套件**

**提示词：**
```

运行全面的回归测试并验证修复质量：

来自阶段 3 的上下文：

- 修复摘要：{FIX_SUMMARY}
- 更改的文件：{CHANGED_FILES}
- 测试覆盖：{TEST_COVERAGE}
- 测试结果：{TEST_RESULTS}

交付成果：

1. 完整测试套件执行：
   - 单元测试（所有现有 + 新增）
   - 集成测试
   - 端到端测试
   - 契约测试（如果是微服务）
2. 回归检测：
   - 比较修复前后的测试结果
   - 识别任何新失败
   - 验证所有边缘情况都已覆盖
3. 测试质量评估：
   - 代码覆盖率指标（行、分支、条件）
   - 变异测试（如适用）
   - 测试确定性（多次运行）
4. 跨环境测试：
   - 在 staging/QA 环境中测试
   - 使用类生产数据量进行测试
   - 在现实网络条件下测试
5. 安全测试：
   - 身份验证/授权检查
   - 输入验证测试
   - SQL 注入、XSS 防护
   - 依赖漏洞扫描
6. 自动化回归测试生成：
   - 使用 AI 生成额外的边缘情况测试
   - 复杂逻辑的基于属性的测试
   - 输入验证的模糊测试

现代测试实践（2024/2025）：

- AI 生成的测试用例（GitHub Copilot、Claude Code）
- UI/API 契约的快照测试
- 前端的视觉回归测试
- 韧性测试的混沌工程
- 负载测试的生产流量回放

```

**预期输出：**

```

TEST_RESULTS: {
total: N，
passed: X，
failed: Y，
skipped: Z，
new_failures: [列表（如有）]，
flaky_tests: [列表（如有）]
}
CODE_COVERAGE: {
line: "X%"，
branch: "Y%"，
function: "Z%"，
delta: "+/-W%"
}
REGRESSION_DETECTED: {yes/no + 详细信息（如有）}
CROSS_ENV_RESULTS: {staging: "..."，qa: "..."}
SECURITY_SCAN: {
vulnerabilities: [列表或 "none"]，
static_analysis: "..."，
dependency_audit: "..."
}
TEST_QUALITY: {deterministic: true/false，coverage_adequate: true/false}

```

**其次：性能工程师验证**

**提示词：**
```

测量性能影响并验证无回归：

来自测试自动化器的上下文：

- 测试结果：{TEST_RESULTS}
- 代码覆盖率：{CODE_COVERAGE}
- 修复摘要：{FIX_SUMMARY}

交付成果：

1. 性能基准测试：
   - 响应时间（p50、p95、p99）
   - 吞吐量（请求/秒）
   - 资源利用率（CPU、内存、I/O）
   - 数据库查询性能
2. 与基线比较：
   - 修复前后的指标
   - 可接受的下降阈值
   - 性能改进机会
3. 负载测试：
   - 峰值负载下的压力测试
   - 内存泄漏的浸泡测试
   - 突发处理的峰值测试
4. APM 分析：
   - 分布式追踪分析
   - 慢查询检测
   - N+1 查询模式
5. 资源分析：
   - CPU 火焰图
   - 内存分配跟踪
   - Goroutine/线程泄漏
6. 生产就绪性：
   - 容量规划影响
   - 扩展特征
   - 成本影响（云资源）

现代性能实践：

- OpenTelemetry 检测
- 持续分析（Pyroscope、pprof）
- 真实用户监控（RUM）
- 综合监控

```

**预期输出：**

```

PERFORMANCE_BASELINE: {
response_time_p95: "Xms"，
throughput: "Y req/s"，
cpu_usage: "Z%"，
memory_usage: "W MB"
}
PERFORMANCE_AFTER_FIX: {
response_time_p95: "Xms (delta)"，
throughput: "Y req/s (delta)"，
cpu_usage: "Z% (delta)"，
memory_usage: "W MB (delta)"
}
PERFORMANCE_IMPACT: {
verdict: "improved|neutral|degraded"，
acceptable: true/false，
reasoning: "..."
}
LOAD_TEST_RESULTS: {
max_throughput: "..."，
breaking_point: "..."，
memory_leaks: "none|detected"
}
APM_INSIGHTS: [慢查询、N+1 模式、瓶颈]
PRODUCTION_READY: {yes/no + 阻塞因素（如有）}

```

**第三：代码审查员最终批准**

**提示词：**
```

执行最终代码审查并批准部署：

来自测试的上下文：

- 测试结果：{TEST_RESULTS}
- 检测到回归：{REGRESSION_DETECTED}
- 性能影响：{PERFORMANCE_IMPACT}
- 安全扫描：{SECURITY_SCAN}

交付成果：

1. 代码质量审查：
   - 遵循项目约定
   - 无代码异味或反模式
   - 正确的错误处理
   - 充分的日志记录和可观测性
2. 架构审查：
   - 维持系统边界
   - 未引入紧耦合
   - 可扩展性考虑
3. 安全审查：
   - 无安全漏洞
   - 正确的输入验证
   - 身份验证/授权正确
4. 文档审查：
   - 需要的地方有代码注释
   - API 文档已更新
   - 如果有运营影响，运行手册已更新
5. 部署就绪性：
   - 回滚计划已记录
   - 功能标志策略已定义
   - 监控/警报已配置
6. 风险评估：
   - 爆炸半径估算
   - 推出策略建议
   - 成功指标已定义

审查清单：

- 所有测试通过
- 无性能回归
- 已解决安全漏洞
- 破坏性更改已记录
- 维持向后兼容性
- 可观测性充分
- 部署计划清晰

```

**预期输出：**

```

REVIEW_STATUS: {APPROVED|NEEDS_REVISION|BLOCKED}
CODE_QUALITY: {分数/评估}
ARCHITECTURE_CONCERNS: [列表或 "none"]
SECURITY_CONCERNS: [列表或 "none"]
DEPLOYMENT_RISK: {low|medium|high}
ROLLBACK_PLAN: {
steps: ["..."]，
estimated_time: "X 分钟"，
data_recovery: "..."
}
ROLLOUT_STRATEGY: {
approach: "canary|blue-green|rolling|big-bang"，
phases: ["..."]，
success_metrics: ["..."]，
abort_criteria: ["..."]
}
MONITORING_REQUIREMENTS: [
{metric: "..."，threshold: "..."，action: "..."}
]
FINAL_VERDICT: {
approved: true/false，
blockers: [列表（如未批准）]，
recommendations: ["..."]
}

```

## 阶段 5：文档和预防 - 长期韧性

使用 Task 工具，配合 subagent_type="comprehensive-review::code-reviewer" 进行预防策略：

**提示词：**
```

记录修复并实施预防策略以避免复发：

来自阶段 4 的上下文：

- 最终裁决：{FINAL_VERDICT}
- 审查状态：{REVIEW_STATUS}
- 根因：{ROOT_CAUSE}
- 回滚计划：{ROLLBACK_PLAN}
- 监控要求：{MONITORING_REQUIREMENTS}

交付成果：

1. 代码文档：
   - 非显而易见逻辑的内联注释（最少）
   - 函数/类文档更新
   - API 契约文档
2. 运营文档：
   - 带有修复描述和版本的 CHANGELOG 条目
   - 利益相关者的发布说明
   - 值班工程师的运行手册条目
   - 事后分析文档（如果是高严重性事件）
3. 通过静态分析预防：
   - 添加 linting 规则（eslint、ruff、golangci-lint）
   - 配置更严格的编译器/类型检查器设置
   - 为域特定模式添加自定义 lint 规则
   - 更新预提交挂钩
4. 类型系统增强：
   - 添加完备性检查
   - 使用可区分联合/求和类型
   - 添加 const/readonly 修饰符
   - 利用品牌类型进行验证
5. 监控和警报：
   - 创建错误率警报（Sentry、DataDog）
   - 为业务逻辑添加自定义指标
   - 设置综合监视器（Pingdom、Checkly）
   - 配置 SLO/SLI 仪表板
6. 架构改进：
   - 识别类似的漏洞模式
   - 提出重构以实现更好的隔离
   - 记录设计决策
   - 更新架构图（如需要）
7. 测试改进：
   - 添加基于属性的测试
   - 扩展集成测试场景
   - 添加混沌工程测试
   - 记录测试策略差距

现代预防实践（2024/2025）：

- AI 辅助代码审查规则（GitHub Copilot、Claude Code）
- 持续安全扫描（Snyk、Dependabot）
- 基础设施即代码验证（Terraform validate、CloudFormation Linter）
- API 的契约测试（Pact、OpenAPI 验证）
- 可观测性驱动开发（在部署前进行检测）

```

**预期输出：**

```

DOCUMENTATION_UPDATES: [
{file: "CHANGELOG.md"，summary: "..."}，
{file: "docs/runbook.md"，summary: "..."}，
{file: "docs/architecture.md"，summary: "..."}
]
PREVENTION_MEASURES: {
static_analysis: [
{tool: "eslint"，rule: "..."，reason: "..."}，
{tool: "ruff"，rule: "..."，reason: "..."}
]，
type_system: [
{enhancement: "..."，location: "..."，benefit: "..."}
]，
pre_commit_hooks: [
{hook: "..."，purpose: "..."}
]
}
MONITORING_ADDED: {
alerts: [
{name: "..."，threshold: "..."，channel: "..."}
]，
dashboards: [
{name: "..."，metrics: [...]，url: "..."}
]，
slos: [
{service: "..."，sli: "..."，target: "..."，window: "..."}
]
}
ARCHITECTURAL_IMPROVEMENTS: [
{improvement: "..."，reasoning: "..."，effort: "small|medium|large"}
]
SIMILAR_VULNERABILITIES: {
found: N，
locations: [...]，
remediation_plan: "..."
}
FOLLOW_UP_TASKS: [
{task: "..."，priority: "high|medium|low"，owner: "..."}
]
POSTMORTEM: {
created: true/false，
location: "..."，
incident_severity: "SEV1|SEV2|SEV3|SEV4"
}
KNOWLEDGE_BASE_UPDATES: [
{article: "..."，summary: "..."}
]

```

## 复杂问题的多域协调

对于跨越多个域的问题，使用显式上下文传递按顺序编排专家智能体：

**示例 1：导致应用程序超时的数据库性能问题**

**序列：**
1. **阶段 1-2**：error-detective + debugger 识别慢数据库查询
2. **阶段 3a**：Task(subagent_type="database-cloud-optimization::database-optimizer")
   - 使用适当的索引优化查询
   - 上下文："查询执行耗时 5 秒，user_id 列缺少索引，检测到 N+1 查询模式"
3. **阶段 3b**：Task(subagent_type="application-performance::performance-engineer")
   - 为频繁访问的数据添加缓存层
   - 上下文："通过在 user_id 列上添加索引，数据库查询从 5 秒优化到 50 毫秒。由于 N+1 查询模式，每个请求加载 100+ 用户记录，应用程序仍经历 2 秒响应时间。为用户配置文件添加 TTL 为 5 分钟的 Redis 缓存。"
4. **阶段 3c**：Task(subagent_type="incident-response::devops-troubleshooter")
   - 配置查询性能和缓存命中率监控
   - 上下文："已使用 Redis 添加缓存层。需要监控：查询 p95 延迟（阈值：100ms）、缓存命中率（阈值：>80%）、缓存内存使用率（警报 80%）。"

**示例 2：生产环境中的前端 JavaScript 错误**

**序列：**
1. **阶段 1**：error-detective 分析 Sentry 错误报告
   - 上下文："TypeError: Cannot read property 'map' of undefined，过去一小时内发生 500+ 次，影响 iOS 14 上的 Safari 用户"
2. **阶段 2**：debugger + code-reviewer 调查
   - 上下文："当没有结果时，API 响应有时返回 null 而不是空数组。前端假定是数组。"
3. **阶段 3a**：Task(subagent_type="javascript-typescript::typescript-pro")
   - 使用正确的空检查修复前端
   - 添加类型保护
   - 上下文："当没有结果时，后端 API /api/users 端点返回 null 而不是 []。修复前端以处理两种情况。添加 TypeScript 严格空检查。"
4. **阶段 3b**：Task(subagent_type="backend-development::backend-architect")
   - 修复后端以始终返回数组
   - 更新 API 契约
   - 上下文："前端现在处理 null，但 API 应遵循契约并返回 [] 而不是 null。更新 OpenAPI 规范以记录此内容。"
5. **阶段 4**：test-automator 运行跨浏览器测试
6. **阶段 5**：code-reviewer 记录 API 契约更改

**示例 3：身份验证中的安全漏洞**

**序列：**
1. **阶段 1**：error-detective 审查安全扫描报告
   - 上下文："登录端点中的 SQL 注入漏洞，Snyk 严重性：HIGH"
2. **阶段 2**：debugger + security-auditor 调查
   - 上下文："用户输入在 SQL WHERE 子句中未清理，允许身份验证绕过"
3. **阶段 3**：Task(subagent_type="security-scanning::security-auditor")
   - 实施参数化查询
   - 添加输入验证
   - 添加速率限制
   - 上下文："用准备好的语句替换字符串连接。添加电子邮件格式的输入验证。实施速率限制（15 分钟内 5 次尝试）。"
4. **阶段 4a**：test-automator 添加安全测试
   - SQL 注入尝试
   - 暴力破解场景
5. **阶段 4b**：security-auditor 执行渗透测试
6. **阶段 5**：code-reviewer 记录安全改进并创建事后分析

**上下文传递模板：**
```

{next_agent} 的上下文：

由 {previous_agent} 完成：

- {summary_of_work}
- {key_findings}
- {changes_made}

剩余工作：

- {specific_tasks_for_next_agent}
- {files_to_modify}
- {constraints_to_follow}

依赖关系：

- {systems_or_components_affected}
- {data_needed}
- {integration_points}

成功标准：

- {measurable_outcomes}
- {verification_steps}

```

## 配置选项

通过在调用时设置优先级来自定义工作流程行为：

**VERIFICATION_LEVEL**：控制测试和验证的深度
- **minimal**：快速修复和基本测试，跳过性能基准测试
  - 用于：低风险 bug、外观问题、文档修复
  - 阶段：1-2-3（跳过详细的阶段 4）
  - 时间线：约 30 分钟
- **standard**：全面测试覆盖 + 代码审查（默认）
  - 用于：大多数生产 bug、功能问题、数据 bug
  - 阶段：1-2-3-4（所有验证）
  - 时间线：约 2-4 小时
- **comprehensive**：标准 + 安全审计 + 性能基准测试 + 混沌测试
  - 用于：安全问题、性能问题、数据损坏、高流量系统
  - 阶段：1-2-3-4-5（包括长期预防）
  - 时间线：约 1-2 天

**PREVENTION_FOCUS**：控制未来预防的投资
- **none**：仅修复，无预防工作
  - 用于：一次性问题、即将弃用的遗留代码、外部库 bug
  - 输出：仅代码修复 + 测试
- **immediate**：添加测试和基本 linting（默认）
  - 用于：常见 bug、重复模式、团队代码库
  - 输出：修复 + 测试 + linting 规则 + 最少监控
- **comprehensive**：全面的预防套件，包括监控、架构改进
  - 用于：高严重性事件、系统性问题、架构问题
  - 输出：修复 + 测试 + linting + 监控 + 架构文档 + 事后分析

**ROLLOUT_STRATEGY**：控制部署方法
- **immediate**：直接部署到生产环境（用于热修复、低风险更改）
- **canary**：逐步推出到部分流量（中等风险的默认值）
- **blue-green**：完全环境切换，具有即时回滚能力
- **feature-flag**：部署代码但通过功能标志控制激活（高风险更改）

**OBSERVABILITY_LEVEL**：控制检测深度
- **minimal**：仅基本错误日志记录
- **standard**：结构化日志 + 关键指标（默认）
- **comprehensive**：完全分布式追踪 + 自定义仪表板 + SLO

**示例调用：**
```

问题：用户在结账页面遇到超时错误（500+ 错误/小时）

配置：

- VERIFICATION_LEVEL: comprehensive（影响收入）
- PREVENTION_FOCUS: comprehensive（高业务影响）
- ROLLOUT_STRATEGY: canary（首先在 5% 流量上测试）
- OBSERVABILITY_LEVEL: comprehensive（需要详细监控）

```

## 现代调试工具集成

此工作流程利用 2024/2025 年的现代工具：

**可观测性平台：**
- Sentry（错误跟踪、发布跟踪、性能监控）
- DataDog（APM、日志、追踪、基础设施监控）
- OpenTelemetry（供应商中立的分布式追踪）
- Honeycomb（复杂分布式系统的可观测性）
- New Relic（APM、综合监控）

**AI 辅助调试：**
- GitHub Copilot（代码建议、测试生成、bug 模式识别）
- Claude Code（全面的代码分析、架构审查）
- Sourcegraph Cody（代码库搜索和理解）
- Tabnine（具有 bug 防止功能的代码完成）

**Git 和版本控制：**
- 使用复现脚本的自动化 git bisect
- 用于在 bisect 提交上自动测试的 GitHub Actions
- 用于识别代码所有权的 Git blame 分析
- 用于理解更改的提交消息分析

**测试框架：**
- Jest/Vitest（JavaScript/TypeScript 单元/集成测试）
- pytest（具有固件和参数化的 Python 测试）
- Go testing + testify（Go 单元和表驱动测试）
- Playwright/Cypress（端到端浏览器测试）
- k6/Locust（负载和性能测试）

**静态分析：**
- ESLint/Prettier（JavaScript/TypeScript linting 和格式化）
- Ruff/mypy（Python linting 和类型检查）
- golangci-lint（Go 全面 linting）
- Clippy（Rust linting 和最佳实践）
- SonarQube（企业代码质量和安全）

**性能分析：**
- Chrome DevTools（前端性能）
- pprof（Go 分析）
- py-spy（Python 分析）
- Pyroscope（持续分析）
- CPU/内存分析的火焰图

**安全扫描：**
- Snyk（依赖漏洞扫描）
- Dependabot（自动化依赖更新）
- OWASP ZAP（安全测试）
- Semgrep（自定义安全规则）
- npm audit / pip-audit / cargo audit

## 成功标准

当满足以下所有条件时，修复被视为完成：

**根因理解：**
- 已识别根因并提供支持证据
- 明确记录了故障机制
- 已识别引入提交（如通过 git bisect 适用）
- 已编目类似漏洞

**修复质量：**
- 修复解决根因，而非仅症状
- 最小代码更改（避免过度工程）
- 遵循项目约定和模式
- 未引入代码异味或反模式
- 维持向后兼容性（或记录破坏性更改）

**测试验证：**
- 所有现有测试通过（零回归）
- 新测试覆盖特定的 bug 复现
- 边缘情况和错误路径已测试
- 集成测试验证端到端行为
- 测试覆盖率增加（或维持在高水平）

**性能和安全：**
- 无性能下降（p95 延迟在基线的 5% 以内）
- 未引入安全漏洞
- 资源使用可接受（内存、CPU、I/O）
- 高流量更改的负载测试通过

**部署就绪性：**
- 代码审查由领域专家批准
- 回滚计划已记录并测试
- 功能标志已配置（如适用）
- 监控和警报已配置
- 运行手册已更新故障排除步骤

**预防措施：**
- 已添加静态分析规则（如适用）
- 已实施类型系统改进（如适用）
- 文档已更新（代码、API、运行手册）
- 已创建事后分析（如果是高严重性事件）
- 已创建知识库文章（如果是新问题）

**指标：**
- 平均恢复时间（MTTR）：SEV2+ < 4 小时
- Bug 复发率：0%（相同的根因不应复发）
- 测试覆盖率：无下降，理想情况下增加
- 部署成功率：> 95%（回滚率 < 5%）

要解决的问题：$ARGUMENTS
```
