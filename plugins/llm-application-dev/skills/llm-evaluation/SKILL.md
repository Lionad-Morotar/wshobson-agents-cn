---
name: llm-evaluation
description: 使用自动化指标、人工反馈和基准测试为 LLM 应用实施综合评估策略。在测试 LLM 性能、衡量 AI 应用质量或建立评估框架时使用。
---

# LLM 评估

掌握 LLM 应用的综合评估策略，从自动化指标到人工评估和 A/B 测试。

## 何时使用此技能

- 系统性地衡量 LLM 应用性能
- 比较不同的模型或提示词
- 在部署前检测性能回归
- 验证提示词改进的效果
- 建立对生产系统的信心
- 建立基线并跟踪随时间的进展
- 调试意外的模型行为

## 核心评估类型

### 1. 自动化指标

使用计算得分进行快速、可重复、可扩展的评估。

**文本生成：**

- **BLEU**：N-gram 重叠度（翻译）
- **ROUGE**：以召回率为导向（摘要）
- **METEOR**：语义相似度
- **BERTScore**：基于嵌入的相似度
- **Perplexity**：语言模型置信度

**分类：**

- **Accuracy**：正确率百分比
- **Precision/Recall/F1**：特定类别性能
- **Confusion Matrix**：错误模式
- **AUC-ROC**：排序质量

**检索（RAG）：**

- **MRR**：平均倒数排名
- **NDCG**：归一化折扣累积增益
- **Precision@K**：前 K 个结果中的相关度
- **Recall@K**：前 K 个结果中的覆盖率

### 2. 人工评估

对难以自动化的质量方面进行手动评估。

**维度：**

- **Accuracy**：事实正确性
- **Coherence**：逻辑流畅性
- **Relevance**：回答问题的相关性
- **Fluency**：自然语言质量
- **Safety**：无有害内容
- **Helpfulness**：对用户的有用性

### 3. LLM 即评判者

使用更强的 LLM 来评估较弱模型的输出。

**方法：**

- **Pointwise**：对单个响应打分
- **Pairwise**：比较两个响应
- **Reference-based**：与黄金标准比较
- **Reference-free**：无基准真值的评判

## 快速开始

```python
from dataclasses import dataclass
from typing import Callable
import numpy as np

@dataclass
class Metric:
    name: str
    fn: Callable

    @staticmethod
    def accuracy():
        return Metric("accuracy", calculate_accuracy)

    @staticmethod
    def bleu():
        return Metric("bleu", calculate_bleu)

    @staticmethod
    def bertscore():
        return Metric("bertscore", calculate_bertscore)

    @staticmethod
    def custom(name: str, fn: Callable):
        return Metric(name, fn)

class EvaluationSuite:
    def __init__(self, metrics: list[Metric]):
        self.metrics = metrics

    async def evaluate(self, model, test_cases: list[dict]) -> dict:
        results = {m.name: [] for m in self.metrics}

        for test in test_cases:
            prediction = await model.predict(test["input"])

            for metric in self.metrics:
                score = metric.fn(
                    prediction=prediction,
                    reference=test.get("expected"),
                    context=test.get("context")
                )
                results[metric.name].append(score)

        return {
            "metrics": {k: np.mean(v) for k, v in results.items()},
            "raw_scores": results
        }

# 使用示例
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom("groundedness", check_groundedness)
])

test_cases = [
    {
        "input": "法国的首都是什么？",
        "expected": "巴黎",
        "context": "法国是欧洲的一个国家。巴黎是其首都。"
    },
]

results = await suite.evaluate(model=your_model, test_cases=test_cases)
```

## 自动化指标实现

### BLEU 分数

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference: str, hypothesis: str, **kwargs) -> float:
    """计算参考文本和假设文本之间的 BLEU 分数。"""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )
```

### ROUGE 分数

```python
from rouge_score import rouge_scorer

def calculate_rouge(reference: str, hypothesis: str, **kwargs) -> dict:
    """计算 ROUGE 分数。"""
    scorer = rouge_scorer.RougeScorer(
        ['rouge1', 'rouge2', 'rougeL'],
        use_stemmer=True
    )
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore

```python
from bert_score import score

def calculate_bertscore(
    references: list[str],
    hypotheses: list[str],
    **kwargs
) -> dict:
    """使用预训练模型计算 BERTScore。"""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### 自定义指标

```python
def calculate_groundedness(response: str, context: str, **kwargs) -> float:
    """检查响应是否基于提供的上下文。"""
    from transformers import pipeline

    nli = pipeline(
        "text-classification",
        model="microsoft/deberta-large-mnli"
    )

    result = nli(f"{context} [SEP] {response}")[0]

    # 返回响应被上下文蕴含的置信度
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text: str, **kwargs) -> float:
    """测量生成文本中的有害性。"""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # 返回最高有害性分数

def calculate_factuality(claim: str, sources: list[str], **kwargs) -> float:
    """根据来源验证事实性声明。"""
    from transformers import pipeline

    nli = pipeline("text-classification", model="facebook/bart-large-mnli")

    scores = []
    for source in sources:
        result = nli(f"{source}</s></s>{claim}")[0]
        if result['label'] == 'entailment':
            scores.append(result['score'])

    return max(scores) if scores else 0.0
```

## LLM 即评判者模式

### 单输出评估

```python
from anthropic import Anthropic
from pydantic import BaseModel, Field
import json

class QualityRating(BaseModel):
    accuracy: int = Field(ge=1, le=10, description="事实正确性")
    helpfulness: int = Field(ge=1, le=10, description="回答问题")
    clarity: int = Field(ge=1, le=10, description="写作清晰度和可理解性")
    reasoning: str = Field(description="简要说明")

async def llm_judge_quality(
    response: str,
    question: str,
    context: str = None
) -> QualityRating:
    """使用 Claude 评判响应质量。"""
    client = Anthropic()

    system = """你是 AI 响应的专家评估者。
    以准确性、有用性和清晰度对响应进行评分（1-10 分制）。
    为你的评分提供简要说明。"""

    prompt = f"""对以下响应进行评分：

问题：{question}
{f'上下文：{context}' if context else ''}
响应：{response}

以 JSON 格式提供评分：
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<简要说明>"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    return QualityRating(**json.loads(message.content[0].text))
```

### 成对比较

```python
from pydantic import BaseModel, Field
from typing import Literal

class ComparisonResult(BaseModel):
    winner: Literal["A", "B", "tie"]
    reasoning: str
    confidence: int = Field(ge=1, le=10)

async def compare_responses(
    question: str,
    response_a: str,
    response_b: str
) -> ComparisonResult:
    """使用 LLM 评判者比较两个响应。"""
    client = Anthropic()

    prompt = f"""比较这两个响应并确定哪个更好。

问题：{question}

响应 A：{response_a}

响应 B：{response_b}

考虑准确性、有用性和清晰度。

以 JSON 回答：
{{
  "winner": "A" 或 "B" 或 "tie",
  "reasoning": "<说明>",
  "confidence": <1-10>
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return ComparisonResult(**json.loads(message.content[0].text))
```

### 基于参考的评估

```python
class ReferenceEvaluation(BaseModel):
    semantic_similarity: float = Field(ge=0, le=1)
    factual_accuracy: float = Field(ge=0, le=1)
    completeness: float = Field(ge=0, le=1)
    issues: list[str]

async def evaluate_against_reference(
    response: str,
    reference: str,
    question: str
) -> ReferenceEvaluation:
    """根据黄金标准参考评估响应。"""
    client = Anthropic()

    prompt = f"""将响应与参考答案进行比较。

问题：{question}
参考答案：{reference}
待评估响应：{response}

评估：
1. 语义相似度（0-1）：意义的相似程度？
2. 事实准确性（0-1）：所有事实是否正确？
3. 完整性（0-1）：是否涵盖所有关键点？
4. 列出任何具体问题或错误。

以 JSON 回答：
{{
  "semantic_similarity": <0-1>,
  "factual_accuracy": <0-1>,
  "completeness": <0-1>,
  "issues": ["问题1", "问题2"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return ReferenceEvaluation(**json.loads(message.content[0].text))
```

## 人工评估框架

### 标注指南

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AnnotationTask:
    """人工标注任务的结构。"""
    response: str
    question: str
    context: Optional[str] = None

    def get_annotation_form(self) -> dict:
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "响应是否符合事实？"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "是否回答了问题？"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "是否逻辑一致？"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### 评分者间一致性

```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(
    rater1_scores: list[int],
    rater2_scores: list[int]
) -> dict:
    """计算评分者间一致性。"""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    if kappa < 0:
        interpretation = "差"
    elif kappa < 0.2:
        interpretation = "轻微"
    elif kappa < 0.4:
        interpretation = "一般"
    elif kappa < 0.6:
        interpretation = "中等"
    elif kappa < 0.8:
        interpretation = " substantial"
    else:
        interpretation = "几乎完美"

    return {
        "kappa": kappa,
        "interpretation": interpretation
    }
```

## A/B 测试

### 统计测试框架

```python
from scipy import stats
import numpy as np
from dataclasses import dataclass, field

@dataclass
class ABTest:
    variant_a_name: str = "A"
    variant_b_name: str = "B"
    variant_a_scores: list[float] = field(default_factory=list)
    variant_b_scores: list[float] = field(default_factory=list)

    def add_result(self, variant: str, score: float):
        """添加变体的评估结果。"""
        if variant == "A":
            self.variant_a_scores.append(score)
        else:
            self.variant_b_scores.append(score)

    def analyze(self, alpha: float = 0.05) -> dict:
        """执行统计分析。"""
        a_scores = np.array(self.variant_a_scores)
        b_scores = np.array(self.variant_b_scores)

        # T 检验
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # 效应量（Cohen's d）
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self._interpret_cohens_d(cohens_d),
            "winner": self.variant_b_name if np.mean(b_scores) > np.mean(a_scores) else self.variant_a_name
        }

    @staticmethod
    def _interpret_cohens_d(d: float) -> str:
        """解释 Cohen's d 效应量。"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "可忽略"
        elif abs_d < 0.5:
            return "小"
        elif abs_d < 0.8:
            return "中"
        else:
            return "大"
```

## 回归测试

### 回归检测

```python
from dataclasses import dataclass

@dataclass
class RegressionResult:
    metric: str
    baseline: float
    current: float
    change: float
    is_regression: bool

class RegressionDetector:
    def __init__(self, baseline_results: dict, threshold: float = 0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results: dict) -> dict:
        """检测新结果是否显示回归。"""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # 计算相对变化
            relative_change = (new_score - baseline_score) / baseline_score

            # 如果显著下降则标记
            is_regression = relative_change < -self.threshold
            if is_regression:
                regressions.append(RegressionResult(
                    metric=metric,
                    baseline=baseline_score,
                    current=new_score,
                    change=relative_change,
                    is_regression=True
                ))

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions,
            "summary": f"{len(regressions)} 个指标回归"
        }
```

## LangSmith 评估集成

```python
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# 初始化 LangSmith 客户端
client = Client()

# 创建数据集
dataset = client.create_dataset("qa_test_cases")
client.create_examples(
    inputs=[{"question": q} for q in questions],
    outputs=[{"answer": a} for a in expected_answers],
    dataset_id=dataset.id
)

# 定义评估器
evaluators = [
    LangChainStringEvaluator("qa"),           # QA 正确性
    LangChainStringEvaluator("context_qa"),   # 基于上下文的 QA
    LangChainStringEvaluator("cot_qa"),       # 思维链 QA
]

# 运行评估
async def target_function(inputs: dict) -> dict:
    result = await your_chain.ainvoke(inputs)
    return {"answer": result}

experiment_results = await evaluate(
    target_function,
    data=dataset.name,
    evaluators=evaluators,
    experiment_prefix="v1.0.0",
    metadata={"model": "claude-sonnet-4-5", "version": "1.0.0"}
)

print(f"平均分数：{experiment_results.aggregate_metrics['qa']['mean']}")
```

## 基准测试

### 运行基准

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class BenchmarkResult:
    metric: str
    mean: float
    std: float
    min: float
    max: float

class BenchmarkRunner:
    def __init__(self, benchmark_dataset: list[dict]):
        self.dataset = benchmark_dataset

    async def run_benchmark(
        self,
        model,
        metrics: list[Metric]
    ) -> dict[str, BenchmarkResult]:
        """在基准上运行模型并计算指标。"""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # 生成预测
            prediction = await model.predict(example["input"])

            # 计算每个指标
            for metric in metrics:
                score = metric.fn(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # 汇总结果
        return {
            metric: BenchmarkResult(
                metric=metric,
                mean=np.mean(scores),
                std=np.std(scores),
                min=min(scores),
                max=max(scores)
            )
            for metric, scores in results.items()
        }
```

## 资源

- [LangSmith 评估指南](https://docs.smith.langchain.com/evaluation)
- [RAGAS 框架](https://docs.ragas.io/)
- [DeepEval 库](https://docs.deepeval.com/)
- [Arize Phoenix](https://docs.arize.com/phoenix/)
- [HELM 基准](https://crfm.stanford.edu/helm/)

## 最佳实践

1. **多指标**：使用多样化的指标以获得全面视角
2. **代表性数据**：在真实世界、多样化的示例上进行测试
3. **基线**：始终与基线性能进行比较
4. **统计严谨性**：使用适当的统计测试进行比较
5. **持续评估**：集成到 CI/CD 流水线中
6. **人工验证**：将自动化指标与人工判断相结合
7. **错误分析**：调查失败案例以了解弱点
8. **版本控制**：跟踪随时间变化的评估结果

## 常见陷阱

- **单一指标痴迷**：以牺牲其他指标为代价优化一个指标
- **小样本量**：从太少的示例中得出结论
- **数据污染**：在训练数据上进行测试
- **忽略方差**：不考虑统计不确定性
- **指标不匹配**：使用与业务目标不一致的指标
- **位置偏差**：在成对评估中，随机化顺序
- **过度拟合提示词**：为测试集优化而非实际使用
