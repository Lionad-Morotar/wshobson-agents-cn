---
name: prompt-engineering-patterns
description: 掌握高级提示工程技术，以最大化生产环境中 LLM 的性能、可靠性和可控性。在优化提示词、改进 LLM 输出或设计生产环境提示模板时使用。
---

# 提示工程模式

掌握高级提示工程技术，以最大化 LLM 的性能、可靠性和可控性。

## 何时使用此技能

- 为生产环境 LLM 应用设计复杂提示词
- 优化提示词性能和一致性
- 实现结构化推理模式（思维链、思维树）
- 构建具有动态示例选择的少样本学习系统
- 创建具有变量插值的可复用提示模板
- 调试和优化产生不一致输出的提示词
- 为专用 AI 助手实现系统提示词
- 使用结构化输出（JSON 模式）进行可靠解析

## 核心能力

### 1. 少样本学习

- 示例选择策略（语义相似度、多样性采样）
- 在上下文窗口约束下平衡示例数量
- 构建有效的输入输出对演示
- 从知识库动态检索示例
- 通过策略性示例选择处理边缘情况

### 2. 思维链提示

- 逐步推理引导
- 零样本 CoT 使用"让我们一步步思考"
- 带推理轨迹的少样本 CoT
- 自一致性技术（采样多条推理路径）
- 验证和校验步骤

### 3. 结构化输出

- 用于可靠解析的 JSON 模式
- Pydantic schema 强制
- 类型安全的响应处理
- 针对格式错误输出的错误处理

### 4. 提示词优化

- 迭代优化工作流
- 提示词变体的 A/B 测试
- 测量提示词性能指标（准确性、一致性、延迟）
- 在保持质量的同时减少 token 使用
- 处理边缘情况和失败模式

### 5. 模板系统

- 变量插值和格式化
- 条件式提示词段落
- 多轮对话模板
- 基于角色的提示词组合
- 模块化提示词组件

### 6. 系统提示词设计

- 设置模型行为和约束
- 定义输出格式和结构
- 建立角色和专业能力
- 安全指南和内容策略
- 上下文设置和背景信息

## 快速开始

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 定义结构化输出 schema
class SQLQuery(BaseModel):
    query: str = Field(description="SQL 查询语句")
    explanation: str = Field(description="查询功能的简要说明")
    tables_used: list[str] = Field(description="引用的表列表")

# 初始化支持结构化输出的模型
llm = ChatAnthropic(model="claude-sonnet-4-5")
structured_llm = llm.with_structured_output(SQLQuery)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的 SQL 开发者。生成高效、安全的 SQL 查询。
    始终使用参数化查询以防止 SQL 注入。
    简要说明你的推理过程。"""),
    ("user", "将此转换为 SQL: {query}")
])

# 创建链
chain = prompt | structured_llm

# 使用
result = await chain.ainvoke({
    "query": "查找所有过去 30 天内注册的用户"
})
print(result.query)
print(result.explanation)
```

## 关键模式

### 模式 1: 使用 Pydantic 的结构化输出

```python
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import Literal
import json

class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    key_phrases: list[str]
    reasoning: str

async def analyze_sentiment(text: str) -> SentimentAnalysis:
    """使用结构化输出分析情感。"""
    client = Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""分析此文本的情感。

文本: {text}

使用符合以下 schema 的 JSON 响应:
{{
    "sentiment": "positive" | "negative" | "neutral",
    "confidence": 0.0-1.0,
    "key_phrases": ["短语1", "短语2"],
    "reasoning": "简要说明"
}}"""
        }]
    )

    return SentimentAnalysis(**json.loads(message.content[0].text))
```

### 模式 2: 带自验证的思维链

```python
from langchain_core.prompts import ChatPromptTemplate

cot_prompt = ChatPromptTemplate.from_template("""
逐步解决这个问题。

问题: {problem}

说明:
1. 将问题分解为清晰的步骤
2. 逐步完成每个步骤并展示推理过程
3. 陈述你的最终答案
4. 通过对照原问题检查来验证你的答案

按以下格式组织响应:
## 步骤
[你的逐步推理过程]

## 答案
[你的最终答案]

## 验证
[检查你的答案是否正确]
""")
```

### 模式 3: 动态示例选择的少样本

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_chroma import Chroma

# 使用语义相似度创建示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples=[
        {"input": "如何重置密码?", "output": "前往 设置 > 安全 > 重置密码"},
        {"input": "在哪里可以查看我的订单历史?", "output": "前往 账户 > 订单"},
        {"input": "如何联系客服?", "output": "点击 帮助 > 联系我们 或发送邮件至 support@example.com"},
    ],
    embeddings=VoyageAIEmbeddings(model="voyage-3-large"),
    vectorstore_cls=Chroma,
    k=2  # 选择 2 个最相似的示例
)

async def get_few_shot_prompt(query: str) -> str:
    """构建具有动态选择示例的提示词。"""
    examples = await example_selector.aselect_examples({"input": query})

    examples_text = "\n".join(
        f"用户: {ex['input']}\n助手: {ex['output']}"
        for ex in examples
    )

    return f"""你是一个有帮助的客服助手。

以下是一些示例交互:
{examples_text}

现在响应此查询:
用户: {query}
助手:"""
```

### 模式 4: 渐进式披露

从简单提示词开始，仅在需要时增加复杂度:

```python
PROMPT_LEVELS = {
    # 级别 1: 直接指令
    "simple": "总结这篇文章: {text}",

    # 级别 2: 添加约束
    "constrained": """用 3 个要点总结这篇文章,重点关注:
- 关键发现
- 主要结论
- 实践意义

文章: {text}""",

    # 级别 3: 添加推理
    "reasoning": """仔细阅读这篇文章。
1. 首先,确定主要主题和论点
2. 然后,提取关键支撑点
3. 最后,用 3 个要点进行总结

文章: {text}

总结:""",

    # 级别 4: 添加示例
    "few_shot": """阅读文章并提供简洁的总结。

示例:
文章: "新研究表明,经常锻炼可以将焦虑减少高达 40%..."
总结:
• 经常锻炼可将焦虑减少高达 40%
• 每周 3 次、每次 30 分钟的中等强度活动即可
• 开始后 2 周内即可见效

现在总结这篇文章:
文章: {text}

总结:"""
}
```

### 模式 5: 错误恢复和回退

```python
from pydantic import BaseModel, ValidationError
import json

class ResponseWithConfidence(BaseModel):
    answer: str
    confidence: float
    sources: list[str]
    alternative_interpretations: list[str] = []

ERROR_RECOVERY_PROMPT = """
根据提供的上下文回答问题。

上下文: {context}
问题: {question}

说明:
1. 如果你能有信心地回答 (>0.8),提供直接答案
2. 如果你有一定信心 (0.5-0.8),提供你的最佳答案并说明限制
3. 如果你不确定 (<0.5),说明缺少哪些信息
4. 如果问题有歧义,始终提供替代解释

使用 JSON 响应:
{{
    "answer": "你的答案或'我无法从上下文中确定这一点'",
    "confidence": 0.0-1.0,
    "sources": ["相关上下文摘录"],
    "alternative_interpretations": ["如果问题有歧义"]
}}
"""

async def answer_with_fallback(
    context: str,
    question: str,
    llm
) -> ResponseWithConfidence:
    """使用错误恢复和回退机制回答。"""
    prompt = ERROR_RECOVERY_PROMPT.format(context=context, question=question)

    try:
        response = await llm.ainvoke(prompt)
        return ResponseWithConfidence(**json.loads(response.content))
    except (json.JSONDecodeError, ValidationError) as e:
        # 回退: 尝试在没有结构的情况下提取答案
        simple_prompt = f"基于: {context}\n\n回答: {question}"
        simple_response = await llm.ainvoke(simple_prompt)
        return ResponseWithConfidence(
            answer=simple_response.content,
            confidence=0.5,
            sources=["回退提取"],
            alternative_interpretations=[]
        )
```

### 模式 6: 基于角色的系统提示词

```python
SYSTEM_PROMPTS = {
    "analyst": """你是一位高级数据分析师,专精于 SQL、Python 和商业智能。

你的职责:
- 编写高效、文档完善的查询
- 解释你的分析方法
- 突出关键见解和建议
- 标记任何数据质量问题

沟通风格:
- 在讨论方法时精确且技术化
- 将技术发现转化为业务影响
- 在有帮助时使用清晰的可视化""",

    "assistant": """你是一个专注于准确性和清晰度的有用 AI 助手。

核心原则:
- 在提出事实声明时始终引用来源
- 承认不确定性而不是猜测
- 当请求有歧义时询问澄清问题
- 为复杂主题提供逐步说明

约束:
- 不提供医疗、法律或财务建议
- 适当地重定向有害请求
- 保护用户隐私""",

    "code_reviewer": """你是一位正在进行代码审查的高级软件工程师。

审查标准:
- 正确性: 代码是否按预期工作?
- 安全性: 是否存在任何漏洞?
- 性能: 是否存在效率问题?
- 可维护性: 代码是否可读且结构良好?
- 最佳实践: 是否遵循语言惯用法?

输出格式:
1. 总结评估(批准/请求更改)
2. 关键问题(必须修复)
3. 建议(最好有)
4. 正面反馈(做得好的地方)"""
}
```

## 集成模式

### 与 RAG 系统集成

```python
RAG_PROMPT = """你是一个基于提供的上下文回答问题的知识渊博的助手。

上下文(从知识库检索):
{context}

说明:
1. 仅基于提供的上下文回答
2. 如果上下文不包含答案,说"我的知识库中没有相关信息"
3. 使用 [1]、[2] 符号引用具体段落
4. 如果问题有歧义,请求澄清

问题: {question}

答案:"""
```

### 与验证和校验集成

```python
VALIDATED_PROMPT = """完成以下任务:

任务: {task}

生成响应后,验证其是否满足所有这些标准:
✓ 直接解决原始请求
✓ 不包含事实错误
✓ 适当详细(不太简略,不太冗长)
✓ 使用正确格式
✓ 安全且适当

如果验证在任何标准上失败,在响应前修改。

响应:"""
```

## 性能优化

### Token 效率

```python
# 之前: 冗长的提示词(150+ tokens)
verbose_prompt = """
我想请你获取以下文本并为我提供一个全面的
要点总结。总结应捕捉关键思想和重要细节
同时简洁易懂。
"""

# 之后: 简洁的提示词(30 tokens)
concise_prompt = """简洁地总结要点:

{text}

总结:"""
```

### 缓存公共前缀

```python
from anthropic import Anthropic

client = Anthropic()

# 对重复的系统提示词使用提示词缓存
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": user_query}]
)
```

## 最佳实践

1. **明确具体**: 模糊的提示词产生不一致的结果
2. **展示而非讲述**: 示例比描述更有效
3. **使用结构化输出**: 使用 Pydantic 强制 schema 以提高可靠性
4. **广泛测试**: 在多样化、具有代表性的输入上进行评估
5. **快速迭代**: 小改动可能产生大影响
6. **监控性能**: 在生产环境中跟踪指标
7. **版本控制**: 将提示词视为代码并进行适当的版本管理
8. **记录意图**: 解释为什么提示词采用这样的结构

## 常见陷阱

- **过度工程化**: 在尝试简单提示词之前就从复杂提示词开始
- **示例污染**: 使用与目标任务不匹配的示例
- **上下文溢出**: 使用过多示例超出 token 限制
- **歧义指令**: 留出多种解释空间
- **忽略边缘情况**: 不在异常或边界输入上测试
- **无错误处理**: 假设输出总是格式良好
- **硬编码值**: 不参数化提示词以供复用

## 成功指标

为你的提示词跟踪这些 KPI:

- **准确性**: 输出的正确性
- **一致性**: 在相似输入上的可复现性
- **延迟**: 响应时间(P50、P95、P99)
- **Token 使用**: 每次请求的平均 token 数
- **成功率**: 有效、可解析输出的百分比
- **用户满意度**: 评分和反馈

## 资源

- [Anthropic 提示工程指南](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Claude 提示词缓存](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [OpenAI 提示工程](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain 提示词](https://python.langchain.com/docs/concepts/prompts/)
