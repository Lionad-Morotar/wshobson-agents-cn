---
name: rag-implementation
description: 使用向量数据库和语义搜索构建 LLM 应用的检索增强生成（RAG）系统。在实现基于知识的 AI、构建文档问答系统或将 LLM 与外部知识库集成时使用。
---

# RAG 实现

掌握检索增强生成（RAG）以构建能够使用外部知识源提供准确、有根有据的响应的 LLM 应用。

## 何时使用此技能

- 为专有文档构建问答系统
- 创建具有当前事实信息的聊天机器人
- 使用自然语言查询实现语义搜索
- 通过有根有据的响应减少幻觉
- 使 LLM 能够访问领域特定知识
- 构建文档助手
- 创建带有来源引用的研究工具

## 核心组件

### 1. 向量数据库

**用途**：高效存储和检索文档嵌入

**选项：**

- **Pinecone**：托管、可扩展、无服务器
- **Weaviate**：开源、混合搜索、GraphQL
- **Milvus**：高性能、本地部署
- **Chroma**：轻量级、易于使用、本地开发
- **Qdrant**：快速、可过滤搜索、基于 Rust
- **pgvector**：PostgreSQL 扩展、SQL 集成

### 2. 嵌入

**用途**：将文本转换为数值向量以进行相似性搜索

**模型 (2026)：**
| 模型 | 维度 | 最适用于 |
|-------|------------|----------|
| **voyage-3-large** | 1024 | Claude 应用（Anthropic 推荐） |
| **voyage-code-3** | 1024 | 代码搜索 |
| **text-embedding-3-large** | 3072 | OpenAI 应用、高准确度 |
| **text-embedding-3-small** | 1536 | OpenAI 应用、成本效益 |
| **bge-large-en-v1.5** | 1024 | 开源、本地部署 |
| **multilingual-e5-large** | 1024 | 多语言支持 |

### 3. 检索策略

**方法：**

- **密集检索**：通过嵌入进行语义相似性
- **稀疏检索**：关键词匹配（BM25、TF-IDF）
- **混合搜索**：结合密集 + 稀疏并使用加权融合
- **多查询**：生成多个查询变体
- **HyDE**：生成假设文档以获得更好的检索

### 4. 重排序

**用途**：通过重新排序结果提高检索质量

**方法：**

- **交叉编码器**：基于 BERT 的重排序（ms-marco-MiniLM）
- **Cohere Rerank**：基于 API 的重排序
- **最大边际相关性（MMR）**：多样性 + 相关性
- **基于 LLM**：使用 LLM 对相关性进行评分

## LangGraph 快速开始

```python
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict, Annotated

class RAGState(TypedDict):
    question: str
    context: list[Document]
    answer: str

# 初始化组件
llm = ChatAnthropic(model="claude-sonnet-4-5")
embeddings = VoyageAIEmbeddings(model="voyage-3-large")
vectorstore = PineconeVectorStore(index_name="docs", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG 提示
rag_prompt = ChatPromptTemplate.from_template(
    """根据以下上下文回答问题。如果无法回答，请说明。

    上下文：
    {context}

    问题：{question}

    回答："""
)

async def retrieve(state: RAGState) -> RAGState:
    """检索相关文档。"""
    docs = await retriever.ainvoke(state["question"])
    return {"context": docs}

async def generate(state: RAGState) -> RAGState:
    """从上下文生成回答。"""
    context_text = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.format_messages(
        context=context_text,
        question=state["question"]
    )
    response = await llm.ainvoke(messages)
    return {"answer": response.content}

# 构建 RAG 图
builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

rag_chain = builder.compile()

# 使用
result = await rag_chain.ainvoke({"question": "主要功能有哪些？"})
print(result["answer"])
```

## 高级 RAG 模式

### 模式 1：使用 RRF 的混合搜索

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# 稀疏检索器（BM25 用于关键词匹配）
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 10

# 密集检索器（嵌入用于语义搜索）
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# 使用倒数排名融合权重组合
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.3, 0.7]  # 30% 关键词，70% 语义
)
```

### 模式 2：多查询检索

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# 生成多个查询视角以获得更好的召回率
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm
)

# 单个查询 → 多个变体 → 组合结果
results = await multi_query_retriever.ainvoke("主要主题是什么？")
```

### 模式 3：上下文压缩

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# 压缩器仅提取相关部分
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

# 仅返回文档的相关部分
compressed_docs = await compression_retriever.ainvoke("特定查询")
```

### 模式 4：父文档检索器

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 小块用于精确检索，大块用于上下文
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

# 父文档存储
docstore = InMemoryStore()

parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# 添加文档（分割子块，存储父块）
await parent_retriever.aadd_documents(documents)

# 检索返回具有完整上下文的父文档
results = await parent_retriever.ainvoke("查询")
```

### 模式 5：HyDE（假设文档嵌入）

```python
from langchain_core.prompts import ChatPromptTemplate

class HyDEState(TypedDict):
    question: str
    hypothetical_doc: str
    context: list[Document]
    answer: str

hyde_prompt = ChatPromptTemplate.from_template(
    """编写一个详细的段落来回答这个问题：

    问题：{question}

    段落："""
)

async def generate_hypothetical(state: HyDEState) -> HyDEState:
    """生成假设文档以获得更好的检索。"""
    messages = hyde_prompt.format_messages(question=state["question"])
    response = await llm.ainvoke(messages)
    return {"hypothetical_doc": response.content}

async def retrieve_with_hyde(state: HyDEState) -> HyDEState:
    """使用假设文档进行检索。"""
    # 使用假设文档而不是原始查询进行检索
    docs = await retriever.ainvoke(state["hypothetical_doc"])
    return {"context": docs}

# 构建 HyDE RAG 图
builder = StateGraph(HyDEState)
builder.add_node("hypothetical", generate_hypothetical)
builder.add_node("retrieve", retrieve_with_hyde)
builder.add_node("generate", generate)
builder.add_edge(START, "hypothetical")
builder.add_edge("hypothetical", "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

hyde_rag = builder.compile()
```

## 文档分块策略

### 递归字符文本分割器

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", "", ""]  # 按顺序尝试
)

chunks = splitter.split_documents(documents)
```

### 基于 Token 的分割

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    encoding_name="cl100k_base"  # OpenAI tiktoken 编码
)
```

### 语义分块

```python
from langchain_experimental.text_splitter import SemanticChunker

splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)
```

### Markdown 标题分割器

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "标题 1"),
    ("##", "标题 2"),
    ("###", "标题 3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)
```

## 向量存储配置

### Pinecone（无服务器）

```python
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# 初始化 Pinecone 客户端
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# 如果需要则创建索引
if "my-index" not in pc.list_indexes().names():
    pc.create_index(
        name="my-index",
        dimension=1024,  # voyage-3-large 维度
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# 创建向量存储
index = pc.Index("my-index")
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
```

### Weaviate

```python
import weaviate
from langchain_weaviate import WeaviateVectorStore

client = weaviate.connect_to_local()  # 或 connect_to_weaviate_cloud()

vectorstore = WeaviateVectorStore(
    client=client,
    index_name="Documents",
    text_key="content",
    embedding=embeddings
)
```

### Chroma（本地开发）

```python
from langchain_chroma import Chroma

vectorstore = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

### pgvector（PostgreSQL）

```python
from langchain_postgres.vectorstores import PGVector

connection_string = "postgresql+psycopg://user:pass@localhost:5432/vectordb"

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection=connection_string,
)
```

## 检索优化

### 1. 元数据过滤

```python
from langchain_core.documents import Document

# 在索引期间添加元数据
docs_with_metadata = []
for doc in documents:
    doc.metadata.update({
        "source": doc.metadata.get("source", "unknown"),
        "category": determine_category(doc.page_content),
        "date": datetime.now().isoformat()
    })
    docs_with_metadata.append(doc)

# 在检索期间过滤
results = await vectorstore.asimilarity_search(
    "查询",
    filter={"category": "technical"},
    k=5
)
```

### 2. 最大边际相关性（MMR）

```python
# 平衡相关性和多样性
results = await vectorstore.amax_marginal_relevance_search(
    "查询",
    k=5,
    fetch_k=20,  # 获取 20 个，返回前 5 个多样化的
    lambda_mult=0.5  # 0=最大多样性，1=最大相关性
)
```

### 3. 使用交叉编码器重排序

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

async def retrieve_and_rerank(query: str, k: int = 5) -> list[Document]:
    # 获取初始结果
    candidates = await vectorstore.asimilarity_search(query, k=20)

    # 重排序
    pairs = [[query, doc.page_content] for doc in candidates]
    scores = reranker.predict(pairs)

    # 按分数排序并取前 k 个
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:k]]
```

### 4. Cohere 重排序

```python
from langchain.retrievers import CohereRerank
from langchain_cohere import CohereRerank

reranker = CohereRerank(model="rerank-english-v3.0", top_n=5)

# 用重排序包装检索器
reranked_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 20})
)
```

## RAG 提示工程

### 带引用的上下文提示

```python
rag_prompt = ChatPromptTemplate.from_template(
    """根据以下上下文回答问题。使用 [1]、[2] 等格式包含引用。

    如果无法根据上下文回答，请说"我没有足够的信息"。

    上下文：
    {context}

    问题：{question}

    说明：
    1. 仅使用上下文中的信息
    2. 使用 [1]、[2] 格式引用来源
    3. 如果不确定，表达不确定性

    回答（带引用）："""
)
```

### RAG 的结构化输出

```python
from pydantic import BaseModel, Field

class RAGResponse(BaseModel):
    answer: str = Field(description="基于上下文的回答")
    confidence: float = Field(description="置信度分数 0-1")
    sources: list[str] = Field(description="使用的源文档 ID")
    reasoning: str = Field(description="回答的简要推理")

# 与结构化输出一起使用
structured_llm = llm.with_structured_output(RAGResponse)
```

## 评估指标

```python
from typing import TypedDict

class RAGEvalMetrics(TypedDict):
    retrieval_precision: float  # 相关文档 / 检索文档
    retrieval_recall: float     # 检索到的相关 / 总相关
    answer_relevance: float     # 回答解决问题
    faithfulness: float         # 回答基于上下文
    context_relevance: float    # 上下文与问题相关

async def evaluate_rag_system(
    rag_chain,
    test_cases: list[dict]
) -> RAGEvalMetrics:
    """在测试用例上评估 RAG 系统。"""
    metrics = {k: [] for k in RAGEvalMetrics.__annotations__}

    for test in test_cases:
        result = await rag_chain.ainvoke({"question": test["question"]})

        # 检索指标
        retrieved_ids = {doc.metadata["id"] for doc in result["context"]}
        relevant_ids = set(test["relevant_doc_ids"])

        precision = len(retrieved_ids & relevant_ids) / len(retrieved_ids)
        recall = len(retrieved_ids & relevant_ids) / len(relevant_ids)

        metrics["retrieval_precision"].append(precision)
        metrics["retrieval_recall"].append(recall)

        # 使用 LLM 作为评估器进行质量指标评估
        quality = await evaluate_answer_quality(
            question=test["question"],
            answer=result["answer"],
            context=result["context"],
            expected=test.get("expected_answer")
        )
        metrics["answer_relevance"].append(quality["relevance"])
        metrics["faithfulness"].append(quality["faithfulness"])
        metrics["context_relevance"].append(quality["context_relevance"])

    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

## 资源

- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [LangGraph RAG 示例](https://langchain-ai.github.io/langgraph/tutorials/rag/)
- [Pinecone 最佳实践](https://docs.pinecone.io/guides/get-started/overview)
- [Voyage AI 嵌入](https://docs.voyageai.com/)
- [RAG 评估指南](https://docs.ragas.io/)

## 最佳实践

1. **块大小**：在上下文（较大）和特异性（较小）之间平衡 - 通常为 500-1000 token
2. **重叠**：使用 10-20% 的重叠以保留边界处的上下文
3. **元数据**：包括来源、页面、时间戳用于过滤和调试
4. **混合搜索**：结合语义和关键词搜索以获得最佳召回率
5. **重排序**：对精度关键的应用使用交叉编码器重排序
6. **引用**：始终返回源文档以保持透明度
7. **评估**：持续测试检索质量和回答准确性
8. **监控**：在生产环境中跟踪检索指标和延迟

## 常见问题

- **检索效果差**：检查嵌入质量、块大小、查询表述
- **结果不相关**：添加元数据过滤、使用混合搜索、重排序
- **信息缺失**：确保文档正确索引、检查分块
- **查询缓慢**：优化向量存储、使用缓存、减少 k
- **幻觉**：改进基础提示、添加验证步骤
- **上下文过长**：使用压缩或父文档检索器
