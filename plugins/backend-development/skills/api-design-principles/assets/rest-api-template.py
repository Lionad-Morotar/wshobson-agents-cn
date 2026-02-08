"""
使用 FastAPI 的生产就绪 REST API 模板。
包括分页、过滤、错误处理和最佳实践。
"""

from fastapi import FastAPI, HTTPException, Query, Path, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="API 模板",
    version="1.0.0",
    docs_url="/api/docs"
)

# 安全中间件
# 可信主机：防止 HTTP Host 标头攻击
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] # TODO: 在生产环境中配置此项，例如 ["api.example.com"]
)

# CORS：配置跨域资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: 在生产环境中更新为特定来源
    allow_credentials=False, # TODO: 如果需要 cookie/身份验证标头，设置为 True，但需限制来源
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模型
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[UserStatus] = None

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 分页
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    pages: int

# 错误处理
class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "错误"),
            details=exc.detail.get("details") if isinstance(exc.detail, dict) else None
        ).model_dump()
    )

# 端点
@app.get("/api/users", response_model=PaginatedResponse, tags=["用户"])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[UserStatus] = Query(None),
    search: Optional[str] = Query(None)
):
    """列出用户，支持分页和过滤。"""
    # 模拟实现
    total = 100
    items = [
        User(
            id=str(i),
            email=f"user{i}@example.com",
            name=f"用户 {i}",
            status=UserStatus.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ).model_dump()
        for i in range((page-1)*page_size, min(page*page_size, total))
    ]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["用户"])
async def create_user(user: UserCreate):
    """创建新用户。"""
    # 模拟实现
    return User(
        id="123",
        email=user.email,
        name=user.name,
        status=user.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/api/users/{user_id}", response_model=User, tags=["用户"])
async def get_user(user_id: str = Path(..., description="用户 ID")):
    """按 ID 获取用户。"""
    # 模拟：检查是否存在
    if user_id == "999":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "用户未找到", "details": {"id": user_id}}
        )

    return User(
        id=user_id,
        email="user@example.com",
        name="用户名称",
        status=UserStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.patch("/api/users/{user_id}", response_model=User, tags=["用户"])
async def update_user(user_id: str, update: UserUpdate):
    """部分更新用户。"""
    # 验证用户存在
    existing = await get_user(user_id)

    # 应用更新
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing, field, value)

    existing.updated_at = datetime.now()
    return existing

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["用户"])
async def delete_user(user_id: str):
    """删除用户。"""
    await get_user(user_id)  # 验证存在
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)