# WCAG 2.2 指南参考

## 概述

Web 内容无障碍指南(WCAG)2.2 提供了使 Web 内容更易访问的建议。它们组织成四个原则(POUR):可感知、可操作、可理解和健壮性。

## 合规级别

- **A 级**:最小无障碍(必须满足)
- **AA 级**:标准无障碍(应该满足)
- **AAA 级**:增强无障碍(可以满足)

大多数组织的目标是 AA 级合规。

## 原则 1: 可感知

内容必须能以用户可感知的方式呈现。

### 1.1 文本替代

#### 1.1.1 非文本内容(A 级)

所有非文本内容都需要文本替代。

```tsx
// 图片
<img src="chart.png" alt="第三季度销售额比第二季度增长25%" />

// 装饰性图片
<img src="decorative-line.svg" alt="" role="presentation" />

// 具有长描述的复杂图片
<figure>
  <img src="org-chart.png" alt="组织结构图" aria-describedby="org-desc" />
  <figcaption id="org-desc">
    CEO 向董事会汇报。三位副总裁向 CEO 汇报:
    工程副总裁、销售副总裁和营销副总裁...
  </figcaption>
</figure>

// 有意义的图标
<button aria-label="删除项目">
  <TrashIcon aria-hidden="true" />
</button>

// 带有可见文本的图标按钮
<button>
  <DownloadIcon aria-hidden="true" />
  <span>下载</span>
</button>
```

### 1.2 基于时间的媒体

#### 1.2.1 仅音频和仅视频(A 级)

```tsx
// 带有文字稿的音频
<audio src="podcast.mp3" controls />
<details>
  <summary>查看文字稿</summary>
  <p>完整文字稿文本...</p>
</details>

// 带有字幕的视频
<video controls>
  <source src="tutorial.mp4" type="video/mp4" />
  <track kind="captions" src="captions-en.vtt" srclang="en" label="英语" />
  <track kind="subtitles" src="subtitles-es.vtt" srclang="es" label="西班牙语" />
</video>
```

### 1.3 可适应

#### 1.3.1 信息和关系(A 级)

结构和关系必须可通过程序确定。

```tsx
// 正确的标题层次结构
<main>
  <h1>页面标题</h1>
  <section>
    <h2>章节标题</h2>
    <h3>小节</h3>
  </section>
</main>

// 带有标题的数据表
<table>
  <caption>季度销售报告</caption>
  <thead>
    <tr>
      <th scope="col">产品</th>
      <th scope="col">第一季度</th>
      <th scope="col">第二季度</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">小部件 A</th>
      <td>$10,000</td>
      <td>$12,000</td>
    </tr>
  </tbody>
</table>

// 用于分组内容的列表
<nav aria-label="主导航">
  <ul>
    <li><a href="/">首页</a></li>
    <li><a href="/about">关于</a></li>
    <li><a href="/contact">联系</a></li>
  </ul>
</nav>
```

#### 1.3.5 识别输入目的(AA 级)

```tsx
// 带有自动完成的输入,用于自动填充
<form>
  <label htmlFor="name">全名</label>
  <input id="name" name="name" autoComplete="name" />

  <label htmlFor="email">电子邮件</label>
  <input id="email" name="email" type="email" autoComplete="email" />

  <label htmlFor="phone">电话</label>
  <input id="phone" name="phone" type="tel" autoComplete="tel" />

  <label htmlFor="address">街道地址</label>
  <input id="address" name="address" autoComplete="street-address" />

  <label htmlFor="cc">信用卡号</label>
  <input id="cc" name="cc" autoComplete="cc-number" />
</form>
```

### 1.4 可区分

#### 1.4.1 颜色使用(A 级)

```tsx
// 不好:仅颜色表示错误
<input className={hasError ? 'border-red-500' : ''} />

// 好:颜色加图标和文本
<div>
  <input
    className={hasError ? 'border-red-500' : ''}
    aria-invalid={hasError}
    aria-describedby={hasError ? 'error-message' : undefined}
  />
  {hasError && (
    <p id="error-message" className="text-red-500 flex items-center gap-1">
      <AlertIcon aria-hidden="true" />
      此字段为必填
    </p>
  )}
</div>
```

#### 1.4.3 对比度(最小)(AA 级)

```css
/* 最小对比度 */
/* 普通文本: 4.5:1 */
/* 大文本(18pt+ 或 14pt 粗体+): 3:1 */

/* 良好对比度示例 */
.text-on-white {
  color: #595959; /* 白色上 7:1 比例 */
}

.text-on-dark {
  color: #ffffff;
  background: #333333; /* 12.6:1 比例 */
}

/* 链接必须与周围文本区分开 */
.link {
  color: #0066cc; /* 白色上 4.5:1 */
  text-decoration: underline; /* 额外的视觉提示 */
}
```

#### 1.4.11 非文本对比度(AA 级)

```css
/* UI 组件需要 3:1 对比度 */
.button {
  border: 2px solid #767676; /* 与白色 3:1 */
  background: white;
}

.input {
  border: 1px solid #767676;
}

.input:focus {
  outline: 2px solid #0066cc; /* 焦点指示器需要 3:1 */
  outline-offset: 2px;
}

/* 自定义复选框 */
.checkbox {
  border: 2px solid #767676;
}

.checkbox:checked {
  background: #0066cc;
  border-color: #0066cc;
}
```

#### 1.4.12 文本间距(AA 级)

用户调整文本间距时不得丢失内容。

```css
/* 允许文本间距调整而不破坏布局 */
.content {
  /* 使用相对单位 */
  line-height: 1.5; /* 至少 1.5x 字体大小 */
  letter-spacing: 0.12em; /* 支持 0.12em */
  word-spacing: 0.16em; /* 支持 0.16em */

  /* 不要在文本容器上使用固定高度 */
  min-height: auto;

  /* 允许换行 */
  overflow-wrap: break-word;
}

/* 使用这些值测试: */
/* 行高: 1.5x 字体大小 */
/* 字间距: 0.12em */
/* 词间距: 0.16em */
/* 段落间距: 2x 字体大小 */
```

#### 1.4.13 悬停或焦点上的内容(AA 级)

```tsx
// 工具提示模式
function Tooltip({ content, children }) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div
          role="tooltip"
          // 可关闭:用户可以不移动指针就关闭
          onKeyDown={(e) => e.key === "Escape" && setIsVisible(false)}
          // 可悬停:当指针移动到内容上时保持可见
          onMouseEnter={() => setIsVisible(true)}
          onMouseLeave={() => setIsVisible(false)}
          // 持久:保持到触发器失去焦点/悬停
        >
          {content}
        </div>
      )}
    </div>
  );
}
```

## 原则 2: 可操作

界面组件必须对所有用户都可操作。

### 2.1 键盘可访问

#### 2.1.1 键盘(A 级)

所有功能都必须通过键盘操作。

```tsx
// 自定义交互元素
function CustomButton({ onClick, children }) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {children}
    </div>
  );
}

// 更好:只使用 button
function BetterButton({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}
```

#### 2.1.2 无键盘陷阱(A 级)

```tsx
// 具有适当焦点管理的模态框
function Modal({ isOpen, onClose, children }) {
  const closeButtonRef = useRef(null);

  // 关闭时返回焦点
  useEffect(() => {
    if (!isOpen) return;

    const previousFocus = document.activeElement;
    closeButtonRef.current?.focus();

    return () => {
      (previousFocus as HTMLElement)?.focus();
    };
  }, [isOpen]);

  // 允许 Escape 关闭
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  return (
    <FocusTrap>
      <div role="dialog" aria-modal="true">
        <button ref={closeButtonRef} onClick={onClose}>
          关闭
        </button>
        {children}
      </div>
    </FocusTrap>
  );
}
```

### 2.4 可导航

#### 2.4.1 绕过块(A 级)

```tsx
// 跳过链接
<body>
  <a href="#main" className="skip-link">
    跳转到主内容
  </a>
  <a href="#nav" className="skip-link">
    跳转到导航
  </a>

  <header>...</header>

  <nav id="nav" aria-label="主">
    ...
  </nav>

  <main id="main" tabIndex={-1}>
    {/* 主内容 */}
  </main>
</body>
```

#### 2.4.4 链接目的(在上下文中)(A 级)

```tsx
// 不好:模糊的链接文本
<a href="/report">点击这里</a>
<a href="/report">阅读更多</a>

// 好:描述性链接文本
<a href="/report">查看季度销售报告</a>

// 好:上下文提供含义
<article>
  <h2>季度销售报告</h2>
  <p>本季度销售额增长25%...</p>
  <a href="/report">阅读完整报告</a>
</article>

// 好:视觉隐藏文本提供上下文
<a href="/report">
  阅读更多
  <span className="sr-only"> 关于季度销售报告</span>
</a>
```

#### 2.4.7 焦点可见(AA 级)

```css
/* 始终显示焦点指示器 */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* 自定义焦点样式 */
.button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--color-focus);
}

/* 链接的高可见性焦点 */
.link:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
  background: var(--color-focus-bg);
}
```

### 2.5 输入方式(2.2 新增)

#### 2.5.8 目标尺寸(最小)(AA 级) - 新增

交互目标必须至少 24x24 CSS 像素。

```css
/* 最小目标尺寸 */
.interactive {
  min-width: 24px;
  min-height: 24px;
}

/* 触摸推荐尺寸(44x44) */
.touch-target {
  min-width: 44px;
  min-height: 44px;
}

/* 如果有足够的间距,内联链接可以豁免 */
.link {
  /* 内联文本链接不需要最小尺寸 */
  /* 但应该有足够的行高 */
  line-height: 1.5;
}
```

## 原则 3: 可理解

内容和界面必须可理解。

### 3.1 可读

#### 3.1.1 页面语言(A 级)

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    ...
  </head>
  <body>
    ...
  </body>
</html>
```

#### 3.1.2 部分语言(AA 级)

```tsx
<p>
  法语短语 <span lang="fr">c'est la vie</span> 意思是"这就是生活"。
</p>
```

### 3.2 可预测

#### 3.2.2 输入时(A 级)

不要在输入时自动更改上下文。

```tsx
// 不好:选择时自动提交
<select onChange={(e) => form.submit()}>
  <option>选择国家</option>
</select>

// 好:显式提交操作
<select onChange={(e) => setCountry(e.target.value)}>
  <option>选择国家</option>
</select>
<button type="submit">继续</button>
```

### 3.3 输入帮助

#### 3.3.1 错误识别(A 级)

```tsx
function FormField({ id, label, error, ...props }) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={`${id}-error`} role="alert" className="text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
```

#### 3.3.7 重复输入(A 级) - 新增

不要要求用户重新输入之前提供的信息。

```tsx
// 从账单地址自动填充送货地址
function CheckoutForm() {
  const [sameAsBilling, setSameAsBilling] = useState(false);
  const [billing, setBilling] = useState({});
  const [shipping, setShipping] = useState({});

  return (
    <form>
      <fieldset>
        <legend>账单地址</legend>
        <AddressFields value={billing} onChange={setBilling} />
      </fieldset>

      <label>
        <input
          type="checkbox"
          checked={sameAsBilling}
          onChange={(e) => {
            setSameAsBilling(e.target.checked);
            if (e.target.checked) setShipping(billing);
          }}
        />
        送货地址与账单地址相同
      </label>

      {!sameAsBilling && (
        <fieldset>
          <legend>送货地址</legend>
          <AddressFields value={shipping} onChange={setShipping} />
        </fieldset>
      )}
    </form>
  );
}
```

## 原则 4: 健壮性

内容必须足够健壮以支持辅助技术。

### 4.1 兼容

#### 4.1.2 名称、角色、值(A 级)

```tsx
// 自定义组件必须暴露名称、角色和值
function CustomCheckbox({ checked, onChange, label }) {
  return (
    <button
      role="checkbox"
      aria-checked={checked}
      aria-label={label}
      onClick={() => onChange(!checked)}
    >
      {checked ? "✓" : "○"} {label}
    </button>
  );
}

// 自定义滑块
function CustomSlider({ value, min, max, label, onChange }) {
  return (
    <div
      role="slider"
      aria-valuemin={min}
      aria-valuemax={max}
      aria-valuenow={value}
      aria-label={label}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "ArrowRight") onChange(Math.min(value + 1, max));
        if (e.key === "ArrowLeft") onChange(Math.max(value - 1, min));
      }}
    >
      <div style={{ width: `${((value - min) / (max - min)) * 100}%` }} />
    </div>
  );
}
```

## 测试检查清单

```markdown
## 键盘测试

- [ ] 所有交互元素都可用 Tab 聚焦
- [ ] 焦点顺序与视觉顺序匹配
- [ ] 焦点指示器始终可见
- [ ] 无键盘陷阱
- [ ] Escape 关闭模态框/下拉菜单
- [ ] Enter/Space 激活按钮和链接

## 屏幕阅读器测试

- [ ] 所有图片都有 alt 文本
- [ ] 表单输入有标签
- [ ] 标题按逻辑顺序
- [ ] 地标存在(main、nav、header、footer)
- [ ] 动态内容被宣布
- [ ] 错误消息被宣布

## 视觉测试

- [ ] 文本对比度至少 4.5:1
- [ ] UI 组件对比度至少 3:1
- [ ] 在 200% 缩放下工作
- [ ] 内容在文本间距下可读
- [ ] 焦点指示器可见
- [ ] 颜色不是含义的唯一指示器
```

## 资源

- [WCAG 2.2 快速参考](https://www.w3.org/WAI/WCAG22/quickref/)
- [理解 WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/)
- [WCAG 2.2 技术](https://www.w3.org/WAI/WCAG22/Techniques/)
