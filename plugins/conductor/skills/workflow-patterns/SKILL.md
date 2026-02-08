---
name: workflow-patterns
description: 使用此技能来按照 Conductor 的 TDD 工作流程实施任务、处理阶段检查点、管理任务的 git 提交或理解验证协议。
version: 1.0.0
---

# 工作流程模式

使用 Conductor 的 TDD 工作流程实施任务、管理阶段检查点、处理 git 提交和执行验证协议以确保实施质量的指南。

## 何时使用此技能

- 从 track 的 plan.md 实施任务
- 遵循 TDD 红绿重构循环
- 完成阶段检查点
- 管理 git 提交和注释
- 理解质量保证门
- 处理验证协议
- 在计划文件中记录进度

## TDD 任务生命周期

为每个任务遵循这 11 个步骤：

### 步骤 1：选择下一个任务

阅读 plan.md 并识别下一个待处理 `[ ]` 任务。在当前阶段内按顺序选择任务。不要跳到后面的阶段。

### 步骤 2：标记为进行中

更新 plan.md 将任务标记为 `[~]`：

```markdown
- [~] **任务 2.1**：实施用户验证
```

将此状态更改与实施分开提交。

### 步骤 3：RED - 编写失败测试

在编写实施之前编写定义预期行为的测试：

- 如需要则创建测试文件
- 编写覆盖正常路径的测试用例
- 编写覆盖边缘情况的测试用例
- 编写覆盖错误条件的测试用例
- 运行测试 - 它们应该失败

示例：

```python
def test_validate_user_email_valid():
    user = User(email="test@example.com")
    assert user.validate_email() is True

def test_validate_user_email_invalid():
    user = User(email="invalid")
    assert user.validate_email() is False
```

### 步骤 4：GREEN - 实施最少代码

编写使测试通过所需的最少代码：

- 专注于使测试变绿，而不是完美
- 避免过早优化
- 保持实施简单
- 运行测试 - 它们应该通过

### 步骤 5：REFACTOR - 改进清晰度

在测试变绿的情况下，改进代码：

- 提取通用模式
- 改进命名
- 删除重复
- 简化逻辑
- 每次更改后运行测试 - 它们应保持变绿

### 步骤 6：验证覆盖率

检查测试覆盖率是否达到 80% 目标：

```bash
pytest --cov=module --cov-report=term-missing
```

如果覆盖率低于 80%：

- 识别未覆盖的行
- 为缺失路径添加测试
- 重新运行覆盖率检查

### 步骤 7：记录偏差

如果实施偏离计划或引入新依赖：

- 使用新依赖更新 tech-stack.md
- 在 plan.md 任务注释中记录偏差
- 如果需求更改，更新 spec.md

### 步骤 8：提交实施

为任务创建聚焦的提交：

```bash
git add -A
git commit -m "feat(user): implement email validation

- Add validate_email method to User class
- Handle empty and malformed emails
- Add comprehensive test coverage

Task: 2.1
Track: user-auth_20250115"
```

提交消息格式：

- 类型：feat、fix、refactor、test、docs、chore
- 范围：受影响的模块或组件
- 摘要：祈使句，现在时态
- 正文：更改的要点
- 页脚：任务和 track 引用

### 步骤 9：附加 Git 注释

添加丰富的任务摘要作为 git 注释：

```bash
git notes add -m "Task 2.1: Implement user validation

Summary:
- Added email validation using regex pattern
- Handles edge cases: empty, no @, no domain
- Coverage: 94% on validation module

Files changed:
- src/models/user.py (modified)
- tests/test_user.py (modified)

Decisions:
- Used simple regex over email-validator library
- Reason: No external dependency for basic validation"
```

### 步骤 10：使用 SHA 更新计划

更新 plan.md 标记任务完成并附带提交 SHA：

```markdown
- [x] **任务 2.1**：实施用户验证 `abc1234`
```

### 步骤 11：提交计划更新

提交计划状态更新：

```bash
git add conductor/tracks/*/plan.md
git commit -m "docs: update plan - task 2.1 complete

Track: user-auth_20250115"
```

## 阶段完成协议

当阶段中的所有任务完成时，执行验证协议：

### 识别已更改的文件

列出自上次检查点以来修改的所有文件：

```bash
git diff --name-only <last-checkpoint-sha>..HEAD
```

### 确保测试覆盖率

对于每个修改的文件：

1. 识别相应的测试文件
2. 验证新/更改代码的测试存在
3. 为修改的模块运行覆盖率
4. 如果覆盖率 < 80%，添加测试

### 运行完整测试套件

执行完整测试套件：

```bash
pytest -v --tb=short
```

所有测试必须在继续之前通过。

### 生成手动验证步骤

创建手动验证清单：

```markdown
## 阶段 1 验证清单

- [ ] 用户可以使用有效电子邮件注册
- [ ] 无效电子邮件显示适当的错误
- [ ] 数据库正确存储用户
- [ ] API 返回预期的响应代码
```

### 等待用户批准

向用户展示验证清单：

```
阶段 1 完成。请验证：
1. [ ] 测试套件通过（自动）
2. [ ] 覆盖率满足目标（自动）
3. [ ] 手动验证项目（需要人工）

回复 'approved' 以继续，或记录问题。
```

未经明确批准不得继续。

### 创建检查点提交

批准后，创建检查点提交：

```bash
git add -A
git commit -m "checkpoint: phase 1 complete - user-auth_20250115

Verified:
- All tests passing
- Coverage: 87%
- Manual verification approved

Phase 1 tasks:
- [x] Task 1.1: Setup database schema
- [x] Task 1.2: Implement user model
- [x] Task 1.3: Add validation logic"
```

### 记录检查点 SHA

更新 plan.md 检查点表：

```markdown
## 检查点

| 阶段   | 检查点 SHA | 日期       | 状态   |
| ------- | -------------- | ---------- | -------- |
| 阶段 1 | def5678        | 2025-01-15 | verified |
| 阶段 2 |                |            | pending  |
```

## 质量保证门

在标记任何任务完成之前，验证这些门：

### 通过的测试

- 所有现有测试通过
- 新测试通过
- 没有测试回归

### 覆盖率 >= 80%

- 新代码有 80%+ 覆盖率
- 保持整体项目覆盖率
- 关键路径完全覆盖

### 风格合规

- 代码遵循风格指南
- Linting 通过
- 格式正确

### 文档

- 公共 API 已记录
- 解释了复杂逻辑
- 如需要则更新 README

### 类型安全

- 存在类型提示（如适用）
- 类型检查器通过
- 没有原因的 `type: ignore`

### 无 Linting 错误

- 零 linter 错误
- 已解决或证明警告合理
- 静态分析干净

### 移动兼容性

如适用：

- 验证响应式设计
- 触摸交互有效
- 性能可接受

### 安全审计

- 代码中没有秘密
- 存在输入验证
- 身份验证/授权正确
- 依赖项无漏洞

## Git 集成

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：

- `feat`：新功能
- `fix`：Bug 修复
- `refactor`：没有功能/修复的代码更改
- `test`：添加测试
- `docs`：文档
- `chore`：维护

### Git 注释用于丰富摘要

向提交附加详细注释：

```bash
git notes add -m "<detailed summary>"
```

查看注释：

```bash
git log --show-notes
```

好处：

- 在不杂乱提交消息的情况下保留上下文
- 启用跨提交的语义查询
- 支持基于 track 的操作

### 在 plan.md 中记录 SHA

完成任务时始终记录提交 SHA：

```markdown
- [x] **任务 1.1**：设置模式 `abc1234`
- [x] **任务 1.2**：添加模型 `def5678`
```

这实现：

- 从计划到代码的可追溯性
- 语义撤销操作
- 进度审计

## 验证检查点

### 为什么检查点很重要

检查点为语义撤销创建恢复点：

- 撤销到任何阶段的结束
- 维护逻辑代码状态
- 启用安全实验

### 何时创建检查点

在以下情况后创建检查点：

- 所有阶段任务完成
- 所有阶段验证通过
- 收到用户批准

### 检查点提交内容

在检查点提交中包括：

- 所有未提交的更改
- 更新的 plan.md
- 更新的 metadata.json
- 任何文档更新

### 如何使用检查点

用于撤销：

```bash
# 撤销到阶段 1 结束
git revert --no-commit <phase-2-commits>...
git commit -m "revert: rollback to phase 1 checkpoint"
```

用于审查：

```bash
# 查看阶段 2 中更改的内容
git diff <phase-1-sha>..<phase-2-sha>
```

## 处理偏差

在实施期间，可能会发生偏离计划的情况。系统地处理它们：

### 偏差类型

**范围增加**

发现原始规范中未包含的需求。

- 在 spec.md 中记录为新需求
- 将任务添加到 plan.md
- 在任务注释中记录增加

**范围减少**

实施期间被认为不必要的功能。

- 使用原因将任务标记为 `[-]`（已跳过）
- 更新 spec.md 范围部分
- 记录决策理由

**技术偏差**

与计划不同的实施方法。

- 在任务完成注释中记录偏差
- 如果依赖更改，更新 tech-stack.md
- 记录为什么原始方法不合适

**需求变更**

工作期间对需求的理解发生变化。

- 使用更正的需求更新 spec.md
- 如需要则调整 plan.md 任务
- 重新验证验收标准

### 偏差文档格式

完成有偏差的任务时：

```markdown
- [x] **任务 2.1**：实施验证 `abc1234`
  - DEVIATION: 使用库而不是自定义代码
  - Reason: 更好的边缘情况处理
  - Impact: 将 email-validator 添加到依赖
```

## 错误恢复

### GREEN 后测试失败

如果在达到 GREEN 后测试失败：

1. 不要继续到 REFACTOR
2. 识别哪个测试开始失败
3. 检查重构是否破坏了某些东西
4. 恢复到最后已知的 GREEN 状态
5. 重新接近实施

### 检查点被拒绝

如果用户拒绝检查点：

1. 在 plan.md 中记录拒绝原因
2. 创建解决问题的任务
3. 完成补救任务
4. 再次请求检查点批准

### 被依赖阻塞

如果任务无法继续：

1. 使用阻塞描述将任务标记为 `[!]`
2. 检查其他任务是否可以继续
3. 记录预期解决时间表
4. 考虑创建依赖解决 track

## 按任务类型的 TDD 变体

### 数据模型任务

```
RED: 编写模型创建和验证的测试
GREEN: 实施具有字段的模型类
REFACTOR: 添加计算属性，改进类型
```

### API 端点任务

```
RED: 编写请求/响应契约的测试
GREEN: 实施端点处理程序
REFACTOR: 提取验证，改进错误处理
```

### 集成任务

```
RED: 编写组件交互的测试
GREEN: 将组件连接在一起
REFACTOR: 改进错误传播，添加日志记录
```

### 重构任务

```
RED: 为当前行为添加表征测试
GREEN: 应用重构（测试应保持变绿）
REFACTOR: 清理引入的任何复杂性
```

## 使用现有测试

修改具有现有测试的代码时：

### 扩展，不要替换

- 保持现有测试通过
- 为新行为添加新测试
- 仅在需求更改时更新测试

### 测试迁移

当重构改变测试结构时：

1. 运行现有测试（应通过）
2. 为重构代码添加新测试
3. 将测试用例迁移到新结构
4. 仅在新测试通过后删除旧测试

### 回归预防

任何更改后：

1. 运行完整测试套件
2. 检查意外失败
3. 调查任何新失败
4. 在继续之前修复回归

## 检查点验证详细信息

### 自动验证

在请求批准之前运行：

```bash
# 测试套件
pytest -v --tb=short

# 覆盖率
pytest --cov=src --cov-report=term-missing

# Linting
ruff check src/ tests/

# 类型检查（如适用）
mypy src/
```

### 手动验证指导

对于手动项目，提供具体说明：

```markdown
## 手动验证步骤

### 用户注册

1. 导航到 /register
2. 输入有效电子邮件：test@example.com
3. 输入满足要求的密码
4. 点击提交
5. 验证成功消息出现
6. 验证用户出现在数据库中

### 错误处理

1. 输入无效电子邮件："notanemail"
2. 验证错误消息显示
3. 验证表单保留其他输入的数据
```

## 性能考虑

### 测试套件性能

保持测试套件快速：

- 使用夹具避免冗余设置
- 模拟缓慢的外部调用
- 在开发期间运行子集，在检查点运行完整套件

### 提交性能

保持提交原子性：

- 每个提交一个逻辑更改
- 完整的想法，而不是进行中
- 每次提交后测试应通过

## 最佳实践

1. **永远不要跳过 RED**：始终先编写失败测试
2. **小提交**：每个提交一个逻辑更改
3. **立即更新**：任务完成后立即更新 plan.md
4. **等待批准**：永远不要跳过检查点验证
5. **丰富的 git 注释**：包含有助于未来理解的上下文
6. **覆盖率纪律**：不接受低于目标的覆盖率
7. **质量门**：在标记完成之前检查所有门
8. **顺序阶段**：按顺序完成阶段
9. **记录偏差**：记录与原始计划的任何更改
10. **干净状态**：每个提交应使代码处于工作状态
11. **快速反馈**：在开发期间频繁运行相关测试
12. **清晰的阻塞项**：及时解决阻塞项，不要绕过它们
