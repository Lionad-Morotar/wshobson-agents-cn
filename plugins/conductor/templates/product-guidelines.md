# 产品指南

## 语音与语调

### 品牌语音

{{BRAND_VOICE_DESCRIPTION}}

### 语音属性

- **{{ATTRIBUTE_1}}：** {{ATTRIBUTE_1_DESCRIPTION}}
- **{{ATTRIBUTE_2}}：** {{ATTRIBUTE_2_DESCRIPTION}}
- **{{ATTRIBUTE_3}}：** {{ATTRIBUTE_3_DESCRIPTION}}

### 按上下文变化的语调

| 上下文        | 语调                 | 示例                 |
| -------------- | -------------------- | ----------------------- |
| 成功状态 | {{SUCCESS_TONE}}     | {{SUCCESS_EXAMPLE}}     |
| 错误状态   | {{ERROR_TONE}}       | {{ERROR_EXAMPLE}}       |
| 入门指南     | {{ONBOARDING_TONE}}  | {{ONBOARDING_EXAMPLE}}  |
| 空状态   | {{EMPTY_STATE_TONE}} | {{EMPTY_STATE_EXAMPLE}} |

### 我们使用的词汇

- {{PREFERRED_WORD_1}}
- {{PREFERRED_WORD_2}}
- {{PREFERRED_WORD_3}}

### 我们避免的词汇

- {{AVOIDED_WORD_1}}
- {{AVOIDED_WORD_2}}
- {{AVOIDED_WORD_3}}

## 消息传递指南

### 核心消息

**主要消息：**

> {{PRIMARY_MESSAGE}}

**支持消息：**

1. {{SUPPORTING_MESSAGE_1}}
2. {{SUPPORTING_MESSAGE_2}}
3. {{SUPPORTING_MESSAGE_3}}

### 消息层次

1. **必须传达：** {{MUST_COMMUNICATE}}
2. **应该传达：** {{SHOULD_COMMUNICATE}}
3. **可以传达：** {{COULD_COMMUNICATE}}

### 特定受众的消息传递

| 受众       | 关键消息   | 证明点 |
| -------------- | ------------- | ------------ |
| {{AUDIENCE_1}} | {{MESSAGE_1}} | {{PROOF_1}}  |
| {{AUDIENCE_2}} | {{MESSAGE_2}} | {{PROOF_2}}  |

## 设计原则

### 原则 1：{{PRINCIPLE_1_NAME}}

{{PRINCIPLE_1_DESCRIPTION}}

**应该做：**

- {{PRINCIPLE_1_DO_1}}
- {{PRINCIPLE_1_DO_2}}

**不应该做：**

- {{PRINCIPLE_1_DONT_1}}
- {{PRINCIPLE_1_DONT_2}}

### 原则 2：{{PRINCIPLE_2_NAME}}

{{PRINCIPLE_2_DESCRIPTION}}

**应该做：**

- {{PRINCIPLE_2_DO_1}}
- {{PRINCIPLE_2_DO_2}}

**不应该做：**

- {{PRINCIPLE_2_DONT_1}}
- {{PRINCIPLE_2_DONT_2}}

### 原则 3：{{PRINCIPLE_3_NAME}}

{{PRINCIPLE_3_DESCRIPTION}}

**应该做：**

- {{PRINCIPLE_3_DO_1}}
- {{PRINCIPLE_3_DO_2}}

**不应该做：**

- {{PRINCIPLE_3_DONT_1}}
- {{PRINCIPLE_3_DONT_2}}

## 无障碍标准

### 合规目标

{{ACCESSIBILITY_STANDARD}}（例如 WCAG 2.1 AA）

### 核心要求

#### 可感知

- 所有图像都有有意义的替代文本
- 颜色不是传达信息的唯一手段
- 文本的最小对比度比例为 4.5:1
- 内容在 200% 缩放时可读

#### 可操作

- 所有功能均可通过键盘使用
- 没有内容每秒闪烁超过 3 次
- 提供跳过导航链接
- 焦点指示器清晰可见

#### 可理解

- 语言清晰简单
- 导航一致
- 错误消息具有描述性和帮助性
- 标签和说明清晰

#### 健壮

- 有效的 HTML 标记
- 适当使用 ARIA 标签
- 与辅助技术兼容
- 渐进增强方法

### 测试要求

- 使用 {{SCREEN_READER}} 进行屏幕阅读器测试
- 仅键盘导航测试
- 颜色对比度验证
- 自动化无障碍扫描

## 错误处理理念

### 错误预防

- 尽早并频繁地验证输入
- 提前提供明确的约束和要求
- 在适当的地方使用内联验证
- 确认破坏性操作

### 错误传达

#### 原则

1. **具体：** 准确告诉用户出了什么问题
2. **有帮助：** 解释如何解决问题
3. **人性化：** 使用友好的、非技术性语言
4. **及时：** 检测到错误后立即显示

#### 错误消息结构

```
[发生了什么] + [为什么发生（如相关）] + [如何修复]
```

#### 示例

| 糟糕             | 良好                                                 |
| --------------- | ---------------------------------------------------- |
| "无效输入" | "电子邮件地址必须包含 @ 符号"                |
| "错误 500"     | "我们无法保存您的更改。请再试一次。"   |
| "失败"        | "无法连接。请检查您的互联网连接。" |

### 错误状态

| 严重性 | 视觉处理       | 需要用户操作 |
| -------- | ---------------------- | -------------------- |
| 信息     | {{INFO_TREATMENT}}     | 可选             |
| 警告  | {{WARNING_TREATMENT}}  | 推荐          |
| 错误    | {{ERROR_TREATMENT}}    | 必需             |
| 严重 | {{CRITICAL_TREATMENT}} | 立即            |

### 恢复模式

- 尽可能自动保存用户进度
- 提供清晰的"重试"操作
- 当主要操作失败时提供替代路径
- 在错误时保留用户输入
