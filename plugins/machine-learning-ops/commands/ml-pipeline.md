# 机器学习管道 - 多代理 MLOps 编排

为以下需求设计和实现完整的 ML 管道：$ARGUMENTS

## 思考

此工作流编排多个专业代理以构建遵循现代 MLOps 最佳实践的生产就绪 ML 管道。该方法强调：

- **基于阶段的协调**：每个阶段都基于之前的输出构建，在代理之间有清晰的交接
- **现代工具集成**：用于实验的 MLflow/W&B、用于特征的 Feast/Tecton、用于服务的 KServe/Seldon
- **生产优先思维**：每个组件都为规模、监控和可靠性而设计
- **可重现性**：数据、模型和基础设施的版本控制
- **持续改进**：自动重新训练、A/B 测试和漂移检测

多代理方法确保每个方面都由领域专家处理：

- 数据工程师处理摄入和质量
- 数据科学家设计特征和实验
- ML 工程师实现训练管道
- MLOps 工程师处理生产部署
- 可观测性工程师确保监控

## 阶段 1：数据和需求分析

<Task>
subagent_type: data-engineer
prompt: |
  为 ML 系统分析和设计数据管道，需求：$ARGUMENTS

交付物：

1. 数据源审计和摄入策略：
   - 源系统和连接模式
   - 使用 Pydantic/Great Expectations 进行架构验证
   - 使用 DVC 或 lakeFS 进行数据版本控制
   - 增量加载和 CDC 策略

2. 数据质量框架：
   - 剖析和统计生成
   - 异常检测规则
   - 数据血缘跟踪
   - 质量关卡和 SLA

3. 存储架构：
   - 原始/处理/特征层
   - 分区策略
   - 保留策略
   - 成本优化

提供关键组件的集成模式和实现代码。
</Task>

<Task>
subagent_type: data-scientist
prompt: |
  为以下需求设计特征工程和模型需求：$ARGUMENTS
  使用数据架构：{phase1.data-engineer.output}

交付物：

1. 特征工程管道：
   - 转换规范
   - 特征存储架构 (Feast/Tecton)
   - 统计验证规则
   - 缺失数据/异常值的处理策略

2. 模型需求：
   - 算法选择理由
   - 性能指标和基线
   - 训练数据需求
   - 评估标准和阈值

3. 实验设计：
   - 假设和成功指标
   - A/B 测试方法
   - 样本量计算
   - 偏见检测方法

包含特征转换代码和统计验证逻辑。
</Task>

## 阶段 2：模型开发和训练

<Task>
subagent_type: ml-engineer
prompt: |
  基于需求实现训练管道：{phase1.data-scientist.output}
  使用数据管道：{phase1.data-engineer.output}

构建全面的训练系统：

1. 训练管道实现：
   - 具有清晰接口的模块化训练代码
   - 超参数优化 (Optuna/Ray Tune)
   - 分布式训练支持 (Horovod/PyTorch DDP)
   - 交叉验证和集成策略

2. 实验跟踪设置：
   - MLflow/Weights & Biases 集成
   - 指标记录和可视化
   - 工件管理（模型、图表、数据样本）
   - 实验比较和分析工具

3. 模型注册表集成：
   - 版本控制和标记策略
   - 模型元数据和血缘
   - 推广工作流（dev -> staging -> prod）
   - 回滚程序

提供具有配置管理的完整训练代码。
</Task>

<Task>
subagent_type: python-pro
prompt: |
  优化并生产化来自以下代码的 ML 代码：{phase2.ml-engineer.output}

重点领域：

1. 代码质量和结构：
   - 为生产标准重构
   - 添加全面的错误处理
   - 使用结构化格式实现适当的日志记录
   - 创建可重用的组件和实用程序

2. 性能优化：
   - 分析和优化瓶颈
   - 实现缓存策略
   - 优化数据加载和预处理
   - 大规模训练的内存管理

3. 测试框架：
   - 数据转换的单元测试
   - 管道组件的集成测试
   - 模型质量测试（不变性、方向性）
   - 性能回归测试

交付生产就绪、可维护的代码，具有完整的测试覆盖。
</Task>

## 阶段 3：生产部署和服务

<Task>
subagent_type: mlops-engineer
prompt: |
  为模型设计生产部署：{phase2.ml-engineer.output}
  使用优化代码：{phase2.python-pro.output}

实现需求：

1. 模型服务基础设施：
   - 使用 FastAPI/TorchServe 的 REST/gRPC API
   - 批量预测管道 (Airflow/Kubeflow)
   - 流处理 (Kafka/Kinesis 集成)
   - 模型服务平台 (KServe/Seldon Core)

2. 部署策略：
   - 用于零停机的蓝绿部署
   - 带流量分割的金丝雀发布
   - 用于验证的影子部署
   - A/B 测试基础设施

3. CI/CD 管道：
   - GitHub Actions/GitLab CI 工作流
   - 自动测试关卡
   - 部署前的模型验证
   - 用于 GitOps 部署的 ArgoCD

4. 基础设施即代码：
   - 用于云资源的 Terraform 模块
   - 用于 Kubernetes 部署的 Helm charts
   - 用于优化的 Docker 多阶段构建
   - 使用 Vault/Secrets Manager 的密钥管理

提供完整的部署配置和自动化脚本。
</Task>

<Task>
subagent_type: kubernetes-architect
prompt: |
  为 ML 工作负载设计 Kubernetes 基础设施：{phase3.mlops-engineer.output}

Kubernetes 特定需求：

1. 工作负载编排：
   - 使用 Kubeflow 的训练作业调度
   - GPU 资源分配和共享
   - Spot/可抢占实例集成
   - 优先级类别和资源配额

2. 服务基础设施：
   - 用于自动扩展的 HPA/VPA
   - 用于事件驱动扩展的 KEDA
   - 用于流量管理的 Istio 服务网格
   - 模型缓存和热身策略

3. 存储和数据访问：
   - 训练数据的 PVC 策略
   - 使用 CSI 驱动器的模型工件存储
   - 特征存储的分布式存储
   - 用于推理优化的缓存层

为整个 ML 平台提供 Kubernetes 清单和 Helm charts。
</Task>

## 阶段 4：监控和持续改进

<Task>
subagent_type: observability-engineer
prompt: |
  为部署在以下位置的 ML 系统实现全面监控：{phase3.mlops-engineer.output}
  使用 Kubernetes 基础设施：{phase3.kubernetes-architect.output}

监控框架：

1. 模型性能监控：
   - 预测准确度跟踪
   - 延迟和吞吐量指标
   - 特征重要性变化
   - 业务 KPI 相关性

2. 数据和模型漂移检测：
   - 统计漂移检测 (KS 检验、PSI)
   - 概念漂移监控
   - 特征分布跟踪
   - 自动漂移警报和报告

3. 系统可观测性：
   - 所有组件的 Prometheus 指标
   - 用于可视化的 Grafana 仪表板
   - 使用 Jaeger/Zipkin 的分布式跟踪
   - 使用 ELK/Loki 的日志聚合

4. 警报和自动化：
   - PagerDuty/Opsgenie 集成
   - 自动重新训练触发器
   - 性能下降工作流
   - 事件响应手册

5. 成本跟踪：
   - 资源利用率指标
   - 按模型/实验的成本分配
   - 优化建议
   - 预算警报和控制

交付监控配置、仪表板和警报规则。
</Task>

## 配置选项

- **experiment_tracking**: mlflow | wandb | neptune | clearml
- **feature_store**: feast | tecton | databricks | custom
- **serving_platform**: kserve | seldon | torchserve | triton
- **orchestration**: kubeflow | airflow | prefect | dagster
- **cloud_provider**: aws | azure | gcp | multi-cloud
- **deployment_mode**: realtime | batch | streaming | hybrid
- **monitoring_stack**: prometheus | datadog | newrelic | custom

## 成功标准

1. **数据管道成功**：
   - 生产中数据质量问题 < 0.1%
   - 自动数据验证 99.9% 时间通过
   - 完整的数据血缘跟踪
   - 亚秒级特征服务延迟

2. **模型性能**：
   - 达到或超过基线指标
   - 重新训练前性能下降 < 5%
   - 具有统计意义的成功 A/B 测试
   - 未检测到的模型漂移不超过 24 小时

3. **运营卓越**：
   - 模型服务 99.9% 正常运行时间
   - p99 推理延迟 < 200ms
   - 5 分钟内自动回滚
   - 完整可观测性，警报时间 < 1 分钟

4. **开发速度**：
   - 从提交到生产 < 1 小时
   - 并行实验执行
   - 可重现的训练运行
   - 自助模型部署

5. **成本效率**：
   - 基础设施浪费 < 20%
   - 优化的资源分配
   - 基于负载的自动扩展
   - Spot 实例利用率 > 60%

## 最终交付物

完成后，编排的管道将提供：

- 具有全面自动化的端到端 ML 管道
- 全面的文档和操作手册
- 生产就绪的基础设施即代码
- 完整的监控和警报系统
- 用于持续改进的 CI/CD 管道
- 成本优化和扩展策略
- 灾难恢复和回滚程序
