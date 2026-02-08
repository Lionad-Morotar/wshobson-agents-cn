# 数据驱动功能开发

使用专业的智能体进行分析、实施和实验,通过数据洞察、A/B 测试和持续测量来指导功能构建。

[扩展思考:此工作流协调了一个全面的数据驱动开发流程,从初始数据分析和假设制定,到集成分析、A/B 测试基础设施的功能实现,以及发布后分析。每个阶段都利用专业智能体确保功能基于数据洞察构建,为测量进行适当的仪器化,并通过受控实验进行验证。该工作流程强调现代产品分析实践、测试中的统计严谨性,以及从用户行为中持续学习。]

## 第一阶段:数据分析和假设形成

### 1. 探索性数据分析

- 使用 Task 工具,设置 subagent_type="machine-learning-ops::data-scientist"
- 提示词:"为功能 $ARGUMENTS 执行探索性数据分析。分析现有用户行为数据,识别模式和机会,按行为对用户进行细分,并计算基线指标。使用现代分析工具(Amplitude、Mixpanel、Segment)了解当前用户旅程、转化漏斗和参与模式。"
- 输出:包含可视化的 EDA 报告、用户细分、行为模式、基线指标

### 2. 业务假设开发

- 使用 Task 工具,设置 subagent_type="business-analytics::business-analyst"
- 上下文:数据科学家的 EDA 发现和行为模式
- 提示词:"基于数据分析为功能 $ARGUMENTS 制定业务假设。定义明确的成功指标、对关键业务 KPI 的预期影响、目标用户细分和最小可检测效应。使用 ICE 评分或 RICE 优先级框架创建可测量的假设。"
- 输出:假设文档、成功指标定义、预期 ROI 计算

### 3. 统计实验设计

- 使用 Task 工具,设置 subagent_type="machine-learning-ops::data-scientist"
- 上下文:业务假设和成功指标
- 提示词:"为功能 $ARGUMENTS 设计统计实验。计算统计功效所需的样本量,定义对照组和处理组,指定随机化策略,并规划多重检验校正。考虑贝叶斯 A/B 测试方法以加快决策速度。同时为主要指标和护栏指标进行设计。"
- 输出:实验设计文档、功效分析、统计检验计划

## 第二阶段:功能架构和分析设计

### 4. 功能架构规划

- 使用 Task 工具,设置 subagent_type="data-engineering::backend-architect"
- 上下文:业务需求和实验设计
- 提示词:"为功能 $ARGUMENTS 设计具有 A/B 测试能力的功能架构。包括功能标志集成(LaunchDarkly、Split.io 或 Optimizely)、渐进式发布策略、用于安全的熔断器,以及对照组和处理组逻辑的清晰分离。确保架构支持实时配置更新。"
- 输出:架构图、功能标志架构、发布策略

### 5. 分析仪器化设计

- 使用 Task 工具,设置 subagent_type="data-engineering::data-engineer"
- 上下文:功能架构和成功指标
- 提示词:"为功能 $ARGUMENTS 设计全面的分析仪器化。定义用户交互的事件架构,指定用于细分和分析的属性,设计漏斗跟踪和转化事件,规划队列分析能力。使用现代 SDK(Segment、Amplitude、Mixpanel)并采用正确的事件分类法实施。"
- 输出:事件跟踪计划、分析架构、仪器化指南

### 6. 数据管道架构

- 使用 Task 工具,设置 subagent_type="data-engineering::data-engineer"
- 上下文:分析需求和现有数据基础设施
- 提示词:"为功能 $ARGUMENTS 设计数据管道。包括用于实时指标的流式处理(Kafka、Kinesis)、用于详细分析的批处理、数据仓库集成(Snowflake、BigQuery),以及适用的 ML 特征存储。确保适当的数据治理和 GDPR 合规性。"
- 输出:管道架构、ETL/ELT 规范、数据流图

## 第三阶段:带仪器化的实现

### 7. 后端实现

- 使用 Task 工具,设置 subagent_type="backend-development::backend-architect"
- 上下文:架构设计和功能需求
- 提示词:"为功能 $ARGUMENTS 实现完整的仪器化后端。包括决策点的功能标志检查、所有用户操作的全面事件跟踪、性能指标收集、错误跟踪和监控。为实验分析实施适当的日志记录。"
- 输出:带分析的后端代码、功能标志集成、监控设置

### 8. 前端实现

- 使用 Task 工具,设置 subagent_type="frontend-mobile-development::frontend-developer"
- 上下文:后端 API 和分析需求
- 提示词:"为功能 $ARGUMENTS 构建带分析跟踪的前端。为所有用户交互实施事件跟踪、会话录制集成(如适用)、性能指标(Core Web Vitals)和适当的错误边界。确保对照组和处理组之间的一致体验。"
- 输出:带分析的前端代码、A/B 测试变体、性能监控

### 9. ML 模型集成(如适用)

- 使用 Task 工具,设置 subagent_type="machine-learning-ops::ml-engineer"
- 上下文:功能需求和数据管道
- 提示词:"如需要,为功能 $ARGUMENTS 集成 ML 模型。实施低延迟的在线推理、模型版本之间的 A/B 测试、模型性能跟踪和自动回退机制。设置模型监控以进行漂移检测。"
- 输出:ML 管道、模型服务基础设施、监控设置

## 第四阶段:发布前验证

### 10. 分析验证

- 使用 Task 工具,设置 subagent_type="data-engineering::data-engineer"
- 上下文:已实现的跟踪和事件架构
- 提示词:"验证功能 $ARGUMENTS 的分析实现。在测试环境中测试所有事件跟踪,验证数据质量和完整性,验证漏斗定义,确保适当的用户识别和会话跟踪。对数据管道运行端到端测试。"
- 输出:验证报告、数据质量指标、跟踪覆盖率分析

### 11. 实验设置

- 使用 Task 工具,设置 subagent_type="cloud-infrastructure::deployment-engineer"
- 上下文:功能标志和实验设计
- 提示词:"为功能 $ARGUMENTS 配置实验基础设施。设置具有适当定位规则的功能标志,配置流量分配(从 5-10% 开始),实施终止开关,为关键指标设置监控警报。测试随机化和分配逻辑。"
- 输出:实验配置、监控仪表板、发布计划

## 第五阶段:发布和实验

### 12. 渐进式发布

- 使用 Task 工具,设置 subagent_type="cloud-infrastructure::deployment-engineer"
- 上下文:实验配置和监控设置
- 提示词:"执行功能 $ARGUMENTS 的渐进式发布。从内部内部测试开始,然后是 Beta 用户(1-5%),逐渐增加到目标流量。监控错误率、性能指标和早期指标。在异常时实施自动回滚。"
- 输出:发布执行、监控警报、健康指标

### 13. 实时监控

- 使用 Task 工具,设置 subagent_type="observability-monitoring::observability-engineer"
- 上下文:已部署的功能和成功指标
- 提示词:"为功能 $ARGUMENTS 设置全面监控。创建实验指标的实时仪表板,配置统计显著性警报,监控负面影响的护栏指标,跟踪系统性能和错误率。使用 Datadog、New Relic 或自定义仪表板等工具。"
- 输出:监控仪表板、警报配置、SLO 定义

## 第六阶段:分析和决策制定

### 14. 统计分析

- 使用 Task 工具,设置 subagent_type="machine-learning-ops::data-scientist"
- 上下文:实验数据和原始假设
- 提示词:"分析功能 $ARGUMENTS 的 A/B 测试结果。计算带置信区间的统计显著性,检查细分级别效应,分析次要指标影响,调查任何意外模式。同时使用频率学派和贝叶斯方法。如适用,考虑多重检验。"
- 输出:统计分析报告、显著性检验、细分分析

### 15. 业务影响评估

- 使用 Task 工具,设置 subagent_type="business-analytics::business-analyst"
- 上下文:统计分析和业务指标
- 提示词:"评估功能 $ARGUMENTS 的业务影响。计算实际与预期的 ROI,分析对关键业务指标的影响,评估包含运营开销的成本效益,预测长期价值。对全面发布、迭代或回滚提出建议。"
- 输出:业务影响报告、ROI 分析、建议文档

### 16. 发布后优化

- 使用 Task 工具,设置 subagent_type="machine-learning-ops::data-scientist"
- 上下文:发布结果和用户反馈
- 提示词:"基于数据识别功能 $ARGUMENTS 的优化机会。分析处理组中的用户行为模式,识别用户旅程中的摩擦点,基于数据提出改进建议,规划后续实验。使用队列分析进行长期影响评估。"
- 输出:优化建议、后续实验计划

## 配置选项

```yaml
experiment_config:
  min_sample_size: 10000
  confidence_level: 0.95
  runtime_days: 14
  traffic_allocation: "gradual" # gradual、fixed 或 adaptive

analytics_platforms:
  - amplitude
  - segment
  - mixpanel

feature_flags:
  provider: "launchdarkly" # launchdarkly、split、optimizely、unleash

statistical_methods:
  - frequentist
  - bayesian

monitoring:
  - real_time_metrics: true
  - anomaly_detection: true
  - automatic_rollback: true
```

## 成功标准

- **数据覆盖率**: 100% 的用户交互通过正确的事件架构进行跟踪
- **实验有效性**: 适当的随机化、足够的统计功效、无样本比率不匹配
- **统计严谨性**: 明确的显著性检验、适当的置信区间、多重检验校正
- **业务影响**: 目标指标的可衡量改进,且不降低护栏指标
- **技术性能**: p95 延迟无降低,错误率低于 0.1%
- **决策速度**: 在计划的实验运行时间内做出明确的通过/不通过决策
- **学习成果**: 为未来功能开发记录洞察

## 协作说明

- 数据科学家和业务分析师在假设形成上协作
- 工程师将分析作为一等要求实施,而非事后补充
- 功能标志支持安全实验而无需完整部署
- 实时监控允许快速迭代和在需要时回滚
- 统计严谨性与业务实用性和上市速度相平衡
- 持续学习循环反馈到下一个功能开发周期

使用数据驱动方法开发的功能: $ARGUMENTS
