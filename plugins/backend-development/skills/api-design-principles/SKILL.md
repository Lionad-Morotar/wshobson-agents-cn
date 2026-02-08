---
name: api-design-principles
description: 精通 REST 和 GraphQL API 设计原则，构建直观、可扩展且可维护的令开发者满意的 API。在设计新 API、审查 API 规范或建立 API 设计标准时使用。
---

# API 设计原则

精通 REST 和 GraphQL API 设计原则，构建直观、可扩展且可维护的令开发者满意的经得起时间考验的 API。

## 何时使用此技能

- 设计新的 REST 或 GraphQL API
- 为更好的可用性重构现有 API
- 为团队建立 API 设计标准
- 实施前审查 API 规范
- 在 API 范式之间迁移（REST 到 GraphQL 等）
- 创建对开发者友好的 API 文档
- 为特定用例优化 API（移动端、第三方集成）

## 核心概念

### 1. RESTful 设计原则

**面向资源的架构**

- 资源是名词（users、orders、products），而非动词
- 使用 HTTP 方法执行操作（GET、POST、PUT、PATCH、DELETE）
- URL 表示资源层次结构
- 一致的命名约定

**HTTP 方法语义：**

- `GET`: 检索资源（幂等、安全）
- `POST`: 创建新资源
- `PUT`: 替换整个资源（幂等）
- `PATCH`: 部分资源更新
- `DELETE`: 删除资源（幂等）

### 2. GraphQL 设计原则

**Schema 优先开发**

- 类型定义域模型
- 查询用于读取数据
- 变更用于修改数据
- 订阅用于实时更新

**查询结构：**

- 客户端精确请求所需内容
- 单一端点、多种操作
- 强类型 Schema
- 内置内省能力

### 3. API 版本控制策略

**URL 版本控制：**

```
/api/v1/users
/api/v2/users
```

**标头版本控制：**

```
Accept: application/vnd.api+json; version=1
```

**查询参数版本控制：**

```
/api/users?version=1
```

## REST API 设计模式

### 模式 1：资源集合设计

```python
# 良好：面向资源的端点
GET    /api/users              # 列出用户（带分页）
POST   /api/users              # 创建用户
GET    /api/users/{id}         # 获取特定用户
PUT    /api/users/{id}         # 替换用户
PATCH  /api/users/{id}         # 更新用户字段
DELETE /api/users/{id}         # 删除用户

# 嵌套资源
GET    /api/users/{id}/orders  # 获取用户的订单
POST   /api/users/{id}/orders  # 为用户创建订单

# 不佳：面向操作的端点（避免）
POST   /api/createUser
POST   /api/getUserById
POST   /api/deleteUser
```

### 模式 2：分页和过滤

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页项目数")

class FilterParams(BaseModel):
    status: Optional[str] = None
    created_after: Optional[str] = None
    search: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

# FastAPI 端点示例
from fastapi import FastAPI, Query, Depends

app = FastAPI()

@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    # 应用过滤条件
    query = build_query(status=status, search=search)

    # 计算总数
    total = await count_users(query)

    # 获取页面数据
    offset = (page - 1) * page_size
    users = await fetch_users(query, limit=page_size, offset=offset)

    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### 模式 3：错误处理和状态码

```python
from fastapi import HTTPException, status
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: str
    path: str

class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    value: Any

# 一致的错误响应
STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable": 422,
    "internal_error": 500
}

def raise_not_found(resource: str, id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"{resource} 未找到",
            "details": {"id": id}
        }
    )

def raise_validation_error(errors: List[ValidationErrorDetail]):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": "ValidationError",
            "message": "请求验证失败",
            "details": {"errors": [e.dict() for e in errors]}
        }
    )

# 示例用法
@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = await fetch_user(user_id)
    if not user:
        raise_not_found("User", user_id)
    return user
```

### 模式 4：HATEOAS（超媒体作为应用状态引擎）

```python
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    _links: dict

    @classmethod
    def from_user(cls, user: User, base_url: str):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            _links={
                "self": {"href": f"{base_url}/api/users/{user.id}"},
                "orders": {"href": f"{base_url}/api/users/{user.id}/orders"},
                "update": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "PATCH"
                },
                "delete": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "DELETE"
                }
            }
        )
```

## GraphQL 设计模式

### 模式 1：Schema 设计

```graphql
# schema.graphql

# 清晰的类型定义
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!

  # 关联关系
  orders(first: Int = 20, after: String, status: OrderStatus): OrderConnection!

  profile: UserProfile
}

type Order {
  id: ID!
  status: OrderStatus!
  total: Money!
  items: [OrderItem!]!
  createdAt: DateTime!

  # 反向引用
  user: User!
}

# 分页模式（Relay 风格）
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# 枚举类型确保类型安全
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

# 自定义标量
scalar DateTime
scalar Money

# 查询根
type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, search: String): UserConnection!

  order(id: ID!): Order
}

# 变更根
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}

# 变更的输入类型
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

# 变更的负载类型
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
}
```

### 模式 2：解析器设计

```python
from typing import Optional, List
from ariadne import QueryType, MutationType, ObjectType
from dataclasses import dataclass

query = QueryType()
mutation = MutationType()
user_type = ObjectType("User")

@query.field("user")
async def resolve_user(obj, info, id: str) -> Optional[dict]:
    """按 ID 解析单个用户。"""
    return await fetch_user_by_id(id)

@query.field("users")
async def resolve_users(
    obj,
    info,
    first: int = 20,
    after: Optional[str] = None,
    search: Optional[str] = None
) -> dict:
    """解析分页用户列表。"""
    # 解码游标
    offset = decode_cursor(after) if after else 0

    # 获取用户
    users = await fetch_users(
        limit=first + 1,  # 多获取一个以检查 hasNextPage
        offset=offset,
        search=search
    )

    # 分页处理
    has_next = len(users) > first
    if has_next:
        users = users[:first]

    edges = [
        {
            "node": user,
            "cursor": encode_cursor(offset + i)
        }
        for i, user in enumerate(users)
    ]

    return {
        "edges": edges,
        "pageInfo": {
            "hasNextPage": has_next,
            "hasPreviousPage": offset > 0,
            "startCursor": edges[0]["cursor"] if edges else None,
            "endCursor": edges[-1]["cursor"] if edges else None
        },
        "totalCount": await count_users(search=search)
    }

@user_type.field("orders")
async def resolve_user_orders(user: dict, info, first: int = 20) -> dict:
    """解析用户的订单（使用 DataLoaders 防止 N+1）。"""
    # 使用 DataLoader 批量处理请求
    loader = info.context["loaders"]["orders_by_user"]
    orders = await loader.load(user["id"])

    return paginate_orders(orders, first)

@mutation.field("createUser")
async def resolve_create_user(obj, info, input: dict) -> dict:
    """创建新用户。"""
    try:
        # 验证输入
        validate_user_input(input)

        # 创建用户
        user = await create_user(
            email=input["email"],
            name=input["name"],
            password=hash_password(input["password"])
        )

        return {
            "user": user,
            "errors": []
        }
    except ValidationError as e:
        return {
            "user": None,
            "errors": [{"field": e.field, "message": e.message}]
        }
```

### 模式 3：DataLoader（N+1 问题预防）

```python
from aiodataloader import DataLoader
from typing import List, Optional

class UserLoader(DataLoader):
    """按 ID 批量加载用户。"""

    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        """在单个查询中加载多个用户。"""
        users = await fetch_users_by_ids(user_ids)

        # 将结果映射回输入顺序
        user_map = {user["id"]: user for user in users}
        return [user_map.get(user_id) for user_id in user_ids]

class OrdersByUserLoader(DataLoader):
    """按用户 ID 批量加载订单。"""

    async def batch_load_fn(self, user_ids: List[str]) -> List[List[dict]]:
        """在单个查询中加载多个用户的订单。"""
        orders = await fetch_orders_by_user_ids(user_ids)

        # 按 user_id 分组订单
        orders_by_user = {}
        for order in orders:
            user_id = order["user_id"]
            if user_id not in orders_by_user:
                orders_by_user[user_id] = []
            orders_by_user[user_id].append(order)

        # 按输入顺序返回
        return [orders_by_user.get(user_id, []) for user_id in user_ids]

# 上下文设置
def create_context():
    return {
        "loaders": {
            "user": UserLoader(),
            "orders_by_user": OrdersByUserLoader()
        }
    }
```

## 最佳实践

### REST API

1. **一致的命名**：对集合使用复数名词（`/users`，而非 `/user`）
2. **无状态**：每个请求包含所有必要信息
3. **正确使用 HTTP 状态码**：2xx 成功，4xx 客户端错误，5xx 服务器错误
4. **API 版本控制**：从一开始就规划破坏性变更
5. **分页**：始终对大集合进行分页
6. **速率限制**：使用速率限制保护 API
7. **文档**：使用 OpenAPI/Swagger 生成交互式文档

### GraphQL API

1. **Schema 优先**：在编写解析器之前设计 Schema
2. **避免 N+1**：使用 DataLoaders 高效获取数据
3. **输入验证**：在 Schema 和解析器级别进行验证
4. **错误处理**：在变更负载中返回结构化错误
5. **分页**：使用基于游标的分页（Relay 规范）
6. **弃用**：使用 `@deprecated` 指令进行渐进式迁移
7. **监控**：跟踪查询复杂度和执行时间

## 常见陷阱

- **过度获取/获取不足（REST）**：在 GraphQL 中修复但需要 DataLoaders
- **破坏性变更**：对 API 进行版本控制或使用弃用策略
- **不一致的错误格式**：标准化错误响应
- **缺少速率限制**：没有限制的 API 容易受到滥用
- **文档不当**：未记录的 API 令开发者沮丧
- **忽略 HTTP 语义**：对幂等操作使用 POST 会破坏预期
- **紧密耦合**：API 结构不应镜像数据库 Schema

## 资源

- **references/rest-best-practices.md**：全面的 REST API 设计指南
- **references/graphql-schema-design.md**：GraphQL Schema 模式和反模式
- **references/api-versioning-strategies.md**：版本控制方法和迁移路径
- **assets/rest-api-template.py**：FastAPI REST API 模板
- **assets/graphql-schema-template.graphql**：完整的 GraphQL Schema 示例
- **assets/api-design-checklist.md**：实施前审查检查清单
- **scripts/openapi-generator.py**：从代码生成 OpenAPI 规范