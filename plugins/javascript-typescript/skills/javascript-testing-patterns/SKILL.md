---
name: javascript-testing-patterns
description: 使用 Jest、Vitest 和 Testing Library 实现全面的测试策略，包括单元测试、集成测试和端到端测试，以及模拟、固件和测试驱动开发。在编写 JavaScript/TypeScript 测试、设置测试基础设施或实施 TDD/BDD 工作流程时使用。
---

# JavaScript 测试模式

使用现代测试框架和最佳实践在 JavaScript/TypeScript 应用程序中实施健壮测试策略的综合指南。

## 何时使用此技能

- 为新项目设置测试基础设施
- 为函数和类编写单元测试
- 为 API 和服务创建集成测试
- 为用户流程实施端到端测试
- 模拟外部依赖和 API
- 测试 React、Vue 或其他前端组件
- 实施测试驱动开发（TDD）
- 在 CI/CD 流水线中设置持续测试

## 测试框架

### Jest - 全功能测试框架

**设置：**

```typescript
// jest.config.ts
import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  testMatch: ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.interface.ts",
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ["<rootDir>/src/test/setup.ts"],
};

export default config;
```

### Vitest - 快速的 Vite 原生测试

**设置：**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["**/*.d.ts", "**/*.config.ts", "**/dist/**"],
    },
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

## 单元测试模式

### 模式 1：测试纯函数

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from "vitest";
import { add, divide } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("应该将两个正数相加", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("应该处理负数", () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it("应该处理零", () => {
      expect(add(0, 5)).toBe(5);
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("应该除两个数", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("应该处理小数结果", () => {
      expect(divide(5, 2)).toBe(2.5);
    });

    it("除以零时应该抛出错误", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});
```

### 模式 2：测试类

```typescript
// services/user.service.ts
export class UserService {
  private users: Map<string, User> = new Map();

  create(user: User): User {
    if (this.users.has(user.id)) {
      throw new Error("User already exists");
    }
    this.users.set(user.id, user);
    return user;
  }

  findById(id: string): User | undefined {
    return this.users.get(id);
  }

  update(id: string, updates: Partial<User>): User {
    const user = this.users.get(id);
    if (!user) {
      throw new Error("User not found");
    }
    const updated = { ...user, ...updates };
    this.users.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.users.delete(id);
  }
}

// services/user.service.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { UserService } from "./user.service";

describe("UserService", () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  describe("create", () => {
    it("应该创建新用户", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      const created = service.create(user);

      expect(created).toEqual(user);
      expect(service.findById("1")).toEqual(user);
    });

    it("如果用户已存在应该抛出错误", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      service.create(user);

      expect(() => service.create(user)).toThrow("User already exists");
    });
  });

  describe("update", () => {
    it("应该更新现有用户", () => {
      const user = { id: "1", name: "John", email: "john@example.com" };
      service.create(user);

      const updated = service.update("1", { name: "Jane" });

      expect(updated.name).toBe("Jane");
      expect(updated.email).toBe("john@example.com");
    });

    it("如果用户未找到应该抛出错误", () => {
      expect(() => service.update("999", { name: "Jane" })).toThrow(
        "User not found",
      );
    });
  });
});
```

### 模式 3：测试异步函数

```typescript
// services/api.service.ts
export class ApiService {
  async fetchUser(id: string): Promise<User> {
    const response = await fetch(`https://api.example.com/users/${id}`);
    if (!response.ok) {
      throw new Error("User not found");
    }
    return response.json();
  }

  async createUser(user: CreateUserDTO): Promise<User> {
    const response = await fetch("https://api.example.com/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
    });
    return response.json();
  }
}

// services/api.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { ApiService } from "./api.service";

// 全局模拟 fetch
global.fetch = vi.fn();

describe("ApiService", () => {
  let service: ApiService;

  beforeEach(() => {
    service = new ApiService();
    vi.clearAllMocks();
  });

  describe("fetchUser", () => {
    it("应该成功获取用户", async () => {
      const mockUser = { id: "1", name: "John", email: "john@example.com" };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockUser,
      });

      const user = await service.fetchUser("1");

      expect(user).toEqual(mockUser);
      expect(fetch).toHaveBeenCalledWith("https://api.example.com/users/1");
    });

    it("如果用户未找到应该抛出错误", async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: false,
      });

      await expect(service.fetchUser("999")).rejects.toThrow("User not found");
    });
  });

  describe("createUser", () => {
    it("应该成功创建用户", async () => {
      const newUser = { name: "John", email: "john@example.com" };
      const createdUser = { id: "1", ...newUser };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => createdUser,
      });

      const user = await service.createUser(newUser);

      expect(user).toEqual(createdUser);
      expect(fetch).toHaveBeenCalledWith(
        "https://api.example.com/users",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify(newUser),
        }),
      );
    });
  });
});
```

## 模拟模式

### 模式 1：模拟模块

```typescript
// services/email.service.ts
import nodemailer from "nodemailer";

export class EmailService {
  private transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: 587,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  async sendEmail(to: string, subject: string, html: string) {
    await this.transporter.sendMail({
      from: process.env.EMAIL_FROM,
      to,
      subject,
      html,
    });
  }
}

// services/email.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { EmailService } from "./email.service";

vi.mock("nodemailer", () => ({
  default: {
    createTransport: vi.fn(() => ({
      sendMail: vi.fn().mockResolvedValue({ messageId: "123" }),
    })),
  },
}));

describe("EmailService", () => {
  let service: EmailService;

  beforeEach(() => {
    service = new EmailService();
  });

  it("应该成功发送邮件", async () => {
    await service.sendEmail(
      "test@example.com",
      "Test Subject",
      "<p>Test Body</p>",
    );

    expect(service["transporter"].sendMail).toHaveBeenCalledWith(
      expect.objectContaining({
        to: "test@example.com",
        subject: "Test Subject",
      }),
    );
  });
});
```

### 模式 2：依赖注入测试

```typescript
// services/user.service.ts
export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  create(user: User): Promise<User>;
}

export class UserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error("User not found");
    }
    return user;
  }

  async createUser(userData: CreateUserDTO): Promise<User> {
    // 业务逻辑
    const user = { id: generateId(), ...userData };
    return this.userRepository.create(user);
  }
}

// services/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { UserService, IUserRepository } from "./user.service";

describe("UserService", () => {
  let service: UserService;
  let mockRepository: IUserRepository;

  beforeEach(() => {
    mockRepository = {
      findById: vi.fn(),
      create: vi.fn(),
    };
    service = new UserService(mockRepository);
  });

  describe("getUser", () => {
    it("如果找到应该返回用户", async () => {
      const mockUser = { id: "1", name: "John", email: "john@example.com" };
      vi.mocked(mockRepository.findById).mockResolvedValue(mockUser);

      const user = await service.getUser("1");

      expect(user).toEqual(mockUser);
      expect(mockRepository.findById).toHaveBeenCalledWith("1");
    });

    it("如果用户未找到应该抛出错误", async () => {
      vi.mocked(mockRepository.findById).mockResolvedValue(null);

      await expect(service.getUser("999")).rejects.toThrow("User not found");
    });
  });

  describe("createUser", () => {
    it("应该成功创建用户", async () => {
      const userData = { name: "John", email: "john@example.com" };
      const createdUser = { id: "1", ...userData };

      vi.mocked(mockRepository.create).mockResolvedValue(createdUser);

      const user = await service.createUser(userData);

      expect(user).toEqual(createdUser);
      expect(mockRepository.create).toHaveBeenCalled();
    });
  });
});
```

### 模式 3：监视函数

```typescript
// utils/logger.ts
export const logger = {
  info: (message: string) => console.log(`INFO: ${message}`),
  error: (message: string) => console.error(`ERROR: ${message}`),
};

// services/order.service.ts
import { logger } from "../utils/logger";

export class OrderService {
  async processOrder(orderId: string): Promise<void> {
    logger.info(`Processing order ${orderId}`);
    // 处理订单逻辑
    logger.info(`Order ${orderId} processed successfully`);
  }
}

// services/order.service.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { OrderService } from "./order.service";
import { logger } from "../utils/logger";

describe("OrderService", () => {
  let service: OrderService;
  let loggerSpy: any;

  beforeEach(() => {
    service = new OrderService();
    loggerSpy = vi.spyOn(logger, "info");
  });

  afterEach(() => {
    loggerSpy.mockRestore();
  });

  it("应该记录订单处理", async () => {
    await service.processOrder("123");

    expect(loggerSpy).toHaveBeenCalledWith("Processing order 123");
    expect(loggerSpy).toHaveBeenCalledWith("Order 123 processed successfully");
    expect(loggerSpy).toHaveBeenCalledTimes(2);
  });
});
```

## 集成测试

### 模式 1：API 集成测试

```typescript
// tests/integration/user.api.test.ts
import request from "supertest";
import { app } from "../../src/app";
import { pool } from "../../src/config/database";

describe("User API Integration Tests", () => {
  beforeAll(async () => {
    // 设置测试数据库
    await pool.query("CREATE TABLE IF NOT EXISTS users (...)");
  });

  afterAll(async () => {
    // 清理
    await pool.query("DROP TABLE IF EXISTS users");
    await pool.end();
  });

  beforeEach(async () => {
    // 每个测试前清除数据
    await pool.query("TRUNCATE TABLE users CASCADE");
  });

  describe("POST /api/users", () => {
    it("应该创建新用户", async () => {
      const userData = {
        name: "John Doe",
        email: "john@example.com",
        password: "password123",
      };

      const response = await request(app)
        .post("/api/users")
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        name: userData.name,
        email: userData.email,
      });
      expect(response.body).toHaveProperty("id");
      expect(response.body).not.toHaveProperty("password");
    });

    it("如果邮箱无效应该返回 400", async () => {
      const userData = {
        name: "John Doe",
        email: "invalid-email",
        password: "password123",
      };

      const response = await request(app)
        .post("/api/users")
        .send(userData)
        .expect(400);

      expect(response.body).toHaveProperty("error");
    });

    it("如果邮箱已存在应该返回 409", async () => {
      const userData = {
        name: "John Doe",
        email: "john@example.com",
        password: "password123",
      };

      await request(app).post("/api/users").send(userData);

      const response = await request(app)
        .post("/api/users")
        .send(userData)
        .expect(409);

      expect(response.body.error).toContain("already exists");
    });
  });

  describe("GET /api/users/:id", () => {
    it("应该通过 id 获取用户", async () => {
      const createResponse = await request(app).post("/api/users").send({
        name: "John Doe",
        email: "john@example.com",
        password: "password123",
      });

      const userId = createResponse.body.id;

      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body).toMatchObject({
        id: userId,
        name: "John Doe",
        email: "john@example.com",
      });
    });

    it("如果用户未找到应该返回 404", async () => {
      await request(app).get("/api/users/999").expect(404);
    });
  });

  describe("Authentication", () => {
    it("应该要求保护路由的身份验证", async () => {
      await request(app).get("/api/users/me").expect(401);
    });

    it("应该允许使用有效令牌访问", async () => {
      // 创建用户并登录
      await request(app).post("/api/users").send({
        name: "John Doe",
        email: "john@example.com",
        password: "password123",
      });

      const loginResponse = await request(app).post("/api/auth/login").send({
        email: "john@example.com",
        password: "password123",
      });

      const token = loginResponse.body.token;

      const response = await request(app)
        .get("/api/users/me")
        .set("Authorization", `Bearer ${token}`)
        .expect(200);

      expect(response.body.email).toBe("john@example.com");
    });
  });
});
```

### 模式 2：数据库集成测试

```typescript
// tests/integration/user.repository.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { Pool } from "pg";
import { UserRepository } from "../../src/repositories/user.repository";

describe("UserRepository Integration Tests", () => {
  let pool: Pool;
  let repository: UserRepository;

  beforeAll(async () => {
    pool = new Pool({
      host: "localhost",
      port: 5432,
      database: "test_db",
      user: "test_user",
      password: "test_password",
    });

    repository = new UserRepository(pool);

    // 创建表
    await pool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
  });

  afterAll(async () => {
    await pool.query("DROP TABLE IF EXISTS users");
    await pool.end();
  });

  beforeEach(async () => {
    await pool.query("TRUNCATE TABLE users CASCADE");
  });

  it("应该创建用户", async () => {
    const user = await repository.create({
      name: "John Doe",
      email: "john@example.com",
      password: "hashed_password",
    });

    expect(user).toHaveProperty("id");
    expect(user.name).toBe("John Doe");
    expect(user.email).toBe("john@example.com");
  });

  it("应该通过邮箱查找用户", async () => {
    await repository.create({
      name: "John Doe",
      email: "john@example.com",
      password: "hashed_password",
    });

    const user = await repository.findByEmail("john@example.com");

    expect(user).toBeTruthy();
    expect(user?.name).toBe("John Doe");
  });

  it("如果用户未找到应该返回 null", async () => {
    const user = await repository.findByEmail("nonexistent@example.com");
    expect(user).toBeNull();
  });
});
```

## 使用 Testing Library 进行前端测试

### 模式 1：React 组件测试

```typescript
// components/UserForm.tsx
import { useState } from 'react';

interface Props {
  onSubmit: (user: { name: string; email: string }) => void;
}

export function UserForm({ onSubmit }: Props) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ name, email });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        data-testid="name-input"
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        data-testid="email-input"
      />
      <button type="submit">Submit</button>
    </form>
  );
}

// components/UserForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { UserForm } from './UserForm';

describe('UserForm', () => {
  it('应该渲染表单输入', () => {
    render(<UserForm onSubmit={vi.fn()} />);

    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('应该更新输入值', () => {
    render(<UserForm onSubmit={vi.fn()} />);

    const nameInput = screen.getByTestId('name-input') as HTMLInputElement;
    const emailInput = screen.getByTestId('email-input') as HTMLInputElement;

    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });

    expect(nameInput.value).toBe('John Doe');
    expect(emailInput.value).toBe('john@example.com');
  });

  it('应该使用表单数据调用 onSubmit', () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByTestId('name-input'), {
      target: { value: 'John Doe' },
    });
    fireEvent.change(screen.getByTestId('email-input'), {
      target: { value: 'john@example.com' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    expect(onSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
    });
  });
});
```

### 模式 2：测试 Hooks

```typescript
// hooks/useCounter.ts
import { useState, useCallback } from "react";

export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => setCount((c) => c + 1), []);
  const decrement = useCallback(() => setCount((c) => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);

  return { count, increment, decrement, reset };
}

// hooks/useCounter.test.ts
import { renderHook, act } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("应该使用默认值初始化", () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it("应该使用自定义值初始化", () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it("应该增加计数", () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it("应该减少计数", () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it("应该重置为初始值", () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

## 测试固件和工厂

```typescript
// tests/fixtures/user.fixture.ts
import { faker } from "@faker-js/faker";

export function createUserFixture(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    createdAt: faker.date.past(),
    ...overrides,
  };
}

export function createUsersFixture(count: number): User[] {
  return Array.from({ length: count }, () => createUserFixture());
}

// 在测试中使用
import {
  createUserFixture,
  createUsersFixture,
} from "../fixtures/user.fixture";

describe("UserService", () => {
  it("应该处理用户", () => {
    const user = createUserFixture({ name: "John Doe" });
    // 在测试中使用用户
  });

  it("应该处理多个用户", () => {
    const users = createUsersFixture(10);
    // 在测试中使用用户
  });
});
```

## 快照测试

```typescript
// components/UserCard.test.tsx
import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  it('应该匹配快照', () => {
    const user = {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      avatar: 'https://example.com/avatar.jpg',
    };

    const { container } = render(<UserCard user={user} />);

    expect(container.firstChild).toMatchSnapshot();
  });

  it('应该匹配加载状态的快照', () => {
    const { container } = render(<UserCard loading />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
```

## 覆盖率报告

```typescript
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "test:ui": "vitest --ui"
  }
}
```

## 最佳实践

1. **遵循 AAA 模式**：Arrange（准备）、Act（执行）、Assert（断言）
2. **每个测试一个断言**：或逻辑相关的断言
3. **描述性测试名称**：应该描述正在测试的内容
4. **使用 beforeEach/afterEach**：用于设置和清理
5. **模拟外部依赖**：保持测试隔离
6. **测试边缘情况**：不仅是快乐路径
7. **避免实现细节**：测试行为，而不是实现
8. **使用测试工厂**：用于一致的测试数据
9. **保持测试快速**：模拟慢操作
10. **先编写测试（TDD）**：尽可能
11. **维护测试覆盖率**：目标 80%+ 覆盖率
12. **使用 TypeScript**：用于类型安全的测试
13. **测试错误处理**：不仅是成功情况
14. **谨慎使用 data-testid**：首选语义查询
15. **测试后清理**：防止测试污染

## 常见模式

### 测试组织

```typescript
describe("UserService", () => {
  describe("createUser", () => {
    it("应该成功创建用户", () => {});
    it("如果邮箱存在应该抛出错误", () => {});
    it("应该哈希密码", () => {});
  });

  describe("updateUser", () => {
    it("应该更新用户", () => {});
    it("如果未找到应该抛出错误", () => {});
  });
});
```

### 测试 Promises

```typescript
// 使用 async/await
it("应该获取用户", async () => {
  const user = await service.fetchUser("1");
  expect(user).toBeDefined();
});

// 测试拒绝
it("应该抛出错误", async () => {
  await expect(service.fetchUser("invalid")).rejects.toThrow("Not found");
});
```

### 测试定时器

```typescript
import { vi } from "vitest";

it("应该在延迟后调用函数", () => {
  vi.useFakeTimers();

  const callback = vi.fn();
  setTimeout(callback, 1000);

  expect(callback).not.toHaveBeenCalled();

  vi.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();

  vi.useRealTimers();
});
```

## 资源

- **Jest 文档**：https://jestjs.io/
- **Vitest 文档**：https://vitest.dev/
- **Testing Library**：https://testing-library.com/
- **Kent C. Dodds 测试博客**：https://kentcdodds.com/blog/
