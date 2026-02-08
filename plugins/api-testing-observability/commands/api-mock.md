# API 模拟框架

你是一位 API 模拟专家，专注于为开发、测试和演示目的创建逼真的模拟服务。设计全面的模拟解决方案，模拟真实的 API 行为，实现并行开发并促进全面测试。

## 上下文

用户需要为开发、测试或演示目的创建模拟 API。专注于创建灵活、逼真的模拟，准确模拟生产 API 行为，同时实现高效的工作流程。

## 需求

$ARGUMENTS

## 指令

### 1. 模拟服务器设置

创建全面的模拟服务器基础设施：

**模拟服务器框架**

```python
from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime
from fastapi import FastAPI, Request, Response
import uvicorn

class MockAPIServer:
    def __init__(self, config: Dict[str, Any]):
        self.app = FastAPI(title="Mock API Server")
        self.routes = {}
        self.middleware = []
        self.state_manager = StateManager()
        self.scenario_manager = ScenarioManager()

    def setup_mock_server(self):
        """设置全面的模拟服务器"""
        # 配置中间件
        self._setup_middleware()

        # 加载模拟定义
        self._load_mock_definitions()

        # 设置动态路由
        self._setup_dynamic_routes()

        # 初始化场景
        self._initialize_scenarios()

        return self.app

    def _setup_middleware(self):
        """配置服务器中间件"""
        @self.app.middleware("http")
        async def add_mock_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Mock-Server"] = "true"
            response.headers["X-Mock-Scenario"] = self.scenario_manager.current_scenario
            return response

        @self.app.middleware("http")
        async def simulate_latency(request: Request, call_next):
            # 模拟网络延迟
            latency = self._calculate_latency(request.url.path)
            await asyncio.sleep(latency / 1000)  # 转换为秒
            response = await call_next(request)
            return response

        @self.app.middleware("http")
        async def track_requests(request: Request, call_next):
            # 跟踪请求以供验证
            self.state_manager.track_request({
                'method': request.method,
                'path': str(request.url.path),
                'headers': dict(request.headers),
                'timestamp': datetime.now()
            })
            response = await call_next(request)
            return response

    def _setup_dynamic_routes(self):
        """设置动态路由处理"""
        @self.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        async def handle_mock_request(path: str, request: Request):
            # 查找匹配的模拟
            mock = self._find_matching_mock(request.method, path, request)

            if not mock:
                return Response(
                    content=json.dumps({"error": "No mock found for this endpoint"}),
                    status_code=404,
                    media_type="application/json"
                )

            # 处理模拟响应
            response_data = await self._process_mock_response(mock, request)

            return Response(
                content=json.dumps(response_data['body']),
                status_code=response_data['status'],
                headers=response_data['headers'],
                media_type="application/json"
            )

    async def _process_mock_response(self, mock: Dict[str, Any], request: Request):
        """处理并生成模拟响应"""
        # 检查条件响应
        if mock.get('conditions'):
            for condition in mock['conditions']:
                if self._evaluate_condition(condition, request):
                    return await self._generate_response(condition['response'], request)

        # 使用默认响应
        return await self._generate_response(mock['response'], request)

    def _generate_response(self, response_template: Dict[str, Any], request: Request):
        """从模板生成响应"""
        response = {
            'status': response_template.get('status', 200),
            'headers': response_template.get('headers', {}),
            'body': self._process_response_body(response_template['body'], request)
        }

        # 应用响应转换
        if response_template.get('transformations'):
            response = self._apply_transformations(response, response_template['transformations'])

        return response
```

### 2. 请求/响应存根

实现灵活的存根系统：

**存根引擎**

```python
class StubbingEngine:
    def __init__(self):
        self.stubs = {}
        self.matchers = self._initialize_matchers()

    def create_stub(self, method: str, path: str, **kwargs):
        """创建新存根"""
        stub_id = self._generate_stub_id()

        stub = {
            'id': stub_id,
            'method': method,
            'path': path,
            'matchers': self._build_matchers(kwargs),
            'response': kwargs.get('response', {}),
            'priority': kwargs.get('priority', 0),
            'times': kwargs.get('times', -1),  # -1 表示无限
            'delay': kwargs.get('delay', 0),
            'scenario': kwargs.get('scenario', 'default')
        }

        self.stubs[stub_id] = stub
        return stub_id

    def _build_matchers(self, kwargs):
        """构建请求匹配器"""
        matchers = []

        # 路径参数匹配
        if 'path_params' in kwargs:
            matchers.append({
                'type': 'path_params',
                'params': kwargs['path_params']
            })

        # 查询参数匹配
        if 'query_params' in kwargs:
            matchers.append({
                'type': 'query_params',
                'params': kwargs['query_params']
            })

        # Header 匹配
        if 'headers' in kwargs:
            matchers.append({
                'type': 'headers',
                'headers': kwargs['headers']
            })

        # Body 匹配
        if 'body' in kwargs:
            matchers.append({
                'type': 'body',
                'body': kwargs['body'],
                'match_type': kwargs.get('body_match_type', 'exact')
            })

        return matchers

    def match_request(self, request: Dict[str, Any]):
        """为请求查找匹配的存根"""
        candidates = []

        for stub in self.stubs.values():
            if self._matches_stub(request, stub):
                candidates.append(stub)

        # 按优先级排序并返回最佳匹配
        if candidates:
            return sorted(candidates, key=lambda x: x['priority'], reverse=True)[0]

        return None

    def _matches_stub(self, request: Dict[str, Any], stub: Dict[str, Any]):
        """检查请求是否匹配存根"""
        # 检查方法
        if request['method'] != stub['method']:
            return False

        # 检查路径
        if not self._matches_path(request['path'], stub['path']):
            return False

        # 检查所有匹配器
        for matcher in stub['matchers']:
            if not self._evaluate_matcher(request, matcher):
                return False

        # 检查存根是否仍然有效
        if stub['times'] == 0:
            return False

        return True

    def create_dynamic_stub(self):
        """创建带回调的动态存根"""
        return '''
class DynamicStub:
    def __init__(self, path_pattern: str):
        self.path_pattern = path_pattern
        self.response_generator = None
        self.state_modifier = None

    def with_response_generator(self, generator):
        """设置动态响应生成器"""
        self.response_generator = generator
        return self

    def with_state_modifier(self, modifier):
        """设置状态修改回调"""
        self.state_modifier = modifier
        return self

    async def process_request(self, request: Request, state: Dict[str, Any]):
        """动态处理请求"""
        # 提取请求数据
        request_data = {
            'method': request.method,
            'path': request.url.path,
            'headers': dict(request.headers),
            'query_params': dict(request.query_params),
            'body': await request.json() if request.method in ['POST', 'PUT'] else None
        }

        # 根据需要修改状态
        if self.state_modifier:
            state = self.state_modifier(state, request_data)

        # 生成响应
        if self.response_generator:
            response = self.response_generator(request_data, state)
        else:
            response = {'status': 200, 'body': {}}

        return response, state

# 使用示例
dynamic_stub = DynamicStub('/api/users/{user_id}')
dynamic_stub.with_response_generator(lambda req, state: {
    'status': 200,
    'body': {
        'id': req['path_params']['user_id'],
        'name': state.get('users', {}).get(req['path_params']['user_id'], 'Unknown'),
        'request_count': state.get('request_count', 0)
    }
}).with_state_modifier(lambda state, req: {
    **state,
    'request_count': state.get('request_count', 0) + 1
})
'''
```

### 3. 动态数据生成

生成逼真的模拟数据：

**模拟数据生成器**

```python
from faker import Faker
import random
from datetime import datetime, timedelta

class MockDataGenerator:
    def __init__(self):
        self.faker = Faker()
        self.templates = {}
        self.generators = self._init_generators()

    def generate_data(self, schema: Dict[str, Any]):
        """基于模式生成数据"""
        if isinstance(schema, dict):
            if '$ref' in schema:
                # 引用另一个模式
                return self.generate_data(self.resolve_ref(schema['$ref']))

            result = {}
            for key, value in schema.items():
                if key.startswith('$'):
                    continue
                result[key] = self._generate_field(value)
            return result

        elif isinstance(schema, list):
            # 生成数组
            count = random.randint(1, 10)
            return [self.generate_data(schema[0]) for _ in range(count)]

        else:
            return schema

    def _generate_field(self, field_schema: Dict[str, Any]):
        """基于模式生成字段值"""
        field_type = field_schema.get('type', 'string')

        # 检查自定义生成器
        if 'generator' in field_schema:
            return self._use_custom_generator(field_schema['generator'])

        # 检查枚举
        if 'enum' in field_schema:
            return random.choice(field_schema['enum'])

        # 基于类型生成
        generators = {
            'string': self._generate_string,
            'number': self._generate_number,
            'integer': self._generate_integer,
            'boolean': self._generate_boolean,
            'array': self._generate_array,
            'object': lambda s: self.generate_data(s)
        }

        generator = generators.get(field_type, self._generate_string)
        return generator(field_schema)

    def _generate_string(self, schema: Dict[str, Any]):
        """生成字符串值"""
        # 检查格式
        format_type = schema.get('format', '')

        format_generators = {
            'email': self.faker.email,
            'name': self.faker.name,
            'first_name': self.faker.first_name,
            'last_name': self.faker.last_name,
            'phone': self.faker.phone_number,
            'address': self.faker.address,
            'url': self.faker.url,
            'uuid': self.faker.uuid4,
            'date': lambda: self.faker.date().isoformat(),
            'datetime': lambda: self.faker.date_time().isoformat(),
            'password': lambda: self.faker.password()
        }

        if format_type in format_generators:
            return format_generators[format_type]()

        # 检查模式
        if 'pattern' in schema:
            return self._generate_from_pattern(schema['pattern'])

        # 默认字符串生成
        min_length = schema.get('minLength', 5)
        max_length = schema.get('maxLength', 20)
        return self.faker.text(max_nb_chars=random.randint(min_length, max_length))

    def create_data_templates(self):
        """创建可重用的数据模板"""
        return {
            'user': {
                'id': {'type': 'string', 'format': 'uuid'},
                'username': {'type': 'string', 'generator': 'username'},
                'email': {'type': 'string', 'format': 'email'},
                'profile': {
                    'type': 'object',
                    'properties': {
                        'firstName': {'type': 'string', 'format': 'first_name'},
                        'lastName': {'type': 'string', 'format': 'last_name'},
                        'avatar': {'type': 'string', 'format': 'url'},
                        'bio': {'type': 'string', 'maxLength': 200}
                    }
                },
                'createdAt': {'type': 'string', 'format': 'datetime'},
                'status': {'type': 'string', 'enum': ['active', 'inactive', 'suspended']}
            },
            'product': {
                'id': {'type': 'string', 'format': 'uuid'},
                'name': {'type': 'string', 'generator': 'product_name'},
                'description': {'type': 'string', 'maxLength': 500},
                'price': {'type': 'number', 'minimum': 0.01, 'maximum': 9999.99},
                'category': {'type': 'string', 'enum': ['electronics', 'clothing', 'food', 'books']},
                'inStock': {'type': 'boolean'},
                'rating': {'type': 'number', 'minimum': 0, 'maximum': 5}
            }
        }

    def generate_relational_data(self):
        """生成具有关系的数据"""
        return '''
class RelationalDataGenerator:
    def generate_related_entities(self, schema: Dict[str, Any], count: int):
        """生成维护引用完整性的相关实体"""
        entities = {}

        # 第一遍：生成主要实体
        for entity_name, entity_schema in schema['entities'].items():
            entities[entity_name] = []
            for i in range(count):
                entity = self.generate_entity(entity_schema)
                entity['id'] = f"{entity_name}_{i}"
                entities[entity_name].append(entity)

        # 第二遍：建立关系
        for relationship in schema.get('relationships', []):
            self.establish_relationship(entities, relationship)

        return entities

    def establish_relationship(self, entities: Dict[str, List], relationship: Dict):
        """在实体之间建立关系"""
        source = relationship['source']
        target = relationship['target']
        rel_type = relationship['type']

        if rel_type == 'one-to-many':
            for source_entity in entities[source['entity']]:
                # 选择随机目标
                num_targets = random.randint(1, 5)
                target_refs = random.sample(
                    entities[target['entity']],
                    min(num_targets, len(entities[target['entity']]))
                )
                source_entity[source['field']] = [t['id'] for t in target_refs]

        elif rel_type == 'many-to-one':
            for target_entity in entities[target['entity']]:
                # 选择一个源
                source_ref = random.choice(entities[source['entity']])
                target_entity[target['field']] = source_ref['id']
'''
```

### 4. 模拟场景

实现基于场景的模拟：

**场景管理器**

```python
class ScenarioManager:
    def __init__(self):
        self.scenarios = {}
        self.current_scenario = 'default'
        self.scenario_states = {}

    def define_scenario(self, name: str, definition: Dict[str, Any]):
        """定义模拟场景"""
        self.scenarios[name] = {
            'name': name,
            'description': definition.get('description', ''),
            'initial_state': definition.get('initial_state', {}),
            'stubs': definition.get('stubs', []),
            'sequences': definition.get('sequences', []),
            'conditions': definition.get('conditions', [])
        }

    def create_test_scenarios(self):
        """创建常见测试场景"""
        return {
            'happy_path': {
                'description': '所有操作成功',
                'stubs': [
                    {
                        'path': '/api/auth/login',
                        'response': {
                            'status': 200,
                            'body': {
                                'token': 'valid_token',
                                'user': {'id': '123', 'name': 'Test User'}
                            }
                        }
                    },
                    {
                        'path': '/api/users/{id}',
                        'response': {
                            'status': 200,
                            'body': {
                                'id': '{id}',
                                'name': 'Test User',
                                'email': 'test@example.com'
                            }
                        }
                    }
                ]
            },
            'error_scenario': {
                'description': '各种错误条件',
                'sequences': [
                    {
                        'name': 'rate_limiting',
                        'steps': [
                            {'repeat': 5, 'response': {'status': 200}},
                            {'repeat': 10, 'response': {'status': 429, 'body': {'error': 'Rate limit exceeded'}}}
                        ]
                    }
                ],
                'stubs': [
                    {
                        'path': '/api/auth/login',
                        'conditions': [
                            {
                                'match': {'body': {'username': 'locked_user'}},
                                'response': {'status': 423, 'body': {'error': 'Account locked'}}
                            }
                        ]
                    }
                ]
            },
            'degraded_performance': {
                'description': '缓慢响应和超时',
                'stubs': [
                    {
                        'path': '/api/*',
                        'delay': 5000,  # 5 秒延迟
                        'response': {'status': 200}
                    }
                ]
            }
        }

    def execute_scenario_sequence(self):
        """执行场景序列"""
        return '''
class SequenceExecutor:
    def __init__(self):
        self.sequence_states = {}

    def get_sequence_response(self, sequence_name: str, request: Dict):
        """基于序列状态获取响应"""
        if sequence_name not in self.sequence_states:
            self.sequence_states[sequence_name] = {'step': 0, 'count': 0}

        state = self.sequence_states[sequence_name]
        sequence = self.get_sequence_definition(sequence_name)

        # 获取当前步骤
        current_step = sequence['steps'][state['step']]

        # 检查是否应该前进到下一步
        state['count'] += 1
        if state['count'] >= current_step.get('repeat', 1):
            state['step'] = (state['step'] + 1) % len(sequence['steps'])
            state['count'] = 0

        return current_step['response']

    def create_stateful_scenario(self):
        """创建具有状态行为的场景"""
        return {
            'shopping_cart': {
                'initial_state': {
                    'cart': {},
                    'total': 0
                },
                'stubs': [
                    {
                        'method': 'POST',
                        'path': '/api/cart/items',
                        'handler': 'add_to_cart',
                        'modifies_state': True
                    },
                    {
                        'method': 'GET',
                        'path': '/api/cart',
                        'handler': 'get_cart',
                        'uses_state': True
                    }
                ],
                'handlers': {
                    'add_to_cart': lambda state, request: {
                        'state': {
                            **state,
                            'cart': {
                                **state['cart'],
                                request['body']['product_id']: request['body']['quantity']
                            },
                            'total': state['total'] + request['body']['price']
                        },
                        'response': {
                            'status': 201,
                            'body': {'message': 'Item added to cart'}
                        }
                    },
                    'get_cart': lambda state, request: {
                        'response': {
                            'status': 200,
                            'body': {
                                'items': state['cart'],
                                'total': state['total']
                            }
                        }
                    }
                }
            }
        }
'''
```

### 5. 契约测试

实现基于契约的模拟：

**契约测试框架**

```python
class ContractMockServer:
    def __init__(self):
        self.contracts = {}
        self.validators = self._init_validators()

    def load_contract(self, contract_path: str):
        """加载 API 契约（OpenAPI、AsyncAPI 等）"""
        with open(contract_path, 'r') as f:
            contract = yaml.safe_load(f)

        # 解析契约
        self.contracts[contract['info']['title']] = {
            'spec': contract,
            'endpoints': self._parse_endpoints(contract),
            'schemas': self._parse_schemas(contract)
        }

    def generate_mocks_from_contract(self, contract_name: str):
        """从契约规范生成模拟"""
        contract = self.contracts[contract_name]
        mocks = []

        for path, methods in contract['endpoints'].items():
            for method, spec in methods.items():
                mock = self._create_mock_from_spec(path, method, spec)
                mocks.append(mock)

        return mocks

    def _create_mock_from_spec(self, path: str, method: str, spec: Dict):
        """从端点规范创建模拟"""
        mock = {
            'method': method.upper(),
            'path': self._convert_path_to_pattern(path),
            'responses': {}
        }

        # 为每个状态代码生成响应
        for status_code, response_spec in spec.get('responses', {}).items():
            mock['responses'][status_code] = {
                'status': int(status_code),
                'headers': self._get_response_headers(response_spec),
                'body': self._generate_response_body(response_spec)
            }

        # 添加请求验证
        if 'requestBody' in spec:
            mock['request_validation'] = self._create_request_validator(spec['requestBody'])

        return mock

    def validate_against_contract(self):
        """根据契约验证模拟响应"""
        return '''
class ContractValidator:
    def validate_response(self, contract_spec, actual_response):
        """根据契约验证响应"""
        validation_results = {
            'valid': True,
            'errors': []
        }

        # 查找状态代码的响应规范
        response_spec = contract_spec['responses'].get(
            str(actual_response['status']),
            contract_spec['responses'].get('default')
        )

        if not response_spec:
            validation_results['errors'].append({
                'type': 'unexpected_status',
                'message': f"Status {actual_response['status']} not defined in contract"
            })
            validation_results['valid'] = False
            return validation_results

        # 验证 headers
        if 'headers' in response_spec:
            header_errors = self.validate_headers(
                response_spec['headers'],
                actual_response['headers']
            )
            validation_results['errors'].extend(header_errors)

        # 验证 body 模式
        if 'content' in response_spec:
            body_errors = self.validate_body(
                response_spec['content'],
                actual_response['body']
            )
            validation_results['errors'].extend(body_errors)

        validation_results['valid'] = len(validation_results['errors']) == 0
        return validation_results

    def validate_body(self, content_spec, actual_body):
        """根据模式验证响应体"""
        errors = []

        # 获取内容类型的模式
        schema = content_spec.get('application/json', {}).get('schema')
        if not schema:
            return errors

        # 根据 JSON 模式验证
        try:
            validate(instance=actual_body, schema=schema)
        except ValidationError as e:
            errors.append({
                'type': 'schema_validation',
                'path': e.json_path,
                'message': e.message
            })

        return errors
'''
```

### 6. 性能测试

创建性能测试模拟：

**性能模拟服务器**

```python
class PerformanceMockServer:
    def __init__(self):
        self.performance_profiles = {}
        self.metrics_collector = MetricsCollector()

    def create_performance_profile(self, name: str, config: Dict):
        """创建性能测试配置"""
        self.performance_profiles[name] = {
            'latency': config.get('latency', {'min': 10, 'max': 100}),
            'throughput': config.get('throughput', 1000),  # 每秒请求数
            'error_rate': config.get('error_rate', 0.01),  # 1% 错误率
            'response_size': config.get('response_size', {'min': 100, 'max': 10000})
        }

    async def simulate_performance(self, profile_name: str, request: Request):
        """模拟性能特征"""
        profile = self.performance_profiles[profile_name]

        # 模拟延迟
        latency = random.uniform(profile['latency']['min'], profile['latency']['max'])
        await asyncio.sleep(latency / 1000)

        # 模拟错误
        if random.random() < profile['error_rate']:
            return self._generate_error_response()

        # 生成指定大小的响应
        response_size = random.randint(
            profile['response_size']['min'],
            profile['response_size']['max']
        )

        response_data = self._generate_data_of_size(response_size)

        # 跟踪指标
        self.metrics_collector.record({
            'latency': latency,
            'response_size': response_size,
            'timestamp': datetime.now()
        })

        return response_data

    def create_load_test_scenarios(self):
        """创建负载测试场景"""
        return {
            'gradual_load': {
                'description': '逐渐增加负载',
                'stages': [
                    {'duration': 60, 'target_rps': 100},
                    {'duration': 120, 'target_rps': 500},
                    {'duration': 180, 'target_rps': 1000},
                    {'duration': 60, 'target_rps': 100}
                ]
            },
            'spike_test': {
                'description': '流量突然激增',
                'stages': [
                    {'duration': 60, 'target_rps': 100},
                    {'duration': 10, 'target_rps': 5000},
                    {'duration': 60, 'target_rps': 100}
                ]
            },
            'stress_test': {
                'description': '找到崩溃点',
                'stages': [
                    {'duration': 60, 'target_rps': 100},
                    {'duration': 60, 'target_rps': 500},
                    {'duration': 60, 'target_rps': 1000},
                    {'duration': 60, 'target_rps': 2000},
                    {'duration': 60, 'target_rps': 5000},
                    {'duration': 60, 'target_rps': 10000}
                ]
            }
        }

    def implement_throttling(self):
        """实现请求节流"""
        return '''
class ThrottlingMiddleware:
    def __init__(self, max_rps: int):
        self.max_rps = max_rps
        self.request_times = deque()

    async def __call__(self, request: Request, call_next):
        current_time = time.time()

        # 移除旧请求
        while self.request_times and self.request_times[0] < current_time - 1:
            self.request_times.popleft()

        # 检查是否超过限制
        if len(self.request_times) >= self.max_rps:
            return Response(
                content=json.dumps({
                    'error': 'Rate limit exceeded',
                    'retry_after': 1
                }),
                status_code=429,
                headers={'Retry-After': '1'}
            )

        # 记录此请求
        self.request_times.append(current_time)

        # 处理请求
        response = await call_next(request)
        return response
'''
```

### 7. 模拟数据管理

有效管理模拟数据：

**模拟数据存储**

```python
class MockDataStore:
    def __init__(self):
        self.collections = {}
        self.indexes = {}

    def create_collection(self, name: str, schema: Dict = None):
        """创建新数据集合"""
        self.collections[name] = {
            'data': {},
            'schema': schema,
            'counter': 0
        }

        # 在 'id' 上创建默认索引
        self.create_index(name, 'id')

    def insert(self, collection: str, data: Dict):
        """向集合插入数据"""
        collection_data = self.collections[collection]

        # 根据模式验证
        if collection_data['schema']:
            self._validate_data(data, collection_data['schema'])

        # 如果未提供则生成 ID
        if 'id' not in data:
            collection_data['counter'] += 1
            data['id'] = str(collection_data['counter'])

        # 存储数据
        collection_data['data'][data['id']] = data

        # 更新索引
        self._update_indexes(collection, data)

        return data['id']

    def query(self, collection: str, filters: Dict = None):
        """使用过滤器查询集合"""
        collection_data = self.collections[collection]['data']

        if not filters:
            return list(collection_data.values())

        # 使用可用索引
        if self._can_use_index(collection, filters):
            return self._query_with_index(collection, filters)

        # 全扫描
        results = []
        for item in collection_data.values():
            if self._matches_filters(item, filters):
                results.append(item)

        return results

    def create_relationships(self):
        """在集合之间定义关系"""
        return '''
class RelationshipManager:
    def __init__(self, data_store: MockDataStore):
        self.store = data_store
        self.relationships = {}

    def define_relationship(self,
                          source_collection: str,
                          target_collection: str,
                          relationship_type: str,
                          foreign_key: str):
        """在集合之间定义关系"""
        self.relationships[f"{source_collection}->{target_collection}"] = {
            'type': relationship_type,
            'source': source_collection,
            'target': target_collection,
            'foreign_key': foreign_key
        }

    def populate_related_data(self, entity: Dict, collection: str, depth: int = 1):
        """为实体填充相关数据"""
        if depth <= 0:
            return entity

        # 查找此集合的关系
        for rel_key, rel in self.relationships.items():
            if rel['source'] == collection:
                # 获取相关数据
                foreign_id = entity.get(rel['foreign_key'])
                if foreign_id:
                    related = self.store.get(rel['target'], foreign_id)
                    if related:
                        # 递归填充
                        related = self.populate_related_data(
                            related,
                            rel['target'],
                            depth - 1
                        )
                        entity[rel['target']] = related

        return entity

    def cascade_operations(self, operation: str, collection: str, entity_id: str):
        """处理级联操作"""
        if operation == 'delete':
            # 查找依赖关系
            for rel in self.relationships.values():
                if rel['target'] == collection:
                    # 删除依赖实体
                    dependents = self.store.query(
                        rel['source'],
                        {rel['foreign_key']: entity_id}
                    )
                    for dep in dependents:
                        self.store.delete(rel['source'], dep['id'])
'''
```

### 8. 测试框架集成

与流行测试框架集成：

**测试集成**

```python
class TestingFrameworkIntegration:
    def create_jest_integration(self):
        """Jest 测试集成"""
        return '''
// jest.mock.config.js
import { MockServer } from './mockServer';

const mockServer = new MockServer();

beforeAll(async () => {
    await mockServer.start({ port: 3001 });

    // 加载模拟定义
    await mockServer.loadMocks('./mocks/*.json');

    // 设置默认场景
    await mockServer.setScenario('test');
});

afterAll(async () => {
    await mockServer.stop();
});

beforeEach(async () => {
    // 重置模拟状态
    await mockServer.reset();
});

// 测试辅助函数
export const setupMock = async (stub) => {
    return await mockServer.addStub(stub);
};

export const verifyRequests = async (matcher) => {
    const requests = await mockServer.getRequests(matcher);
    return requests;
};

// 示例测试
describe('User API', () => {
    it('should fetch user details', async () => {
        // 设置模拟
        await setupMock({
            method: 'GET',
            path: '/api/users/123',
            response: {
                status: 200,
                body: { id: '123', name: 'Test User' }
            }
        });

        // 发出请求
        const response = await fetch('http://localhost:3001/api/users/123');
        const user = await response.json();

        // 验证
        expect(user.name).toBe('Test User');

        // 验证模拟被调用
        const requests = await verifyRequests({ path: '/api/users/123' });
        expect(requests).toHaveLength(1);
    });
});
'''

    def create_pytest_integration(self):
        """Pytest 集成"""
        return '''
# conftest.py
import pytest
from mock_server import MockServer
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def mock_server(event_loop):
    server = MockServer()
    await server.start(port=3001)
    yield server
    await server.stop()

@pytest.fixture(autouse=True)
async def reset_mocks(mock_server):
    await mock_server.reset()
    yield
    # 验证没有意外的调用
    unmatched = await mock_server.get_unmatched_requests()
    assert len(unmatched) == 0, f"Unmatched requests: {unmatched}"

# 测试工具
class MockBuilder:
    def __init__(self, mock_server):
        self.server = mock_server
        self.stubs = []

    def when(self, method, path):
        self.current_stub = {
            'method': method,
            'path': path
        }
        return self

    def with_body(self, body):
        self.current_stub['body'] = body
        return self

    def then_return(self, status, body=None, headers=None):
        self.current_stub['response'] = {
            'status': status,
            'body': body,
            'headers': headers or {}
        }
        self.stubs.append(self.current_stub)
        return self

    async def setup(self):
        for stub in self.stubs:
            await self.server.add_stub(stub)

# 示例测试
@pytest.mark.asyncio
async def test_user_creation(mock_server):
    # 设置模拟
    mock = MockBuilder(mock_server)
    mock.when('POST', '/api/users') \
        .with_body({'name': 'New User'}) \
        .then_return(201, {'id': '456', 'name': 'New User'})

    await mock.setup()

    # 测试代码
    response = await create_user({'name': 'New User'})
    assert response['id'] == '456'
'''
```

### 9. 模拟服务器部署

部署模拟服务器：

**部署配置**

```yaml
# mock services 的 docker-compose.yml
version: "3.8"

services:
  mock-api:
    build:
      context: .
      dockerfile: Dockerfile.mock
    ports:
      - "3001:3001"
    environment:
      - MOCK_SCENARIO=production
      - MOCK_DATA_PATH=/data/mocks
    volumes:
      - ./mocks:/data/mocks
      - ./scenarios:/data/scenarios
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  mock-admin:
    build:
      context: .
      dockerfile: Dockerfile.admin
    ports:
      - "3002:3002"
    environment:
      - MOCK_SERVER_URL=http://mock-api:3001
    depends_on:
      - mock-api


# Kubernetes deployment
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mock-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mock-server
  template:
    metadata:
      labels:
        app: mock-server
    spec:
      containers:
        - name: mock-server
          image: mock-server:latest
          ports:
            - containerPort: 3001
          env:
            - name: MOCK_SCENARIO
              valueFrom:
                configMapKeyRef:
                  name: mock-config
                  key: scenario
          volumeMounts:
            - name: mock-definitions
              mountPath: /data/mocks
      volumes:
        - name: mock-definitions
          configMap:
            name: mock-definitions
```

### 10. 模拟文档

生成模拟 API 文档：

**文档生成器**

````python
class MockDocumentationGenerator:
    def generate_documentation(self, mock_server):
        """生成全面的模拟文档"""
        return f"""
# Mock API 文档

## 概述
{self._generate_overview(mock_server)}

## 可用端点
{self._generate_endpoints_doc(mock_server)}

## 场景
{self._generate_scenarios_doc(mock_server)}

## 数据模型
{self._generate_models_doc(mock_server)}

## 使用示例
{self._generate_examples(mock_server)}

## 配置
{self._generate_config_doc(mock_server)}
"""

    def _generate_endpoints_doc(self, mock_server):
        """生成端点文档"""
        doc = ""
        for endpoint in mock_server.get_endpoints():
            doc += f"""
### {endpoint['method']} {endpoint['path']}

**描述**: {endpoint.get('description', 'No description')}

**请求**:
```json
{json.dumps(endpoint.get('request_example', {}), indent=2)}
````

**响应**:

```json
{json.dumps(endpoint.get('response_example', {}), indent=2)}
```

**场景**:
{self.\_format_endpoint_scenarios(endpoint)}
"""
return doc

    def create_interactive_docs(self):
        """创建交互式 API 文档"""
        return '''

<!DOCTYPE html>
<html>
<head>
    <title>Mock API 交互式文档</title>
    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: "/api/mock/openapi.json",
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                tryItOutEnabled: true,
                requestInterceptor: (request) => {
                    request.headers['X-Mock-Scenario'] =
                        document.getElementById('scenario-select').value;
                    return request;
                }
            });
        }
    </script>

    <div class="scenario-selector">
        <label>场景:</label>
        <select id="scenario-select">
            <option value="default">Default</option>
            <option value="error">Error Conditions</option>
            <option value="slow">Slow Responses</option>
        </select>
    </div>
</body>
</html>
'''
````

## 输出格式

1. **模拟服务器设置**: 完整的模拟服务器实现
2. **存根配置**: 灵活的请求/响应存根
3. **数据生成**: 逼真的模拟数据生成
4. **场景定义**: 全面的测试场景
5. **契约测试**: 基于契约的模拟验证
6. **性能模拟**: 性能测试功能
7. **数据管理**: 模拟数据存储和关系
8. **测试集成**: 框架集成示例
9. **部署指南**: 模拟服务器部署配置
10. **文档**: 自动生成的模拟 API 文档

专注于创建灵活、逼真的模拟服务，实现高效开发、全面测试和可靠的 API 模拟，覆盖开发生命周期的所有阶段。
