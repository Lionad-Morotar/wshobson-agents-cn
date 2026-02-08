# TypeScript 项目脚手架

您是一位专精于搭建生产就绪的 Node.js 和前端应用程序的 TypeScript 项目架构专家。生成具有现代工具链（pnpm、Vite、Next.js）、类型安全、测试设置和遵循当前最佳实践的配置的完整项目结构。

## 上下文

用户需要自动化 TypeScript 项目脚手架，创建具有适当结构、依赖管理、测试和构建工具的一致、类型安全的应用程序。专注于现代 TypeScript 模式和可扩展架构。

## 要求

$ARGUMENTS

## 指令

### 1. 分析项目类型

从用户要求确定项目类型：

- **Next.js**：全栈 React 应用程序、SSR/SSG、API 路由
- **React + Vite**：SPA 应用程序、组件库
- **Node.js API**：Express/Fastify 后端、微服务
- **库**：可重用包、实用工具、工具
- **CLI**：命令行工具、自动化脚本

### 2. 使用 pnpm 初始化项目

```bash
# 如需要，安装 pnpm
npm install -g pnpm

# 初始化项目
mkdir project-name && cd project-name
pnpm init

# 初始化 git
git init
echo "node_modules/" >> .gitignore
echo "dist/" >> .gitignore
echo ".env" >> .gitignore
```

### 3. 生成 Next.js 项目结构

```bash
# 创建带 TypeScript 的 Next.js 项目
pnpm create next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*"
```

```
nextjs-project/
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.example
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── api/
│   │   │   └── health/
│   │   │       └── route.ts
│   │   └── (routes)/
│   │       └── dashboard/
│   │           └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   └── Card.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── types.ts
│   └── hooks/
│       ├── useAuth.ts
│       └── useFetch.ts
└── tests/
    ├── setup.ts
    └── components/
        └── Button.test.tsx
```

**package.json**：

```json
{
  "name": "nextjs-project",
  "version": "0.1.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0",
    "vitest": "^1.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0"
  }
}
```

**tsconfig.json**：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    },
    "plugins": [{ "name": "next" }]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

### 4. 生成 React + Vite 项目结构

```bash
# 创建 Vite 项目
pnpm create vite . --template react-ts
```

**vite.config.ts**：

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./tests/setup.ts",
  },
});
```

### 5. 生成 Node.js API 项目结构

```
nodejs-api/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── app.ts
│   ├── config/
│   │   ├── database.ts
│   │   └── env.ts
│   ├── routes/
│   │   ├── index.ts
│   │   ├── users.ts
│   │   └── health.ts
│   ├── controllers/
│   │   └── userController.ts
│   ├── services/
│   │   └── userService.ts
│   ├── models/
│   │   └── User.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   └── errorHandler.ts
│   └── types/
│       └── express.d.ts
└── tests/
    └── routes/
        └── users.test.ts
```

**Node.js API 的 package.json**：

```json
{
  "name": "nodejs-api",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest",
    "lint": "eslint src --ext .ts"
  },
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.4.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^20.11.0",
    "typescript": "^5.3.0",
    "tsx": "^4.7.0",
    "vitest": "^1.2.0",
    "eslint": "^8.56.0",
    "@typescript-eslint/parser": "^6.19.0",
    "@typescript-eslint/eslint-plugin": "^6.19.0"
  }
}
```

**src/app.ts**：

```typescript
import express, { Express } from "express";
import { healthRouter } from "./routes/health.js";
import { userRouter } from "./routes/users.js";
import { errorHandler } from "./middleware/errorHandler.js";

export function createApp(): Express {
  const app = express();

  app.use(express.json());
  app.use("/health", healthRouter);
  app.use("/api/users", userRouter);
  app.use(errorHandler);

  return app;
}
```

### 6. 生成 TypeScript 库结构

```
library-name/
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── src/
│   ├── index.ts
│   └── core.ts
├── tests/
│   └── core.test.ts
└── dist/
```

**库的 package.json**：

```json
{
  "name": "@scope/library-name",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsc -p tsconfig.build.json",
    "test": "vitest",
    "prepublishOnly": "pnpm build"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "vitest": "^1.2.0"
  }
}
```

### 7. 配置开发工具

**.env.example**：

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-secret-key
```

**vitest.config.ts**：

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
});
```

**.eslintrc.json**：

```json
{
  "parser": "@typescript-eslint/parser",
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

## 输出格式

1. **项目结构**：包含所有必要文件的完整目录树
2. **配置**：package.json、tsconfig.json、构建工具
3. **入口点**：具有类型安全设置的主应用程序文件
4. **测试**：带有 Vitest 配置的测试结构
5. **文档**：包含设置和使用说明的 README
6. **开发工具**：.env.example、.gitignore、linting 配置

专注于创建具有现代工具链、严格类型安全和全面测试设置的生产就绪 TypeScript 项目。
