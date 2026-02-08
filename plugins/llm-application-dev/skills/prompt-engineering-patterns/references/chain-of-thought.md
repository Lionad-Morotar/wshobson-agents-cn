# 思维链提示

## 概述

思维链(Chain-of-Thought, CoT)提示能够引导 LLM 逐步进行推理,显著提升在复杂推理、数学和逻辑任务上的表现。

## 核心技术

### 零样本思维链 (Zero-Shot CoT)

添加简单的触发短语来引导推理:

```python
def zero_shot_cot(query):
    return f"""{query}

让我们一步步思考:"""

# 示例
query = "如果一列火车以 60 英里/小时的速度行驶 2.5 小时,它能行驶多远?"
prompt = zero_shot_cot(query)

# 模型输出:
# "让我们一步步思考:
# 1. 速度 = 60 英里/小时
# 2. 时间 = 2.5 小时
# 3. 距离 = 速度 × 时间
# 4. 距离 = 60 × 2.5 = 150 英里
# 答案: 150 英里"
```

### 少样本思维链 (Few-Shot CoT)

提供包含明确推理链的示例:

```python
few_shot_examples = """
问: Roger 有 5 个网球。他又买了 2 罐网球。每罐有 3 个球。他现在有多少个网球?
答: 让我们一步步思考:
1. Roger 开始有 5 个球
2. 他买了 2 罐,每罐有 3 个球
3. 罐中的球: 2 × 3 = 6 个球
4. 总计: 5 + 6 = 11 个球
答案: 11

问: 食堂有 23 个苹果。如果他们用 20 个做午餐,又买了 6 个,现在有多少个?
答: 让我们一步步思考:
1. 开始有 23 个苹果
2. 午餐用了 20 个: 23 - 20 = 剩 3 个苹果
3. 又买了 6 个: 3 + 6 = 9 个苹果
答案: 9

问: {user_query}
答: 让我们一步步思考:"""
```

### 自我一致性 (Self-Consistency)

生成多条推理路径并采用多数投票:

```python
import openai
from collections import Counter

def self_consistency_cot(query, n=5, temperature=0.7):
    prompt = f"{query}\n\n让我们一步步思考:"

    responses = []
    for _ in range(n):
        response = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        responses.append(extract_final_answer(response))

    # 采用多数投票
    answer_counts = Counter(responses)
    final_answer = answer_counts.most_common(1)[0][0]

    return {
        'answer': final_answer,
        'confidence': answer_counts[final_answer] / n,
        'all_responses': responses
    }
```

## 高级模式

### 从简到繁提示 (Least-to-Most Prompting)

将复杂问题分解为更简单的子问题:

```python
def least_to_most_prompt(complex_query):
    # 阶段 1: 分解
    decomp_prompt = f"""将这个复杂问题分解为更简单的子问题:

问题: {complex_query}

子问题:"""

    subproblems = get_llm_response(decomp_prompt)

    # 阶段 2: 顺序求解
    solutions = []
    context = ""

    for subproblem in subproblems:
        solve_prompt = f"""{context}

解决这个子问题:
{subproblem}

解决方案:"""
        solution = get_llm_response(solve_prompt)
        solutions.append(solution)
        context += f"\n\n已解决: {subproblem}\n解决方案: {solution}"

    # 阶段 3: 最终整合
    final_prompt = f"""给定这些子问题的解决方案:
{context}

提供以下问题的最终答案: {complex_query}

最终答案:"""

    return get_llm_response(final_prompt)
```

### 思维树 (Tree-of-Thought, ToT)

探索多条推理分支:

```python
class TreeOfThought:
    def __init__(self, llm_client, max_depth=3, branches_per_step=3):
        self.client = llm_client
        self.max_depth = max_depth
        self.branches_per_step = branches_per_step

    def solve(self, problem):
        # 生成初始思维分支
        initial_thoughts = self.generate_thoughts(problem, depth=0)

        # 评估每个分支
        best_path = None
        best_score = -1

        for thought in initial_thoughts:
            path, score = self.explore_branch(problem, thought, depth=1)
            if score > best_score:
                best_score = score
                best_path = path

        return best_path

    def generate_thoughts(self, problem, context="", depth=0):
        prompt = f"""问题: {problem}
{context}

生成 {self.branches_per_step} 个不同的下一步骤来解决这个问题:

1."""
        response = self.client.complete(prompt)
        return self.parse_thoughts(response)

    def evaluate_thought(self, problem, thought_path):
        prompt = f"""问题: {problem}

目前的推理路径:
{thought_path}

从 0-10 分评估这条推理路径的:
- 正确性
- 达成解决方案的可能性
- 逻辑连贯性

评分:"""
        return float(self.client.complete(prompt))
```

### 验证步骤

添加显式验证以捕获错误:

```python
def cot_with_verification(query):
    # 步骤 1: 生成推理和答案
    reasoning_prompt = f"""{query}

让我们一步步解决这个问题:"""

    reasoning_response = get_llm_response(reasoning_prompt)

    # 步骤 2: 验证推理
    verification_prompt = f"""原始问题: {query}

提出的解决方案:
{reasoning_response}

通过以下方式验证这个解决方案:
1. 检查每一步是否有逻辑错误
2. 验证算术计算
3. 确保最终答案合理

这个解决方案正确吗?如果不正确,有什么问题?

验证:"""

    verification = get_llm_response(verification_prompt)

    # 步骤 3: 如需要则修正
    if "incorrect" in verification.lower() or "error" in verification.lower():
        revision_prompt = f"""之前的解决方案有错误:
{verification}

请提供以下问题的修正解决方案: {query}

修正后的解决方案:"""
        return get_llm_response(revision_prompt)

    return reasoning_response
```

## 领域特定的思维链

### 数学问题

```python
math_cot_template = """
问题: {problem}

解决方案:
步骤 1: 确定已知条件
- {list_known_values}

步骤 2: 确定需要求解的内容
- {target_variable}

步骤 3: 选择相关公式
- {formulas}

步骤 4: 代入数值
- {substitution}

步骤 5: 计算
- {calculation}

步骤 6: 验证并给出答案
- {verification}

答案: {final_answer}
"""
```

### 代码调试

```python
debug_cot_template = """
带有错误的代码:
{code}

错误信息:
{error}

调试过程:
步骤 1: 理解错误信息
- {interpret_error}

步骤 2: 定位问题行
- {identify_line}

步骤 3: 分析为什么这行代码失败
- {root_cause}

步骤 4: 确定修复方案
- {proposed_fix}

步骤 5: 验证修复是否解决错误
- {verification}

修复后的代码:
{corrected_code}
"""
```

### 逻辑推理

```python
logic_cot_template = """
前提:
{premises}

问题: {question}

推理过程:
步骤 1: 列出所有已知事实
{facts}

步骤 2: 识别逻辑关系
{relationships}

步骤 3: 应用演绎推理
{deductions}

步骤 4: 得出结论
{conclusion}

答案: {final_answer}
"""
```

## 性能优化

### 缓存推理模式

```python
class ReasoningCache:
    def __init__(self):
        self.cache = {}

    def get_similar_reasoning(self, problem, threshold=0.85):
        problem_embedding = embed(problem)

        for cached_problem, reasoning in self.cache.items():
            similarity = cosine_similarity(
                problem_embedding,
                embed(cached_problem)
            )
            if similarity > threshold:
                return reasoning

        return None

    def add_reasoning(self, problem, reasoning):
        self.cache[problem] = reasoning
```

### 自适应推理深度

```python
def adaptive_cot(problem, initial_depth=3):
    depth = initial_depth

    while depth <= 10:  # 最大深度
        response = generate_cot(problem, num_steps=depth)

        # 检查解决方案是否看起来完整
        if is_solution_complete(response):
            return response

        depth += 2  # 增加推理深度

    return response  # 返回最佳尝试
```

## 评估指标

```python
def evaluate_cot_quality(reasoning_chain):
    metrics = {
        'coherence': measure_logical_coherence(reasoning_chain),
        'completeness': check_all_steps_present(reasoning_chain),
        'correctness': verify_final_answer(reasoning_chain),
        'efficiency': count_unnecessary_steps(reasoning_chain),
        'clarity': rate_explanation_clarity(reasoning_chain)
    }
    return metrics
```

## 最佳实践

1. **清晰的步骤标记**: 使用编号步骤或清晰的分隔符
2. **展示全部过程**: 不要跳过步骤,即使是显而易见的步骤
3. **验证计算**: 添加显式验证步骤
4. **陈述假设**: 将隐含假设显式化
5. **检查边界情况**: 考虑边界条件
6. **使用示例**: 首先用示例展示推理模式

## 常见陷阱

- **过早下结论**: 在没有完整推理的情况下直接得出答案
- **循环逻辑**: 使用结论来证明推理
- **遗漏步骤**: 跳过中间计算
- **过度复杂**: 添加不必要的混淆步骤
- **格式不一致**: 在推理过程中改变步骤结构

## 何时使用思维链

**适用于思维链的场景:**

- 数学和算术问题
- 逻辑推理任务
- 多步骤规划
- 代码生成和调试
- 复杂决策

**不适合思维链的场景:**

- 简单事实查询
- 直接查找
- 创意写作
- 需要简洁性的任务
- 实时、延迟敏感的应用

## 资源

- 思维链评估的基准数据集
- 预构建的思维链提示模板
- 推理验证工具
- 步骤提取和解析实用程序
