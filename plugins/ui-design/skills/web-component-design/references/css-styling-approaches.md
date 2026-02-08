# CSS 样式方法参考

## 对比矩阵

| 方法              | 运行时 | 打包体积      | 学习曲线 | 动态样式       | SSR   |
| ----------------- | ------ | ------------- | -------- | -------------- | ----- |
| CSS Modules       | 无     | 最小          | 低       | 有限           | 是    |
| Tailwind          | 无     | 小（已清除）  | 中       | 通过类名       | 是    |
| styled-components | 是     | 中            | 中       | 完全           | 是\*  |
| Emotion           | 是     | 中            | 中       | 完全           | 是    |
| Vanilla Extract   | 无     | 最小          | 高       | 有限           | 是    |

## CSS Modules

零运行时开销的作用域 CSS。

### 设置

```tsx
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.primary {
  background-color: #2563eb;
  color: white;
}

.primary:hover {
  background-color: #1d4ed8;
}

.secondary {
  background-color: #f3f4f6;
  color: #1f2937;
}

.secondary:hover {
  background-color: #e5e7eb;
}

.small {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.large {
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}
```

```tsx
// Button.tsx
import styles from "./Button.module.css";
import { clsx } from "clsx";

interface ButtonProps {
  variant?: "primary" | "secondary";
  size?: "small" | "medium" | "large";
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = "primary",
  size = "medium",
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={clsx(
        styles.button,
        styles[variant],
        size !== "medium" && styles[size],
      )}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### 组合

```css
/* base.module.css */
.visuallyHidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

/* Button.module.css */
.srOnly {
  composes: visuallyHidden from "./base.module.css";
}
```

## Tailwind CSS

实用优先的 CSS，具有设计系统约束。

### 类变体权威 (CVA)

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  // 基础样式
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  },
);
```

### Tailwind 合并工具

```tsx
// lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 使用示例 - 处理冲突的类名
cn("px-4 py-2", "px-6"); // => 'py-2 px-6'
cn("text-red-500", condition && "text-blue-500"); // => 条件为真时返回 'text-blue-500'
```

### 自定义插件

```js
// tailwind.config.js
const plugin = require("tailwindcss/plugin");

module.exports = {
  plugins: [
    plugin(function ({ addUtilities, addComponents, theme }) {
      // 添加工具类
      addUtilities({
        ".text-balance": {
          "text-wrap": "balance",
        },
        ".scrollbar-hide": {
          "-ms-overflow-style": "none",
          "scrollbar-width": "none",
          "&::-webkit-scrollbar": {
            display: "none",
          },
        },
      });

      // 添加组件
      addComponents({
        ".card": {
          backgroundColor: theme("colors.white"),
          borderRadius: theme("borderRadius.lg"),
          padding: theme("spacing.6"),
          boxShadow: theme("boxShadow.md"),
        },
      });
    }),
  ],
};
```

## styled-components

使用模板字符串的 CSS-in-JS。

```tsx
import styled, { css, keyframes } from "styled-components";

// 关键帧动画
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// 带变体的基础按钮
interface ButtonProps {
  $variant?: "primary" | "secondary" | "ghost";
  $size?: "sm" | "md" | "lg";
  $isLoading?: boolean;
}

const sizeStyles = {
  sm: css`
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
  `,
  md: css`
    padding: 0.5rem 1rem;
    font-size: 1rem;
  `,
  lg: css`
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
  `,
};

const variantStyles = {
  primary: css`
    background-color: ${({ theme }) => theme.colors.primary};
    color: white;
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }
  `,
  secondary: css`
    background-color: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.text};
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.secondaryHover};
    }
  `,
  ghost: css`
    background-color: transparent;
    color: ${({ theme }) => theme.colors.text};
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.ghost};
    }
  `,
};

const Button = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  animation: ${fadeIn} 0.3s ease;

  ${({ $size = "md" }) => sizeStyles[$size]}
  ${({ $variant = "primary" }) => variantStyles[$variant]}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  ${({ $isLoading }) =>
    $isLoading &&
    css`
      pointer-events: none;
      opacity: 0.7;
    `}
`;

// 扩展组件
const IconButton = styled(Button)`
  padding: 0.5rem;
  aspect-ratio: 1;
`;

// 主题提供者
const theme = {
  colors: {
    primary: "#2563eb",
    primaryHover: "#1d4ed8",
    secondary: "#f3f4f6",
    secondaryHover: "#e5e7eb",
    ghost: "rgba(0, 0, 0, 0.05)",
    text: "#1f2937",
  },
};

// 使用示例
<ThemeProvider theme={theme}>
  <Button $variant="primary" $size="lg">
    点击我
  </Button>
</ThemeProvider>;
```

## Emotion

灵活的 CSS-in-JS，支持对象和模板语法。

```tsx
/** @jsxImportSource @emotion/react */
import { css, Theme, ThemeProvider, useTheme } from "@emotion/react";
import styled from "@emotion/styled";

// 主题类型定义
declare module "@emotion/react" {
  export interface Theme {
    colors: {
      primary: string;
      background: string;
      text: string;
    };
    spacing: (factor: number) => string;
  }
}

const theme: Theme = {
  colors: {
    primary: "#2563eb",
    background: "#ffffff",
    text: "#1f2937",
  },
  spacing: (factor: number) => `${factor * 0.25}rem`,
};

// 对象语法
const cardStyles = (theme: Theme) =>
  css({
    backgroundColor: theme.colors.background,
    padding: theme.spacing(4),
    borderRadius: "0.5rem",
    boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
  });

// 模板字符串语法
const buttonStyles = css`
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;

  &:hover {
    opacity: 0.9;
  }
`;

// 带主题的样式化组件
const Card = styled.div`
  background-color: ${({ theme }) => theme.colors.background};
  padding: ${({ theme }) => theme.spacing(4)};
  border-radius: 0.5rem;
`;

// 使用 css prop 的组件
function Alert({ children }: { children: React.ReactNode }) {
  const theme = useTheme();

  return (
    <div
      css={css`
        padding: ${theme.spacing(3)};
        background-color: ${theme.colors.primary}10;
        border-left: 4px solid ${theme.colors.primary};
      `}
    >
      {children}
    </div>
  );
}

// 使用示例
<ThemeProvider theme={theme}>
  <Card>
    <Alert>重要消息</Alert>
  </Card>
</ThemeProvider>;
```

## Vanilla Extract

零运行时 CSS-in-JS，完全类型安全。

```tsx
// styles.css.ts
import { style, styleVariants, createTheme } from "@vanilla-extract/css";
import { recipe, type RecipeVariants } from "@vanilla-extract/recipes";

// 主题契约
export const [themeClass, vars] = createTheme({
  color: {
    primary: "#2563eb",
    secondary: "#64748b",
    background: "#ffffff",
    text: "#1f2937",
  },
  space: {
    small: "0.5rem",
    medium: "1rem",
    large: "1.5rem",
  },
  radius: {
    small: "0.25rem",
    medium: "0.375rem",
    large: "0.5rem",
  },
});

// 简单样式
export const container = style({
  padding: vars.space.medium,
  backgroundColor: vars.color.background,
});

// 样式变体
export const text = styleVariants({
  primary: { color: vars.color.text },
  secondary: { color: vars.color.secondary },
  accent: { color: vars.color.primary },
});

// 配方（类似 CVA）
export const button = recipe({
  base: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 500,
    borderRadius: vars.radius.medium,
    transition: "background-color 0.2s",
    cursor: "pointer",
    border: "none",
    ":disabled": {
      opacity: 0.5,
      cursor: "not-allowed",
    },
  },
  variants: {
    variant: {
      primary: {
        backgroundColor: vars.color.primary,
        color: "white",
        ":hover": {
          backgroundColor: "#1d4ed8",
        },
      },
      secondary: {
        backgroundColor: "#f3f4f6",
        color: vars.color.text,
        ":hover": {
          backgroundColor: "#e5e7eb",
        },
      },
    },
    size: {
      small: {
        padding: "0.25rem 0.75rem",
        fontSize: "0.875rem",
      },
      medium: {
        padding: "0.5rem 1rem",
        fontSize: "1rem",
      },
      large: {
        padding: "0.75rem 1.5rem",
        fontSize: "1.125rem",
      },
    },
  },
  defaultVariants: {
    variant: "primary",
    size: "medium",
  },
});

export type ButtonVariants = RecipeVariants<typeof button>;
```

```tsx
// Button.tsx
import { button, type ButtonVariants, themeClass } from "./styles.css";

interface ButtonProps extends ButtonVariants {
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant, size, children, onClick }: ButtonProps) {
  return (
    <button className={button({ variant, size })} onClick={onClick}>
      {children}
    </button>
  );
}

// App.tsx - 用主题包装
function App() {
  return (
    <div className={themeClass}>
      <Button variant="primary" size="large">
        点击我
      </Button>
    </div>
  );
}
```

## 性能考虑

### 关键 CSS 提取

```tsx
// Next.js 配合 styled-components
// pages/_document.tsx
import Document, { DocumentContext } from "next/document";
import { ServerStyleSheet } from "styled-components";

export default class MyDocument extends Document {
  static async getInitialProps(ctx: DocumentContext) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: [initialProps.styles, sheet.getStyleElement()],
      };
    } finally {
      sheet.seal();
    }
  }
}
```

### 代码分割样式

```tsx
// 动态导入重型样式化组件
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton height={400} />,
  ssr: false,
});
```
