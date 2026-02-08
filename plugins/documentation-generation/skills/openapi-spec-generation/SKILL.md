---
name: openapi-spec-generation
description: 从代码、设计优先规范和验证模式生成和维护 OpenAPI 3.1 规范。用于创建 API 文档、生成 SDK 或确保 API 契约合规。
---

# OpenAPI 规范生成

用于创建、维护和验证 RESTful API 的 OpenAPI 3.1 规范的综合模式。

## 何时使用此技能

- 从头开始创建 API 文档
- 从现有代码生成 OpenAPI 规范
- 设计 API 契约（设计优先方法）
- 根据规范验证 API 实现
- 从规范生成客户端 SDK
- 设置 API 文档门户

## 核心概念

### 1. OpenAPI 3.1 结构

```yaml
openapi: 3.1.0
info:
  title: API 标题
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### 2. 设计方法

| Approach         | Description                  | Best For            |
| ---------------- | ---------------------------- | ------------------- |
| **设计优先**     | 在代码之前编写规范           | 新 API、契约        |
| **代码优先**     | 从代码生成规范               | 现有 API            |
| **混合**         | 注释代码，生成规范           | 演化中的 API        |

## 模板

### 模板 1：完整 API 规范

```yaml
openapi: 3.1.0
info:
  title: 用户管理 API
  description: |
    用于管理用户及其配置文件的 API。

    ## 身份验证
    所有端点都需要 Bearer 令牌身份验证。

    ## 速率限制
    - 标准层级每分钟 1000 个请求
    - 企业层级每分钟 10000 个请求
  version: 2.0.0
  contact:
    name: API 支持
    email: api-support@example.com
    url: https://docs.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v2
    description: 生产环境
  - url: https://staging-api.example.com/v2
    description: 预发布环境
  - url: http://localhost:3000/v2
    description: 本地开发

tags:
  - name: 用户
    description: 用户管理操作
  - name: 配置文件
    description: 用户配置文件操作
  - name: 管理
    description: 管理操作

paths:
  /users:
    get:
      operationId: listUsers
      summary: 列出所有用户
      description: 返回带有可选过滤的用户分页列表。
      tags:
        - 用户
      parameters:
        - $ref: "#/components/parameters/PageParam"
        - $ref: "#/components/parameters/LimitParam"
        - name: status
          in: query
          description: 按用户状态过滤
          schema:
            $ref: "#/components/schemas/UserStatus"
        - name: search
          in: query
          description: 按名称或电子邮件搜索
          schema:
            type: string
            minLength: 2
            maxLength: 100
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserListResponse"
              examples:
                default:
                  $ref: "#/components/examples/UserListExample"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "429":
          $ref: "#/components/responses/RateLimited"
      security:
        - bearerAuth: []

    post:
      operationId: createUser
      summary: 创建新用户
      description: 创建新用户账户并发送欢迎电子邮件。
      tags:
        - 用户
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
            examples:
              standard:
                summary: 标准用户
                value:
                  email: user@example.com
                  name: John Doe
                  role: user
              admin:
                summary: 管理员用户
                value:
                  email: admin@example.com
                  name: Admin User
                  role: admin
      responses:
        "201":
          description: 用户创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
          headers:
            Location:
              description: 创建用户的 URL
              schema:
                type: string
                format: uri
        "400":
          $ref: "#/components/responses/BadRequest"
        "409":
          description: 电子邮件已存在
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
      security:
        - bearerAuth: []

  /users/{userId}:
    parameters:
      - $ref: "#/components/parameters/UserIdParam"

    get:
      operationId: getUser
      summary: 按 ID 获取用户
      tags:
        - 用户
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          $ref: "#/components/responses/NotFound"
      security:
        - bearerAuth: []

    patch:
      operationId: updateUser
      summary: 更新用户
      tags:
        - 用户
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateUserRequest"
      responses:
        "200":
          description: 用户已更新
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          $ref: "#/components/responses/BadRequest"
        "404":
          $ref: "#/components/responses/NotFound"
      security:
        - bearerAuth: []

    delete:
      operationId: deleteUser
      summary: 删除用户
      tags:
        - 用户
        - 管理
      responses:
        "204":
          description: 用户已删除
        "404":
          $ref: "#/components/responses/NotFound"
      security:
        - bearerAuth: []
        - apiKey: []

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
          description: 唯一用户标识符
        email:
          type: string
          format: email
          description: 用户电子邮件地址
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: 用户显示名称
        status:
          $ref: "#/components/schemas/UserStatus"
        role:
          type: string
          enum: [user, moderator, admin]
          default: user
        avatar:
          type: string
          format: uri
          nullable: true
        metadata:
          type: object
          additionalProperties: true
          description: 自定义元数据
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    UserStatus:
      type: string
      enum: [active, inactive, suspended, pending]
      description: 用户账户状态

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, moderator, admin]
          default: user
        metadata:
          type: object
          additionalProperties: true

    UpdateUserRequest:
      type: object
      minProperties: 1
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        status:
          $ref: "#/components/schemas/UserStatus"
        role:
          type: string
          enum: [user, moderator, admin]
        metadata:
          type: object
          additionalProperties: true

    UserListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/User"
        pagination:
          $ref: "#/components/schemas/Pagination"

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
        - totalPages
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
          minimum: 0
        totalPages:
          type: integer
          minimum: 0
        hasNext:
          type: boolean
        hasPrev:
          type: boolean

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: 用于程序化处理的错误代码
        message:
          type: string
          description: 人类可读的错误消息
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
        requestId:
          type: string
          description: 用于支持的请求 ID

  parameters:
    UserIdParam:
      name: userId
      in: path
      required: true
      description: 用户 ID
      schema:
        type: string
        format: uuid

    PageParam:
      name: page
      in: query
      description: 页码（从 1 开始）
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: 每页项目数
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    BadRequest:
      description: 无效请求
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: VALIDATION_ERROR
            message: 无效的请求参数
            details:
              - field: email
                message: 必须是有效的电子邮件地址

    Unauthorized:
      description: 需要身份验证
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: UNAUTHORIZED
            message: 需要身份验证

    NotFound:
      description: 未找到资源
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: NOT_FOUND
            message: 未找到用户

    RateLimited:
      description: 请求过多
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
      headers:
        Retry-After:
          description: 速率限制重置前的秒数
          schema:
            type: integer
        X-RateLimit-Limit:
          description: 每个窗口的请求限制
          schema:
            type: integer
        X-RateLimit-Remaining:
          description: 窗口中剩余的请求数
          schema:
            type: integer

  examples:
    UserListExample:
      value:
        data:
          - id: "550e8400-e29b-41d4-a716-446655440000"
            email: "john@example.com"
            name: "John Doe"
            status: "active"
            role: "user"
            createdAt: "2024-01-15T10:30:00Z"
        pagination:
          page: 1
          limit: 20
          total: 1
          totalPages: 1
          hasNext: false
          hasPrev: false

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: 来自 /auth/login 的 JWT 令牌

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: 用于服务对服务调用的 API 密钥

security:
  - bearerAuth: []
```

### 模板 2：代码优先生成（Python/FastAPI）

```python
# FastAPI 自动生成 OpenAPI
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

app = FastAPI(
    title="用户管理 API",
    description="用于管理用户和配置文件的 API",
    version="2.0.0",
    openapi_tags=[
        {"name": "用户", "description": "用户操作"},
        {"name": "配置文件", "description": "配置文件操作"},
    ],
    servers=[
        {"url": "https://api.example.com/v2", "description": "生产环境"},
        {"url": "http://localhost:8000", "description": "开发环境"},
    ],
)

# 枚举
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

# 模型
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="用户电子邮件地址")
    name: str = Field(..., min_length=1, max_length=100, description="显示名称")

class UserCreate(UserBase):
    role: UserRole = Field(default=UserRole.user)
    metadata: Optional[dict] = Field(default=None, description="自定义元数据")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "name": "John Doe",
                    "role": "user"
                }
            ]
        }
    }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[UserStatus] = None
    role: Optional[UserRole] = None
    metadata: Optional[dict] = None

class User(UserBase):
    id: UUID = Field(..., description="唯一标识符")
    status: UserStatus
    role: UserRole
    avatar: Optional[str] = Field(None, description="头像 URL")
    metadata: Optional[dict] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}

class Pagination(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0, alias="totalPages")
    has_next: bool = Field(..., alias="hasNext")
    has_prev: bool = Field(..., alias="hasPrev")

class UserListResponse(BaseModel):
    data: List[User]
    pagination: Pagination

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    code: str = Field(..., description="错误代码")
    message: str = Field(..., description="错误消息")
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = Field(None, alias="requestId")

# 端点
@app.get(
    "/users",
    response_model=UserListResponse,
    tags=["用户"],
    summary="列出所有用户",
    description="返回带有可选过滤的用户分页列表。",
    responses={
        400: {"model": ErrorResponse, "description": "无效请求"},
        401: {"model": ErrorResponse, "description": "未授权"},
    },
)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页项目数"),
    status: Optional[UserStatus] = Query(None, description="按状态过滤"),
    search: Optional[str] = Query(None, min_length=2, max_length=100),
):
    """
    列出带有分页和过滤的用户。

    - **page**：页码（从 1 开始）
    - **limit**：每页项目数（最多 100）
    - **status**：按用户状态过滤
    - **search**：按名称或电子邮件搜索
    """
    # 实现
    pass

@app.post(
    "/users",
    response_model=User,
    status_code=201,
    tags=["用户"],
    summary="创建新用户",
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "电子邮件已存在"},
    },
)
async def create_user(user: UserCreate):
    """创建新用户并发送欢迎电子邮件。"""
    pass

@app.get(
    "/users/{user_id}",
    response_model=User,
    tags=["用户"],
    summary="按 ID 获取用户",
    responses={404: {"model": ErrorResponse}},
)
async def get_user(
    user_id: UUID = Path(..., description="用户 ID"),
):
    """按其 ID 检索特定用户。"""
    pass

@app.patch(
    "/users/{user_id}",
    response_model=User,
    tags=["用户"],
    summary="更新用户",
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_user(
    user_id: UUID = Path(..., description="用户 ID"),
    user: UserUpdate = ...,
):
    """更新用户属性。"""
    pass

@app.delete(
    "/users/{user_id}",
    status_code=204,
    tags=["用户", "管理"],
    summary="删除用户",
    responses={404: {"model": ErrorResponse}},
)
async def delete_user(
    user_id: UUID = Path(..., description="用户 ID"),
):
    """永久删除用户。"""
    pass

# 导出 OpenAPI 规范
if __name__ == "__main__":
    import json
    print(json.dumps(app.openapi(), indent=2))
```

### 模板 3：代码优先（TypeScript/Express 与 tsoa）

```typescript
// tsoa 从 TypeScript 装饰器生成 OpenAPI

import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Route,
  Path,
  Query,
  Body,
  Response,
  SuccessResponse,
  Tags,
  Security,
  Example,
} from "tsoa";

// 模型
interface User {
  /** 唯一标识符 */
  id: string;
  /** 用户电子邮件地址 */
  email: string;
  /** 显示名称 */
  name: string;
  status: UserStatus;
  role: UserRole;
  /** 头像 URL */
  avatar?: string;
  /** 自定义元数据 */
  metadata?: Record<string, unknown>;
  createdAt: Date;
  updatedAt?: Date;
}

enum UserStatus {
  Active = "active",
  Inactive = "inactive",
  Suspended = "suspended",
  Pending = "pending",
}

enum UserRole {
  User = "user",
  Moderator = "moderator",
  Admin = "admin",
}

interface CreateUserRequest {
  email: string;
  name: string;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface UpdateUserRequest {
  name?: string;
  status?: UserStatus;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

interface UserListResponse {
  data: User[];
  pagination: Pagination;
}

interface ErrorResponse {
  code: string;
  message: string;
  details?: { field: string; message: string }[];
  requestId?: string;
}

@Route("users")
@Tags("用户")
export class UsersController extends Controller {
  /**
   * 列出所有带有分页和过滤的用户
   * @param page 页码（从 1 开始）
   * @param limit 每页项目数（最多 100）
   * @param status 按用户状态过滤
   * @param search 按名称或电子邮件搜索
   */
  @Get()
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "无效请求")
  @Response<ErrorResponse>(401, "未授权")
  @Example<UserListResponse>({
    data: [
      {
        id: "550e8400-e29b-41d4-a716-446655440000",
        email: "john@example.com",
        name: "John Doe",
        status: UserStatus.Active,
        role: UserRole.User,
        createdAt: new Date("2024-01-15T10:30:00Z"),
      },
    ],
    pagination: {
      page: 1,
      limit: 20,
      total: 1,
      totalPages: 1,
      hasNext: false,
      hasPrev: false,
    },
  })
  public async listUsers(
    @Query() page: number = 1,
    @Query() limit: number = 20,
    @Query() status?: UserStatus,
    @Query() search?: string,
  ): Promise<UserListResponse> {
    // 实现
    throw new Error("Not implemented");
  }

  /**
   * 创建新用户
   */
  @Post()
  @Security("bearerAuth")
  @SuccessResponse(201, "已创建")
  @Response<ErrorResponse>(400, "无效请求")
  @Response<ErrorResponse>(409, "电子邮件已存在")
  public async createUser(@Body() body: CreateUserRequest): Promise<User> {
    this.setStatus(201);
    throw new Error("Not implemented");
  }

  /**
   * 按 ID 获取用户
   * @param userId 用户 ID
   */
  @Get("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(404, "未找到用户")
  public async getUser(@Path() userId: string): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * 更新用户属性
   * @param userId 用户 ID
   */
  @Patch("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "无效请求")
  @Response<ErrorResponse>(404, "未找到用户")
  public async updateUser(
    @Path() userId: string,
    @Body() body: UpdateUserRequest,
  ): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * 删除用户
   * @param userId 用户 ID
   */
  @Delete("{userId}")
  @Tags("用户", "管理")
  @Security("bearerAuth")
  @SuccessResponse(204, "已删除")
  @Response<ErrorResponse>(404, "未找到用户")
  public async deleteUser(@Path() userId: string): Promise<void> {
    this.setStatus(204);
  }
}
```

### 模板 4：验证和检查

```bash
# 安装验证工具
npm install -g @stoplight/spectral-cli
npm install -g @redocly/cli

# Spectral 规则集 (.spectral.yaml)
cat > .spectral.yaml << 'EOF'
extends: ["spectral:oas", "spectral:asyncapi"]

rules:
  # 强制操作 ID
  operation-operationId: error

  # 需要描述
  operation-description: warn
  info-description: error

  # 命名约定
  operation-operationId-valid-in-url: true

  # 安全
  operation-security-defined: error

  # 响应代码
  operation-success-response: error

  # 自定义规则
  path-params-snake-case:
    description: 路径参数应为 snake_case
    severity: warn
    given: "$.paths[*].parameters[?(@.in == 'path')].name"
    then:
      function: pattern
      functionOptions:
        match: "^[a-z][a-z0-9_]*$"

  schema-properties-camelCase:
    description: 模式属性应为 camelCase
    severity: warn
    given: "$.components.schemas[*].properties[*]~"
    then:
      function: casing
      functionOptions:
        type: camel
EOF

# 运行 Spectral
spectral lint openapi.yaml

# Redocly 配置 (redocly.yaml)
cat > redocly.yaml << 'EOF'
extends:
  - recommended

rules:
  no-invalid-media-type-examples: error
  no-invalid-schema-examples: error
  operation-4xx-response: warn
  request-mime-type:
    severity: error
    allowedValues:
      - application/json
  response-mime-type:
    severity: error
    allowedValues:
      - application/json
      - application/problem+json

theme:
  openapi:
    generateCodeSamples:
      languages:
        - lang: curl
        - lang: python
        - lang: javascript
EOF

# 运行 Redocly
redocly lint openapi.yaml
redocly bundle openapi.yaml -o bundled.yaml
redocly preview-docs openapi.yaml
```

## SDK 生成

```bash
# OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# 生成 TypeScript 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/typescript-client \
  --additional-properties=supportsES6=true,npmName=@myorg/api-client

# 生成 Python 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --additional-properties=packageName=api_client

# 生成 Go 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./generated/go-client
```

## 最佳实践

### 应该做的

- **使用 $ref** - 重用模式、参数、响应
- **添加示例** - 真实世界的值有助于使用者
- **记录错误** - 所有可能的错误代码
- **对 API 进行版本控制** - 在 URL 或标头中
- **使用语义版本控制** - 用于规范更改

### 不应该做的

- **不要使用通用描述** - 要具体
- **不要跳过安全** - 定义所有方案
- **不要忘记可空** - 明确说明 null
- **不要混合样式** - 始终如一的命名
- **不要硬编码 URL** - 使用服务器变量

## 资源

- [OpenAPI 3.1 规范](https://spec.openapis.org/oas/v3.1.0)
- [Swagger 编辑器](https://editor.swagger.io/)
- [Redocly](https://redocly.com/)
- [Spectral](https://stoplight.io/open-source/spectral)
