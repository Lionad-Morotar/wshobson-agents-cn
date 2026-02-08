---
name: auth-implementation-patterns
description: 掌握身份验证和授权模式，包括 JWT、OAuth2、会话管理和 RBAC，以构建安全、可扩展的访问控制系统。在实施身份验证系统、保护 API 或调试安全问题时使用。
---

# 身份验证与授权实现模式

使用行业标准模式和现代最佳实践构建安全、可扩展的身份验证和授权系统。

## 何时使用此技能

- 实施用户身份验证系统
- 保护 REST 或 GraphQL API
- 添加 OAuth2/社交登录
- 实施基于角色的访问控制（RBAC）
- 设计会话管理
- 迁移身份验证系统
- 调试身份验证问题
- 实施 SSO 或多租户

## 核心概念

### 1. 身份验证 vs 授权

**身份验证（AuthN）**：您是谁？

- 验证身份（用户名/密码、OAuth、生物识别）
- 颁发凭证（会话、令牌）
- 管理登录/登出

**授权（AuthZ）**：您可以做什么？

- 权限检查
- 基于角色的访问控制（RBAC）
- 资源所有权验证
- 策略执行

### 2. 身份验证策略

**基于会话：**

- 服务器存储会话状态
- Cookie 中的会话 ID
- 传统、简单、有状态

**基于令牌（JWT）：**

- 无状态、自包含
- 水平扩展
- 可存储声明

**OAuth2/OpenID Connect：**

- 委托身份验证
- 社交登录（Google、GitHub）
- 企业 SSO

## JWT 身份验证

### 模式 1：JWT 实现

```typescript
// JWT 结构：header.payload.signature
import jwt from "jsonwebtoken";
import { Request, Response, NextFunction } from "express";

interface JWTPayload {
  userId: string;
  email: string;
  role: string;
  iat: number;
  exp: number;
}

// 生成 JWT
function generateTokens(userId: string, email: string, role: string) {
  const accessToken = jwt.sign(
    { userId, email, role },
    process.env.JWT_SECRET!,
    { expiresIn: "15m" }, // 短期有效
  );

  const refreshToken = jwt.sign(
    { userId },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: "7d" }, // 长期有效
  );

  return { accessToken, refreshToken };
}

// 验证 JWT
function verifyToken(token: string): JWTPayload {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new Error("令牌已过期");
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new Error("无效令牌");
    }
    throw error;
  }
}

// 中间件
function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "未提供令牌" });
  }

  const token = authHeader.substring(7);
  try {
    const payload = verifyToken(token);
    req.user = payload; // 将用户附加到请求
    next();
  } catch (error) {
    return res.status(401).json({ error: "无效令牌" });
  }
}

// 使用
app.get("/api/profile", authenticate, (req, res) => {
  res.json({ user: req.user });
});
```

### 模式 2：刷新令牌流程

```typescript
interface StoredRefreshToken {
  token: string;
  userId: string;
  expiresAt: Date;
  createdAt: Date;
}

class RefreshTokenService {
  // 在数据库中存储刷新令牌
  async storeRefreshToken(userId: string, refreshToken: string) {
    const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    await db.refreshTokens.create({
      token: await hash(refreshToken), // 存储前哈希
      userId,
      expiresAt,
    });
  }

  // 刷新访问令牌
  async refreshAccessToken(refreshToken: string) {
    // 验证刷新令牌
    let payload;
    try {
      payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!) as {
        userId: string;
      };
    } catch {
      throw new Error("无效的刷新令牌");
    }

    // 检查令牌是否存在于数据库中
    const storedToken = await db.refreshTokens.findOne({
      where: {
        token: await hash(refreshToken),
        userId: payload.userId,
        expiresAt: { $gt: new Date() },
      },
    });

    if (!storedToken) {
      throw new Error("刷新令牌未找到或已过期");
    }

    // 获取用户
    const user = await db.users.findById(payload.userId);
    if (!user) {
      throw new Error("用户未找到");
    }

    // 生成新的访问令牌
    const accessToken = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET!,
      { expiresIn: "15m" },
    );

    return { accessToken };
  }

  // 撤销刷新令牌（登出）
  async revokeRefreshToken(refreshToken: string) {
    await db.refreshTokens.deleteOne({
      token: await hash(refreshToken),
    });
  }

  // 撤销所有用户令牌（登出所有设备）
  async revokeAllUserTokens(userId: string) {
    await db.refreshTokens.deleteMany({ userId });
  }
}

// API 端点
app.post("/api/auth/refresh", async (req, res) => {
  const { refreshToken } = req.body;
  try {
    const { accessToken } =
      await refreshTokenService.refreshAccessToken(refreshToken);
    res.json({ accessToken });
  } catch (error) {
    res.status(401).json({ error: "无效的刷新令牌" });
  }
});

app.post("/api/auth/logout", authenticate, async (req, res) => {
  const { refreshToken } = req.body;
  await refreshTokenService.revokeRefreshToken(refreshToken);
  res.json({ message: "成功登出" });
});
```

## 基于会话的身份验证

### 模式 1：Express 会话

```typescript
import session from "express-session";
import RedisStore from "connect-redis";
import { createClient } from "redis";

// 为会话存储设置 Redis
const redisClient = createClient({
  url: process.env.REDIS_URL,
});
await redisClient.connect();

app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === "production", // 仅 HTTPS
      httpOnly: true, // 无 JavaScript 访问
      maxAge: 24 * 60 * 60 * 1000, // 24 小时
      sameSite: "strict", // CSRF 保护
    },
  }),
);

// 登录
app.post("/api/auth/login", async (req, res) => {
  const { email, password } = req.body;

  const user = await db.users.findOne({ email });
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: "无效的凭证" });
  }

  // 在会话中存储用户
  req.session.userId = user.id;
  req.session.role = user.role;

  res.json({ user: { id: user.id, email: user.email, role: user.role } });
});

// 会话中间件
function requireAuth(req: Request, res: Response, next: NextFunction) {
  if (!req.session.userId) {
    return res.status(401).json({ error: "未通过身份验证" });
  }
  next();
}

// 受保护路由
app.get("/api/profile", requireAuth, async (req, res) => {
  const user = await db.users.findById(req.session.userId);
  res.json({ user });
});

// 登出
app.post("/api/auth/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: "登出失败" });
    }
    res.clearCookie("connect.sid");
    res.json({ message: "成功登出" });
  });
});
```

## OAuth2 / 社交登录

### 模式 1：使用 Passport.js 的 OAuth2

```typescript
import passport from "passport";
import { Strategy as GoogleStrategy } from "passport-google-oauth20";
import { Strategy as GitHubStrategy } from "passport-github2";

// Google OAuth
passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      callbackURL: "/api/auth/google/callback",
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        // 查找或创建用户
        let user = await db.users.findOne({
          googleId: profile.id,
        });

        if (!user) {
          user = await db.users.create({
            googleId: profile.id,
            email: profile.emails?.[0]?.value,
            name: profile.displayName,
            avatar: profile.photos?.[0]?.value,
          });
        }

        return done(null, user);
      } catch (error) {
        return done(error, undefined);
      }
    },
  ),
);

// 路由
app.get(
  "/api/auth/google",
  passport.authenticate("google", {
    scope: ["profile", "email"],
  }),
);

app.get(
  "/api/auth/google/callback",
  passport.authenticate("google", { session: false }),
  (req, res) => {
    // 生成 JWT
    const tokens = generateTokens(req.user.id, req.user.email, req.user.role);
    // 使用令牌重定向到前端
    res.redirect(
      `${process.env.FRONTEND_URL}/auth/callback?token=${tokens.accessToken}`,
    );
  },
);
```

## 授权模式

### 模式 1：基于角色的访问控制（RBAC）

```typescript
enum Role {
  USER = "user",
  MODERATOR = "moderator",
  ADMIN = "admin",
}

const roleHierarchy: Record<Role, Role[]> = {
  [Role.ADMIN]: [Role.ADMIN, Role.MODERATOR, Role.USER],
  [Role.MODERATOR]: [Role.MODERATOR, Role.USER],
  [Role.USER]: [Role.USER],
};

function hasRole(userRole: Role, requiredRole: Role): boolean {
  return roleHierarchy[userRole].includes(requiredRole);
}

// 中间件
function requireRole(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "未通过身份验证" });
    }

    if (!roles.some((role) => hasRole(req.user.role, role))) {
      return res.status(403).json({ error: "权限不足" });
    }

    next();
  };
}

// 使用
app.delete(
  "/api/users/:id",
  authenticate,
  requireRole(Role.ADMIN),
  async (req, res) => {
    // 仅管理员可以删除用户
    await db.users.delete(req.params.id);
    res.json({ message: "用户已删除" });
  },
);
```

### 模式 2：基于权限的访问控制

```typescript
enum Permission {
  READ_USERS = "read:users",
  WRITE_USERS = "write:users",
  DELETE_USERS = "delete:users",
  READ_POSTS = "read:posts",
  WRITE_POSTS = "write:posts",
}

const rolePermissions: Record<Role, Permission[]> = {
  [Role.USER]: [Permission.READ_POSTS, Permission.WRITE_POSTS],
  [Role.MODERATOR]: [
    Permission.READ_POSTS,
    Permission.WRITE_POSTS,
    Permission.READ_USERS,
  ],
  [Role.ADMIN]: Object.values(Permission),
};

function hasPermission(userRole: Role, permission: Permission): boolean {
  return rolePermissions[userRole]?.includes(permission) ?? false;
}

function requirePermission(...permissions: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "未通过身份验证" });
    }

    const hasAllPermissions = permissions.every((permission) =>
      hasPermission(req.user.role, permission),
    );

    if (!hasAllPermissions) {
      return res.status(403).json({ error: "权限不足" });
    }

    next();
  };
}

// 使用
app.get(
  "/api/users",
  authenticate,
  requirePermission(Permission.READ_USERS),
  async (req, res) => {
    const users = await db.users.findAll();
    res.json({ users });
  },
);
```

### 模式 3：资源所有权

```typescript
// 检查用户是否拥有资源
async function requireOwnership(
  resourceType: "post" | "comment",
  resourceIdParam: string = "id",
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "未通过身份验证" });
    }

    const resourceId = req.params[resourceIdParam];

    // 管理员可以访问任何内容
    if (req.user.role === Role.ADMIN) {
      return next();
    }

    // 检查所有权
    let resource;
    if (resourceType === "post") {
      resource = await db.posts.findById(resourceId);
    } else if (resourceType === "comment") {
      resource = await db.comments.findById(resourceId);
    }

    if (!resource) {
      return res.status(404).json({ error: "资源未找到" });
    }

    if (resource.userId !== req.user.userId) {
      return res.status(403).json({ error: "未授权" });
    }

    next();
  };
}

// 使用
app.put(
  "/api/posts/:id",
  authenticate,
  requireOwnership("post"),
  async (req, res) => {
    // 用户只能更新自己的帖子
    const post = await db.posts.update(req.params.id, req.body);
    res.json({ post });
  },
);
```

## 安全最佳实践

### 模式 1：密码安全

```typescript
import bcrypt from "bcrypt";
import { z } from "zod";

// 密码验证架构
const passwordSchema = z
  .string()
  .min(12, "密码必须至少 12 个字符")
  .regex(/[A-Z]/, "密码必须包含大写字母")
  .regex(/[a-z]/, "密码必须包含小写字母")
  .regex(/[0-9]/, "密码必须包含数字")
  .regex(/[^A-Za-z0-9]/, "密码必须包含特殊字符");

// 哈希密码
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12; // 2^12 次迭代
  return bcrypt.hash(password, saltRounds);
}

// 验证密码
async function verifyPassword(
  password: string,
  hash: string,
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// 带密码验证的注册
app.post("/api/auth/register", async (req, res) => {
  try {
    const { email, password } = req.body;

    // 验证密码
    passwordSchema.parse(password);

    // 检查用户是否存在
    const existingUser = await db.users.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: "邮箱已注册" });
    }

    // 哈希密码
    const passwordHash = await hashPassword(password);

    // 创建用户
    const user = await db.users.create({
      email,
      passwordHash,
    });

    // 生成令牌
    const tokens = generateTokens(user.id, user.email, user.role);

    res.status(201).json({
      user: { id: user.id, email: user.email },
      ...tokens,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors[0].message });
    }
    res.status(500).json({ error: "注册失败" });
  }
});
```

### 模式 2：速率限制

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";

// 登录速率限制器
const loginLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 5, // 5 次尝试
  message: "登录尝试过多，请稍后再试",
  standardHeaders: true,
  legacyHeaders: false,
});

// API 速率限制器
const apiLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 分钟
  max: 100, // 每分钟 100 个请求
  standardHeaders: true,
});

// 应用到路由
app.post("/api/auth/login", loginLimiter, async (req, res) => {
  // 登录逻辑
});

app.use("/api/", apiLimiter);
```

## 最佳实践

1. **永远不要存储明文密码**：始终使用 bcrypt/argon2 哈希
2. **使用 HTTPS**：加密传输中的数据
3. **短期访问令牌**：最多 15-30 分钟
4. **安全 Cookie**：httpOnly、secure、sameSite 标志
5. **验证所有输入**：邮箱格式、密码强度
6. **对身份验证端点进行速率限制**：防止暴力攻击
7. **实施 CSRF 保护**：对于基于会话的身份验证
8. **定期轮换密钥**：JWT 密钥、会话密钥
9. **记录安全事件**：登录尝试、失败的身份验证
10. **尽可能使用 MFA**：额外的安全层

## 常见陷阱

- **弱密码**：执行强密码策略
- **localStorage 中的 JWT**：易受 XSS 攻击，使用 httpOnly cookie
- **令牌永不过期**：令牌应该过期
- **仅客户端身份验证检查**：始终在服务器端验证
- **不安全的密码重置**：使用带过期的安全令牌
- **无速率限制**：易受暴力攻击
- **信任客户端数据**：始终在服务器上验证

## 资源

- **references/jwt-best-practices.md**：JWT 实施指南
- **references/oauth2-flows.md**：OAuth2 流程图和示例
- **references/session-security.md**：安全会话管理
- **assets/auth-security-checklist.md**：安全审查清单
- **assets/password-policy-template.md**：密码要求模板
- **scripts/token-validator.ts**：JWT 验证工具
