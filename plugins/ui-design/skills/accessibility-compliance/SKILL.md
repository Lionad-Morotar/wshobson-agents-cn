---
name: accessibility-compliance
description: 实现符合 WCAG 2.2 标准的界面,包括移动端无障碍访问、包容性设计模式和辅助技术支持。在进行无障碍审计、实现 ARIA 模式、构建屏幕阅读器支持或确保包容性用户体验时使用。
---

# 无障碍合规

掌握无障碍实现,为所有人创造包容性体验,包括残障用户。

## 何时使用此技能

- 实现 WCAG 2.2 AA 级或 AAA 级合规
- 构建屏幕阅读器可访问的界面
- 为交互式组件添加键盘导航
- 实现焦点管理和焦点陷阱
- 创建具有适当标签的可访问表单
- 支持减少动画和高对比度偏好
- 构建移动端无障碍功能(iOS VoiceOver、Android TalkBack)
- 进行无障碍审计并修复违规问题

## 核心能力

### 1. WCAG 2.2 指南

- 可感知:内容必须能以不同的方式呈现
- 可操作:界面必须能通过键盘和辅助技术导航
- 可理解:内容和操作必须清晰
- 健壮性:内容必须能与当前和未来的辅助技术一起工作

### 2. ARIA 模式

- 角色:定义元素目的(按钮、对话框、导航)
- 状态:指示当前条件(展开、选中、禁用)
- 属性:描述关系和额外信息(labelledby、describedby)
- 实时区域:宣布动态内容变化

### 3. 键盘导航

- 焦点顺序和 Tab 序列
- 焦点指示器和可见焦点状态
- 键盘快捷键和热键
- 模态框和对话框的焦点陷阱

### 4. 屏幕阅读器支持

- 语义化 HTML 结构
- 图片的替代文本
- 正确的标题层次结构
- 跳过链接和地标

### 5. 移动端无障碍

- 触摸目标尺寸(最小 44x44dp)
- VoiceOver 和 TalkBack 兼容性
- 手势替代方案
- 动态类型支持

## 快速参考

### WCAG 2.2 成功标准检查清单

| 级别 | 标准    | 描述                                        |
| ---- | ------- | ------------------------------------------- |
| A    | 1.1.1   | 非文本内容具有文本替代                      |
| A    | 1.3.1   | 信息和关系可通过程序确定                    |
| A    | 2.1.1   | 所有功能都可通过键盘访问                    |
| A    | 2.4.1   | 跳转到主内容的机制                          |
| AA   | 1.4.3   | 对比度 4.5:1(文本)、3:1(大文本)            |
| AA   | 1.4.11  | 非文本对比度 3:1                            |
| AA   | 2.4.7   | 焦点可见                                    |
| AA   | 2.5.8   | 目标尺寸最小 24x24px(2.2 新增)             |
| AAA  | 1.4.6   | 增强对比度 7:1                              |
| AAA  | 2.5.5   | 目标尺寸最小 44x44px                         |

## 关键模式

### 模式 1: 可访问按钮

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
  isLoading?: boolean;
}

function AccessibleButton({
  children,
  variant = "primary",
  isLoading = false,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      // 加载时禁用
      disabled={disabled || isLoading}
      // 向屏幕阅读器宣布加载状态
      aria-busy={isLoading}
      // 描述按钮当前状态
      aria-disabled={disabled || isLoading}
      className={cn(
        // 可见焦点环
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
        // 最小触摸目标尺寸(44x44px)
        "min-h-[44px] min-w-[44px]",
        variant === "primary" && "bg-primary text-primary-foreground",
        (disabled || isLoading) && "opacity-50 cursor-not-allowed",
      )}
      {...props}
    >
      {isLoading ? (
        <>
          <span className="sr-only">加载中</span>
          <Spinner aria-hidden="true" />
        </>
      ) : (
        children
      )}
    </button>
  );
}
```

### 模式 2: 可访问模态对话框

```tsx
import * as React from "react";
import { FocusTrap } from "@headlessui/react";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

function AccessibleDialog({ isOpen, onClose, title, children }: DialogProps) {
  const titleId = React.useId();
  const descriptionId = React.useId();

  // 按 Escape 键关闭
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // 打开时防止 body 滚动
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
    >
      {/* 背景遮罩 */}
      <div
        className="fixed inset-0 bg-black/50"
        aria-hidden="true"
        onClick={onClose}
      />

      {/* 焦点陷阱容器 */}
      <FocusTrap>
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <div className="bg-background rounded-lg shadow-lg max-w-md w-full p-6">
            <h2 id={titleId} className="text-lg font-semibold">
              {title}
            </h2>
            <div id={descriptionId}>{children}</div>
            <button
              onClick={onClose}
              className="absolute top-4 right-4"
              aria-label="关闭对话框"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      </FocusTrap>
    </div>
  );
}
```

### 模式 3: 可访问表单

```tsx
function AccessibleForm() {
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  return (
    <form aria-describedby="form-errors" noValidate>
      {/* 屏幕阅读器的错误摘要 */}
      {Object.keys(errors).length > 0 && (
        <div
          id="form-errors"
          role="alert"
          aria-live="assertive"
          className="bg-destructive/10 border border-destructive p-4 rounded-md mb-4"
        >
          <h2 className="font-semibold text-destructive">
            请修复以下错误:
          </h2>
          <ul className="list-disc list-inside mt-2">
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`} className="underline">
                  {message}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 带错误的必填字段 */}
      <div className="space-y-2">
        <label htmlFor="email" className="block font-medium">
          电子邮件地址
          <span aria-hidden="true" className="text-destructive ml-1">
            *
          </span>
          <span className="sr-only">(必填)</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : "email-hint"}
          className={cn(
            "w-full px-3 py-2 border rounded-md",
            errors.email && "border-destructive",
          )}
        />
        {errors.email ? (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email}
          </p>
        ) : (
          <p id="email-hint" className="text-sm text-muted-foreground">
            我们绝不会分享您的电子邮件。
          </p>
        )}
      </div>

      <button type="submit" className="mt-4">
        提交
      </button>
    </form>
  );
}
```

### 模式 4: 跳过导航链接

```tsx
function SkipLink() {
  return (
    <a
      href="#main-content"
      className={cn(
        // 默认隐藏,聚焦时可见
        "sr-only focus:not-sr-only",
        "focus:absolute focus:top-4 focus:left-4 focus:z-50",
        "focus:bg-background focus:px-4 focus:py-2 focus:rounded-md",
        "focus:ring-2 focus:ring-primary",
      )}
    >
      跳转到主内容
    </a>
  );
}

// 在布局中
function Layout({ children }) {
  return (
    <>
      <SkipLink />
      <header>...</header>
      <nav aria-label="主导航">...</nav>
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
      <footer>...</footer>
    </>
  );
}
```

### 模式 5: 用于公告的实时区域

```tsx
function useAnnounce() {
  const [message, setMessage] = React.useState("");

  const announce = React.useCallback(
    (text: string, priority: "polite" | "assertive" = "polite") => {
      setMessage(""); // 先清除以确保重新公告
      setTimeout(() => setMessage(text), 100);
    },
    [],
  );

  const Announcer = () => (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );

  return { announce, Announcer };
}

// 使用示例
function SearchResults({ results, isLoading }) {
  const { announce, Announcer } = useAnnounce();

  React.useEffect(() => {
    if (!isLoading && results) {
      announce(`找到 ${results.length} 个结果`);
    }
  }, [results, isLoading, announce]);

  return (
    <>
      <Announcer />
      <ul>{/* 结果 */}</ul>
    </>
  );
}
```

## 颜色对比度要求

```typescript
// 对比度工具函数
function getContrastRatio(foreground: string, background: string): number {
  const fgLuminance = getLuminance(foreground);
  const bgLuminance = getLuminance(background);
  const lighter = Math.max(fgLuminance, bgLuminance);
  const darker = Math.min(fgLuminance, bgLuminance);
  return (lighter + 0.05) / (darker + 0.05);
}

// WCAG 要求
const CONTRAST_REQUIREMENTS = {
  // 普通文本(<18pt 或 <14pt 粗体)
  normalText: {
    AA: 4.5,
    AAA: 7,
  },
  // 大文本(>=18pt 或 >=14pt 粗体)
  largeText: {
    AA: 3,
    AAA: 4.5,
  },
  // UI 组件和图形
  uiComponents: {
    AA: 3,
  },
};
```

## 最佳实践

1. **使用语义化 HTML**: 尽可能优先使用原生元素而非 ARIA
2. **与真实用户测试**: 在用户测试中包括残障人士
3. **键盘优先**: 设计无需鼠标即可工作的交互
4. **不要禁用焦点样式**: 样式化它们,不要移除
5. **提供文本替代**: 所有非文本内容都需要描述
6. **支持缩放**: 内容应在 200% 缩放下工作
7. **宣布变化**: 对动态内容使用实时区域
8. **尊重偏好**: 遵守 prefers-reduced-motion 和 prefers-contrast

## 常见问题

- **缺少 alt 文本**: 没有描述的图片
- **颜色对比度差**: 文本难以在背景上阅读
- **键盘陷阱**: 焦点困在组件中
- **缺少标签**: 没有关联标签的表单输入
- **自动播放媒体**: 未经用户启动就播放的内容
- **不可访问的自定义控件**: 重新实现原生功能效果不佳
- **缺少跳过链接**: 无法绕过重复内容
- **焦点顺序问题**: Tab 顺序与视觉顺序不匹配

## 测试工具

- **自动化**: axe DevTools、WAVE、Lighthouse
- **手动测试**: VoiceOver(macOS/iOS)、NVDA/JAWS(Windows)、TalkBack(Android)
- **模拟器**: NoCoffee(视力)、Silktide(各种残疾)

## 资源

- [WCAG 2.2 指南](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA 创作实践](https://www.w3.org/WAI/ARIA/apg/)
- [A11y Project 检查清单](https://www.a11yproject.com/checklist/)
- [包容性组件](https://inclusive-components.design/)
- [Deque University](https://dequeuniversity.com/)
