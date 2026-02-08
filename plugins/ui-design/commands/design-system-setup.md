---
description: "初始化设计系统（包含设计令牌）"
argument-hint: "[--preset minimal|standard|comprehensive]"
---

# 设计系统初始化

使用设计令牌、组件模式和文档初始化设计系统。为一致的 UI 开发创建基础。

## 前置检查

1. 检查 `.ui-design/` 目录是否存在：
   - 如果存在且包含 `design-system.json`：询问是更新还是重新初始化
   - 如果不存在：创建 `.ui-design/` 目录

2. 检测现有设计系统指标：
   - 检查 `tailwind.config.js` 是否有自定义主题
   - 检查全局样式中是否有 CSS 自定义属性
   - 检查是否存在令牌文件（tokens.json、theme.ts 等）
   - 检查设计系统包（chakra、radix、shadcn 等）

3. 加载项目上下文：
   - 如果存在则读取 `conductor/tech-stack.md`
   - 检测样式方案（CSS、Tailwind、styled-components 等）
   - 检测 TypeScript 使用情况

4. 如果检测到现有设计系统：

   ```
   检测到现有的设计系统配置：

   - {detected_system}

   您希望：
   1. 与现有系统集成（添加缺失的令牌）
   2. 使用新的设计系统替换
   3. 查看当前配置
   4. 取消

   请输入数字：
   ```

## 交互式配置

**关键规则：**

- 每次只问一个问题
- 等待用户响应后再继续
- 在生成文件之前构建完整的规范

### 问题 1：设计系统预设（如果未提供）

```
您需要什么级别的设计系统？

1. 精简版   - 仅包含颜色、排版、间距
               最适合：小型项目、快速原型开发

2. 标准版  - 颜色、排版、间距、阴影、边框、断点
               最适合：大多数项目、灵活性的良好平衡

3. 完整版 - 包含语义化命名、组件令牌、动画和文档的完整令牌系统
               最适合：大型项目、设计团队、长期维护

请输入数字：
```

### 问题 2：品牌颜色

```
让我们定义您的品牌颜色。

请输入您的主品牌颜色（十六进制代码，例如 #3B82F6）：
```

收到主颜色后：

```
主颜色：{color}

现在请输入您的次要/强调颜色（或按回车键自动生成）：
```

### 问题 3：色彩模式支持

```
设计系统应该支持哪些色彩模式？

1. 仅浅色模式
2. 仅深色模式
3. 浅色和深色模式
4. 浅色、深色和系统偏好

请输入数字：
```

### 问题 4：排版

```
应该使用什么字体族？

1. 系统字体（加载最快，原生感觉）
   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...

2. Inter（现代，高可读性）
3. Open Sans（友好，通用）
4. Roboto（简洁，Google 标准）
5. 自定义（提供名称）

请输入数字或字体名称：
```

### 问题 5：间距比例

```
采用什么间距比例理念？

1. 线性（4px 基础）
   4, 8, 12, 16, 20, 24, 32, 40, 48, 64

2. 几何（4px 基础，1.5 倍乘数）
   4, 6, 9, 14, 21, 32, 48, 72

3. Tailwind 兼容
   0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64

4. 自定义（提供值）

请输入数字：
```

### 问题 6：边框圆角

```
采用什么圆角样式？

1. 锐角    - 0px（无圆角）
2. 微圆   - 4px（轻微圆角）
3. 适中 - 8px（明显圆角）
4. 较圆  - 12px（显著圆角）
5. 胶囊     - 按钮 9999px，卡片 16px

请输入数字：
```

### 问题 7：输出格式

```
设计令牌应该如何输出？

1. CSS 自定义属性（随处可用）
2. Tailwind 配置（tailwind.config.js 扩展）
3. JavaScript/TypeScript 模块
4. JSON 令牌（Design Token Community Group 格式）
5. 多种格式（以上所有）

请输入数字：
```

### 问题 8：组件指南（仅完整版）

如果选择了完整版预设：

```
是否生成组件设计指南？

指南包括：
- 按钮变体和状态
- 表单输入模式
- 卡片/容器模式
- 排版层次结构
- 图标使用指南

1. 是，生成所有指南
2. 是，但让我选择需要哪些
3. 否，仅生成令牌

请输入数字：
```

## 状态管理

创建 `.ui-design/setup_state.json`：

```json
{
  "status": "in_progress",
  "preset": "standard",
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#8B5CF6"
  },
  "color_modes": ["light", "dark"],
  "typography": {
    "family": "Inter",
    "scale": "1.25"
  },
  "spacing": "linear",
  "radius": "moderate",
  "output_formats": ["css", "tailwind"],
  "current_step": 1,
  "started_at": "ISO_TIMESTAMP"
}
```

## 令牌生成

### 1. 生成调色板

从主颜色和次要颜色，生成：

```json
{
  "colors": {
    "primary": {
      "50": "#EFF6FF",
      "100": "#DBEAFE",
      "200": "#BFDBFE",
      "300": "#93C5FD",
      "400": "#60A5FA",
      "500": "#3B82F6",
      "600": "#2563EB",
      "700": "#1D4ED8",
      "800": "#1E40AF",
      "900": "#1E3A8A",
      "950": "#172554"
    },
    "secondary": { ... },
    "neutral": {
      "50": "#F9FAFB",
      "100": "#F3F4F6",
      "200": "#E5E7EB",
      "300": "#D1D5DB",
      "400": "#9CA3AF",
      "500": "#6B7280",
      "600": "#4B5563",
      "700": "#374151",
      "800": "#1F2937",
      "900": "#111827",
      "950": "#030712"
    },
    "semantic": {
      "success": "#22C55E",
      "warning": "#F59E0B",
      "error": "#EF4444",
      "info": "#3B82F6"
    }
  }
}
```

### 2. 生成排版比例

```json
{
  "typography": {
    "fontFamily": {
      "sans": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      "mono": "ui-monospace, 'Fira Code', monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem"
    },
    "fontWeight": {
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700"
    },
    "lineHeight": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75"
    }
  }
}
```

### 3. 生成间距比例

```json
{
  "spacing": {
    "0": "0",
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "8": "2rem",
    "10": "2.5rem",
    "12": "3rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem"
  }
}
```

### 4. 生成附加令牌

```json
{
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",
    "base": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "full": "9999px"
  },
  "boxShadow": {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "base": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
  },
  "breakpoints": {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
  },
  "animation": {
    "duration": {
      "fast": "150ms",
      "normal": "300ms",
      "slow": "500ms"
    },
    "easing": {
      "ease": "cubic-bezier(0.4, 0, 0.2, 1)",
      "easeIn": "cubic-bezier(0.4, 0, 1, 1)",
      "easeOut": "cubic-bezier(0, 0, 0.2, 1)"
    }
  }
}
```

## 文件生成

### 核心设计系统文件

创建 `.ui-design/design-system.json`：

```json
{
  "name": "{project_name} Design System",
  "version": "1.0.0",
  "created": "ISO_TIMESTAMP",
  "preset": "{preset}",
  "tokens": {
    "colors": { ... },
    "typography": { ... },
    "spacing": { ... },
    "borderRadius": { ... },
    "boxShadow": { ... },
    "breakpoints": { ... },
    "animation": { ... }
  },
  "colorModes": ["light", "dark"],
  "outputFormats": ["css", "tailwind"]
}
```

### CSS 自定义属性

创建 `.ui-design/tokens/tokens.css`：

```css
/* Design System Tokens - Generated */
/* Do not edit directly. Regenerate with /ui-design:design-system-setup */

:root {
  /* Colors - Primary */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Colors - Neutral */
  --color-neutral-50: #f9fafb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-500: #6b7280;
  --color-neutral-900: #111827;

  /* Colors - Semantic */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Typography */
  --font-family-sans: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-family-mono: ui-monospace, "Fira Code", monospace;

  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-base: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-neutral-50: #111827;
    --color-neutral-100: #1f2937;
    --color-neutral-500: #9ca3af;
    --color-neutral-900: #f9fafb;
  }
}

[data-theme="dark"] {
  --color-neutral-50: #111827;
  --color-neutral-100: #1f2937;
  --color-neutral-500: #9ca3af;
  --color-neutral-900: #f9fafb;
}
```

### Tailwind 配置扩展

创建 `.ui-design/tokens/tailwind.config.js`：

```javascript
// Design System Tailwind Extension
// Import and spread in your tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#EFF6FF",
          100: "#DBEAFE",
          200: "#BFDBFE",
          300: "#93C5FD",
          400: "#60A5FA",
          500: "#3B82F6",
          600: "#2563EB",
          700: "#1D4ED8",
          800: "#1E40AF",
          900: "#1E3A8A",
          950: "#172554",
        },
        // ... other colors
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["ui-monospace", "Fira Code", "monospace"],
      },
      // ... other tokens
    },
  },
};
```

### TypeScript 模块

创建 `.ui-design/tokens/tokens.ts`：

```typescript
// Design System Tokens - Generated
// Do not edit directly.

export const colors = {
  primary: {
    50: "#EFF6FF",
    // ... full palette
  },
  // ... other color groups
} as const;

export const typography = {
  fontFamily: {
    sans: "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    mono: "ui-monospace, 'Fira Code', monospace",
  },
  fontSize: {
    xs: "0.75rem",
    // ... full scale
  },
} as const;

export const spacing = {
  1: "0.25rem",
  // ... full scale
} as const;

// Type exports for TypeScript consumers
export type ColorToken = keyof typeof colors;
export type SpacingToken = keyof typeof spacing;
```

## 文档生成（完整版预设）

创建 `.ui-design/docs/design-system.md`：

````markdown
# Design System Documentation

## Overview

This design system provides the foundation for consistent UI development.

## Colors

### Primary Palette

| Token       | Value   | Usage                  |
| ----------- | ------- | ---------------------- |
| primary-500 | #3B82F6 | Primary actions, links |
| primary-600 | #2563EB | Hover state            |
| primary-700 | #1D4ED8 | Active state           |

### Semantic Colors

| Token   | Value   | Usage                               |
| ------- | ------- | ----------------------------------- |
| success | #22C55E | Success messages, positive actions  |
| warning | #F59E0B | Warning messages, caution           |
| error   | #EF4444 | Error messages, destructive actions |

## Typography

### Scale

| Name | Size     | Usage            |
| ---- | -------- | ---------------- |
| xs   | 0.75rem  | Captions, labels |
| sm   | 0.875rem | Secondary text   |
| base | 1rem     | Body text        |
| lg   | 1.125rem | Emphasized body  |
| xl   | 1.25rem  | Subheadings      |

## Spacing

Use spacing tokens for consistent margins and padding:

- `spacing-1` (4px): Tight spacing
- `spacing-2` (8px): Compact spacing
- `spacing-4` (16px): Default spacing
- `spacing-6` (24px): Comfortable spacing
- `spacing-8` (32px): Loose spacing

## Usage

### CSS Custom Properties

```css
.button {
  background: var(--color-primary-500);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
}
```
````

### Tailwind

```html
<button class="bg-primary-500 px-4 py-2 rounded-md">Click me</button>
```

```

## 完成总结

更新状态并显示摘要：

```

设计系统初始化完成！

已创建的文件：

- .ui-design/design-system.json（主配置文件）
- .ui-design/tokens/tokens.css（CSS 自定义属性）
- .ui-design/tokens/tailwind.config.js（Tailwind 扩展）
- .ui-design/tokens/tokens.ts（TypeScript 模块）
- .ui-design/docs/design-system.md（文档）

快速开始：

1. CSS：@import '.ui-design/tokens/tokens.css';
2. Tailwind：在您的 tailwind.config.js 中引入
3. TypeScript：import { colors } from '.ui-design/tokens/tokens';

后续步骤：

1. 根据需要查看和自定义令牌
2. 运行 /ui-design:create-component 使用您的设计系统构建组件
3. 运行 /ui-design:design-review 根据令牌验证现有 UI

需要修改令牌？运行 /ui-design:design-system-setup --preset {preset}

```

## 错误处理

- 如果检测到冲突的配置：提供合并策略
- 如果文件写入失败：报告错误，建议手动创建
- 如果颜色生成失败：提供手动调色板输入选项
- 如果未检测到 Tailwind：跳过 Tailwind 输出，通知用户
```
