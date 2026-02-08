# ARIA 模式和最佳实践

## 概述

ARIA(Accessible Rich Internet Applications,无障碍富互联网应用)提供了在原生 HTML 语义不足时增强无障碍性的属性。ARIA 的第一条规则是:如果原生 HTML 可以完成工作,就不要使用 ARIA。

## ARIA 基础

### 角色

角色定义元素是什么或做什么。

```tsx
// 小部件角色
<div role="button">点击我</div>
<div role="checkbox" aria-checked="true">选项</div>
<div role="slider" aria-valuenow="50">音量</div>

// 地标角色(优先使用语义化 HTML)
<div role="main">...</div>      // 更好:<main>
<div role="navigation">...</div> // 更好:<nav>
<div role="banner">...</div>     // 更好:<header>

// 文档结构角色
<div role="region" aria-label="精选内容">...</div>
<div role="group" aria-label="格式选项">...</div>
```

### 状态和属性

状态指示当前条件;属性描述关系。

```tsx
// 状态(可以改变)
aria-checked="true|false|mixed"
aria-disabled="true|false"
aria-expanded="true|false"
aria-hidden="true|false"
aria-pressed="true|false"
aria-selected="true|false"

// 属性(通常静态)
aria-label="可访问名称"
aria-labelledby="label-id"
aria-describedby="description-id"
aria-controls="controlled-element-id"
aria-owns="owned-element-id"
aria-live="polite|assertive|off"
```

## 常见 ARIA 模式

### 手风琴

```tsx
function Accordion({ items }) {
  const [openIndex, setOpenIndex] = useState(-1);

  return (
    <div className="accordion">
      {items.map((item, index) => {
        const isOpen = openIndex === index;
        const headingId = `accordion-heading-${index}`;
        const panelId = `accordion-panel-${index}`;

        return (
          <div key={index}>
            <h3>
              <button
                id={headingId}
                aria-expanded={isOpen}
                aria-controls={panelId}
                onClick={() => setOpenIndex(isOpen ? -1 : index)}
              >
                {item.title}
                <span aria-hidden="true">{isOpen ? "−" : "+"}</span>
              </button>
            </h3>
            <div
              id={panelId}
              role="region"
              aria-labelledby={headingId}
              hidden={!isOpen}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

### 标签页

```tsx
function Tabs({ tabs }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const tabListRef = useRef(null);

  const handleKeyDown = (e, index) => {
    let newIndex = index;

    switch (e.key) {
      case "ArrowRight":
        newIndex = (index + 1) % tabs.length;
        break;
      case "ArrowLeft":
        newIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case "Home":
        newIndex = 0;
        break;
      case "End":
        newIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    setActiveIndex(newIndex);
    tabListRef.current?.children[newIndex]?.focus();
  };

  return (
    <div>
      <div role="tablist" ref={tabListRef} aria-label="内容标签页">
        {tabs.map((tab, index) => (
          <button
            key={index}
            role="tab"
            id={`tab-${index}`}
            aria-selected={index === activeIndex}
            aria-controls={`panel-${index}`}
            tabIndex={index === activeIndex ? 0 : -1}
            onClick={() => setActiveIndex(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab, index) => (
        <div
          key={index}
          role="tabpanel"
          id={`panel-${index}`}
          aria-labelledby={`tab-${index}`}
          hidden={index !== activeIndex}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

### 菜单按钮

```tsx
function MenuButton({ label, items }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const buttonRef = useRef(null);
  const menuRef = useRef(null);
  const menuId = useId();

  const handleKeyDown = (e) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setActiveIndex(0);
        } else {
          setActiveIndex((prev) => Math.min(prev + 1, items.length - 1));
        }
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((prev) => Math.max(prev - 1, 0));
        break;
      case "Escape":
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
      case "Enter":
      case " ":
        if (isOpen && activeIndex >= 0) {
          e.preventDefault();
          items[activeIndex].onClick();
          setIsOpen(false);
        }
        break;
    }
  };

  // 焦点管理
  useEffect(() => {
    if (isOpen && activeIndex >= 0) {
      menuRef.current?.children[activeIndex]?.focus();
    }
  }, [isOpen, activeIndex]);

  return (
    <div>
      <button
        ref={buttonRef}
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-controls={menuId}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
      >
        {label}
      </button>

      {isOpen && (
        <ul
          ref={menuRef}
          id={menuId}
          role="menu"
          aria-label={label}
          onKeyDown={handleKeyDown}
        >
          {items.map((item, index) => (
            <li
              key={index}
              role="menuitem"
              tabIndex={-1}
              onClick={() => {
                item.onClick();
                setIsOpen(false);
                buttonRef.current?.focus();
              }}
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### 组合框(自动完成)

```tsx
function Combobox({ options, onSelect, placeholder }) {
  const [inputValue, setInputValue] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef(null);
  const listboxId = useId();

  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes(inputValue.toLowerCase()),
  );

  const handleKeyDown = (e) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex((prev) =>
          Math.min(prev + 1, filteredOptions.length - 1),
        );
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((prev) => Math.max(prev - 1, 0));
        break;
      case "Enter":
        if (activeIndex >= 0) {
          e.preventDefault();
          selectOption(filteredOptions[activeIndex]);
        }
        break;
      case "Escape":
        setIsOpen(false);
        setActiveIndex(-1);
        break;
    }
  };

  const selectOption = (option) => {
    setInputValue(option);
    onSelect(option);
    setIsOpen(false);
    setActiveIndex(-1);
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="text"
        role="combobox"
        aria-expanded={isOpen}
        aria-controls={listboxId}
        aria-activedescendant={
          activeIndex >= 0 ? `option-${activeIndex}` : undefined
        }
        aria-autocomplete="list"
        value={inputValue}
        placeholder={placeholder}
        onChange={(e) => {
          setInputValue(e.target.value);
          setIsOpen(true);
          setActiveIndex(-1);
        }}
        onKeyDown={handleKeyDown}
        onFocus={() => setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
      />

      {isOpen && filteredOptions.length > 0 && (
        <ul id={listboxId} role="listbox">
          {filteredOptions.map((option, index) => (
            <li
              key={option}
              id={`option-${index}`}
              role="option"
              aria-selected={index === activeIndex}
              onClick={() => selectOption(option)}
              onMouseEnter={() => setActiveIndex(index)}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### 警告对话框

```tsx
function AlertDialog({ isOpen, onConfirm, onCancel, title, message }) {
  const confirmRef = useRef(null);
  const dialogId = useId();
  const titleId = `${dialogId}-title`;
  const descId = `${dialogId}-desc`;

  useEffect(() => {
    if (isOpen) {
      confirmRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <FocusTrap>
      <div
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descId}
      >
        <div className="backdrop" onClick={onCancel} />

        <div className="dialog">
          <h2 id={titleId}>{title}</h2>
          <p id={descId}>{message}</p>

          <div className="actions">
            <button onClick={onCancel}>取消</button>
            <button ref={confirmRef} onClick={onConfirm}>
              确认
            </button>
          </div>
        </div>
      </div>
    </FocusTrap>
  );
}
```

### 工具栏

```tsx
function Toolbar({ items }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const toolbarRef = useRef(null);

  const handleKeyDown = (e) => {
    let newIndex = activeIndex;

    switch (e.key) {
      case "ArrowRight":
        newIndex = (activeIndex + 1) % items.length;
        break;
      case "ArrowLeft":
        newIndex = (activeIndex - 1 + items.length) % items.length;
        break;
      case "Home":
        newIndex = 0;
        break;
      case "End":
        newIndex = items.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    setActiveIndex(newIndex);
    toolbarRef.current?.querySelectorAll("button")[newIndex]?.focus();
  };

  return (
    <div
      ref={toolbarRef}
      role="toolbar"
      aria-label="文本格式化"
      onKeyDown={handleKeyDown}
    >
      {items.map((item, index) => (
        <button
          key={index}
          tabIndex={index === activeIndex ? 0 : -1}
          aria-pressed={item.isActive}
          aria-label={item.label}
          onClick={item.onClick}
        >
          {item.icon}
        </button>
      ))}
    </div>
  );
}
```

## 实时区域

### 礼貌公告

```tsx
// 不中断的状态消息
function SearchStatus({ count, query }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true">
      为"{query}"找到 {count} 个结果
    </div>
  );
}

// 进度指示器
function LoadingStatus({ progress }) {
  return (
    <div role="status" aria-live="polite">
      加载中:已完成 {progress}%
    </div>
  );
}
```

### 紧急公告

```tsx
// 应该中断的重要错误
function ErrorAlert({ message }) {
  return (
    <div role="alert" aria-live="assertive">
      错误:{message}
    </div>
  );
}

// 表单验证摘要
function ValidationSummary({ errors }) {
  if (errors.length === 0) return null;

  return (
    <div role="alert" aria-live="assertive">
      <h2>请修复以下错误:</h2>
      <ul>
        {errors.map((error, index) => (
          <li key={index}>{error}</li>
        ))}
      </ul>
    </div>
  );
}
```

### 日志区域

```tsx
// 聊天消息或活动日志
function ChatLog({ messages }) {
  return (
    <div role="log" aria-live="polite" aria-relevant="additions">
      {messages.map((msg) => (
        <div key={msg.id}>
          <span className="author">{msg.author}:</span>
          <span className="text">{msg.text}</span>
        </div>
      ))}
    </div>
  );
}
```

## 避免的常见错误

### 1. 冗余的 ARIA

```tsx
// 不好:在按钮上使用 role="button"
<button role="button">点击我</button>

// 好:只使用 button
<button>点击我</button>

// 不好:aria-label 重复可见文本
<button aria-label="提交表单">提交表单</button>

// 好:只使用可见文本
<button>提交表单</button>
```

### 2. 无效的 ARIA

```tsx
// 不好:在不可选择元素上使用 aria-selected
<div aria-selected="true">项目</div>

// 好:与适当的角色一起使用
<div role="option" aria-selected="true">项目</div>

// 不好:没有控制关系的 aria-expanded
<button aria-expanded="true">菜单</button>
<div>菜单内容</div>

// 好:使用 aria-controls
<button aria-expanded="true" aria-controls="menu">菜单</button>
<div id="menu">菜单内容</div>
```

### 3. 隐藏内容仍然被宣布

```tsx
// 不好:视觉上隐藏但仍在无障碍树中
<div style={{ display: 'none' }}>隐藏内容</div>

// 好:正确隐藏
<div style={{ display: 'none' }} aria-hidden="true">隐藏内容</div>

// 或者只使用 display: none(隐式隐藏)
<div hidden>隐藏内容</div>
```

## 资源

- [WAI-ARIA 创作实践](https://www.w3.org/WAI/ARIA/apg/)
- [HTML 中的 ARIA](https://www.w3.org/TR/html-aria/)
- [使用 ARIA](https://www.w3.org/TR/using-aria/)
