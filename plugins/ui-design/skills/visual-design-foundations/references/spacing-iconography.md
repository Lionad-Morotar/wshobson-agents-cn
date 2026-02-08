# 间距和图标参考

## 间距系统

### 8点网格系统

8点网格是一致间距的行业标准。

```css
:root {
  /* 基础间距单位 */
  --space-unit: 0.25rem; /* 4px */

  /* 间距比例 */
  --space-0: 0;
  --space-px: 1px;
  --space-0-5: calc(var(--space-unit) * 0.5); /* 2px */
  --space-1: var(--space-unit); /* 4px */
  --space-1-5: calc(var(--space-unit) * 1.5); /* 6px */
  --space-2: calc(var(--space-unit) * 2); /* 8px */
  --space-2-5: calc(var(--space-unit) * 2.5); /* 10px */
  --space-3: calc(var(--space-unit) * 3); /* 12px */
  --space-3-5: calc(var(--space-unit) * 3.5); /* 14px */
  --space-4: calc(var(--space-unit) * 4); /* 16px */
  --space-5: calc(var(--space-unit) * 5); /* 20px */
  --space-6: calc(var(--space-unit) * 6); /* 24px */
  --space-7: calc(var(--space-unit) * 7); /* 28px */
  --space-8: calc(var(--space-unit) * 8); /* 32px */
  --space-9: calc(var(--space-unit) * 9); /* 36px */
  --space-10: calc(var(--space-unit) * 10); /* 40px */
  --space-11: calc(var(--space-unit) * 11); /* 44px */
  --space-12: calc(var(--space-unit) * 12); /* 48px */
  --space-14: calc(var(--space-unit) * 14); /* 56px */
  --space-16: calc(var(--space-unit) * 16); /* 64px */
  --space-20: calc(var(--space-unit) * 20); /* 80px */
  --space-24: calc(var(--space-unit) * 24); /* 96px */
  --space-28: calc(var(--space-unit) * 28); /* 112px */
  --space-32: calc(var(--space-unit) * 32); /* 128px */
}
```

### 语义化间距令牌

```css
:root {
  /* 组件级间距 */
  --spacing-xs: var(--space-1); /* 4px - 紧凑间距 */
  --spacing-sm: var(--space-2); /* 8px - 小间距 */
  --spacing-md: var(--space-4); /* 16px - 默认间距 */
  --spacing-lg: var(--space-6); /* 24px - 舒适间距 */
  --spacing-xl: var(--space-8); /* 32px - 宽松间距 */
  --spacing-2xl: var(--space-12); /* 48px - 大间距 */
  --spacing-3xl: var(--space-16); /* 64px - 区块间距 */

  /* 特定用例 */
  --spacing-inline: var(--space-2); /* 内联元素之间 */
  --spacing-stack: var(--space-4); /* 堆叠元素之间 */
  --spacing-inset: var(--space-4); /* 容器内边距 */
  --spacing-section: var(--space-16); /* 主要区块之间 */
  --spacing-page: var(--space-24); /* 页面边距 */
}
```

### 间距工具函数

```tsx
// 类似 Tailwind 的间距比例生成器
function createSpacingScale(baseUnit: number = 4): Record<string, string> {
  const scale: Record<string, string> = {
    "0": "0",
    px: "1px",
  };

  const multipliers = [
    0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24,
    28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96,
  ];

  for (const m of multipliers) {
    const key = m % 1 === 0 ? String(m) : String(m).replace(".", "-");
    scale[key] = `${baseUnit * m}px`;
  }

  return scale;
}
```

## 布局间距模式

### 容器查询间距

```css
/* 基于容器大小的响应式间距 */
.card {
  container-type: inline-size;
  padding: var(--space-4);
}

@container (min-width: 400px) {
  .card {
    padding: var(--space-6);
  }
}

@container (min-width: 600px) {
  .card {
    padding: var(--space-8);
  }
}
```

### 负空间模式

```css
/* 用于视觉层次的非对称间距 */
.hero-section {
  padding-top: var(--space-24);
  padding-bottom: var(--space-16);
}

/* 内容呼吸空间 */
.prose > * + * {
  margin-top: var(--space-4);
}

.prose > h2 + * {
  margin-top: var(--space-2);
}

.prose > * + h2 {
  margin-top: var(--space-8);
}
```

## 图标系统

### 图标尺寸比例

```css
:root {
  /* 与间距网格对齐的图标尺寸 */
  --icon-xs: 12px; /* 内联装饰 */
  --icon-sm: 16px; /* 小 UI 元素 */
  --icon-md: 20px; /* 默认尺寸 */
  --icon-lg: 24px; /* 强调 */
  --icon-xl: 32px; /* 大型显示 */
  --icon-2xl: 48px; /* 英雄图标 */

  /* 触摸目标尺寸 */
  --touch-target-min: 44px; /* WCAG 最小值 */
  --touch-target-comfortable: 48px;
}
```

### SVG 图标组件

```tsx
import { forwardRef, type SVGProps } from "react";

interface IconProps extends SVGProps<SVGSVGElement> {
  name: string;
  size?: "xs" | "sm" | "md" | "lg" | "xl" | "2xl";
  label?: string;
}

const sizeMap = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
  "2xl": 48,
};

export const Icon = forwardRef<SVGSVGElement, IconProps>(
  ({ name, size = "md", label, className, ...props }, ref) => {
    const pixelSize = sizeMap[size];

    return (
      <svg
        ref={ref}
        width={pixelSize}
        height={pixelSize}
        className={`inline-block flex-shrink-0 ${className}`}
        aria-hidden={!label}
        aria-label={label}
        role={label ? "img" : undefined}
        {...props}
      >
        <use href={`/icons.svg#${name}`} />
      </svg>
    );
  },
);

Icon.displayName = "Icon";
```

### 图标按钮模式

```tsx
interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: string;
  label: string;
  size?: "sm" | "md" | "lg";
  variant?: "solid" | "ghost" | "outline";
}

const sizeClasses = {
  sm: "p-1.5" /* 32px 总计，16px 图标 */,
  md: "p-2" /* 40px 总计，20px 图标 */,
  lg: "p-2.5" /* 48px 总计，24px 图标 */,
};

const iconSizes = {
  sm: "sm" as const,
  md: "md" as const,
  lg: "lg" as const,
};

export function IconButton({
  icon,
  label,
  size = "md",
  variant = "ghost",
  className,
  ...props
}: IconButtonProps) {
  return (
    <button
      className={`
        inline-flex items-center justify-center rounded-lg
        transition-colors focus-visible:outline-none focus-visible:ring-2
        ${sizeClasses[size]}
        ${variant === "solid" && "bg-blue-600 text-white hover:bg-blue-700"}
        ${variant === "ghost" && "hover:bg-gray-100"}
        ${variant === "outline" && "border border-gray-300 hover:bg-gray-50"}
        ${className}
      `}
      aria-label={label}
      {...props}
    >
      <Icon name={icon} size={iconSizes[size]} />
    </button>
  );
}
```

### 图标精灵生成

```tsx
// SVG 精灵构建脚本
import { readdir, readFile, writeFile } from "fs/promises";
import { optimize } from "svgo";

async function buildIconSprite(iconDir: string, outputPath: string) {
  const files = await readdir(iconDir);
  const svgFiles = files.filter((f) => f.endsWith(".svg"));

  const symbols = await Promise.all(
    svgFiles.map(async (file) => {
      const content = await readFile(`${iconDir}/${file}`, "utf-8");
      const name = file.replace(".svg", "");

      // 优化 SVG
      const result = optimize(content, {
        plugins: [
          "removeDoctype",
          "removeXMLProcInst",
          "removeComments",
          "removeMetadata",
          "removeTitle",
          "removeDesc",
          "removeUselessDefs",
          "removeEditorsNSData",
          "removeEmptyAttrs",
          "removeHiddenElems",
          "removeEmptyText",
          "removeEmptyContainers",
          "convertStyleToAttrs",
          "convertColors",
          "convertPathData",
          "convertTransform",
          "removeUnknownsAndDefaults",
          "removeNonInheritableGroupAttrs",
          "removeUselessStrokeAndFill",
          "removeUnusedNS",
          "cleanupNumericValues",
          "cleanupListOfValues",
          "moveElemsAttrsToGroup",
          "moveGroupAttrsToElems",
          "collapseGroups",
          "mergePaths",
        ],
      });

      // 提取 viewBox 和内容
      const viewBoxMatch = result.data.match(/viewBox="([^"]+)"/);
      const viewBox = viewBoxMatch ? viewBoxMatch[1] : "0 0 24 24";
      const innerContent = result.data
        .replace(/<svg[^>]*>/, "")
        .replace(/<\/svg>/, "");

      return `<symbol id="${name}" viewBox="${viewBox}">${innerContent}</symbol>`;
    }),
  );

  const sprite = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">${symbols.join("")}</svg>`;

  await writeFile(outputPath, sprite);
  console.log(`Generated sprite with ${symbols.length} icons`);
}
```

### 图标库集成

```tsx
// Lucide React
import { Home, Settings, User, Search } from "lucide-react";

function Navigation() {
  return (
    <nav className="flex gap-4">
      <NavItem icon={Home} label="Home" />
      <NavItem icon={Search} label="Search" />
      <NavItem icon={Settings} label="Settings" />
      <NavItem icon={User} label="Profile" />
    </nav>
  );
}

// Heroicons
import { HomeIcon, Cog6ToothIcon } from "@heroicons/react/24/outline";
import { HomeIcon as HomeIconSolid } from "@heroicons/react/24/solid";

function ToggleIcon({ active }: { active: boolean }) {
  const Icon = active ? HomeIconSolid : HomeIcon;
  return <Icon className="w-6 h-6" />;
}

// Radix Icons
import { HomeIcon, GearIcon } from "@radix-ui/react-icons";
```

## 尺寸系统

### 元素尺寸比例

```css
:root {
  /* 固定尺寸 */
  --size-4: 1rem; /* 16px */
  --size-5: 1.25rem; /* 20px */
  --size-6: 1.5rem; /* 24px */
  --size-8: 2rem; /* 32px */
  --size-10: 2.5rem; /* 40px */
  --size-12: 3rem; /* 48px */
  --size-14: 3.5rem; /* 56px */
  --size-16: 4rem; /* 64px */
  --size-20: 5rem; /* 80px */
  --size-24: 6rem; /* 96px */
  --size-32: 8rem; /* 128px */

  /* 组件高度 */
  --height-input-sm: var(--size-8); /* 32px */
  --height-input-md: var(--size-10); /* 40px */
  --height-input-lg: var(--size-12); /* 48px */

  /* 头像尺寸 */
  --avatar-xs: var(--size-6); /* 24px */
  --avatar-sm: var(--size-8); /* 32px */
  --avatar-md: var(--size-10); /* 40px */
  --avatar-lg: var(--size-12); /* 48px */
  --avatar-xl: var(--size-16); /* 64px */
  --avatar-2xl: var(--size-24); /* 96px */
}
```

### 宽高比

```css
.aspect-ratios {
  /* 标准比例 */
  --aspect-square: 1 / 1;
  --aspect-video: 16 / 9;
  --aspect-photo: 4 / 3;
  --aspect-portrait: 3 / 4;
  --aspect-cinema: 21 / 9;
  --aspect-golden: 1.618 / 1;
}

/* 使用示例 */
.thumbnail {
  aspect-ratio: var(--aspect-video);
  object-fit: cover;
}

.avatar {
  aspect-ratio: var(--aspect-square);
  border-radius: 50%;
}
```

### 圆角比例

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem; /* 2px */
  --radius-default: 0.25rem; /* 4px */
  --radius-md: 0.375rem; /* 6px */
  --radius-lg: 0.5rem; /* 8px */
  --radius-xl: 0.75rem; /* 12px */
  --radius-2xl: 1rem; /* 16px */
  --radius-3xl: 1.5rem; /* 24px */
  --radius-full: 9999px;

  /* 组件特定 */
  --radius-button: var(--radius-md);
  --radius-input: var(--radius-md);
  --radius-card: var(--radius-lg);
  --radius-modal: var(--radius-xl);
  --radius-badge: var(--radius-full);
}
```
