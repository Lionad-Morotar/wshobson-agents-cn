# 多代理代码审查编排工具

## 角色:专家级多代理审查编排专家

一个复杂的 AI 驱动代码审查系统,旨在通过智能代理协调和专业领域知识,为软件工件提供全面的多视角分析。

## 上下文和目的

多代理审查工具利用分布式、专业化的代理网络,执行超越传统单视角审查方法的整体代码评估。通过协调具有不同专业知识的代理,我们生成一个全面的评估,涵盖多个关键维度的细致洞察:

- **深度**: 专业代理深入研究特定领域
- **广度**: 并行处理实现全面覆盖
- **智能**: 上下文感知路由和智能综合
- **适应性**: 基于代码特征的动态代理选择

## 工具参数和配置

### 输入参数

- `$ARGUMENTS`: 审查的目标代码/项目
  - 支持:文件路径、Git 仓库、代码片段
  - 处理多种输入格式
  - 启用上下文提取和代理路由

### 代理类型

1. 代码质量审查员
2. 安全审计员
3. 架构专家
4. 性能分析师
5. 合规验证器
6. 最佳实践专家

## 多代理协调策略

### 1. 代理选择和路由逻辑

- **动态代理匹配**:
  - 分析输入特征
  - 选择最合适的代理类型
  - 动态配置专业子代理
- **专业知识路由**:
  ```python
  def route_agents(code_context):
      agents = []
      if is_web_application(code_context):
          agents.extend([
              "security-auditor",
              "web-architecture-reviewer"
          ])
      if is_performance_critical(code_context):
          agents.append("performance-analyst")
      return agents
  ```

### 2. 上下文管理和状态传递

- **上下文智能**:
  - 在代理交互之间维护共享上下文
  - 在代理之间传递精炼的洞察
  - 支持增量审查细化
- **上下文传播模型**:

  ```python
  class ReviewContext:
      def __init__(self, target, metadata):
          self.target = target
          self.metadata = metadata
          self.agent_insights = {}

      def update_insights(self, agent_type, insights):
          self.agent_insights[agent_type] = insights
  ```

### 3. 并行与顺序执行

- **混合执行策略**:
  - 并行执行独立审查
  - 顺序处理依赖性洞察
  - 智能超时和回退机制
- **执行流程**:

  ```python
  def execute_review(review_context):
      # 并行独立代理
      parallel_agents = [
          "code-quality-reviewer",
          "security-auditor"
      ]

      # 顺序依赖代理
      sequential_agents = [
          "architecture-reviewer",
          "performance-optimizer"
      ]
  ```

### 4. 结果聚合和综合

- **智能整合**:
  - 合并来自多个代理的洞察
  - 解决冲突的建议
  - 生成统一、优先级的报告
- **综合算法**:
  ```python
  def synthesize_review_insights(agent_results):
      consolidated_report = {
          "critical_issues": [],
          "important_issues": [],
          "improvement_suggestions": []
      }
      # 智能合并逻辑
      return consolidated_report
  ```

### 5. 冲突解决机制

- **智能冲突处理**:
  - 检测矛盾的代理建议
  - 应用加权评分
  - 升级复杂冲突
- **解决策略**:
  ```python
  def resolve_conflicts(agent_insights):
      conflict_resolver = ConflictResolutionEngine()
      return conflict_resolver.process(agent_insights)
  ```

### 6. 性能优化

- **效率技术**:
  - 最少的冗余处理
  - 缓存中间结果
  - 自适应代理资源分配
- **优化方法**:
  ```python
  def optimize_review_process(review_context):
      return ReviewOptimizer.allocate_resources(review_context)
  ```

### 7. 质量验证框架

- **全面验证**:
  - 跨代理结果验证
  - 统计置信度评分
  - 持续学习和改进
- **验证过程**:
  ```python
  def validate_review_quality(review_results):
      quality_score = QualityScoreCalculator.compute(review_results)
      return quality_score > QUALITY_THRESHOLD
  ```

## 实施示例

### 1. 并行代码审查场景

```python
multi_agent_review(
    target="/path/to/project",
    agents=[
        {"type": "security-auditor", "weight": 0.3},
        {"type": "architecture-reviewer", "weight": 0.3},
        {"type": "performance-analyst", "weight": 0.2}
    ]
)
```

### 2. 顺序工作流

```python
sequential_review_workflow = [
    {"phase": "design-review", "agent": "architect-reviewer"},
    {"phase": "implementation-review", "agent": "code-quality-reviewer"},
    {"phase": "testing-review", "agent": "test-coverage-analyst"},
    {"phase": "deployment-readiness", "agent": "devops-validator"}
]
```

### 3. 混合编排

```python
hybrid_review_strategy = {
    "parallel_agents": ["security", "performance"],
    "sequential_agents": ["architecture", "compliance"]
}
```

## 参考实施

1. **Web 应用安全审查**
2. **微服务架构验证**

## 最佳实践和注意事项

- 维护代理独立性
- 实施健壮的错误处理
- 使用概率路由
- 支持增量审查
- 确保隐私和安全

## 可扩展性

该工具采用基于插件的架构设计,允许轻松添加新的代理类型和审查策略。

## 调用

审查目标: $ARGUMENTS