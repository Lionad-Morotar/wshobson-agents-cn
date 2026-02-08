---
description: "构建具有 NLU、对话管理和集成功能的 AI 助手应用"
argument-hint: "<助手类型> [选项]"
---

# AI 助手开发

你是一位 AI 助手开发专家，专注于创建智能对话界面、聊天机器人和 AI 驱动的应用。设计全面的 AI 助手解决方案，具备自然语言理解、上下文管理和无缝集成功能。

## 上下文

用户需要开发一个具有自然语言能力、智能响应和实用功能的 AI 助手或聊天机器人。专注于创建能为用户提供真实价值的生产级助手。

## 需求

$ARGUMENTS

## 指令

### 1. AI 助手架构

设计全面的助手架构：

**助手架构框架**

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio

@dataclass
class ConversationContext:
    """维护对话状态和上下文"""
    user_id: str
    session_id: str
    messages: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    conversation_state: Dict[str, Any]
    metadata: Dict[str, Any]

class AIAssistantArchitecture:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.components = self._initialize_components()

    def design_architecture(self):
        """设计全面的 AI 助手架构"""
        return {
            'core_components': {
                'nlu': self._design_nlu_component(),
                'dialog_manager': self._design_dialog_manager(),
                'response_generator': self._design_response_generator(),
                'context_manager': self._design_context_manager(),
                'integration_layer': self._design_integration_layer()
            },
            'data_flow': self._design_data_flow(),
            'deployment': self._design_deployment_architecture(),
            'scalability': self._design_scalability_features()
        }

    def _design_nlu_component(self):
        """自然语言理解组件"""
        return {
            'intent_recognition': {
                'model': 'transformer-based classifier',
                'features': [
                    'Multi-intent detection',
                    'Confidence scoring',
                    'Fallback handling'
                ],
                'implementation': '''
class IntentClassifier:
    def __init__(self, model_path: str, *, config: Optional[Dict[str, Any]] = None):
        self.model = self.load_model(model_path)
        self.intents = self.load_intent_schema()
        default_config = {"threshold": 0.65}
        self.config = {**default_config, **(config or {})}

    async def classify(self, text: str) -> Dict[str, Any]:
        # 预处理文本
        processed = self.preprocess(text)

        # 获取模型预测
        predictions = await self.model.predict(processed)

        # 提取意图及置信度
        intents = []
        for intent, confidence in predictions:
            if confidence > self.config['threshold']:
                intents.append({
                    'name': intent,
                    'confidence': confidence,
                    'parameters': self.extract_parameters(text, intent)
                })

        return {
            'intents': intents,
            'primary_intent': intents[0] if intents else None,
            'requires_clarification': len(intents) > 1
        }
'''
            },
            'entity_extraction': {
                'model': 'NER with custom entities',
                'features': [
                    'Domain-specific entities',
                    'Contextual extraction',
                    'Entity resolution'
                ]
            },
            'sentiment_analysis': {
                'model': 'Fine-tuned sentiment classifier',
                'features': [
                    'Emotion detection',
                    'Urgency classification',
                    'User satisfaction tracking'
                ]
            }
        }

    def _design_dialog_manager(self):
        """对话管理系统"""
        return '''
class DialogManager:
    """管理对话流程和状态"""

    def __init__(self):
        self.state_machine = ConversationStateMachine()
        self.policy_network = DialogPolicy()

    async def process_turn(self,
                          context: ConversationContext,
                          nlu_result: Dict[str, Any]) -> Dict[str, Any]:
        # 确定当前状态
        current_state = self.state_machine.get_state(context)

        # 应用对话策略
        action = await self.policy_network.select_action(
            current_state,
            nlu_result,
            context
        )

        # 执行动作
        result = await self.execute_action(action, context)

        # 更新状态
        new_state = self.state_machine.transition(
            current_state,
            action,
            result
        )

        return {
            'action': action,
            'new_state': new_state,
            'response_data': result
        }

    async def execute_action(self, action: str, context: ConversationContext):
        """执行对话动作"""
        action_handlers = {
            'greet': self.handle_greeting,
            'provide_info': self.handle_information_request,
            'clarify': self.handle_clarification,
            'confirm': self.handle_confirmation,
            'execute_task': self.handle_task_execution,
            'end_conversation': self.handle_conversation_end
        }

        handler = action_handlers.get(action, self.handle_unknown)
        return await handler(context)
'''
```

### 2. 自然语言处理

实现高级 NLP 功能：

**NLP 流水线实现**

```python
class NLPPipeline:
    def __init__(self):
        self.tokenizer = self._initialize_tokenizer()
        self.embedder = self._initialize_embedder()
        self.models = self._load_models()

    async def process_message(self, message: str, context: ConversationContext):
        """通过 NLP 流水线处理用户消息"""
        # 分词和预处理
        tokens = self.tokenizer.tokenize(message)

        # 生成嵌入
        embeddings = await self.embedder.embed(tokens)

        # 并行处理 NLP 任务
        tasks = [
            self.detect_intent(embeddings),
            self.extract_entities(tokens, embeddings),
            self.analyze_sentiment(embeddings),
            self.detect_language(tokens),
            self.check_spelling(tokens)
        ]

        results = await asyncio.gather(*tasks)

        return {
            'intent': results[0],
            'entities': results[1],
            'sentiment': results[2],
            'language': results[3],
            'corrections': results[4],
            'original_message': message,
            'processed_tokens': tokens
        }

    async def detect_intent(self, embeddings):
        """高级意图检测"""
        # 多标签分类
        intent_scores = await self.models['intent_classifier'].predict(embeddings)

        # 层次化意图检测
        primary_intent = self.get_primary_intent(intent_scores)
        sub_intents = self.get_sub_intents(primary_intent, embeddings)

        return {
            'primary': primary_intent,
            'secondary': sub_intents,
            'confidence': max(intent_scores.values()),
            'all_scores': intent_scores
        }

    def extract_entities(self, tokens, embeddings):
        """提取和解析实体"""
        # 命名实体识别
        entities = self.models['ner'].extract(tokens, embeddings)

        # 实体链接和解析
        resolved_entities = []
        for entity in entities:
            resolved = self.resolve_entity(entity)
            resolved_entities.append({
                'text': entity['text'],
                'type': entity['type'],
                'resolved_value': resolved['value'],
                'confidence': resolved['confidence'],
                'alternatives': resolved.get('alternatives', [])
            })

        return resolved_entities

    def build_semantic_understanding(self, nlu_result, context):
        """构建用户意图的语义表示"""
        return {
            'user_goal': self.infer_user_goal(nlu_result, context),
            'required_information': self.identify_missing_info(nlu_result),
            'constraints': self.extract_constraints(nlu_result),
            'preferences': self.extract_preferences(nlu_result, context)
        }
```

### 3. 对话流程设计

设计智能对话流程：

**对话流程引擎**

```python
class ConversationFlowEngine:
    def __init__(self):
        self.flows = self._load_conversation_flows()
        self.state_tracker = StateTracker()

    def design_conversation_flow(self):
        """设计多轮对话流程"""
        return {
            'greeting_flow': {
                'triggers': ['hello', 'hi', 'greetings'],
                'nodes': [
                    {
                        'id': 'greet_user',
                        'type': 'response',
                        'content': self.personalized_greeting,
                        'next': 'ask_how_to_help'
                    },
                    {
                        'id': 'ask_how_to_help',
                        'type': 'question',
                        'content': "今天我能为您做什么？",
                        'expected_intents': ['request_help', 'ask_question'],
                        'timeout': 30,
                        'timeout_action': 'offer_suggestions'
                    }
                ]
            },
            'task_completion_flow': {
                'triggers': ['task_request'],
                'nodes': [
                    {
                        'id': 'understand_task',
                        'type': 'nlu_processing',
                        'extract': ['task_type', 'parameters'],
                        'next': 'check_requirements'
                    },
                    {
                        'id': 'check_requirements',
                        'type': 'validation',
                        'validate': self.validate_task_requirements,
                        'on_success': 'confirm_task',
                        'on_missing': 'request_missing_info'
                    },
                    {
                        'id': 'request_missing_info',
                        'type': 'slot_filling',
                        'slots': self.get_required_slots,
                        'prompts': self.get_slot_prompts,
                        'next': 'confirm_task'
                    },
                    {
                        'id': 'confirm_task',
                        'type': 'confirmation',
                        'content': self.generate_task_summary,
                        'on_confirm': 'execute_task',
                        'on_deny': 'clarify_task'
                    }
                ]
            }
        }

    async def execute_flow(self, flow_id: str, context: ConversationContext):
        """执行对话流程"""
        flow = self.flows[flow_id]
        current_node = flow['nodes'][0]

        while current_node:
            result = await self.execute_node(current_node, context)

            # 确定下一个节点
            if result.get('user_input'):
                next_node_id = self.determine_next_node(
                    current_node,
                    result['user_input'],
                    context
                )
            else:
                next_node_id = current_node.get('next')

            current_node = self.get_node(flow, next_node_id)

            # 更新上下文
            context.conversation_state.update(result.get('state_updates', {}))

        return context
```

### 4. 响应生成

创建智能响应生成：

**响应生成器**

```python
class ResponseGenerator:
    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.templates = self._load_response_templates()
        self.personality = self._load_personality_config()

    async def generate_response(self,
                               intent: str,
                               context: ConversationContext,
                               data: Dict[str, Any]) -> str:
        """生成上下文相关的响应"""

        # 选择响应策略
        if self.should_use_template(intent):
            response = self.generate_from_template(intent, data)
        elif self.should_use_llm(intent, context):
            response = await self.generate_with_llm(intent, context, data)
        else:
            response = self.generate_hybrid_response(intent, context, data)

        # 应用个性和语气
        response = self.apply_personality(response, context)

        # 确保响应适当性
        response = self.validate_response(response, context)

        return response

    async def generate_with_llm(self, intent, context, data):
        """使用 LLM 生成响应"""
        # 构建提示词
        prompt = self.build_llm_prompt(intent, context, data)

        # 设置生成参数
        params = {
            'temperature': self.get_temperature(intent),
            'max_tokens': 150,
            'stop_sequences': ['\n\n', 'User:', 'Human:']
        }

        # 生成响应
        response = await self.llm.generate(prompt, **params)

        # 后处理响应
        return self.post_process_llm_response(response)

    def build_llm_prompt(self, intent, context, data):
        """为 LLM 构建上下文感知的提示词"""
        return f"""
你是一个有益的 AI 助手，具有以下特征：
{self.personality.description}

对话历史：
{self.format_conversation_history(context.messages[-5:])}

用户意图：{intent}
相关数据：{json.dumps(data, indent=2)}

生成一个有益、简洁的响应，该响应应：
1. 回应用户的意图
2. 适当地使用提供的数据
3. 保持对话连续性
4. 遵循个性指南

响应："""

    def generate_from_template(self, intent, data):
        """从模板生成响应"""
        template = self.templates.get(intent)
        if not template:
            return self.get_fallback_response()

        # 选择模板变体
        variant = self.select_template_variant(template, data)

        # 填充模板槽
        response = variant
        for key, value in data.items():
            response = response.replace(f"{{{key}}}", str(value))

        return response

    def apply_personality(self, response, context):
        """将个性特征应用于响应"""
        # 添加个性标记
        if self.personality.get('friendly'):
            response = self.add_friendly_markers(response)

        if self.personality.get('professional'):
            response = self.ensure_professional_tone(response)

        # 根据用户偏好调整
        if context.user_profile.get('prefers_brief'):
            response = self.make_concise(response)

        return response
```

### 5. 上下文管理

实现复杂的上下文管理：

**上下文管理系统**

```python
class ContextManager:
    def __init__(self):
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemory()

    async def manage_context(self,
                            new_input: Dict[str, Any],
                            current_context: ConversationContext) -> ConversationContext:
        """管理对话上下文"""

        # 更新对话历史
        current_context.messages.append({
            'role': 'user',
            'content': new_input['message'],
            'timestamp': datetime.now(),
            'metadata': new_input.get('metadata', {})
        })

        # 解析引用
        resolved_input = await self.resolve_references(new_input, current_context)

        # 更新工作记忆
        self.working_memory.update(resolved_input, current_context)

        # 检测主题变化
        topic_shift = self.detect_topic_shift(resolved_input, current_context)
        if topic_shift:
            current_context = self.handle_topic_shift(topic_shift, current_context)

        # 维护实体状态
        current_context = self.update_entity_state(resolved_input, current_context)

        # 如果需要，修剪旧上下文
        if len(current_context.messages) > self.config['max_context_length']:
            current_context = self.prune_context(current_context)

        return current_context

    async def resolve_references(self, input_data, context):
        """解析代词和引用"""
        text = input_data['message']

        # 代词解析
        pronouns = self.extract_pronouns(text)
        for pronoun in pronouns:
            referent = self.find_referent(pronoun, context)
            if referent:
                text = text.replace(pronoun['text'], referent['resolved'])

        # 时间引用解析
        temporal_refs = self.extract_temporal_references(text)
        for ref in temporal_refs:
            resolved_time = self.resolve_temporal_reference(ref, context)
            text = text.replace(ref['text'], str(resolved_time))

        input_data['resolved_message'] = text
        return input_data

    def maintain_entity_state(self):
        """跨对话跟踪实体状态"""
        return '''
class EntityStateTracker:
    def __init__(self):
        self.entities = {}

    def update_entity(self, entity_id: str, updates: Dict[str, Any]):
        """更新实体状态"""
        if entity_id not in self.entities:
            self.entities[entity_id] = {
                'id': entity_id,
                'type': updates.get('type'),
                'attributes': {},
                'history': []
            }

        # 记录历史
        self.entities[entity_id]['history'].append({
            'timestamp': datetime.now(),
            'updates': updates
        })

        # 应用更新
        self.entities[entity_id]['attributes'].update(updates)

    def get_entity_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """获取当前实体状态"""
        return self.entities.get(entity_id)

    def query_entities(self, entity_type: str = None, **filters):
        """按类型和属性查询实体"""
        results = []
        for entity in self.entities.values():
            if entity_type and entity['type'] != entity_type:
                continue

            matches = True
            for key, value in filters.items():
                if entity['attributes'].get(key) != value:
                    matches = False
                    break

            if matches:
                results.append(entity)

        return results
'''
```

### 6. 与 LLM 集成

与各种 LLM 提供商集成：

**LLM 集成层**

```python
class LLMIntegrationLayer:
    def __init__(self):
        self.providers = {
            'openai': OpenAIProvider(),
            'anthropic': AnthropicProvider(),
            'local': LocalLLMProvider()
        }
        self.current_provider = None

    async def setup_llm_integration(self, provider: str, config: Dict[str, Any]):
        """设置 LLM 集成"""
        self.current_provider = self.providers[provider]
        await self.current_provider.initialize(config)

        return {
            'provider': provider,
            'capabilities': self.current_provider.get_capabilities(),
            'rate_limits': self.current_provider.get_rate_limits()
        }

    async def generate_completion(self,
                                 prompt: str,
                                 system_prompt: str = None,
                                 **kwargs):
        """生成带有回退处理的补全"""
        try:
            # 首次尝试
            response = await self.current_provider.complete(
                prompt=prompt,
                system_prompt=system_prompt,
                **kwargs
            )

            # 验证响应
            if self.is_valid_response(response):
                return response
            else:
                return await self.handle_invalid_response(prompt, response)

        except RateLimitError:
            # 切换到回退提供商
            return await self.use_fallback_provider(prompt, system_prompt, **kwargs)
        except Exception as e:
            # 记录错误并在可用时使用缓存响应
            return self.get_cached_response(prompt) or self.get_default_response()

    def create_function_calling_interface(self):
        """为 LLM 创建函数调用接口"""
        return '''
class FunctionCallingInterface:
    def __init__(self):
        self.functions = {}

    def register_function(self,
                         name: str,
                         func: callable,
                         description: str,
                         parameters: Dict[str, Any]):
        """注册供 LLM 调用的函数"""
        self.functions[name] = {
            'function': func,
            'description': description,
            'parameters': parameters
        }

    async def process_function_call(self, llm_response):
        """处理来自 LLM 的函数调用"""
        if 'function_call' not in llm_response:
            return llm_response

        function_name = llm_response['function_call']['name']
        arguments = llm_response['function_call']['arguments']

        if function_name not in self.functions:
            return {'error': f'未知函数：{function_name}'}

        # 验证参数
        validated_args = self.validate_arguments(
            function_name,
            arguments
        )

        # 执行函数
        result = await self.functions[function_name]['function'](**validated_args)

        # 返回结果供 LLM 处理
        return {
            'function_result': result,
            'function_name': function_name
        }
'''
```

### 7. 测试对话式 AI

实现全面测试：

**对话测试框架**

```python
class ConversationTestFramework:
    def __init__(self):
        self.test_suites = []
        self.metrics = ConversationMetrics()

    def create_test_suite(self):
        """创建全面的测试套件"""
        return {
            'unit_tests': self._create_unit_tests(),
            'integration_tests': self._create_integration_tests(),
            'conversation_tests': self._create_conversation_tests(),
            'performance_tests': self._create_performance_tests(),
            'user_simulation': self._create_user_simulation()
        }

    def _create_conversation_tests(self):
        """测试多轮对话"""
        return '''
class ConversationTest:
    async def test_multi_turn_conversation(self):
        """测试完整的对话流程"""
        assistant = AIAssistant()
        context = ConversationContext(user_id="test_user")

        # 对话脚本
        conversation = [
            {
                'user': "你好，我需要帮助处理订单",
                'expected_intent': 'order_help',
                'expected_action': 'ask_order_details'
            },
            {
                'user': "我的订单号是 12345",
                'expected_entities': [{'type': 'order_id', 'value': '12345'}],
                'expected_action': 'retrieve_order'
            },
            {
                'user': "什么时候能送到？",
                'expected_intent': 'delivery_inquiry',
                'should_use_context': True
            }
        ]

        for turn in conversation:
            # 发送用户消息
            response = await assistant.process_message(
                turn['user'],
                context
            )

            # 验证意图检测
            if 'expected_intent' in turn:
                assert response['intent'] == turn['expected_intent']

            # 验证实体提取
            if 'expected_entities' in turn:
                self.validate_entities(
                    response['entities'],
                    turn['expected_entities']
                )

            # 验证上下文使用
            if turn.get('should_use_context'):
                assert 'order_id' in response['context_used']

    def test_error_handling(self):
        """测试错误场景"""
        error_cases = [
            {
                'input': "askdjfkajsdf",
                'expected_behavior': 'fallback_response'
            },
            {
                'input': "I want to [REDACTED]",
                'expected_behavior': 'safety_response'
            },
            {
                'input': "Tell me about " + "x" * 1000,
                'expected_behavior': 'length_limit_response'
            }
        ]

        for case in error_cases:
            response = assistant.process_message(case['input'])
            assert response['behavior'] == case['expected_behavior']
'''

    def create_automated_testing(self):
        """自动化对话测试"""
        return '''
class AutomatedConversationTester:
    def __init__(self):
        self.test_generator = TestCaseGenerator()
        self.evaluator = ResponseEvaluator()

    async def run_automated_tests(self, num_tests: int = 100):
        """运行自动化对话测试"""
        results = {
            'total_tests': num_tests,
            'passed': 0,
            'failed': 0,
            'metrics': {}
        }

        for i in range(num_tests):
            # 生成测试用例
            test_case = self.test_generator.generate()

            # 运行对话
            conversation_log = await self.run_conversation(test_case)

            # 评估结果
            evaluation = self.evaluator.evaluate(
                conversation_log,
                test_case['expectations']
            )

            if evaluation['passed']:
                results['passed'] += 1
            else:
                results['failed'] += 1

            # 收集指标
            self.update_metrics(results['metrics'], evaluation['metrics'])

        return results

    def generate_adversarial_tests(self):
        """生成对抗性测试用例"""
        return [
            # 模糊输入
            "I want that thing we discussed",

            # 上下文切换
            "Actually, forget that. Tell me about the weather",

            # 多意图
            "Cancel my order and also update my address",

            # 信息不完整
            "Book a flight",

            # 矛盾
            "I want a vegetarian meal with bacon"
        ]
'''
```

### 8. 部署和扩展

部署和扩展 AI 助手：

**部署架构**

```python
class AssistantDeployment:
    def create_deployment_architecture(self):
        """创建可扩展的部署架构"""
        return {
            'containerization': '''
# AI 助手的 Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY . .

# 在构建时加载模型
RUN python -m app.model_loader

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -m app.health_check

# 运行应用
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", "--bind", "0.0.0.0:8080", "app.main:app"]
''',
            'kubernetes_deployment': '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant
  template:
    metadata:
      labels:
        app: ai-assistant
    spec:
      containers:
      - name: assistant
        image: ai-assistant:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: MODEL_CACHE_SIZE
          value: "1000"
        - name: MAX_CONCURRENT_SESSIONS
          value: "100"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ai-assistant-service
spec:
  selector:
    app: ai-assistant
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-assistant-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-assistant
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
''',
            'caching_strategy': self._design_caching_strategy(),
            'load_balancing': self._design_load_balancing()
        }

    def _design_caching_strategy(self):
        """设计缓存以提高性能"""
        return '''
class AssistantCache:
    def __init__(self):
        self.response_cache = ResponseCache()
        self.model_cache = ModelCache()
        self.context_cache = ContextCache()

    async def get_cached_response(self,
                                 message: str,
                                 context_hash: str) -> Optional[str]:
        """如果可用，获取缓存的响应"""
        cache_key = self.generate_cache_key(message, context_hash)

        # 检查响应缓存
        cached = await self.response_cache.get(cache_key)
        if cached and not self.is_expired(cached):
            return cached['response']

        return None

    def cache_response(self,
                      message: str,
                      context_hash: str,
                      response: str,
                      ttl: int = 3600):
        """缓存带有 TTL 的响应"""
        cache_key = self.generate_cache_key(message, context_hash)

        self.response_cache.set(
            cache_key,
            {
                'response': response,
                'timestamp': datetime.now(),
                'ttl': ttl
            }
        )

    def preload_model_cache(self):
        """预加载常用模型"""
        models_to_cache = [
            'intent_classifier',
            'entity_extractor',
            'response_generator'
        ]

        for model_name in models_to_cache:
            model = load_model(model_name)
            self.model_cache.store(model_name, model)
'''
```

### 9. 监控和分析

监控助手性能：

**助手分析系统**

```python
class AssistantAnalytics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.analytics_engine = AnalyticsEngine()

    def create_monitoring_dashboard(self):
        """创建监控仪表板配置"""
        return {
            'real_time_metrics': {
                'active_sessions': 'gauge',
                'messages_per_second': 'counter',
                'response_time_p95': 'histogram',
                'intent_accuracy': 'gauge',
                'fallback_rate': 'gauge'
            },
            'conversation_metrics': {
                'avg_conversation_length': 'gauge',
                'completion_rate': 'gauge',
                'user_satisfaction': 'gauge',
                'escalation_rate': 'gauge'
            },
            'system_metrics': {
                'model_inference_time': 'histogram',
                'cache_hit_rate': 'gauge',
                'error_rate': 'counter',
                'resource_utilization': 'gauge'
            },
            'alerts': [
                {
                    'name': 'high_fallback_rate',
                    'condition': 'fallback_rate > 0.2',
                    'severity': 'warning'
                },
                {
                    'name': 'slow_response_time',
                    'condition': 'response_time_p95 > 2000',
                    'severity': 'critical'
                }
            ]
        }

    def analyze_conversation_quality(self):
        """分析对话质量指标"""
        return '''
class ConversationQualityAnalyzer:
    def analyze_conversations(self, time_range: str):
        """分析对话质量"""
        conversations = self.fetch_conversations(time_range)

        metrics = {
            'intent_recognition': self.analyze_intent_accuracy(conversations),
            'response_relevance': self.analyze_response_relevance(conversations),
            'conversation_flow': self.analyze_conversation_flow(conversations),
            'user_satisfaction': self.analyze_satisfaction(conversations),
            'error_patterns': self.identify_error_patterns(conversations)
        }

        return self.generate_quality_report(metrics)

    def identify_improvement_areas(self, analysis):
        """识别需要改进的领域"""
        improvements = []

        # 意图准确率低
        if analysis['intent_recognition']['accuracy'] < 0.85:
            improvements.append({
                'area': 'Intent Recognition',
                'issue': '意图检测准确率低',
                'recommendation': '使用更多示例重新训练意图分类器',
                'priority': 'high'
            })

        # 回退率高
        if analysis['conversation_flow']['fallback_rate'] > 0.15:
            improvements.append({
                'area': 'Coverage',
                'issue': '回退率高',
                'recommendation': '为未覆盖的意图扩展训练数据',
                'priority': 'medium'
            })

        return improvements
'''
```

### 10. 持续改进

实施持续改进循环：

**改进流水线**

```python
class ContinuousImprovement:
    def create_improvement_pipeline(self):
        """创建持续改进流水线"""
        return {
            'data_collection': '''
class ConversationDataCollector:
    async def collect_feedback(self, session_id: str):
        """收集用户反馈"""
        feedback_prompt = {
            'satisfaction': '您对本次对话的满意程度如何？（1-5）',
            'resolved': '您的问题解决了吗？',
            'improvements': '我们如何改进？'
        }

        feedback = await self.prompt_user_feedback(
            session_id,
            feedback_prompt
        )

        # 存储反馈
        await self.store_feedback({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'feedback': feedback,
            'conversation_metadata': self.get_session_metadata(session_id)
        })

        return feedback

    def identify_training_opportunities(self):
        """识别用于训练的对话"""
        # 查找低置信度交互
        low_confidence = self.find_low_confidence_interactions()

        # 查找失败的对话
        failed = self.find_failed_conversations()

        # 查找高评分对话
        exemplary = self.find_exemplary_conversations()

        return {
            'needs_improvement': low_confidence + failed,
            'good_examples': exemplary
        }
''',
            'model_retraining': '''
class ModelRetrainer:
    async def retrain_models(self, new_data):
        """使用新数据重新训练模型"""
        # 准备训练数据
        training_data = self.prepare_training_data(new_data)

        # 验证数据质量
        validation_result = self.validate_training_data(training_data)
        if not validation_result['passed']:
            return {'error': '数据质量检查失败', 'issues': validation_result['issues']}

        # 重新训练模型
        models_to_retrain = ['intent_classifier', 'entity_extractor']

        for model_name in models_to_retrain:
            # 加载当前模型
            current_model = self.load_model(model_name)

            # 创建新版本
            new_model = await self.train_model(
                model_name,
                training_data,
                base_model=current_model
            )

            # 评估新模型
            evaluation = await self.evaluate_model(
                new_model,
                self.get_test_set()
            )

            # 如果改进则部署
            if evaluation['performance'] > current_model.performance:
                await self.deploy_model(new_model, model_name)

        return {'status': 'completed', 'models_updated': models_to_retrain}
''',
            'a_b_testing': '''
class ABTestingFramework:
    def create_ab_test(self,
                      test_name: str,
                      variants: List[Dict[str, Any]],
                      metrics: List[str]):
        """为助手改进创建 A/B 测试"""
        test = {
            'id': generate_test_id(),
            'name': test_name,
            'variants': variants,
            'metrics': metrics,
            'allocation': self.calculate_traffic_allocation(variants),
            'duration': self.estimate_test_duration(metrics)
        }

        # 部署测试
        self.deploy_test(test)

        return test

    async def analyze_test_results(self, test_id: str):
        """分析 A/B 测试结果"""
        data = await self.collect_test_data(test_id)

        results = {}
        for metric in data['metrics']:
            # 统计分析
            analysis = self.statistical_analysis(
                data['control'][metric],
                data['variant'][metric]
            )

            results[metric] = {
                'control_mean': analysis['control_mean'],
                'variant_mean': analysis['variant_mean'],
                'lift': analysis['lift'],
                'p_value': analysis['p_value'],
                'significant': analysis['p_value'] < 0.05
            }

        return results
'''
        }
```

## 输出格式

1. **架构设计**：包含组件的完整 AI 助手架构
2. **NLP 实现**：自然语言处理流水线和模型
3. **对话流程**：对话管理和流程设计
4. **响应生成**：带有 LLM 集成的智能响应创建
5. **上下文管理**：复杂的上下文和状态管理
6. **测试框架**：对话式 AI 的全面测试
7. **部署指南**：可扩展的部署架构
8. **监控设置**：分析和性能监控
9. **改进流水线**：持续改进流程

专注于创建生产级 AI 助手，通过自然对话、智能响应和从用户交互中持续学习来提供真正的价值。
