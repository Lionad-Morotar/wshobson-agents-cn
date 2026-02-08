---
name: screen-reader-testing
description: 使用屏幕阅读器（包括 VoiceOver、NVDA 和 JAWS）测试 Web 应用程序。用于验证屏幕阅读器兼容性、调试无障碍问题或确保辅助技术支持时使用。
---

# 屏幕阅读器测试

使用屏幕阅读器（包括 VoiceOver、NVDA 和 JAWS）测试 Web 应用程序的实用指南，以进行全面的无障碍验证。

## 何时使用此技能

- 验证屏幕阅读器兼容性
- 测试 ARIA 实现
- 调试辅助技术问题
- 验证表单无障碍性
- 测试动态内容通知
- 确保导航无障碍性

## 核心概念

### 1. 主要屏幕阅读器

| 屏幕阅读器   | 平台       | 浏览器         | 使用率 |
| ------------ | ---------- | -------------- | ------ |
| **VoiceOver** | macOS/iOS  | Safari         | ~15%   |
| **NVDA**      | Windows    | Firefox/Chrome | ~31%   |
| **JAWS**      | Windows    | Chrome/IE      | ~40%   |
| **TalkBack**  | Android    | Chrome         | ~10%   |
| **Narrator**  | Windows    | Edge           | ~4%    |

### 2. 测试优先级

```
最低覆盖范围:
1. NVDA + Firefox (Windows)
2. VoiceOver + Safari (macOS)
3. VoiceOver + Safari (iOS)

全面覆盖范围:
+ JAWS + Chrome (Windows)
+ TalkBack + Chrome (Android)
+ Narrator + Edge (Windows)
```

### 3. 屏幕阅读器模式

| 模式                | 用途                  | 使用场景         |
| ------------------- | --------------------- | ---------------- |
| **浏览/虚拟模式**   | 阅读内容              | 默认阅读         |
| **焦点/表单模式**   | 与控件交互            | 填写表单         |
| **应用程序模式**    | 自定义小部件          | ARIA 应用程序    |

## VoiceOver (macOS)

### 设置

```
启用: 系统偏好设置 → 辅助功能 → VoiceOver
切换: Cmd + F5
快速切换: 三连按 Touch ID
```

### 基本命令

```
导航:
VO = Ctrl + Option (VoiceOver 修饰键)

VO + 右箭头        下一个元素
VO + 左箭头        上一个元素
VO + Shift + 下箭头  进入组
VO + Shift + 上箭头  退出组

阅读:
VO + A             从光标位置读取全部
Ctrl               停止朗读
VO + B             朗读当前段落

交互:
VO + 空格          激活元素
VO + Shift + M     打开菜单
Tab                下一个可聚焦元素
Shift + Tab        上一个可聚焦元素

转子 (VO + U):
导航方式: 标题、链接、表单、地标
左/右箭头          更改转子类别
上/下箭头          在类别内导航
Enter              转到项目

Web 专用:
VO + Cmd + H       下一个标题
VO + Cmd + J       下一个表单控件
VO + Cmd + L       下一个链接
VO + Cmd + T       下一个表格
```

### 测试清单

```markdown
## VoiceOver 测试清单

### 页面加载

- [ ] 页面标题已播报
- [ ] 找到主要地标
- [ ] 跳过链接正常工作

### 导航

- [ ] 所有标题可通过转子发现
- [ ] 标题级别符合逻辑 (H1 → H2 → H3)
- [ ] 地标正确标记
- [ ] 跳过链接功能正常

### 链接和按钮

- [ ] 链接用途清晰
- [ ] 按钮操作已描述
- [ ] 新窗口/标签页已播报

### 表单

- [ ] 所有标签与输入一起朗读
- [ ] 必填字段已播报
- [ ] 错误消息已朗读
- [ ] 说明可用
- [ ] 焦点移至错误

### 动态内容

- [ ] 警报立即播报
- [ ] 加载状态已传达
- [ ] 内容更新已播报
- [ ] 模态框正确限制焦点

### 表格

- [ ] 表头与单元格关联
- [ ] 表格导航正常工作
- [ ] 复杂表格有标题
```

### 常见问题与修复

```html
<!-- 问题: 按钮未播报用途 -->
<button><svg>...</svg></button>

<!-- 修复 -->
<button aria-label="Close dialog"><svg aria-hidden="true">...</svg></button>

<!-- 问题: 动态内容未播报 -->
<div id="results">New results loaded</div>

<!-- 修复 -->
<div id="results" role="status" aria-live="polite">New results loaded</div>

<!-- 问题: 表单错误未朗读 -->
<input type="email" />
<span class="error">Invalid email</span>

<!-- 修复 -->
<input type="email" aria-invalid="true" aria-describedby="email-error" />
<span id="email-error" role="alert">Invalid email</span>
```

## NVDA (Windows)

### 设置

```
下载: nvaccess.org
启动: Ctrl + Alt + N
停止: Insert + Q
```

### 基本命令

```
导航:
Insert = NVDA 修饰键

下箭头              下一行
上箭头              上一行
Tab                 下一个可聚焦元素
Shift + Tab         上一个可聚焦元素

阅读:
NVDA + 下箭头       朗读全部
Ctrl                停止语音
NVDA + 上箭头       当前行

标题:
H                   下一个标题
Shift + H           上一个标题
1-6                 标题级别 1-6

表单:
F                   下一个表单字段
B                   下一个按钮
E                   下一个编辑字段
X                   下一个复选框
C                   下一个下拉框

链接:
K                   下一个链接
U                   下一个未访问链接
V                   下一个已访问链接

地标:
D                   下一个地标
Shift + D           上一个地标

表格:
T                   下一个表格
Ctrl + Alt + 箭头   导航单元格

元素列表 (NVDA + F7):
显示所有链接、标题、表单字段、地标
```

### 浏览模式与焦点模式

```
NVDA 自动切换模式:
- 浏览模式: 箭头键导航内容
- 焦点模式: 箭头键控制交互元素

手动切换: NVDA + 空格

注意:
- 导航时播报"浏览模式"
- 进入表单字段时播报"焦点模式"
- 应用程序角色强制表单模式
```

### 测试脚本

```markdown
## NVDA 测试脚本

### 初始加载

1. 导航到页面
2. 等待页面加载完成
3. 按 Insert + 下箭头朗读全部
4. 记录: 页面标题、主要内容是否已识别？

### 地标导航

1. 反复按 D
2. 检查: 所有主要区域是否可达？
3. 检查: 地标是否正确标记？

### 标题导航

1. 按 Insert + F7 → 标题
2. 检查: 标题结构是否符合逻辑？
3. 按 H 导航标题
4. 检查: 所有部分是否可发现？

### 表单测试

1. 按 F 查找第一个表单字段
2. 检查: 标签是否朗读？
3. 填写无效数据
4. 提交表单
5. 检查: 错误是否播报？
6. 检查: 焦点是否移至错误？

### 交互元素

1. 使用 Tab 遍历所有交互元素
2. 检查: 每个元素是否播报角色和状态
3. 使用 Enter/空格 激活按钮
4. 检查: 结果是否播报？

### 动态内容

1. 触发内容更新
2. 检查: 更改是否播报？
3. 打开模态框
4. 检查: 焦点是否被限制？
5. 关闭模态框
6. 检查: 焦点是否返回？
```

## JAWS (Windows)

### 基本命令

```
启动: 桌面快捷方式或 Ctrl + Alt + J
虚拟光标: 在浏览器中自动启用

导航:
箭头键             导航内容
Tab                下一个可聚焦元素
Insert + 下箭头    朗读全部
Ctrl               停止语音

快速键:
H                  下一个标题
T                  下一个表格
F                  下一个表单字段
B                  下一个按钮
G                  下一个图形
L                  下一个列表
;                  下一个地标

表单模式:
Enter              进入表单模式
Numpad +           退出表单模式
F5                 列出表单字段

列表:
Insert + F7        链接列表
Insert + F6        标题列表
Insert + F5        表单字段列表

表格:
Ctrl + Alt + 箭头  表格导航
```

## TalkBack (Android)

### 设置

```
启用: 设置 → 辅助功能 → TalkBack
切换: 同时按住两个音量按钮 3 秒
```

### 手势

```
探索: 在屏幕上拖动手指
下一个: 向右滑动
上一个: 向左滑动
激活: 双击
滚动: 双指滑动

阅读控制（向上滑动然后向右）:
- 标题
- 链接
- 控件
- 字符
- 单词
- 行
- 段落
```

## 常见测试场景

### 1. 模态对话框

```html
<!-- 可访问的模态框结构 -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

```javascript
// 焦点管理
function openModal(modal) {
  // 存储最后聚焦的元素
  lastFocus = document.activeElement;

  // 将焦点移至模态框
  modal.querySelector("h2").focus();

  // 限制焦点
  modal.addEventListener("keydown", trapFocus);
}

function closeModal(modal) {
  // 返回焦点
  lastFocus.focus();
}

function trapFocus(e) {
  if (e.key === "Tab") {
    const focusable = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      last.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === last) {
      first.focus();
      e.preventDefault();
    }
  }

  if (e.key === "Escape") {
    closeModal(modal);
  }
}
```

### 2. 实时区域

```html
<!-- 状态消息（礼貌） -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- 内容更新将在当前语音播报完成后播报 -->
</div>

<!-- 警报（紧急） -->
<div role="alert" aria-live="assertive">
  <!-- 内容更新将立即中断当前语音播报 -->
</div>

<!-- 进度更新 -->
<div
  role="progressbar"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
></div>

<!-- 日志（仅添加） -->
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- 新消息会被播报，移除不会 -->
</div>
```

### 3. 选项卡界面

```html
<div role="tablist" aria-label="Product information">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">
    Description
  </button>
  <button
    role="tab"
    id="tab-2"
    aria-selected="false"
    aria-controls="panel-2"
    tabindex="-1"
  >
    Reviews
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Product description content...
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Reviews content...
</div>
```

```javascript
// 选项卡键盘导航
tablist.addEventListener("keydown", (e) => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const index = tabs.indexOf(document.activeElement);

  let newIndex;
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

  tabs[newIndex].focus();
  activateTab(tabs[newIndex]);
  e.preventDefault();
});
```

## 调试技巧

```javascript
// 记录屏幕阅读器看到的内容
function logAccessibleName(element) {
  const computed = window.getComputedStyle(element);
  console.log({
    role: element.getAttribute("role") || element.tagName,
    name:
      element.getAttribute("aria-label") ||
      element.getAttribute("aria-labelledby") ||
      element.textContent,
    state: {
      expanded: element.getAttribute("aria-expanded"),
      selected: element.getAttribute("aria-selected"),
      checked: element.getAttribute("aria-checked"),
      disabled: element.disabled,
    },
    visible: computed.display !== "none" && computed.visibility !== "hidden",
  });
}
```

## 最佳实践

### 应该做的

- **使用实际屏幕阅读器测试** - 不仅仅是模拟器
- **优先使用语义化 HTML** - ARIA 是补充
- **在浏览模式和焦点模式下测试** - 不同的体验
- **验证焦点管理** - 特别是对于 SPA
- **首先进行仅键盘测试** - 屏幕阅读器测试的基础

### 不应该做的

- **不要假设一个屏幕阅读器就足够了** - 测试多个
- **不要忽略移动端** - 用户群体在不断增长
- **不要只测试正常路径** - 测试错误状态
- **不要跳过动态内容** - 最常见的问题
- **不要依赖视觉测试** - 不同的体验

## 资源

- [VoiceOver 用户指南](https://support.apple.com/guide/voiceover/welcome/mac)
- [NVDA 用户指南](https://www.nvaccess.org/files/nvda/documentation/userGuide.html)
- [JAWS 文档](https://support.freedomscientific.com/Products/Blindness/JAWS)
- [WebAIM 屏幕阅读器调查](https://webaim.org/projects/screenreadersurvey/)
