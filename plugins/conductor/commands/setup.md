---
description: "使用 Conductor 工件初始化项目（产品定义、技术栈、工作流程、风格指南）"
argument-hint: "[--resume]"
---

# Conductor 设置

初始化或恢复 Conductor 项目设置。此命令通过交互式问答创建基础项目文档。

## 飞行前检查

1. 检查项目根目录中是否已存在 `conductor/` 目录：
   - 如果 `conductor/product.md` 存在：询问用户是恢复设置还是重新初始化
   - 如果 `conductor/setup_state.json` 存在且状态未完成：提供从上一步恢复的选项

2. 通过检查现有指标来检测项目类型：
   - **绿地项目（新建项目）**：无 .git、无 package.json、无 requirements.txt、无 go.mod、无 src/ 目录
   - **棕地项目（现有项目）**：以上任何一项存在

3. 加载或创建 `conductor/setup_state.json`：
   ```json
   {
     "status": "in_progress",
     "project_type": "greenfield|brownfield",
     "current_section": "product|guidelines|tech_stack|workflow|styleguides",
     "current_question": 1,
     "completed_sections": [],
     "answers": {},
     "files_created": [],
     "started_at": "ISO_TIMESTAMP",
     "last_updated": "ISO_TIMESTAMP"
   }
   ```

## 交互式问答协议

**关键规则：**

- 每次只问一个问题
- 等待用户响应后再继续
- 提供 2-3 个建议答案以及"输入您自己的"选项
- 每个部分最多 5 个问题
- 在每个成功步骤后更新 `setup_state.json`
- 验证文件写入成功后再继续

### 第 1 部分：产品定义（最多 5 个问题）

**Q1: 项目名称**

```
您的项目名称是什么？

建议：
1. [从目录名称推断]
2. [从 package.json/go.mod 推断，如果是棕地项目]
3. 输入您自己的
```

**Q2: 项目描述**

```
用一句话描述您的项目。

建议：
1. 一个[做 X]的 Web 应用程序
2. 一个用于[做 Y]的 CLI 工具
3. 输入您自己的
```

**Q3: 问题陈述**

```
这个项目解决了什么问题？

建议：
1. 用户很难[痛点]
2. 没有[需求]的好方法
3. 输入您自己的
```

**Q4: 目标用户**

```
主要的用户是谁？

建议：
1. 构建 [X] 的开发者
2. 需要 [Y] 的最终用户
3. 管理 [Z] 的内部团队
4. 输入您自己的
```

**Q5: 关键目标（可选）**

```
这个项目的 2-3 个关键目标是什么？（按回车键跳过）
```

### 第 2 部分：产品指南（最多 3 个问题）

**Q1: 语气和语调**

```
文档和 UI 文本应使用什么语气/语调？

建议：
1. 专业和技术性
2. 友好和平易近人
3. 简洁直接
4. 输入您自己的
```

**Q2: 设计原则**

```
什么设计原则指导这个项目？

建议：
1. 简单胜于功能
2. 性能优先
3. 专注开发者体验
4. 用户安全和可靠性
5. 输入您自己的（逗号分隔）
```

### 第 3 部分：技术栈（最多 5 个问题）

对于**棕地项目**，首先分析现有代码：

- 运行 `Glob` 查找 package.json、requirements.txt、go.mod、Cargo.toml 等
- 解析检测到的文件以预填充技术栈
- 展示发现并请求确认/补充

**Q1: 主要语言**

```
这个项目使用什么主要语言？

[对于棕地项目："我检测到：Python 3.11、JavaScript。这正确吗？"]

建议：
1. TypeScript
2. Python
3. Go
4. Rust
5. 输入您自己的（逗号分隔）
```

**Q2: 前端框架（如适用）**

```
使用什么前端框架（如果有）？

建议：
1. React
2. Vue
3. Next.js
4. 无 / 仅 CLI
5. 输入您自己的
```

**Q3: 后端框架（如适用）**

```
使用什么后端框架（如果有）？

建议：
1. Express / Fastify
2. Django / FastAPI
3. Go 标准库
4. 无 / 仅前端
5. 输入您自己的
```

**Q4: 数据库（如适用）**

```
使用什么数据库（如果有）？

建议：
1. PostgreSQL
2. MongoDB
3. SQLite
4. 无 / 无状态
5. 输入您自己的
```

**Q5: 基础设施**

```
这将部署在哪里？

建议：
1. AWS（Lambda、ECS 等）
2. Vercel / Netlify
3. 自托管 / Docker
4. 尚未决定
5. 输入您自己的
```

### 第 4 部分：工作流程偏好（最多 4 个问题）

**Q1: TDD 严格度**

```
应该多严格地执行 TDD？

建议：
1. 严格 - 实施前需要测试
2. 适中 - 鼓励测试，不强制
3. 灵活 - 仅对复杂逻辑推荐测试
```

**Q2: 提交策略**

```
应该遵循什么提交策略？

建议：
1. 约定式提交（feat:、fix: 等）
2. 描述性消息，不需要格式
3. 每个任务合并提交
```

**Q3: 代码审查要求**

```
什么代码审查策略？

建议：
1. 所有更改都需要
2. 非平凡更改需要
3. 可选 / 自我审查即可
```

**Q4: 验证检查点**

```
什么时候应该需要手动验证？

建议：
1. 每个阶段完成后
2. 每个任务完成后
3. 仅在 track 完成时
```

### 第 5 部分：代码风格指南（最多 2 个问题）

**Q1: 要包含的语言**

```
应该生成哪些语言的风格指南？

[基于检测到的语言预选]

选项：
1. TypeScript/JavaScript
2. Python
3. Go
4. Rust
5. 所有检测到的语言
6. 跳过风格指南
```

**Q2: 现有约定**

```
您有要纳入的现有 linting/格式化配置吗？

[对于棕地项目："我找到了 .eslintrc、.prettierrc。我应该纳入这些吗？"]

建议：
1. 是的，使用现有配置
2. 不，生成新的指南
3. 跳过此步骤
```

## 工件生成

完成问答后，生成以下文件：

### 1. conductor/index.md

```markdown
# Conductor - [项目名称]

项目上下文的导航中心。

## 快速链接

- [产品定义](./product.md)
- [产品指南](./product-guidelines.md)
- [技术栈](./tech-stack.md)
- [工作流程](./workflow.md)
- [Tracks](./tracks.md)

## 活跃 Tracks

<!-- 由 /conductor:new-track 自动填充 -->

## 入门

运行 `/conductor:new-track` 创建您的第一个功能 track。
```

### 2. conductor/product.md

使用问答答案填充的模板：

- 项目名称和描述
- 问题陈述
- 目标用户
- 关键目标

### 3. conductor/product-guidelines.md

使用以下内容填充的模板：

- 语气和语调
- 设计原则
- 任何附加标准

### 4. conductor/tech-stack.md

使用以下内容填充的模板：

- 语言（如果检测到，包含版本）
- 框架（前端、后端）
- 数据库
- 基础设施
- 关键依赖（对于棕地项目，从包文件）

### 5. conductor/workflow.md

使用以下内容填充的模板：

- TDD 策略和严格度级别
- 提交策略和约定
- 代码审查要求
- 验证检查点规则
- 任务生命周期定义

### 6. conductor/tracks.md

```markdown
# Tracks 注册表

| 状态 | Track ID | 标题 | 创建时间 | 更新时间 |
| ---- | -------- | ---- | -------- | -------- |

<!-- 由 /conductor:new-track 注册的 tracks -->
```

### 7. conductor/code_styleguides/

从 `$CLAUDE_PLUGIN_ROOT/templates/code_styleguides/` 生成选定的风格指南

## 状态管理

每次成功创建文件后：

1. 更新 `setup_state.json`：
   - 将文件名添加到 `files_created` 数组
   - 更新 `last_updated` 时间戳
   - 如果部分完成，添加到 `completed_sections`
2. 使用 `Read` 工具验证文件存在

## 完成

创建所有文件后：

1. 将 `setup_state.json` 状态设置为 "complete"
2. 显示摘要：

   ```
   Conductor 设置完成！

   已创建的工件：
   - conductor/index.md
   - conductor/product.md
   - conductor/product-guidelines.md
   - conductor/tech-stack.md
   - conductor/workflow.md
   - conductor/tracks.md
   - conductor/code_styleguides/[语言]

   下一步：
   1. 审查生成的文件并根据需要进行自定义
   2. 运行 /conductor:new-track 创建您的第一个 track
   ```

## 恢复处理

如果使用 `--resume` 参数或从状态恢复：

1. 加载 `setup_state.json`
2. 跳过已完成的部分
3. 从 `current_section` 和 `current_question` 恢复
4. 验证先前创建的文件仍然存在
5. 如果文件缺失，提供重新生成的选项

## 错误处理

- 如果文件写入失败：停止并报告错误，不更新状态
- 如果用户取消：保存当前状态以供将来恢复
- 如果状态文件损坏：提供重新开始或尝试恢复
