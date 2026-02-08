---
name: git-advanced-workflows
description: 掌握高级 Git 工作流程，包括变基、拣选、二分查找、工作树和引用日志，以维护干净的历史记录并从任何情况中恢复。在管理复杂的 Git 历史、在功能分支上协作或排查仓库问题时使用。
---

# Git 高级工作流程

掌握高级 Git 技术，以维护干净的历史记录、有效协作，并充满信心地从任何情况中恢复。

## 何时使用此技能

- 在合并前清理提交历史
- 跨分支应用特定提交
- 查找引入错误的提交
- 同时处理多个功能
- 从 Git 错误或丢失的提交中恢复
- 管理复杂的分支工作流程
- 为评审准备干净的 PR
- 同步已分叉的分支

## 核心概念

### 1. 交互式变基

交互式变基是 Git 历史编辑的瑞士军刀。

**常用操作：**

- `pick`：保持原样
- `reword`：更改提交消息
- `edit`：修改提交内容
- `squash`：与前一个提交合并
- `fixup`：类似 squash 但丢弃消息
- `drop`：完全删除提交

**基本用法：**

```bash
# 变基最近 5 个提交
git rebase -i HEAD~5

# 变基当前分支上的所有提交
git rebase -i $(git merge-base HEAD main)

# 变基到特定提交
git rebase -i abc123
```

### 2. 拣选提交

将特定提交从一个分支应用到另一个分支，而无需合并整个分支。

```bash
# 拣选单个提交
git cherry-pick abc123

# 拣选一系列提交（不包括起始）
git cherry-pick abc123..def456

# 拣选而不提交（仅暂存更改）
git cherry-pick -n abc123

# 拣选并编辑提交消息
git cherry-pick -e abc123
```

### 3. Git 二分查找

通过提交历史进行二分查找，以查找引入错误的提交。

```bash
# 开始二分
git bisect start

# 标记当前提交为坏
git bisect bad

# 标记已知的好提交
git bisect good v1.0.0

# Git 将检出中间提交 - 测试它
# 然后标记为好或坏
git bisect good  # 或：git bisect bad

# 继续直到找到错误
# 完成后
git bisect reset
```

**自动二分：**

```bash
# 使用脚本自动测试
git bisect start HEAD v1.0.0
git bisect run ./test.sh

# test.sh 应为好退出 0，为坏退出 1-127（125 除外）
```

### 4. 工作树

同时在多个分支上工作，而无需储藏或切换。

```bash
# 列出现有工作树
git worktree list

# 为功能分支添加新工作树
git worktree add ../project-feature feature/new-feature

# 添加工作树并创建新分支
git worktree add -b bugfix/urgent ../project-hotfix main

# 删除工作树
git worktree remove ../project-feature

# 清理过期的工作树
git worktree prune
```

### 5. 引用日志

您的安全网 - 跟踪所有引用移动，甚至包括已删除的提交。

```bash
# 查看引用日志
git reflog

# 查看特定分支的引用日志
git reflog show feature/branch

# 恢复已删除的提交
git reflog
# 找到提交哈希
git checkout abc123
git branch recovered-branch

# 恢复已删除的分支
git reflog
git branch deleted-branch abc123
```

## 实用工作流程

### 工作流程 1：在 PR 之前清理功能分支

```bash
# 从功能分支开始
git checkout feature/user-auth

# 交互式变基以清理历史
git rebase -i main

# 示例变基操作：
# - 压缩"修复拼写错误"提交
# - 重写提交消息以获得清晰度
# - 按逻辑重新排序提交
# - 删除不必要的提交

# 强制推送清理的分支（如果没有其他人使用，则是安全的）
git push --force-with-lease origin feature/user-auth
```

### 工作流程 2：将热修复应用到多个版本

```bash
# 在 main 上创建修复
git checkout main
git commit -m "fix: critical security patch"

# 应用到版本分支
git checkout release/2.0
git cherry-pick abc123

git checkout release/1.9
git cherry-pick abc123

# 处理冲突（如果出现）
git cherry-pick --continue
# 或
git cherry-pick --abort
```

### 工作流程 3：查找错误引入

```bash
# 开始二分
git bisect start
git bisect bad HEAD
git bisect good v2.1.0

# Git 检出中间提交 - 运行测试
npm test

# 如果测试失败
git bisect bad

# 如果测试通过
git bisect good

# Git 将自动检出下一个要测试的提交
# 重复直到找到错误

# 自动版本
git bisect start HEAD v2.1.0
git bisect run npm test
```

### 工作流程 4：多分支开发

```bash
# 主项目目录
cd ~/projects/myapp

# 为紧急热修复创建工作树
git worktree add ../myapp-hotfix hotfix/critical-bug

# 在单独的目录中处理热修复
cd ../myapp-hotfix
# 进行更改，提交
git commit -m "fix: resolve critical bug"
git push origin hotfix/critical-bug

# 返回主工作而不中断
cd ~/projects/myapp
git fetch origin
git cherry-pick hotfix/critical-bug

# 完成后清理
git worktree remove ../myapp-hotfix
```

### 工作流程 5：从错误中恢复

```bash
# 意外重置到错误的提交
git reset --hard HEAD~5  # 哎呀！

# 使用引用日志查找丢失的提交
git reflog
# 输出显示：
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: my important changes

# 恢复丢失的提交
git reset --hard def456

# 或从丢失的提交创建分支
git branch recovery def456
```

## 高级技术

### 变基 vs 合并策略

**何时变基：**

- 在推送前清理本地提交
- 保持功能分支与 main 同步
- 创建线性历史以获得更轻松的评审

**何时合并：**

- 将完成的功能集成到 main
- 保留协作的确切历史
- 其他人使用的公共分支

```bash
# 使用 main 更改更新功能分支（变基）
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# 处理冲突
git status
# 修复文件中的冲突
git add .
git rebase --continue

# 或改为合并
git merge origin/main
```

### 自动压缩工作流程

在变基期间自动压缩 fixup 提交。

```bash
# 进行初始提交
git commit -m "feat: add user authentication"

# 稍后，修复该提交中的某些内容
# 暂存更改
git commit --fixup HEAD  # 或指定提交哈希

# 进行更多更改
git commit --fixup abc123

# 使用自动压缩变基
git rebase -i --autosquash main

# Git 自动标记 fixup 提交
```

### 拆分提交

将一个提交拆分为多个逻辑提交。

```bash
# 开始交互式变基
git rebase -i HEAD~3

# 用 'edit' 标记要拆分的提交
# Git 将在该提交处停止

# 重置提交但保持更改
git reset HEAD^

# 按逻辑块暂存和提交
git add file1.py
git commit -m "feat: add validation"

git add file2.py
git commit -m "feat: add error handling"

# 继续变基
git rebase --continue
```

### 部分拣选

仅从提交中拣选特定文件。

```bash
# 显示提交中的文件
git show --name-only abc123

# 从提交中检出特定文件
git checkout abc123 -- path/to/file1.py path/to/file2.py

# 暂存和提交
git commit -m "cherry-pick: apply specific changes from abc123"
```

## 最佳实践

1. **始终使用 --force-with-lease**：比 --force 更安全，防止覆盖他人的工作
2. **仅变基本地提交**：不要变基已推送和共享的提交
3. **描述性提交消息**：未来的您会感谢现在的您
4. **原子提交**：每个提交应该是单个逻辑更改
5. **强制推送前测试**：确保历史重写没有破坏任何内容
6. **保持引用日志意识**：记住引用日志是 90 天的安全网
7. **在风险操作前创建分支**：在复杂变基前创建备份分支

```bash
# 安全强制推送
git push --force-with-lease origin feature/branch

# 在风险操作前创建备份
git branch backup-branch
git rebase -i main
# 如果出现问题
git reset --hard backup-branch
```

## 常见陷阱

- **变基公共分支**：导致协作者的历史冲突
- **不使用 Lease 强制推送**：可能覆盖队友的工作
- **在变基中丢失工作**：仔细解决冲突，变基后测试
- **忘记工作树清理**：孤立的工作树消耗磁盘空间
- **实验前不备份**：始终创建安全分支
- **在脏工作目录上二分**：在二分前提交或储藏

## 恢复命令

```bash
# 中止正在进行的操作
git rebase --abort
git merge --abort
git cherry-pick --abort
git bisect reset

# 将文件恢复到特定提交的版本
git restore --source=abc123 path/to/file

# 撤消最后一个提交但保留更改
git reset --soft HEAD^

# 撤消最后一个提交并放弃更改
git reset --hard HEAD^

# 恢复已删除的分支（90 天内）
git reflog
git branch recovered-branch abc123
```

## 资源

- **references/git-rebase-guide.md**：深入交互式变基
- **references/git-conflict-resolution.md**：高级冲突解决策略
- **references/git-history-rewriting.md**：安全地重写 Git 历史
- **assets/git-workflow-checklist.md**：PR 前清理清单
- **assets/git-aliases.md**：高级工作流程的有用 Git 别名
- **scripts/git-clean-branches.sh**：清理已合并和过期的分支
