---
description: "使用正确模式引导创建组件"
argument-hint: "[组件名称]"
---

# 创建组件

遵循既定模式和最佳实践创建新 UI 组件的引导式工作流程。

## 前置检查

1. 检查 `.ui-design/` 目录是否存在:
   - 如果不存在: 创建 `.ui-design/` 目录
   - 创建 `.ui-design/components/` 子目录用于组件追踪

2. 检测项目配置:
   - 扫描框架 (React、Vue、Svelte、Angular)
   - 扫描样式方案 (CSS Modules、Tailwind、styled-components 等)
   - 检查 `src/components/` 或类似目录中的现有组件模式
   - 如果存在,加载 `.ui-design/design-system.json`

3. 加载项目上下文:
   - 检查 `conductor/tech-stack.md`
   - 检查现有组件约定

4. 如果未检测到框架:

   ```
   我无法检测到 UI 框架。您使用的是什么?

   1. React
   2. Vue 3
   3. Svelte
   4. Angular
   5. Vanilla JavaScript/HTML
   6. 其他 (请说明)

   请输入数字:
   ```

## 组件规格说明

**关键规则:**

- 每次只问一个问题
- 等待用户响应后再继续
- 在生成代码前构建完整的规格说明

### Q1: 组件名称 (如果未提供)

```
这个组件应该叫什么?

指导原则:
- 使用 PascalCase (例如: UserCard、DataTable)
- 描述性强但简洁
- 避免使用通用名称,如 "Component" 或 "Widget"

请输入组件名称:
```

### Q2: 组件用途

```
这个组件的主要用途是什么?

1. 展示内容 (卡片、列表、文本块)
2. 收集输入 (表单、选择器、开关)
3. 导航 (菜单、标签页、面包屑)
4. 反馈 (警告、提示、模态框)
5. 布局 (容器、网格、区块)
6. 数据可视化 (图表、图形、指示器)
7. 其他 (请描述)

请输入数字或描述:
```

### Q3: 组件复杂度

```
组件的复杂度级别是什么?

1. 简单 - 单一职责、最少 props、无内部状态
2. 复合 - 多个部分、一些内部状态、少量 props
3. 复杂 - 多个子组件、状态管理、许多 props
4. 组合 - 编排其他组件、重要逻辑

请输入数字:
```

### Q4: Props/输入规格

```
这个组件应该接受哪些 props/输入?

对于每个 prop,提供:
- 名称 (camelCase)
- 类型 (string、number、boolean、function、object、array)
- 必需或可选
- 默认值 (如果可选)

示例格式:
title: string, required
variant: "primary" | "secondary", optional, default: "primary"
onClick: function, optional

请输入 props (每行一个,完成后输入空行):
```

### Q5: 状态需求

```
这个组件需要内部状态吗?

1. 无状态 - 纯展示,所有数据通过 props 传入
2. 本地状态 - 简单的内部状态 (打开/关闭、悬停等)
3. 受控 - 状态由父组件管理,组件报告变更
4. 非受控 - 管理自己的状态,暴露 refs 供父组件访问
5. 混合 - 同时支持受控和非受控模式

请输入数字:
```

### Q6: 组合模式 (如果复杂度 > 简单)

```
应该如何处理子内容?

1. 无子组件 - 自包含的组件
2. 简单子组件 - 接受 children prop 用于内容
3. 命名插槽 - 多个内容区域 (页眉、主体、页脚)
4. 复合组件 - 导出子组件 (例如: Card.Header、Card.Body)
5. 渲染 props - 接受渲染函数以提供灵活性

请输入数字:
```

### Q7: 可访问性需求

```
需要哪些可访问性功能?

1. 基础 - 语义化 HTML,必要时添加 aria-labels
2. 键盘导航 - 完整的键盘支持、焦点管理
3. 屏幕阅读器优化 - 实时区域、公告
4. 完整 WCAG AA - 所有适用的成功标准

请输入数字:
```

### Q8: 样式方案

```
应该如何为这个组件设置样式?

检测到的方案: {detected_approach}

1. 使用检测到的方案 ({detected_approach})
2. CSS Modules
3. Tailwind CSS
4. Styled Components / Emotion
5. 普通 CSS/SCSS
6. 其他 (请说明)

请输入数字:
```

## 状态管理

创建 `.ui-design/components/{component_name}.json`:

```json
{
  "name": "{ComponentName}",
  "created_at": "ISO_TIMESTAMP",
  "purpose": "{purpose}",
  "complexity": "{level}",
  "props": [
    {
      "name": "{prop_name}",
      "type": "{type}",
      "required": true,
      "default": null,
      "description": "{description}"
    }
  ],
  "state_pattern": "{pattern}",
  "composition": "{pattern}",
  "accessibility_level": "{level}",
  "styling": "{approach}",
  "files_created": [],
  "status": "in_progress"
}
```

## 组件生成

### 1. 创建目录结构

基于检测到的模式或询问用户:

```
应该在哪里创建这个组件?

检测到的组件目录:
1. src/components/{ComponentName}/
2. app/components/{ComponentName}/
3. components/{ComponentName}/
4. 其他 (请指定路径)

请输入数字或路径:
```

创建结构:

```
{component_path}/
├── index.ts                 # Barrel export
├── {ComponentName}.tsx      # 主组件
├── {ComponentName}.test.tsx # 测试 (如果检测到测试)
├── {ComponentName}.styles.{ext}  # 样式 (基于方案)
└── types.ts                 # TypeScript 类型 (如果是 TS 项目)
```

### 2. 生成组件代码

基于收集的规格说明生成组件。

**React/TypeScript 示例:**

```tsx
// {ComponentName}.tsx
import { forwardRef } from 'react';
import type { {ComponentName}Props } from './types';
import styles from './{ComponentName}.styles.module.css';

/**
 * {ComponentName}
 *
 * {Purpose description}
 */
export const {ComponentName} = forwardRef<HTML{Element}Element, {ComponentName}Props>(
  ({ prop1, prop2 = 'default', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={styles.root}
        {...props}
      >
        {children}
      </div>
    );
  }
);

{ComponentName}.displayName = '{ComponentName}';
```

### 3. 生成类型

```tsx
// types.ts
import type { HTMLAttributes, ReactNode } from 'react';

export interface {ComponentName}Props extends HTMLAttributes<HTMLDivElement> {
  /** {prop1 description} */
  prop1: string;

  /** {prop2 description} */
  prop2?: 'primary' | 'secondary';

  /** 组件子元素 */
  children?: ReactNode;
}
```

### 4. 生成样式

基于样式方案:

**CSS Modules:**

```css
/* {ComponentName}.styles.module.css */
.root {
  /* 基础样式 */
}

.variant-primary {
  /* Primary 变体 */
}

.variant-secondary {
  /* Secondary 变体 */
}
```

**Tailwind:**

```tsx
// 在组件中内联
className={cn(
  'base-classes',
  variant === 'primary' && 'primary-classes',
  className
)}
```

### 5. 生成测试 (如果检测到测试框架)

```tsx
// {ComponentName}.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { {ComponentName} } from './{ComponentName}';

describe('{ComponentName}', () => {
  it('renders without crashing', () => {
    render(<{ComponentName} prop1="test" />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  it('applies variant styles correctly', () => {
    // 变体测试
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    // 交互测试
  });

  it('meets accessibility requirements', () => {
    // 可访问性测试
  });
});
```

### 6. 生成 Barrel Export

```tsx
// index.ts
export { {ComponentName} } from './{ComponentName}';
export type { {ComponentName}Props } from './types';
```

## 用户审查

生成文件后:

```
我已经创建了 {ComponentName} 组件:

创建的文件:
- {path}/index.ts
- {path}/{ComponentName}.tsx
- {path}/{ComponentName}.test.tsx
- {path}/{ComponentName}.styles.module.css
- {path}/types.ts

您想要:
1. 审查生成的代码
2. 进行修改
3. 添加更多 props 或功能
4. 生成 Storybook stories
5. 完成,保持原样

请输入数字:
```

### 如果请求修改:

```
您想要修改什么?

1. 添加新的 prop
2. 更改样式方案
3. 添加变体
4. 修改组件结构
5. 添加可访问性功能
6. 其他 (请描述)

请输入数字:
```

## Storybook 集成 (可选)

如果检测到 Storybook 或用户请求:

```tsx
// {ComponentName}.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { {ComponentName} } from './{ComponentName}';

const meta: Meta<typeof {ComponentName}> = {
  title: 'Components/{ComponentName}',
  component: {ComponentName},
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof {ComponentName}>;

export const Default: Story = {
  args: {
    prop1: 'Example',
  },
};

export const Primary: Story = {
  args: {
    ...Default.args,
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    ...Default.args,
    variant: 'secondary',
  },
};
```

## 完成

更新 `.ui-design/components/{component_name}.json`:

```json
{
  "status": "complete",
  "files_created": [
    "{path}/index.ts",
    "{path}/{ComponentName}.tsx",
    "{path}/{ComponentName}.test.tsx",
    "{path}/{ComponentName}.styles.module.css",
    "{path}/types.ts"
  ],
  "completed_at": "ISO_TIMESTAMP"
}
```

显示摘要:

```
组件创建成功!

组件: {ComponentName}
位置: {path}/
文件: 创建了 {count} 个文件

快速参考:
  导入: import { {ComponentName} } from '{import_path}';
  使用:  <{ComponentName} prop1="value" />

下一步:
1. 运行 /ui-design:design-review {path} 进行验证
2. 运行 /ui-design:accessibility-audit {path} 进行可访问性检查
3. 添加到您的页面/布局

需要创建另一个组件? 运行 /ui-design:create-component
```

## 错误处理

- 如果组件名称冲突: 建议替代方案,提供覆盖选项
- 如果目录创建失败: 报告错误,建议手动创建
- 如果不支持框架: 提供通用模板,说明限制
- 如果文件写入失败: 保存到临时位置,提供恢复说明
