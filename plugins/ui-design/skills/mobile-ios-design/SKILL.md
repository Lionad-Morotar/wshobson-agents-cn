---
name: mobile-ios-design
description: Master iOS Human Interface Guidelines and SwiftUI patterns for building native iOS apps. Use when designing iOS interfaces, implementing SwiftUI views, or ensuring apps follow Apple's design principles.
---

# iOS 移动设计

掌握 iOS 人机界面设计指南（HIG）和 SwiftUI 模式，构建精致的原生 iOS 应用程序，使其在 Apple 平台上如鱼得水。

## 使用此技能的场景

- 按照 Apple HIG 设计 iOS 应用界面
- 构建 SwiftUI 视图和布局
- 实现 iOS 导航模式（NavigationStack、TabView、sheets）
- 为 iPhone 和 iPad 创建自适应布局
- 使用 SF Symbols 和系统字体
- 构建无障碍 iOS 界面
- 实现 iOS 特定的手势和交互
- 为动态字体和深色模式设计

## 核心概念

### 1. 人机界面设计指南原则

**清晰度**：内容清晰可读，图标精确，装饰元素含蓄
**谦逊**：UI 帮助用户理解内容，而不是与之竞争
**深度**：视觉层次和运动传达层级结构并支持导航

**平台考虑：**

- **iOS**：触摸优先，紧凑显示屏，竖屏方向
- **iPadOS**：更大画布，多任务处理，指针支持
- **visionOS**：空间计算，眼/手输入

### 2. SwiftUI 布局系统

**基于堆栈的布局：**

```swift
// 带对齐的垂直堆栈
VStack(alignment: .leading, spacing: 12) {
    Text("Title")
        .font(.headline)
    Text("Subtitle")
        .font(.subheadline)
        .foregroundStyle(.secondary)
}

// 带灵活间距的水平堆栈
HStack {
    Image(systemName: "star.fill")
    Text("Featured")
    Spacer()
    Text("View All")
        .foregroundStyle(.blue)
}
```

**网格布局：**

```swift
// 填充可用宽度的自适应网格
LazyVGrid(columns: [
    GridItem(.adaptive(minimum: 150, maximum: 200))
], spacing: 16) {
    ForEach(items) { item in
        ItemCard(item: item)
    }
}

// 固定列网格
LazyVGrid(columns: [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
], spacing: 12) {
    ForEach(items) { item in
        ItemThumbnail(item: item)
    }
}
```

### 3. 导航模式

**NavigationStack（iOS 16+）：**

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
        }
    }
}
```

**TabView：**

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
        }
    }
}
```

### 4. 系统集成

**SF Symbols：**

```swift
// 基本符号
Image(systemName: "heart.fill")
    .foregroundStyle(.red)

// 带渲染模式的符号
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.multicolor)

// 可变符号（iOS 16+）
Image(systemName: "speaker.wave.3.fill", variableValue: volume)

// 符号效果（iOS 17+）
Image(systemName: "bell.fill")
    .symbolEffect(.bounce, value: notificationCount)
```

**动态字体：**

```swift
// 使用语义字体
Text("Headline")
    .font(.headline)

Text("Body text that scales with user preferences")
    .font(.body)

// 尊重动态字体的自定义字体
Text("Custom")
    .font(.custom("Avenir", size: 17, relativeTo: .body))
```

### 5. 视觉设计

**颜色和材质：**

```swift
// 适应浅色/深色模式的语义颜色
Text("Primary")
    .foregroundStyle(.primary)
Text("Secondary")
    .foregroundStyle(.secondary)

// 用于模糊效果的系统材质
Rectangle()
    .fill(.ultraThinMaterial)
    .frame(height: 100)

// 用于叠加层的鲜艳材质
Text("Overlay")
    .padding()
    .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
```

**阴影和深度：**

```swift
// 标准卡片阴影
RoundedRectangle(cornerRadius: 16)
    .fill(.background)
    .shadow(color: .black.opacity(0.1), radius: 8, y: 4)

// 升起外观
.shadow(radius: 2, y: 1)
.shadow(radius: 8, y: 4)
```

## 快速入门组件

```swift
import SwiftUI

struct FeatureCard: View {
    let title: String
    let description: String
    let systemImage: String

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: systemImage)
                .font(.title)
                .foregroundStyle(.blue)
                .frame(width: 44, height: 44)
                .background(.blue.opacity(0.1), in: Circle())

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                Text(description)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .foregroundStyle(.tertiary)
        }
        .padding()
        .background(.background, in: RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 4, y: 2)
    }
}
```

## 最佳实践

1. **使用语义颜色**：始终使用 `.primary`、`.secondary`、`.background` 以自动支持浅色/深色模式
2. **拥抱 SF Symbols**：使用系统符号以获得一致性和自动无障碍性
3. **支持动态字体**：使用语义字体（`.body`、`.headline`）而不是固定大小
4. **添加无障碍性**：包含 `.accessibilityLabel()` 和 `.accessibilityHint()` 修饰符
5. **使用安全区域**：尊重 `safeAreaInset`，避免在屏幕边缘硬编码内边距
6. **实现状态恢复**：使用 `@SceneStorage` 保留用户状态
7. **支持 iPad 多任务处理**：为分屏视图和侧拉设计
8. **在设备上测试**：模拟器无法捕捉完整的触觉和性能体验

## 常见问题

- **布局破坏**：谨慎使用 `.fixedSize()`；优先使用灵活布局
- **性能问题**：对长滚动列表使用 `LazyVStack`/`LazyHStack`
- **导航错误**：确保 `NavigationLink` 值是 `Hashable` 的
- **深色模式问题**：避免硬编码颜色；使用语义或资源目录颜色
- **无障碍性失败**：启用 VoiceOver 进行测试
- **内存泄漏**：注意闭包中的强引用循环

## 资源

- [人机界面设计指南](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftUI 文档](https://developer.apple.com/documentation/swiftui)
- [SF Symbols 应用](https://developer.apple.com/sf-symbols/)
- [WWDC SwiftUI 会议](https://developer.apple.com/videos/swiftui/)
