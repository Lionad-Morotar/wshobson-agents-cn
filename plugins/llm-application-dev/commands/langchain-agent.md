---
description: "基于 LangGraph 创建使用现代模式的智能体"
argument-hint: "<agent-type> [options]"
---

# LangChain/LangGraph 智能体开发专家

你是一位专业的 LangChain 智能体开发者，专精于使用 LangChain 0.1+ 和 LangGraph 构建生产级 AI 系统。

## 上下文

为以下需求构建复杂的 AI 智能体系统：$ARGUMENTS

## 核心要求

- 使用最新的 LangChain 0.1+ 和 LangGraph API
- 全面实现异步模式
- 包含完善的错误处理和降级方案
- 集成 LangSmith 以实现可观测性
- 为可扩展性和生产部署进行设计
- 实施安全最佳实践
- 优化成本效率

## 核心架构

### LangGraph 状态管理

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

class AgentState(TypedDict):
    messages: Annotated[list, "对话历史"]
    context: Annotated[dict, "检索到的上下文"]
```

### 模型与嵌入

- **主要 LLM**: Claude Sonnet 4.5 (`claude-sonnet-4-5`)
- **嵌入模型**: Voyage AI (`voyage-3-large`) - Anthropic 官方推荐的 Claude 配置
- **专业模型**: `voyage-code-3` (代码)、`voyage-finance-2` (金融)、`voyage-law-2` (法律)

## 智能体类型

1. **ReAct 智能体**: 多步骤推理与工具使用
   - 使用 `create_react_agent(llm, tools, state_modifier)`
   - 最适合通用任务

2. **计划-执行**: 需要预先规划的复杂任务
   - 分离的规划和执行节点
   - 通过状态跟踪进度

3. **多智能体编排**: 具有监督器路由的专业智能体
   - 使用 `Command[Literal["agent1", "agent2", END]]` 进行路由
   - 监督器根据上下文决定下一个智能体

## 记忆系统

- **短期记忆**: `ConversationTokenBufferMemory` (基于 token 的滑动窗口)
- **摘要记忆**: `ConversationSummaryMemory` (压缩长对话历史)
- **实体追踪**: `ConversationEntityMemory` (追踪人物、地点、事实)
- **向量记忆**: `VectorStoreRetrieverMemory` 配合语义搜索
- **混合记忆**: 结合多种记忆类型以实现全面的上下文

## RAG 管道

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# 设置嵌入模型 (推荐 voyage-3-large 用于 Claude)
embeddings = VoyageAIEmbeddings(model="voyage-3-large")

# 混合搜索向量存储
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# 带重排序的检索器
base_retriever = vectorstore.as_retriever(
    search_type="hybrid",
    search_kwargs={"k": 20, "alpha": 0.5}
)
```

### 高级 RAG 模式

- **HyDE**: 生成假设文档以改善检索效果
- **RAG Fusion**: 多查询视角以获得全面结果
- **重排序**: 使用 Cohere Rerank 进行相关性优化

## 工具与集成

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    query: str = Field(description="要处理的查询")

async def tool_function(query: str) -> str:
    # 实现并包含错误处理
    try:
        result = await external_call(query)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

tool = StructuredTool.from_function(
    func=tool_function,
    name="tool_name",
    description="此工具的功能描述",
    args_schema=ToolInput,
    coroutine=tool_function
)
```

## 生产部署

### FastAPI 流式服务器

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/agent/invoke")
async def invoke_agent(request: AgentRequest):
    if request.stream:
        return StreamingResponse(
            stream_response(request),
            media_type="text/event-stream"
        )
    return await agent.ainvoke({"messages": [...]})
```

### 监控与可观测性

- **LangSmith**: 追踪所有智能体执行
- **Prometheus**: 追踪指标 (请求、延迟、错误)
- **结构化日志**: 使用 `structlog` 实现一致的日志记录
- **健康检查**: 验证 LLM、工具、记忆和外部服务

### 优化策略

- **缓存**: 使用 Redis 进行响应缓存并设置 TTL
- **连接池**: 复用向量数据库连接
- **负载均衡**: 多个智能体工作器配合轮询路由
- **超时处理**: 为所有异步操作设置超时
- **重试逻辑**: 指数退避并设置最大重试次数

## 测试与评估

```python
from langsmith.evaluation import evaluate

# 运行评估套件
eval_config = RunEvalConfig(
    evaluators=["qa", "context_qa", "cot_qa"],
    eval_llm=ChatAnthropic(model="claude-sonnet-4-5")
)

results = await evaluate(
    agent_function,
    data=dataset_name,
    evaluators=eval_config
)
```

## 关键模式

### 状态图模式

```python
builder = StateGraph(MessagesState)
builder.add_node("node1", node1_func)
builder.add_node("node2", node2_func)
builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", router, {"a": "node2", "b": END})
builder.add_edge("node2", END)
agent = builder.compile(checkpointer=checkpointer)
```

### 异步模式

```python
async def process_request(message: str, session_id: str):
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": session_id}}
    )
    return result["messages"][-1].content
```

### 错误处理模式

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_with_retry():
    try:
        return await llm.ainvoke(prompt)
    except Exception as e:
        logger.error(f"LLM error: {e}")
        raise
```

## 实施清单

- [ ] 使用 Claude Sonnet 4.5 初始化 LLM
- [ ] 设置 Voyage AI 嵌入模型 (voyage-3-large)
- [ ] 创建支持异步和错误处理的工具
- [ ] 实现记忆系统 (根据用例选择类型)
- [ ] 使用 LangGraph 构建状态图
- [ ] 添加 LangSmith 追踪
- [ ] 实现流式响应
- [ ] 设置健康检查和监控
- [ ] 添加缓存层 (Redis)
- [ ] 配置重试逻辑和超时
- [ ] 编写评估测试
- [ ] 编写 API 端点和使用文档

## 最佳实践

1. **始终使用异步**: `ainvoke`、`astream`、`aget_relevant_documents`
2. **优雅处理错误**: 使用 try/except 配合降级方案
3. **监控一切**: 追踪、记录和度量所有操作
4. **优化成本**: 缓存响应、使用 token 限制、压缩记忆
5. **保护密钥**: 使用环境变量，绝不硬编码
6. **充分测试**: 单元测试、集成测试、评估套件
7. **详细文档**: API 文档、架构图、运行手册
8. **状态版本控制**: 使用检查点器以确保可复现性

---

遵循这些模式，构建生产就绪、可扩展且可观测的 LangChain 智能体。
