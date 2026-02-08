---
description: "创建包含详细规范和分阶段实施计划的新 track"
argument-hint: "<feature|bug|chore|refactor> <名称>"
---

# 新建 Track

创建一个新的 track（功能、bug 修复、杂务或重构），包含详细规范和分阶段实施计划。

## 飞行前检查

1. 验证 Conductor 已初始化：
   - 检查 `conductor/product.md` 是否存在
   - 检查 `conductor/tech-stack.md` 是否存在
   - 检查 `conductor/workflow.md` 是否存在
   - 如果缺失：显示错误并建议先运行 `/conductor:setup`

2. 加载上下文文件：
   - 读取 `conductor/product.md` 获取产品上下文
   - 读取 `conductor/tech-stack.md` 获取技术上下文
   - 读取 `conductor/workflow.md` 获取 TDD/提交偏好

## Track 分类

根据描述确定 track 类型或询问用户：

```
这是什么类型的 track？

1. Feature（功能）- 新功能
2. Bug（缺陷）- 现有问题的修复
3. Chore（杂务）- 维护、依赖项、配置
4. Refactor（重构）- 不改变行为的代码改进
```

## 交互式规范收集

**关键规则：**

- 每次只问一个问题
- 等待用户响应后再继续
- 根据 track 类型定制问题
- 最多 6 个问题

### 功能类 Track

**Q1: 功能摘要**

```
用 1-2 句话描述该功能。
[如果提供了参数，确认："您想要：{参数}。这正确吗？"]
```

**Q2: 用户故事**

```
谁将从中受益以及如何受益？

格式：作为[用户类型]，我想要[操作]以便[收益]。
```

**Q3: 验收标准**

```
该功能完成必须满足什么条件？

列出 3-5 个验收标准（每行一个）：
```

**Q4: 依赖关系**

```
这是否依赖于任何现有代码、API 或其他 track？

1. 无依赖
2. 依赖于现有代码（请说明）
3. 依赖于未完成的 track（请说明）
```

**Q5: 范围边界**

```
该 track 明确排除哪些内容？
（有助于防止范围蔓延）
```

**Q6: 技术考量（可选）**

```
是否有特定的技术方法或约束？
（按回车键跳过）
```

### 缺陷类 Track

**Q1: 缺陷摘要**

```
什么地方有问题？
[如果提供了参数，进行确认]
```

**Q2: 复现步骤**

```
如何复现这个 bug？
列出步骤：
```

**Q3: 预期与实际行为**

```
应该发生什么与实际发生了什么？
```

**Q4: 受影响区域**

```
系统的哪些部分受到影响？
```

**Q5: 根本原因假设（可选）**

```
对原因有任何假设吗？
（按回车键跳过）
```

### 杂务/重构类 Track

**Q1: 任务摘要**

```
需要做什么？
[如果提供了参数，进行确认]
```

**Q2: 动机**

```
为什么需要这项工作？
```

**Q3: 成功标准**

```
我们如何知道这是否完成？
```

**Q4: 风险评估**

```
可能出现什么问题？有哪些有风险的变更？
```

## Track ID 生成

生成格式为 `{shortname}_{YYYYMMDD}` 的 track ID：

- 从功能/bug 摘要中提取短名称（2-3 个词，小写，连字符分隔）
- 使用当前日期
- 示例：`user-auth_20250115`、`nav-bug_20250115`

验证唯一性：

- 检查 `conductor/tracks.md` 中是否已存在该 ID
- 如果冲突，追加计数器：`user-auth_20250115_2`

## 规范生成

创建 `conductor/tracks/{trackId}/spec.md`：

```markdown
# 规范：{Track 标题}

**Track ID：** {trackId}
**类型：** {Feature|Bug|Chore|Refactor}
**创建时间：** {YYYY-MM-DD}
**状态：** 草稿

## 摘要

{1-2 句话摘要}

## 上下文

{与该 track 相关的 product.md 中的产品上下文}

## 用户故事（针对功能）

作为{用户}，我想要{操作}以便{收益}。

## 问题描述（针对缺陷）

{Bug 描述、复现步骤}

## 验收标准

- [ ] {标准 1}
- [ ] {标准 2}
- [ ] {标准 3}

## 依赖关系

{列出依赖项或"无"}

## 超出范围

{明确排除的内容}

## 技术说明

{技术考量或"未指定"}

---

_由 Conductor 生成。请根据需要审查和编辑。_
```

## 用户审查规范

显示生成的规范并询问：

```
这是我生成的规范：

{规范内容}

此规范是否正确？
1. 是的，继续生成计划
2. 不，让我编辑（打开内联编辑）
3. 使用不同的输入重新开始
```

## 计划生成

规范批准后，生成 `conductor/tracks/{trackId}/plan.md`：

### 计划结构

```markdown
# 实施计划：{Track 标题}

**Track ID：** {trackId}
**规范：** [spec.md](./spec.md)
**创建时间：** {YYYY-MM-DD}
**状态：** [ ] 未开始

## 概述

{实施方法简要摘要}

## 阶段 1：{阶段名称}

{阶段描述}

### 任务

- [ ] 任务 1.1：{描述}
- [ ] 任务 1.2：{描述}
- [ ] 任务 1.3：{描述}

### 验证

- [ ] {阶段 1 的验证步骤}

## 阶段 2：{阶段名称}

{阶段描述}

### 任务

- [ ] 任务 2.1：{描述}
- [ ] 任务 2.2：{描述}

### 验证

- [ ] {阶段 2 的验证步骤}

## 阶段 3：{阶段名称}（如果需要）

...

## 最终验证

- [ ] 满足所有验收标准
- [ ] 测试通过
- [ ] 文档已更新（如适用）
- [ ] 准备好审查

---

_由 Conductor 生成。任务将标记为 [~] 进行中，[x] 已完成。_
```

### 阶段指南

- 将相关任务分组到逻辑阶段中
- 每个阶段应可独立验证
- 在每个阶段后包含验证任务
- TDD track：在实施任务之前包含测试编写任务
- 典型结构：
  1. **设置/基础** - 初始脚手架、接口
  2. **核心实施** - 主要功能
  3. **集成** - 与现有系统连接
  4. **完善** - 错误处理、边界情况、文档

## 用户审查计划

显示生成的计划并询问：

```
这是实施计划：

{计划内容}

此计划是否正确？
1. 是的，创建 track
2. 不，让我编辑（打开内联编辑）
3. 添加更多阶段/任务
4. 重新开始
```

## Track 创建

计划批准后：

1. 创建目录结构：

   ```
   conductor/tracks/{trackId}/
   ├── spec.md
   ├── plan.md
   ├── metadata.json
   └── index.md
   ```

2. 创建 `metadata.json`：

   ```json
   {
     "id": "{trackId}",
     "title": "{Track 标题}",
     "type": "feature|bug|chore|refactor",
     "status": "pending",
     "created": "ISO_TIMESTAMP",
     "updated": "ISO_TIMESTAMP",
     "phases": {
       "total": N,
       "completed": 0
     },
     "tasks": {
       "total": M,
       "completed": 0
     }
   }
   ```

3. 创建 `index.md`：

   ```markdown
   # Track：{Track 标题}

   **ID：** {trackId}
   **状态：** 待处理

   ## 文档

   - [规范](./spec.md)
   - [实施计划](./plan.md)

   ## 进度

   - 阶段：0/{N} 已完成
   - 任务：0/{M} 已完成

   ## 快速链接

   - [返回到 Tracks](../../tracks.md)
   - [产品上下文](../../product.md)
   ```

4. 在 `conductor/tracks.md` 中注册：
   - 在 tracks 表格中添加一行
   - 格式：`| [ ] | {trackId} | {标题} | {创建日期} | {创建日期} |`

5. 更新 `conductor/index.md`：
   - 将 track 添加到"活跃 Tracks"部分

## 完成消息

```
Track 创建成功！

Track ID：{trackId}
位置：conductor/tracks/{trackId}/

已创建的文件：
- spec.md - 需求规范
- plan.md - 分阶段实施计划
- metadata.json - Track 元数据
- index.md - Track 导航

下一步：
1. 审查 spec.md 和 plan.md，进行任何编辑
2. 运行 /conductor:implement {trackId} 开始实施
3. 运行 /conductor:status 查看项目进度
```

## 错误处理

- 如果目录创建失败：停止并报告，不要在 tracks.md 中注册
- 如果任何文件写入失败：清理部分 track，报告错误
- 如果 tracks.md 更新失败：警告用户手动注册 track
