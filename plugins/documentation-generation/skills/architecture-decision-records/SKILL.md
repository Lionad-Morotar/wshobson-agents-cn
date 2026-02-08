---
name: architecture-decision-records
description: 遵循技术决策文档最佳实践编写和维护架构决策记录（ADR）。用于记录重大技术决策、审查过去的架构选择或建立决策流程。
---

# 架构决策记录

用于创建、维护和管理架构决策记录（ADR）的综合模式，记录重大技术决策的上下文和理由。

## 何时使用此技能

- 做出重大架构决策
- 记录技术选择
- 记录设计权衡
- 新团队成员入职
- 审查历史决策
- 建立决策流程

## 核心概念

### 1. 什么是 ADR？

架构决策记录捕获：

- **上下文**：为什么我们需要做出决策
- **决策**：我们决定了什么
- **后果**：因此发生什么

### 2. 何时编写 ADR

| 编写 ADR                  | 跳过 ADR               |
| -------------------------- | ---------------------- |
| 新框架采用                 | 次要版本升级           |
| 数据库技术选择             | Bug 修复               |
| API 设计模式               | 实现细节               |
| 安全架构                   | 常规维护               |
| 集成模式                   | 配置更改               |

### 3. ADR 生命周期

```
提议 → 已接受 → 已弃用 → 已取代
              ↓
           已拒绝
```

## 模板

### 模板 1：标准 ADR（MADR 格式）

```markdown
# ADR-0001: 使用 PostgreSQL 作为主数据库

## 状态

已接受

## 上下文

我们需要为新的电子商务平台选择主数据库。系统将处理：

- 约 10,000 个并发用户
- 具有分层类别的复杂产品目录
- 订单和支付的交易处理
- 产品的全文搜索
- 商店定位器的地理空间查询

团队对 MySQL、PostgreSQL 和 MongoDB 有经验。我们需要对金融交易进行 ACID 合规。

## 决策驱动因素

- **必须有 ACID 合规性**用于支付处理
- **必须支持复杂查询**用于报告
- **应支持全文搜索**以减少基础设施复杂性
- **应有良好的 JSON 支持**用于灵活的产品属性
- **团队熟悉度**减少入职时间

## 考虑的选项

### 选项 1：PostgreSQL

- **优点**：ACID 合规、出色的 JSON 支持（JSONB）、内置全文搜索、PostGIS 用于地理空间、团队有经验
- **缺点**：复制设置比 MySQL 稍微复杂

### 选项 2：MySQL

- **优点**：团队非常熟悉、简单的复制、大型社区
- **缺点**：JSON 支持较弱、没有内置全文搜索（需要 Elasticsearch）、没有扩展的地理空间功能

### 选项 3：MongoDB

- **优点**：灵活的模式、原生 JSON、水平扩展
- **缺点**：多文档交易没有 ACID（在决策时）、团队经验有限、需要模式设计纪律

## 决策

我们将使用 **PostgreSQL 15** 作为主数据库。

## 理由

PostgreSQL 提供了以下方面的最佳平衡：

1. **ACID 合规性**对电子商务交易至关重要
2. **内置功能**（全文搜索、JSONB、PostGIS）减少基础设施复杂性
3. **团队熟悉度**SQL 数据库减少学习曲线
4. **成熟的生态系统**具有出色的工具和社区支持

复制的轻微复杂性被减少的额外服务（不需要单独的 Elasticsearch）所抵消。

## 后果

### 积极影响

- 单个数据库处理交易、搜索和地理空间查询
- 减少运营复杂性（管理的服务更少）
- 财务数据的强一致性保证
- 团队可以利用现有的 SQL 专业知识

### 消极影响

- 需要学习 PostgreSQL 特定功能（JSONB、全文搜索语法）
- 垂直扩展限制可能需要更早的读取副本
- 一些团队成员需要 PostgreSQL 特定培训

### 风险

- 全文搜索可能不如专用搜索引擎扩展
- 缓解措施：设计以在需要时添加 Elasticsearch

## 实现说明

- 使用 JSONB 用于灵活的产品属性
- 使用 PgBouncer 实现连接池
- 设置流复制用于读取副本
- 使用 pg_trgm 扩展进行模糊搜索

## 相关决策

- ADR-0002：缓存策略（Redis）- 补充数据库选择
- ADR-0005：搜索架构 - 如果需要 Elasticsearch 可能会取代

## 参考

- [PostgreSQL JSON 文档](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL 全文搜索](https://www.postgresql.org/docs/current/textsearch.html)
- 内部：`/docs/benchmarks/database-comparison.md` 中的性能基准
```

### 模板 2：轻量级 ADR

```markdown
# ADR-0012: 采用 TypeScript 进行前端开发

**状态**：已接受
**日期**：2024-01-15
**决策者**：@alice, @bob, @charlie

## 上下文

我们的 React 代码库已增长到 50+ 个组件，与 prop 类型不匹配和未定义错误相关的 bug 报告不断增加。PropTypes 仅提供运行时检查。

## 决策

为所有新前端代码采用 TypeScript。逐步迁移现有代码。

## 后果

**好**：在编译时捕获类型错误、更好的 IDE 支持、自文档化代码。

**坏**：团队的学习曲线、初始减速、构建复杂性增加。

**缓解措施**：TypeScript 培训会议、允许通过 `allowJs: true` 逐步采用。
```

### 模板 3：Y 语句格式

```markdown
# ADR-0015：API 网关选择

在 **构建微服务架构** 的上下文中，
面临 **集中式 API 管理、身份验证和速率限制的需求**，
我们决定选择 **Kong Gateway**
而反对 **AWS API Gateway 和自定义 Nginx 解决方案**，
以实现 **供应商独立性、插件可扩展性和团队对 Lua 的熟悉度**，
接受 **我们需要自己管理 Kong 基础设施** 的事实。
```

### 模板 4：弃用的 ADR

```markdown
# ADR-0020：弃用 MongoDB 并改用 PostgreSQL

## 状态

已接受（取代 ADR-0003）

## 上下文

ADR-0003（2021）由于模式灵活性需求选择 MongoDB 用于用户配置文件存储。自那时起：

- MongoDB 的多文档交易对我们的用例仍然有问题
- 我们的模式已稳定，很少变化
- 我们现在拥有来自其他服务的 PostgreSQL 专业知识
- 维护两个数据库增加了运营负担

## 决策

弃用 MongoDB 并将用户配置文件迁移到 PostgreSQL。

## 迁移计划

1. **阶段 1**（第 1-2 周）：创建 PostgreSQL 模式，启用双写
2. **阶段 2**（第 3-4 周）：回填历史数据，验证一致性
3. **阶段 3**（第 5 周）：将读取切换到 PostgreSQL，监控
4. **阶段 4**（第 6 周）：删除 MongoDB 写入，停用

## 后果

### 积极影响

- 单一数据库技术减少运营复杂性
- 用户数据的 ACID 交易
- 团队可以专注于 PostgreSQL 专业知识

### 消极影响

- 迁移工作（约 4 周）
- 迁移期间数据问题的风险
- 失去一些模式灵活性

## 经验教训

从 ADR-0003 经验中记录：

- 模式灵活性的好处被高估了
- 多个数据库的运营成本被低估了
- 在技术决策中考虑长期维护
```

### 模板 5：请求评论（RFC）样式

```markdown
# RFC-0025：采用事件溯源进行订单管理

## 摘要

提议在订单管理领域采用事件溯源模式，以提高可审计性、启用时间查询并支持业务分析。

## 动机

当前的挑战：

1. 审计要求需要完整的订单历史
2. "订单在时间 X 的状态是什么？"查询是不可能的
3. 分析团队需要事件流用于实时仪表板
4. 客户支持的订单状态重建是手动的

## 详细设计

### 事件存储
```

OrderCreated { orderId, customerId, items[], timestamp }
OrderItemAdded { orderId, item, timestamp }
OrderItemRemoved { orderId, itemId, timestamp }
PaymentReceived { orderId, amount, paymentId, timestamp }
OrderShipped { orderId, trackingNumber, timestamp }

```

### 投影

- **CurrentOrderState**：用于查询的物化视图
- **OrderHistory**：用于审计的完整时间线
- **DailyOrderMetrics**：分析聚合

### 技术

- 事件存储：EventStoreDB（专用，处理投影）
- 考虑的替代方案：Kafka + 自定义投影服务

## 缺点

- 团队的学习曲线
- 与 CRUD 相比复杂性增加
- 需要仔细设计事件（一旦存储就不可变）
- 存储增长（事件永不删除）

## 替代方案

1. **审计表**：更简单但不能启用时间查询
2. **从现有数据库进行 CDC**：复杂，不改变数据模型
3. **混合**：仅订单状态更改的事件源

## 未解决的问题

- [ ] 事件模式版本控制策略
- [ ] 事件的保留策略
- [ ] 用于性能的快照频率

## 实现计划

1. 使用单一订单类型进行原型（2 周）
2. 团队事件溯源培训（1 周）
3. 完整实现和迁移（4 周）
4. 监控和优化（持续进行）

## 参考

- [Martin Fowler 的事件溯源](https://martinfowler.com/eaaDev/EventSourcing.html)
- [EventStoreDB 文档](https://www.eventstore.com/docs)
```

## ADR 管理

### 目录结构

```
docs/
├── adr/
│   ├── README.md           # 索引和指南
│   ├── template.md         # 团队的 ADR 模板
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [已弃用]
│   └── 0020-deprecate-mongodb.md      # 取代 0003
```

### ADR 索引（README.md）

```markdown
# 架构决策记录

此目录包含 [项目名称] 的架构决策记录（ADR）。

## 索引

| ADR                                   | 标题                              | 状态       | 日期       |
| ------------------------------------- | --------------------------------- | ---------- | ---------- |
| [0001](0001-use-postgresql.md)        | 使用 PostgreSQL 作为主数据库      | 已接受     | 2024-01-10 |
| [0002](0002-caching-strategy.md)      | 使用 Redis 的缓存策略             | 已接受     | 2024-01-12 |
| [0003](0003-mongodb-user-profiles.md) | MongoDB 用于用户配置文件          | 已弃用     | 2023-06-15 |
| [0020](0020-deprecate-mongodb.md)     | 弃用 MongoDB                      | 已接受     | 2024-01-15 |

## 创建新 ADR

1. 将 `template.md` 复制为 `NNNN-title-with-dashes.md`
2. 填写模板
3. 提交 PR 进行审查
4. 批准后更新此索引

## ADR 状态

- **提议**：正在讨论
- **已接受**：已做出决策，正在实施
- **已弃用**：不再相关
- **已取代**：被另一个 ADR 替换
- **已拒绝**：已考虑但未采用
```

### 自动化（adr-tools）

```bash
# 安装 adr-tools
brew install adr-tools

# 初始化 ADR 目录
adr init docs/adr

# 创建新 ADR
adr new "使用 PostgreSQL 作为主数据库"

# 取代 ADR
adr new -s 3 "弃用 MongoDB 并改用 PostgreSQL"

# 生成目录
adr generate toc > docs/adr/README.md

# 链接相关 ADR
adr link 2 "补充" 1 "被补充"
```

## 审查流程

```markdown
## ADR 审查清单

### 提交前

- [ ] 上下文清楚地解释了问题
- [ ] 考虑了所有可行的选项
- [ ] 优点/缺点平衡且诚实
- [ ] 后果（积极和消极）已记录
- [ ] 相关 ADR 已链接

### 审查期间

- [ ] 至少 2 名高级工程师审查
- [ ] 受影响的团队已咨询
- [ ] 已考虑安全影响
- [ ] 已记录成本影响
- [ ] 已评估可逆性

### 接受后

- [ ] ADR 索引已更新
- [ ] 团队已通知
- [ ] 已创建实施票据
- [ ] 相关文档已更新
```

## 最佳实践

### 应该做的

- **尽早编写 ADR** - 在实施开始之前
- **保持简短** - 最多 1-2 页
- **诚实对待权衡** - 包括真正的缺点
- **链接相关决策** - 构建决策图
- **更新状态** - 被取代时弃用

### 不应该做的

- **不要更改已接受的 ADR** - 编写新的来取代
- **不要跳过上下文** - 未来的读者需要背景
- **不要隐藏失败** - 被拒绝的决策很有价值
- **不要含糊** - 具体的决策，具体的后果
- **不要忘记实施** - 没有行动的 ADR 是浪费

## 资源

- [记录架构决策 (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR 模板](https://adr.github.io/madr/)
- [ADR GitHub 组织](https://adr.github.io/)
- [adr-tools](https://github.com/npryce/adr-tools)
