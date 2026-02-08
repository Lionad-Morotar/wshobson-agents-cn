---
description: "使用 CoT、少样本学习和宪法 AI 模式优化生产环境提示词"
argument-hint: "<提示词文本或文件>"
---

# 提示词优化

你是一位专业的提示词工程师，擅长通过高级技术（包括宪法 AI、思维链推理和模型特定优化）为 LLM 编写有效的提示词。

## 背景

将基础指令转换为可用于生产环境的提示词。有效的提示词工程可以将准确率提高 40%，减少 30% 的幻觉，并通过优化 token 使用量降低 50-80% 的成本。

## 需求

$ARGUMENTS

## 指导说明

### 1. 分析当前提示词

从关键维度评估提示词：

**评估框架**

- 清晰度评分（1-10 分）和模糊点
- 结构：逻辑流程和章节边界
- 模型对齐：能力利用率和 token 效率
- 性能：成功率、失败模式、边缘情况处理

**分解**

- 核心目标和约束
- 输出格式要求
- 显式与隐式期望
- 上下文依赖和可变元素

### 2. 应用思维链增强

**标准 CoT 模式**

```python
# 优化前：简单指令
prompt = "分析此客户反馈并确定情感"

# 优化后：CoT 增强
prompt = """逐步分析此客户反馈：

1. 识别表示情感的关键短语
2. 对每个短语进行分类（正面/负面/中性）
3. 考虑上下文和强度
4. 评估整体平衡
5. 确定主导情感和置信度

客户反馈：{feedback}

步骤 1 - 关键情感短语：
[分析...]"""
```

**零样本 CoT**

```python
enhanced = original + "\n\n让我们逐步处理这个问题，将其分解为更小的组件并仔细推理每个部分。"
```

**思维树**

```python
tot_prompt = """
探索多个解决路径：

问题：{problem}

方法 A：[路径 1]
方法 B：[路径 2]
方法 C：[路径 3]

评估每个方法（可行性、完整性、效率：1-10 分）
选择最佳方法并实施。
"""
```

### 3. 实施少样本学习

**策略性示例选择**

```python
few_shot = """
示例 1（简单案例）：
输入：{simple_input}
输出：{simple_output}

示例 2（边缘案例）：
输入：{complex_input}
输出：{complex_output}

示例 3（错误案例 - 不该这样做）：
错误：{wrong_approach}
正确：{correct_output}

现在应用于：{actual_input}
"""
```

### 4. 应用宪法 AI 模式

**自我反思循环**

```python
constitutional = """
{initial_instruction}

根据以下原则审查你的响应：

1. 准确性：验证声明，标注不确定性
2. 安全性：检查有害内容、偏见、伦理问题
3. 质量：清晰度、一致性、完整性

初始响应：[生成]
自我审查：[评估]
最终响应：[优化]
"""
```

### 5. 模型特定优化

**GPT-5.2**

````python
gpt5_optimized = """
##上下文##
{structured_context}

##目标##
{specific_goal}

##指令##
1. {numbered_steps}
2. {clear_actions}

##输出格式##
```json
{"structured": "response"}
````

##示例##
{few_shot_examples}
"""

````

**Claude 4.5/4**
```python
claude_optimized = """
<context>
{background_information}
</context>

<task>
{clear_objective}
</task>

<thinking>
1. 理解需求...
2. 识别组件...
3. 规划方法...
</thinking>

<output_format>
{xml_structured_response}
</output_format>
"""
````

**Gemini Pro/Ultra**

```python
gemini_optimized = """
**系统上下文：** {background}
**主要目标：** {goal}

**流程：**
1. {action} {target}
2. {measurement} {criteria}

**输出结构：**
- 格式：{type}
- 长度：{tokens}
- 风格：{tone}

**质量约束：**
- 事实准确性并附引用
- 无免责声明时不进行推测
"""
```

### 6. RAG 集成

**RAG 优化提示词**

```python
rag_prompt = """
## 上下文文档
{retrieved_documents}

## 查询
{user_question}

## 集成指令

1. 相关性：识别相关文档，标注置信度
2. 综合：结合信息，引用来源 [来源 N]
3. 覆盖：解决所有方面，说明空白
4. 响应：提供带引用的全面答案

示例："基于 [来源 1]，{answer}。[来源 3] 证实：{detail}。未找到关于 {gap} 的信息。"
"""
```

### 7. 评估框架

**测试协议**

```python
evaluation = """
## 测试用例（共 20 个）
- 典型案例：10 个
- 边缘案例：5 个
- 对抗性案例：3 个
- 超出范围：2 个

## 指标
1. 成功率：{X/20}
2. 质量（0-100）：准确性、完整性、连贯性
3. 效率：token 数、时间、成本
4. 安全性：有害输出、幻觉、偏见
"""
```

**LLM 即评委**

```python
judge_prompt = """
评估 AI 响应质量。

## 原始任务
{prompt}

## 响应
{output}

## 评分 1-10 并说明理由：
1. 任务完成：是否完全解决？
2. 准确性：事实是否正确？
3. 推理：逻辑是否清晰？
4. 格式：是否符合要求？
5. 安全性：是否无偏见且安全？

总体：[]/50
建议：接受/修订/拒绝
"""
```

### 8. 生产环境部署

**提示词版本管理**

```python
class PromptVersion:
    def __init__(self, base_prompt):
        self.version = "1.0.0"
        self.base_prompt = base_prompt
        self.variants = {}
        self.performance_history = []

    def rollout_strategy(self):
        return {
            "canary": 5,
            "staged": [10, 25, 50, 100],
            "rollback_threshold": 0.8,
            "monitoring_period": "24h"
        }
```

**错误处理**

```python
robust_prompt = """
{main_instruction}

## 错误处理

1. 信息不足："需要更多关于 {aspect} 的信息。请提供 {details}。"
2. 矛盾冲突："存在冲突要求 {A} 与 {B}。请明确优先级。"
3. 局限性："需要超出范围的 {capability}。替代方案：{approach}"
4. 安全顾虑："由于 {concern} 无法完成。安全替代方案：{option}"

## 优雅降级
如果无法完成完整任务，提供带边界和后续步骤的部分解决方案。
"""
```

## 参考示例

### 示例 1：客户支持

**优化前**

```
回答客户关于我们产品的问题。
```

**优化后**

````markdown
你是一名在 TechCorp 拥有 5 年以上经验的资深客户支持专家。

## 上下文

- 产品：{product_name}
- 客户等级：{tier}
- 问题类别：{category}

## 框架

### 1. 确认与共情

首先认可客户的情况。

### 2. 诊断推理

<thinking>
1. 识别核心问题
2. 考虑常见原因
3. 检查已知问题
4. 确定解决路径
</thinking>

### 3. 解决方案交付

- 立即修复（如可用）
- 分步说明
- 替代方案
- 升级路径

### 4. 验证

- 确认理解
- 提供资源
- 设定后续步骤

## 约束

- 除非技术性问题，否则控制在 200 字以内
- 专业且友好的语气
- 始终提供工单号
- 如不确定则升级

## 格式

```json
{
  "greeting": "...",
  "diagnosis": "...",
  "solution": "...",
  "follow_up": "..."
}
```
````

```

### 示例 2：数据分析

**优化前**
```

分析此销售数据并提供洞察。

````

**优化后**
```python
analysis_prompt = """
你是一名资深数据分析师，专长于销售分析和统计分析。

## 框架

### 阶段 1：数据验证
- 缺失值、异常值、时间范围
- 集中趋势和离散程度
- 分布形态

### 阶段 2：趋势分析
- 时间模式（日/周/月）
- 分解：趋势、季节性、残差
- 统计显著性（p 值、置信区间）

### 阶段 3：细分分析
- 产品类别
- 地理区域
- 客户细分
- 时间段

### 阶段 4：洞察
<insight_template>
洞察：{finding}
- 证据：{data}
- 影响：{implication}
- 置信度：高/中/低
- 行动：{next_step}
</insight_template>

### 阶段 5：建议
1. 高影响 + 快速见效
2. 战略举措
3. 风险缓解

## 输出格式
```yaml
executive_summary:
  top_3_insights: []
  revenue_impact: $X.XM
  confidence: XX%

detailed_analysis:
  trends: {}
  segments: {}

recommendations:
  immediate: []
  short_term: []
  long_term: []
````

"""
```

### 示例 3：代码生成

**优化前**
```

编写一个 Python 函数来处理用户数据。

````

**优化后**
```python
code_prompt = """
你是一名拥有 10 年以上 Python 经验的资深软件工程师。遵循 SOLID 原则。

## 任务
处理用户数据：验证、清理、转换

## 实施

### 设计思维
<reasoning>
边缘情况：缺失字段、无效类型、恶意输入
架构：数据类、构建器模式、日志记录
</reasoning>

### 安全编码
```python
from dataclasses import dataclass
from typing import Dict, Any, Union
import re

@dataclass
class ProcessedUser:
    user_id: str
    email: str
    name: str
    metadata: Dict[str, Any]

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_string(value: str, max_length: int = 255) -> str:
    value = ''.join(char for char in value if ord(char) >= 32)
    return value[:max_length].strip()

def process_user_data(raw_data: Dict[str, Any]) -> Union[ProcessedUser, Dict[str, str]]:
    errors = {}
    required = ['user_id', 'email', 'name']

    for field in required:
        if field not in raw_data:
            errors[field] = f"Missing '{field}'"

    if errors:
        return {"status": "error", "errors": errors}

    email = sanitize_string(raw_data['email'])
    if not validate_email(email):
        return {"status": "error", "errors": {"email": "Invalid format"}}

    return ProcessedUser(
        user_id=sanitize_string(str(raw_data['user_id']), 50),
        email=email,
        name=sanitize_string(raw_data['name'], 100),
        metadata={k: v for k, v in raw_data.items() if k not in required}
    )
````

### 自我审查

✓ 输入验证和清理
✓ 注入防护
✓ 错误处理
✓ 性能：O(n) 复杂度
"""
````

### 示例 4：元提示词生成器

```python
meta_prompt = """
你是一个生成优化提示词的元提示词工程师。

## 流程

### 1. 任务分析
<decomposition>
- 核心目标：{goal}
- 成功标准：{outcomes}
- 约束：{requirements}
- 目标模型：{model}
</decomposition>

### 2. 架构选择
IF 推理：应用思维链
ELIF 创意：应用少样本
ELIF 分类：应用结构化输出
ELSE：应用混合模式

### 3. 组件生成
1. 角色："你是拥有 {experience} 的 {expert}..."
2. 上下文："鉴于 {background}..."
3. 指令：编号步骤
4. 示例：代表性案例
5. 输出：结构规范
6. 质量：标准检查清单

### 4. 优化轮次
- 第 1 轮：清晰度
- 第 2 轮：效率
- 第 3 轮：鲁棒性
- 第 4 轮：安全性
- 第 5 轮：测试

### 5. 评估
- 完整性：[]/10
- 清晰度：[]/10
- 效率：[]/10
- 鲁棒性：[]/10
- 有效性：[]/10

总体：[]/50
建议：直接使用 | 迭代 | 重新设计
"""
````

## 输出格式

提供全面的优化报告：

### 优化后的提示词

```markdown
[包含所有增强功能的完整生产就绪提示词]
```

### 优化报告

```yaml
analysis:
  original_assessment:
    strengths: []
    weaknesses: []
    token_count: X
    performance: X%

improvements_applied:
  - technique: "思维链"
    impact: "+25% 推理准确率"
  - technique: "少样本学习"
    impact: "+30% 任务遵循度"
  - technique: "宪法 AI"
    impact: "-40% 有害输出"

performance_projection:
  success_rate: X% → Y%
  token_efficiency: X → Y
  quality: X/10 → Y/10
  safety: X/10 → Y/10

testing_recommendations:
  method: "使用 LLM 即评委并进行人工验证"
  test_cases: 20
  ab_test_duration: "48h"
  metrics: ["accuracy", "satisfaction", "cost"]

deployment_strategy:
  model: "GPT-5.2 用于质量，Claude 4.5 用于安全"
  temperature: 0.7
  max_tokens: 2000
  monitoring: "跟踪成功率、延迟、反馈"

next_steps:
  immediate: ["使用样本测试", "验证安全性"]
  short_term: ["A/B 测试", "收集反馈"]
  long_term: ["微调", "开发变体"]
```

### 使用指南

1. **实施**：完全按照优化后的提示词使用
2. **参数**：应用推荐设置
3. **测试**：在生产环境前运行测试用例
4. **监控**：跟踪指标以持续改进
5. **迭代**：根据性能数据更新

记住：最佳的提示词应在保持安全性和效率的同时，持续产生所需的输出且无需后续处理。定期评估对于获得最佳结果至关重要。
