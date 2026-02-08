---
name: parallel-feature-development
description: 使用文件所有权策略、冲突避免规则和多智能体集成的集成模式协调并行功能开发。在为并行开发分解功能、建立文件所有权边界或管理并行工作流之间的集成时使用此技能。
version: 1.0.2
---

# 并行功能开发

将功能分解为并行工作流、建立文件所有权边界、避免冲突以及集成多个实现者智能体结果的策略。

## 何时使用此技能

- 为并行实现分解功能
- 在智能体之间建立文件所有权边界
- 设计并行工作流之间的接口契约
- 选择集成策略(垂直切片 vs 水平层)
- 管理并行开发的分支和合并工作流

## 文件所有权策略

### 按目录

为每个实现者分配特定目录的所有权:

```
implementer-1: src/components/auth/
implementer-2: src/api/auth/
implementer-3: tests/auth/
```

**最适合**: 具有清晰目录边界的良好组织的代码库。

### 按模块

分配逻辑模块的所有权(可能跨越目录):

```
implementer-1: 认证模块(登录、注册、登出)
implementer-2: 授权模块(角色、权限、守卫)
```

**最适合**: 面向功能的架构、领域驱动设计。

### 按层

分配架构层的所有权:

```
implementer-1: UI 层(组件、样式、布局)
implementer-2: 业务逻辑层(服务、验证器)
implementer-3: 数据层(模型、存储库、迁移)
```

**最适合**: 传统 MVC/分层架构。

## 冲突避免规则

### 基本规则

**每个文件一个所有者。** 不应将文件分配给多个实现者。

### 当文件必须共享时

如果文件确实需要多个实现者的更改:

1. **指定单一所有者** — 一个实现者拥有文件
2. **其他实现者请求更改** — 向所有者发送具体的更改请求消息
3. **所有者顺序应用更改** — 防止合并冲突
4. **替代方案:提取接口** — 创建单独的接口文件,非所有者可以在不修改的情况下导入

### 接口契约

当实现者需要在边界处协调时:

```typescript
// src/types/auth-contract.ts(由 team-lead 拥有,实现者只读)
export interface AuthResponse {
  token: string;
  user: UserProfile;
  expiresAt: number;
}

export interface AuthService {
  login(email: string, password: string): Promise<AuthResponse>;
  register(data: RegisterData): Promise<AuthResponse>;
}
```

两个实现者都从契约文件导入,但都不修改它。

## 集成模式

### 垂直切片

每个实现者构建完整的功能切片(UI + API + 测试):

```
implementer-1: 登录功能(登录表单 + 登录 API + 登录测试)
implementer-2: 注册功能(注册表单 + 注册 API + 注册测试)
```

**优点**: 每个切片独立可测试,需要最少的集成。
**缺点**: 可能重复共享工具,对于紧密耦合的功能更难。

### 水平层

每个实现者在所有功能上构建一层:

```
implementer-1: 所有 UI 组件(登录表单、注册表单、配置文件页面)
implementer-2: 所有 API 端点(登录、注册、配置文件)
implementer-3: 所有测试(单元、集成、e2e)
```

**优点**: 每层内的一致模式,自然专业化。
**缺点**: 更多集成点,第 3 层依赖于第 1 层和第 2 层。

### 混合

基于耦合混合垂直和水平:

```
implementer-1: 登录功能(垂直切片 — UI + API + 测试)
implementer-2: 共享认证基础设施(水平 — 中间件、JWT 工具、类型)
```

**最适合**: 具有一些共享基础设施的大多数真实世界功能。

## 分支管理

### 单分支策略

所有实现者在同一功能分支上工作:

- 简单设置,无合并开销
- 需要严格的文件所有权以避免冲突
- 最适合:小团队(2-3),明确定义的边界

### 多分支策略

每个实现者在子分支上工作:

```
feature/auth
  ├── feature/auth-login      (implementer-1)
  ├── feature/auth-register    (implementer-2)
  └── feature/auth-tests       (implementer-3)
```

- 更多隔离,显式合并点
- 更高开销,共享文件中仍可能发生合并冲突
- 最适合:较大的团队(4+),复杂功能
