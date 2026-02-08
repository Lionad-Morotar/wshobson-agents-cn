# 字体系统参考

## 字体比例构建

### 模块化比例

模块化比例使用数学比例创建字体尺寸之间的和谐关系。

```tsx
// 常用比例
const RATIOS = {
  minorSecond: 1.067, // 16:15
  majorSecond: 1.125, // 9:8
  minorThird: 1.2, // 6:5
  majorThird: 1.25, // 5:4
  perfectFourth: 1.333, // 4:3
  augmentedFourth: 1.414, // √2
  perfectFifth: 1.5, // 3:2
  goldenRatio: 1.618, // φ
};

function generateScale(
  baseSize: number,
  ratio: number,
  steps: number,
): number[] {
  const scale: number[] = [];
  for (let i = -2; i <= steps; i++) {
    scale.push(Math.round(baseSize * Math.pow(ratio, i) * 100) / 100);
  }
  return scale;
}

// 使用 16px 基准和完美四度比例生成比例
const typeScale = generateScale(16, RATIOS.perfectFourth, 6);
// 结果: [9, 12, 16, 21.33, 28.43, 37.9, 50.52, 67.34, 89.76]
```

### CSS 自定义属性

```css
:root {
  /* 使用完美四度 (1.333) 的基础比例 */
  --font-size-2xs: 0.563rem; /* ~9px */
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-md: 1.125rem; /* 18px */
  --font-size-lg: 1.333rem; /* ~21px */
  --font-size-xl: 1.5rem; /* 24px */
  --font-size-2xl: 1.777rem; /* ~28px */
  --font-size-3xl: 2.369rem; /* ~38px */
  --font-size-4xl: 3.157rem; /* ~50px */
  --font-size-5xl: 4.209rem; /* ~67px */

  /* 字重 */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* 行高 */
  --line-height-tight: 1.1;
  --line-height-snug: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* 字间距 */
  --letter-spacing-tighter: -0.05em;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
  --letter-spacing-widest: 0.1em;
}
```

## 字体加载策略

### FOUT 防止

```css
/* 使用 font-display 控制加载行为 */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter-Variable.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap; /* 立即显示回退字体，加载后切换 */
}

/* 可选：size-adjust 用于更好的回退匹配 */
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%; /* 调整以匹配 Inter 指标 */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: "Inter", "Inter Fallback", system-ui, sans-serif;
}
```

### 预加载关键字体

```html
<head>
  <!-- 预加载关键字体 -->
  <link
    rel="preload"
    href="/fonts/Inter-Variable.woff2"
    as="font"
    type="font/woff2"
    crossorigin
  />
</head>
```

### 可变字体

```css
/* 带字重和宽度轴的可变字体 */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter-Variable.woff2") format("woff2");
  font-weight: 100 900;
  font-stretch: 75% 125%;
}

/* 使用 font-variation-settings 进行精细控制 */
.custom-weight {
  font-variation-settings:
    "wght" 450,
    "wdth" 95;
}

/* 或使用标准属性 */
.semi-expanded {
  font-weight: 550;
  font-stretch: 110%;
}
```

## 响应式字体

### 流体字体比例

```css
/* 使用 clamp() 实现响应式尺寸 */
h1 {
  /* 最小: 32px，首选: 5vw + 16px，最大: 64px */
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  line-height: 1.1;
}

h2 {
  font-size: clamp(1.5rem, 3vw + 0.5rem, 2.5rem);
  line-height: 1.2;
}

p {
  font-size: clamp(1rem, 1vw + 0.75rem, 1.25rem);
  line-height: 1.6;
}

/* 流体行高 */
.fluid-text {
  --min-line-height: 1.3;
  --max-line-height: 1.6;
  --min-vw: 320;
  --max-vw: 1200;

  line-height: calc(
    var(--min-line-height) + (var(--max-line-height) - var(--min-line-height)) *
      ((100vw - var(--min-vw) * 1px) / (var(--max-vw) - var(--min-vw)))
  );
}
```

### 基于视口的缩放

```tsx
// 响应式字体的 Tailwind 配置
module.exports = {
  theme: {
    fontSize: {
      xs: ["0.75rem", { lineHeight: "1rem" }],
      sm: ["0.875rem", { lineHeight: "1.25rem" }],
      base: ["1rem", { lineHeight: "1.5rem" }],
      lg: ["1.125rem", { lineHeight: "1.75rem" }],
      xl: ["1.25rem", { lineHeight: "1.75rem" }],
      "2xl": ["1.5rem", { lineHeight: "2rem" }],
      "3xl": ["1.875rem", { lineHeight: "2.25rem" }],
      "4xl": ["2.25rem", { lineHeight: "2.5rem" }],
      "5xl": ["3rem", { lineHeight: "1" }],
    },
  },
};

// 带响应式类的组件
function Heading({ children }) {
  return (
    <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
      {children}
    </h1>
  );
}
```

## 可读性指南

### 最佳行长

```css
/* 最佳阅读宽度: 45-75 字符 */
.prose {
  max-width: 65ch; /* ~65 字符 */
}

/* 提示框使用较窄宽度 */
.callout {
  max-width: 50ch;
}

/* 代码块使用较宽宽度 */
pre {
  max-width: 80ch;
}
```

### 垂直韵律

```css
/* 建立基线网格 */
:root {
  --baseline: 1.5rem; /* 16px 基准时的 24px */
}

/* 所有边距应为基线的倍数 */
h1 {
  font-size: 2.5rem;
  line-height: calc(var(--baseline) * 2);
  margin-top: calc(var(--baseline) * 2);
  margin-bottom: var(--baseline);
}

h2 {
  font-size: 2rem;
  line-height: calc(var(--baseline) * 1.5);
  margin-top: calc(var(--baseline) * 1.5);
  margin-bottom: calc(var(--baseline) * 0.5);
}

p {
  font-size: 1rem;
  line-height: var(--baseline);
  margin-bottom: var(--baseline);
}
```

### 文本换行

```css
/* 防止孤行和寡行 */
p {
  text-wrap: pretty; /* 实验性：改善换行 */
  widows: 3;
  orphans: 3;
}

/* 平衡标题 */
h1,
h2,
h3 {
  text-wrap: balance;
}

/* 防止特定元素中断 */
.no-wrap {
  white-space: nowrap;
}

/* 两端对齐文本的连字符 */
.justified {
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
}
```

## 字体搭配指南

### 对比搭配

```css
/* 衬线标题 + 无衬线正文 */
:root {
  --font-heading: "Playfair Display", Georgia, serif;
  --font-body: "Source Sans Pro", -apple-system, sans-serif;
}

/* 几何标题 + 人文主义正文 */
:root {
  --font-heading: "Space Grotesk", sans-serif;
  --font-body: "IBM Plex Sans", sans-serif;
}

/* 现代无衬线标题 + 经典衬线正文 */
:root {
  --font-heading: "Inter", system-ui, sans-serif;
  --font-body: "Georgia", Times, serif;
}
```

### 超家族方法

```css
 /* 所有用途使用单一可变字体系列 */
:root {
  --font-family: "Inter", system-ui, sans-serif;
}

h1 {
  font-family: var(--font-family);
  font-weight: 800;
  letter-spacing: -0.02em;
}

p {
  font-family: var(--font-family);
  font-weight: 400;
  letter-spacing: 0;
}

.caption {
  font-family: var(--font-family);
  font-weight: 500;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

## 语义化字体类

```css
/* 按用途而非外观定义文本样式 */
.text-display {
  font-size: var(--font-size-5xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
}

.text-headline {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
}

.text-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
}

.text-body {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
}

.text-body-sm {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
}

.text-caption {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.text-overline {
  font-size: var(--font-size-2xs);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
}
```

## OpenType 功能

```css
/* 启用高级字体功能 */
.fancy-text {
  /* 小型大写字母 */
  font-variant-caps: small-caps;

  /* 连字 */
  font-variant-ligatures: common-ligatures;

  /* 数字功能 */
  font-variant-numeric: tabular-nums lining-nums;

  /* 分数 */
  font-feature-settings: "frac" 1;
}

/* 对齐列的表格数字 */
.data-table td {
  font-variant-numeric: tabular-nums;
}

/* 正文的旧式数字 */
.prose {
  font-variant-numeric: oldstyle-nums;
}

/* 标题的离散连字 */
.fancy-heading {
  font-variant-ligatures: discretionary-ligatures;
}
```
