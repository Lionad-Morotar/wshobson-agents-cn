---
name: wcag-audit-patterns
description: 通过自动化测试、手动验证和修复指导进行 WCAG 2.2 可访问性审计。在审计网站可访问性、修复 WCAG 违规或实现可访问设计模式时使用。
---

# WCAG 审计模式

根据 WCAG 2.2 指南审计 Web 内容的综合指南，包含可操作的修复策略。

## 何时使用此技能

- 进行可访问性审计
- 修复 WCAG 违规
- 实现可访问组件
- 准备应对可访问性诉讼
- 满足 ADA/Section 508 要求
- 实现 VPAT 合规

## 核心概念

### 1. WCAG 合规级别

| 级别   | 描述            | 适用于      |
| ------- | ---------------------- | ----------------- |
| **A**   | 最低可访问性  | 法律基准    |
| **AA**  | 标准合规   | 大多数法规  |
| **AAA** | 增强可访问性 | 特殊需求 |

### 2. POUR 原则

```
Perceivable:  用户能否感知内容？
Operable:     用户能否操作界面？
Understandable: 用户能否理解内容？
Robust:       是否与辅助技术兼容？
```

### 3. 按影响分类的常见违规

```
严重（阻断性）：
├── 功能图像缺少 alt 文本
├── 交互元素无法通过键盘访问
├── 表单缺少标签
└── 媒体自动播放且无控制

严重：
├── 颜色对比度不足
├── 缺少跳过链接
├── 自定义组件不可访问
└── 缺少页面标题

中等：
├── 缺少语言属性
├── 链接文本不明确
├── 缺少地标
└── 标题层级不当
```

## 审计清单

### 可感知（原则 1）

````markdown
## 1.1 文本替代

### 1.1.1 非文本内容（A 级）

- [ ] 所有图像都有 alt 文本
- [ ] 装饰性图像使用 alt=""
- [ ] 复杂图像有详细描述
- [ ] 有意义的图标有无障碍名称
- [ ] 验证码有替代方案

检查：

```html
<!-- Good -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />
<img src="decorative-line.png" alt="" />

<!-- Bad -->
<img src="chart.png" />
<img src="decorative-line.png" alt="decorative line" />
```
````

## 1.2 基于时间的媒体

### 1.2.1 纯音频和纯视频（A 级）

- [ ] 音频有文本记录
- [ ] 视频有音频描述或文本记录

### 1.2.2 字幕（A 级）

- [ ] 所有视频都有同步字幕
- [ ] 字幕准确完整
- [ ] 包含说话人识别

### 1.2.3 音频描述（A 级）

- [ ] 视频有视觉内容的音频描述

## 1.3 可适应

### 1.3.1 信息和关系（A 级）

- [ ] 标题使用正确的标签（h1-h6）
- [ ] 列表使用 ul/ol/dl
- [ ] 表格有表头
- [ ] 表单输入有标签
- [ ] 存在 ARIA 地标

检查：

```html
<!-- Heading hierarchy -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h2>Another Section</h2>

<!-- Table headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Price</th>
    </tr>
  </thead>
</table>
```

### 1.3.2 有意义的序列（A 级）

- [ ] 阅读顺序符合逻辑
- [ ] CSS 定位不破坏顺序
- [ ] 焦点顺序与视觉顺序一致

### 1.3.3 感官特征（A 级）

- [ ] 指令不仅依赖形状/颜色
- [ ] "点击红色按钮" → "点击提交（红色按钮）"

## 1.4 可区分

### 1.4.1 颜色使用（A 级）

- [ ] 颜色不是传达信息的唯一方式
- [ ] 链接在不依赖颜色时可区分
- [ ] 错误状态不仅用颜色表示

### 1.4.3 对比度（最低）（AA 级）

- [ ] 文本：4.5:1 对比度
- [ ] 大文本（18pt+）：3:1 对比度
- [ ] UI 组件：3:1 对比度

工具：WebAIM Contrast Checker、axe DevTools

### 1.4.4 调整文本大小（AA 级）

- [ ] 文本可放大至 200% 且不丢失内容
- [ ] 在 320px 宽度下无水平滚动
- [ ] 内容正确重排

### 1.4.10 重排（AA 级）

- [ ] 内容在 400% 缩放时重排
- [ ] 无二维滚动
- [ ] 所有内容在 320px 宽度下可访问

### 1.4.11 非文本对比度（AA 级）

- [ ] UI 组件有 3:1 对比度
- [ ] 焦点指示器可见
- [ ] 图形对象可区分

### 1.4.12 文本间距（AA 级）

- [ ] 增加间距时不丢失内容
- [ ] 行高 1.5 倍字体大小
- [ ] 段落间距 2 倍字体大小
- [ ] 字母间距 0.12 倍字体大小
- [ ] 单词间距 0.16 倍字体大小

````

### 可操作（原则 2）

```markdown
## 2.1 键盘可访问

### 2.1.1 键盘（A 级）
- [ ] 所有功能可通过键盘访问
- [ ] 无键盘陷阱
- [ ] Tab 顺序符合逻辑
- [ ] 自定义组件可通过键盘操作

检查：
```javascript
// Custom button must be keyboard accessible
<div role="button" tabindex="0"
     onkeydown="if(event.key === 'Enter' || event.key === ' ') activate()">
````

### 2.1.2 无键盘陷阱（A 级）

- [ ] 焦点可以从所有组件移开
- [ ] 模态对话框正确捕获焦点
- [ ] 模态关闭后焦点返回

## 2.2 充足时间

### 2.2.1 可调整时限（A 级）

- [ ] 会话超时可延长
- [ ] 超时前警告用户
- [ ] 可选择禁用自动刷新

### 2.2.2 暂停、停止、隐藏（A 级）

- [ ] 移动内容可暂停
- [ ] 自动更新内容可暂停
- [ ] 动画尊重 prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## 2.3 癫痫和身体反应

### 2.3.1 三次闪烁（A 级）

- [ ] 无内容每秒闪烁超过 3 次
- [ ] 闪烁区域较小（<25% 视口）

## 2.4 可导航

### 2.4.1 绕过块（A 级）

- [ ] 存在跳转到主内容的链接
- [ ] 定义了地标区域
- [ ] 正确的标题结构

```html
<a href="#main" class="skip-link">Skip to main content</a>
<main id="main">...</main>
```

### 2.4.2 页面标题（A 级）

- [ ] 唯一、描述性的页面标题
- [ ] 标题反映页面内容

### 2.4.3 焦点顺序（A 级）

- [ ] 焦点顺序与视觉顺序一致
- [ ] 正确使用 tabindex

### 2.4.4 链接目的（在上下文中）（A 级）

- [ ] 链接在脱离上下文时仍有意义
- [ ] 没有"点击这里"或"阅读更多"单独使用

```html
<!-- Bad -->
<a href="report.pdf">Click here</a>

<!-- Good -->
<a href="report.pdf">Download Q4 Sales Report (PDF)</a>
```

### 2.4.6 标题和标签（AA 级）

- [ ] 标题描述内容
- [ ] 标签描述目的

### 2.4.7 焦点可见（AA 级）

- [ ] 所有元素上焦点指示器可见
- [ ] 自定义焦点样式符合对比度

```css
:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}
```

### 2.4.11 焦点不被遮挡（AA 级）- WCAG 2.2

- [ ] 焦点元素未被完全隐藏
- [ ] 粘性标题不遮挡焦点

````

### 可理解（原则 3）

```markdown
## 3.1 可读

### 3.1.1 页面语言（A 级）
- [ ] 设置了 HTML lang 属性
- [ ] 语言与内容匹配

```html
<html lang="en">
````

### 3.1.2 部分语言（AA 级）

- [ ] 标记语言变化

```html
<p>The French word <span lang="fr">bonjour</span> means hello.</p>
```

## 3.2 可预测

### 3.2.1 获得焦点时（A 级）

- [ ] 仅获得焦点时不改变上下文
- [ ] 获得焦点时无意外弹窗

### 3.2.2 输入时（A 级）

- [ ] 不自动提交表单
- [ ] 上下文改变前警告用户

### 3.2.3 一致的导航（AA 级）

- [ ] 跨页面导航一致
- [ ] 重复组件顺序相同

### 3.2.4 一致的标识（AA 级）

- [ ] 相同功能 = 相同标签
- [ ] 图标使用一致

## 3.3 输入帮助

### 3.3.1 错误标识（A 级）

- [ ] 错误清晰标识
- [ ] 错误消息描述问题
- [ ] 错误与字段关联

```html
<input aria-describedby="email-error" aria-invalid="true" />
<span id="email-error" role="alert">Please enter valid email</span>
```

### 3.3.2 标签或指令（A 级）

- [ ] 所有输入有可见标签
- [ ] 指示必填字段
- [ ] 提供格式提示

### 3.3.3 错误建议（AA 级）

- [ ] 错误包含修正建议
- [ ] 建议具体明确

### 3.3.4 错误预防（AA 级）

- [ ] 法律/财务表单可撤销
- [ ] 提交前检查数据
- [ ] 用户可在提交前审查

````

### 健壮（原则 4）

```markdown
## 4.1 兼容

### 4.1.1 解析（A 级）- WCAG 2.2 中已废弃
- [ ] 有效的 HTML（良好实践）
- [ ] 无重复 ID
- [ ] 完整的开始/结束标签

### 4.1.2 名称、角色、值（A 级）
- [ ] 自定义组件有无障碍名称
- [ ] ARIA 角色正确
- [ ] 状态变化被宣告

```html
<!-- Accessible custom checkbox -->
<div role="checkbox"
     aria-checked="false"
     tabindex="0"
     aria-labelledby="label">
</div>
<span id="label">Accept terms</span>
````

### 4.1.3 状态消息（AA 级）

- [ ] 状态更新被宣告
- [ ] 正确使用实时区域

```html
<div role="status" aria-live="polite">3 items added to cart</div>

<div role="alert" aria-live="assertive">Error: Form submission failed</div>
```

````

## 自动化测试

```javascript
// axe-core integration
const axe = require('axe-core');

async function runAccessibilityAudit(page) {
  await page.addScriptTag({ path: require.resolve('axe-core') });

  const results = await page.evaluate(async () => {
    return await axe.run(document, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
      }
    });
  });

  return {
    violations: results.violations,
    passes: results.passes,
    incomplete: results.incomplete
  };
}

// Playwright test example
test('should have no accessibility violations', async ({ page }) => {
  await page.goto('/');
  const results = await runAccessibilityAudit(page);

  expect(results.violations).toHaveLength(0);
});
````

```bash
# CLI tools
npx @axe-core/cli https://example.com
npx pa11y https://example.com
lighthouse https://example.com --only-categories=accessibility
```

## 修复模式

### 修复：缺少表单标签

```html
<!-- Before -->
<input type="email" placeholder="Email" />

<!-- After: Option 1 - Visible label -->
<label for="email">Email address</label>
<input id="email" type="email" />

<!-- After: Option 2 - aria-label -->
<input type="email" aria-label="Email address" />

<!-- After: Option 3 - aria-labelledby -->
<span id="email-label">Email</span>
<input type="email" aria-labelledby="email-label" />
```

### 修复：颜色对比度不足

```css
/* Before: 2.5:1 contrast */
.text {
  color: #767676;
}

/* After: 4.5:1 contrast */
.text {
  color: #595959;
}

/* Or add background */
.text {
  color: #767676;
  background: #000;
}
```

### 修复：键盘导航

```javascript
// Make custom element keyboard accessible
class AccessibleDropdown extends HTMLElement {
  connectedCallback() {
    this.setAttribute("tabindex", "0");
    this.setAttribute("role", "combobox");
    this.setAttribute("aria-expanded", "false");

    this.addEventListener("keydown", (e) => {
      switch (e.key) {
        case "Enter":
        case " ":
          this.toggle();
          e.preventDefault();
          break;
        case "Escape":
          this.close();
          break;
        case "ArrowDown":
          this.focusNext();
          e.preventDefault();
          break;
        case "ArrowUp":
          this.focusPrevious();
          e.preventDefault();
          break;
      }
    });
  }
}
```

## 最佳实践

### 要做的

- **尽早开始** - 从设计阶段考虑可访问性
- **与真实用户测试** - 残障用户提供最佳反馈
- **尽可能自动化** - 可检测 30-50% 的问题
- **使用语义 HTML** - 减少 ARIA 需求
- **文档化模式** - 构建可访问组件库

### 不要做的

- **不要仅依赖自动化测试** - 需要手动测试
- **不要将 ARIA 作为首选方案** - 原生 HTML 优先
- **不要隐藏焦点轮廓** - 键盘用户需要它们
- **不要禁用缩放** - 用户需要调整大小
- **不要仅使用颜色** - 需要多个指示器

## 资源

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [WebAIM](https://webaim.org/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [axe DevTools](https://www.deque.com/axe/)
