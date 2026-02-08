# 提示模板库

## 分类模板

### 情感分析

```
将以下文本的情感分类为 Positive（积极）、Negative（消极）或 Neutral（中性）。

文本：{text}

情感：
```

### 意图识别

```
从以下消息中确定用户的意图。

可能的意图：{intent_list}

消息：{message}

意图：
```

### 主题分类

```
将以下文章归类到以下类别之一：{categories}

文章：
{article}

类别：
```

## 提取模板

### 命名实体识别

```
从文本中提取所有命名实体并进行分类。

文本：{text}

实体（JSON 格式）：
{
  "persons": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

### 结构化数据提取

```
从招聘信息中提取结构化信息。

招聘信息：
{posting}

提取的信息（JSON）：
{
  "title": "",
  "company": "",
  "location": "",
  "salary_range": "",
  "requirements": [],
  "responsibilities": []
}
```

## 生成模板

### 邮件生成

```
写一封专业的 {email_type} 邮件。

收件人：{recipient}
上下文：{context}
需包含的关键点：
{key_points}

邮件：
主题：
正文：
```

### 代码生成

```
为以下任务生成 {language} 代码：

任务：{task_description}

要求：
{requirements}

需包含：
- 错误处理
- 输入验证
- 内联注释

代码：
```

### 创意写作

```
写一篇 {length} 词的 {style} 风格故事，主题为 {topic}。

需包含以下元素：
- {element_1}
- {element_2}
- {element_3}

故事：
```

## 转换模板

### 摘要

```
用 {num_sentences} 句话总结以下文本。

文本：
{text}

摘要：
```

### 上下文翻译

```
将以下 {source_lang} 文本翻译为 {target_lang}。

上下文：{context}
语气：{tone}

文本：{text}

译文：
```

### 格式转换

```
将以下 {source_format} 转换为 {target_format}。

输入：
{input_data}

输出（{target_format}）：
```

## 分析模板

### 代码审查

```
审查以下代码的：
1. Bug 和错误
2. 性能问题
3. 安全漏洞
4. 最佳实践违规

代码：
{code}

审查意见：
```

### SWOT 分析

```
对以下主题进行 SWOT 分析：{subject}

上下文：{context}

分析：
优势（Strengths）：
-

劣势（Weaknesses）：
-

机会（Opportunities）：
-

威胁（Threats）：
-
```

## 问答模板

### RAG 模板

```
根据提供的上下文回答问题。如果上下文信息不足，请说明。

上下文：
{context}

问题：{question}

答案：
```

### 多轮问答

```
之前的对话：
{conversation_history}

新问题：{question}

答案（从对话自然延续）：
```

## 专用模板

### SQL 查询生成

```
为以下请求生成 SQL 查询。

数据库架构：
{schema}

请求：{request}

SQL 查询：
```

### 正则表达式创建

```
创建一个正则表达式模式以匹配：{requirement}

应该匹配的测试用例：
{positive_examples}

不应匹配的测试用例：
{negative_examples}

正则表达式模式：
```

### API 文档

```
为此函数生成 API 文档：

代码：
{function_code}

文档（遵循 {doc_format} 格式）：
```

## 通过填写 {variables} 来使用这些模板
