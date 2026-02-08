# 多平台功能开发工作流

使用 API 优先架构和并行实现策略在 Web、移动和桌面平台上一致地构建和部署相同功能。

[扩展思考:此工作流编排多个专业智能体以确保跨平台功能对等,同时维护平台特定优化。协调策略强调共享合同和具有定期同步点的并行开发。通过预先建立 API 合同和数据模型,团队可以独立工作同时确保一致性。工作流优势包括更快的上市时间、减少集成问题和可维护的跨平台代码库。]

## 阶段 1：架构和 API 设计（顺序）

### 1. 定义功能需求和 API 合同

- 使用 Task 工具，subagent_type="backend-architect"
- 提示："设计功能的 API 合同：$ARGUMENTS。创建 OpenAPI 3.1 规范，包括：
  - 具有适当 HTTP 方法和状态码的 RESTful 端点
  - 用于复杂数据查询的 GraphQL 模式（如适用）
  - 用于实时功能的 WebSocket 事件
  - 具有验证规则的请求/响应模式
  - 认证和授权要求
  - 速率限制和缓存策略
  - 错误响应格式和代码
    定义所有平台将使用的共享数据模型。"
- 预期输出：完整 API 规范、数据模型和集成指南

### 2. 设计系统和 UI/UX 一致性

- 使用 Task 工具，subagent_type="ui-ux-designer"
- 提示："使用 API 规范为功能创建跨平台设计系统：[上一个输出]。包括：
  - 每个平台的组件规范（Material Design、iOS HIG、Fluent）
  - Web 的响应式布局（移动优先方法）
  - iOS (SwiftUI) 和 Android (Material You) 的原生模式
  - 桌面特定考虑（键盘快捷键、窗口管理）
  - 辅助功能要求（WCAG 2.2 级别 AA）
  - 深/浅主题规范
  - 动画和过渡指南"
- 来自上一个的上下文：API 端点、数据结构、认证流程
- 预期输出：设计系统文档、组件库规范、平台指南

### 3. 共享业务逻辑架构

- 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
- 提示："设计跨平台功能的共享业务逻辑架构。定义：
  - 核心领域模型和实体（平台不可知）
  - 业务规则和验证逻辑
  - 状态管理模式（MVI/Redux/BLoC）
  - 缓存和离线策略
  - 错误处理和重试策略
  - 平台特定适配器模式
    考虑用于移动的 Kotlin Multiplatform 或用于 Web/桌面共享的 TypeScript。"
- 来自上一个的上下文：API 合同、数据模型、UI 要求
- 预期输出：共享代码架构、平台抽象层、实现指南

## 阶段 2：并行平台实现

### 4a. Web 实现 (React/Next.js)

- 使用 Task 工具，subagent_type="frontend-developer"
- 提示："使用以下工具实现 Web 版本的功能：
  - React 18+ 和 Next.js 14+ App Router
  - TypeScript 用于类型安全
  - TanStack Query 用于 API 集成：[API 规范]
  - Zustand/Redux Toolkit 用于状态管理
  - 使用设计系统的 Tailwind CSS：[设计规范]
  - 渐进式 Web 应用能力
  - 适当的时候使用 SSR/SSG 优化
  - Web 核心指标优化（LCP < 2.5s、FID < 100ms）
    遵循共享业务逻辑：[架构文档]"
- 来自上一个的上下文：API 合同、设计系统、共享逻辑模式
- 预期输出：具有测试的完整 Web 实现

### 4b. iOS 实现 (SwiftUI)

- 使用 Task 工具，subagent_type="ios-developer"
- 提示："使用以下工具实现 iOS 版本：
  - 具有 iOS 17+ 功能的 SwiftUI
  - Swift 5.9+ 和 async/await
  - 使用 Combine 的 URLSession 用于 API：[API 规范]
  - Core Data/SwiftData 用于持久化
  - 设计系统合规：[iOS HIG 规范]
  - 小部件扩展（如适用）
  - 平台特定功能（Face ID、触觉、Live Activities）
  - 可测试的 MVVM 架构
    遵循共享模式：[架构文档]"
- 来自上一个的上下文：API 合同、iOS 设计指南、共享模型
- 预期输出：具有单元/UI 测试的原生 iOS 实现

### 4c. Android 实现 (Kotlin/Compose)

- 使用 Task 工具，subagent_type="mobile-developer"
- 提示："使用以下工具实现 Android 版本：
  - Jetpack Compose 和 Material 3
  - Kotlin 协程和 Flow
  - Retrofit/Ktor 用于 API：[API 规范]
  - Room 数据库用于本地存储
  - Hilt 用于依赖注入
  - Material You 动态主题：[设计规范]
  - 平台功能（生物识别认证、小部件）
  - 使用 MVI 模式的整洁架构
    遵循共享逻辑：[架构文档]"
- 来自上一个的上下文：API 合同、Material Design 规范、共享模式
- 预期输出：具有测试的原生 Android 实现

### 4d. 桌面实现（可选 - Electron/Tauri）

- 使用 Task 工具，subagent_type="frontend-mobile-development::frontend-developer"
- 提示："使用 Tauri 2.0 或 Electron 实现桌面版本：
  - 尽可能共享 Web 代码库
  - 原生 OS 集成（系统托盘、通知）
  - 文件系统访问（如需要）
  - 自动更新功能
  - 代码签名和公证设置
  - 键盘快捷键和菜单栏
  - 多窗口支持（如适用）
    重用 Web 组件：[Web 实现]"
- 来自上一个的上下文：Web 实现、桌面特定要求
- 预期输出：具有平台包的桌面应用

## 阶段 3：集成和验证

### 5. API 文档和测试

- 使用 Task 工具，subagent_type="documentation-generation::api-documenter"
- 提示："创建全面的 API 文档，包括：
  - 交互式 OpenAPI/Swagger 文档
  - 平台特定集成指南
  - 每个平台的 SDK 示例
  - 认证流程图
  - 速率限制和配额信息
  - Postman/Insomnia 集合
  - WebSocket 连接示例
  - 错误处理最佳实践
  - API 版本控制策略
    使用平台实现测试所有端点。"
- 来自上一个的上下文：已实现的平台、API 使用模式
- 预期输出：完整的 API 文档门户、测试结果

### 6. 跨平台测试和功能对等

- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示："验证所有平台的功能对等性：
  - 功能测试矩阵（功能工作相同）
  - UI 一致性验证（遵循设计系统）
  - 每个平台的性能基准
  - 辅助功能测试（平台特定工具）
  - 网络弹性测试（离线、慢连接）
  - 数据同步验证
  - 平台特定边缘情况
  - 端到端用户旅程测试
    创建具有任何平台差异的测试报告。"
- 来自上一个的上下文：所有平台实现、API 文档
- 预期输出：测试报告、对等矩阵、性能指标

### 7. 平台特定优化

- 使用 Task 工具，subagent_type="application-performance::performance-engineer"
- 提示："优化每个平台实现：
  - Web：包大小、延迟加载、CDN 设置、SEO
  - iOS：应用大小、启动时间、内存使用、电池
  - Android：APK 大小、启动时间、帧率、电池
  - 桌面：二进制大小、资源使用、启动时间
  - API：响应时间、缓存、压缩
    在利用平台优势的同时维护功能对等性。
    记录优化技术和权衡。"
- 来自上一个的上下文：测试结果、性能指标
- 预期输出：优化的实现、性能改进

## 配置选项

- **--platforms**: 指定目标平台（web、ios、android、desktop）
- **--api-first**: 在 UI 实现之前生成 API（默认：true）
- **--shared-code**: 使用 Kotlin Multiplatform 或类似（默认：evaluate）
- **--design-system**: 使用现有或创建新的（默认：create）
- **--testing-strategy**: 单元、集成、e2e（默认：all）

## 成功标准

- 在实现之前定义并验证 API 合同
- 所有平台实现功能对等，差异 <5%
- 性能指标满足平台特定标准
- 满足辅助功能标准（WCAG 2.2 AA 最低）
- 跨平台测试显示一致行为
- 所有平台的文档完整
- 适用平台间代码重用 >40%
- 为每个平台的约定优化用户体验

## 平台特定考虑

**Web**：PWA 能力、SEO 优化、浏览器兼容性
**iOS**：App Store 指南、TestFlight 分发、iOS 特定功能
**Android**：Play Store 要求、Android App Bundles、设备碎片化
**Desktop**：代码签名、自动更新、OS 特定安装程序

初始功能规范：$ARGUMENTS
