# Conductor 中心

## 项目：{{PROJECT_NAME}}

所有 Conductor 工件和开发 tracks 的中央导航。

## 快速链接

### 核心文档

| 文档                                      | 描述                | 状态     |
| --------------------------------------------- | -------------------------- | ---------- |
| [产品愿景](./product.md)                | 产品概览和目标 | {{STATUS}} |
| [产品指南](./product-guidelines.md) | 语气、语调和标准 | {{STATUS}} |
| [技术栈](./tech-stack.md)                 | 技术决策       | {{STATUS}} |
| [工作流程](./workflow.md)                     | 开发流程        | {{STATUS}} |

### Track 管理

| 文档                        | 描述            |
| ------------------------------- | ---------------------- |
| [Track 注册表](./tracks.md)   | 所有开发 tracks |
| [活跃 Tracks](#active-tracks) | 当前进行中  |

### 风格指南

| 指南                                          | 语言/域           |
| ---------------------------------------------- | ------------------------- |
| [通用](./code_styleguides/general.md)       | 通用原则      |
| [TypeScript](./code_styleguides/typescript.md) | TypeScript 约定    |
| [JavaScript](./code_styleguides/javascript.md) | JavaScript 最佳实践 |
| [Python](./code_styleguides/python.md)         | Python 标准          |
| [Go](./code_styleguides/go.md)                 | Go 惯用语                 |
| [C#](./code_styleguides/csharp.md)             | C# 约定            |
| [Dart](./code_styleguides/dart.md)             | Dart/Flutter 模式     |
| [HTML/CSS](./code_styleguides/html-css.md)     | Web 标准             |

## 活跃 Tracks

| Track          | 状态     | 优先级     | 规范                                  | 计划                                  |
| -------------- | ---------- | ------------ | ------------------------------------- | ------------------------------------- |
| {{TRACK_NAME}} | {{STATUS}} | {{PRIORITY}} | [规范](./tracks/{{TRACK_ID}}/spec.md) | [计划](./tracks/{{TRACK_ID}}/plan.md) |

## 最近活动

| 日期     | Track     | 操作     |
| -------- | --------- | ---------- |
| {{DATE}} | {{TRACK}} | {{ACTION}} |

## 项目状态

**当前阶段：** {{CURRENT_PHASE}}
**总体进度：** {{PROGRESS_PERCENTAGE}}%

### 里程碑跟踪器

| 里程碑       | 目标日期 | 状态       |
| --------------- | ----------- | ------------ |
| {{MILESTONE_1}} | {{DATE_1}}  | {{STATUS_1}} |
| {{MILESTONE_2}} | {{DATE_2}}  | {{STATUS_2}} |
| {{MILESTONE_3}} | {{DATE_3}}  | {{STATUS_3}} |

## 入门指南

1. 查看 [产品愿景](./product.md) 了解项目上下文
2. 查看 [技术栈](./tech-stack.md) 了解技术决策
3. 阅读 [工作流程](./workflow.md) 了解开发流程
4. 在 [Track 注册表](./tracks.md) 中找到您的 track
5. 按照 track 规范和计划进行

## 命令参考

```bash
# 设置
{{SETUP_COMMAND}}

# 开发
{{DEV_COMMAND}}

# 测试
{{TEST_COMMAND}}

# 构建
{{BUILD_COMMAND}}
```

---

**最后更新：** {{LAST_UPDATED}}
**维护者：** {{MAINTAINER}}
