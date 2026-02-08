# iOS 人机交互指南模式

## 布局和间距

### 标准边距和内边距

```swift
// 系统标准边距
private let standardMargin: CGFloat = 16
private let compactMargin: CGFloat = 8
private let largeMargin: CGFloat = 24

// 遵循 HIG 的内容内边距
extension EdgeInsets {
    static let standard = EdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
    static let listRow = EdgeInsets(top: 12, leading: 16, bottom: 12, trailing: 16)
    static let card = EdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
}
```

### 安全区域处理

```swift
struct SafeAreaAwareView: View {
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 16) {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
            .padding(.horizontal)
        }
        .safeAreaInset(edge: .bottom) {
            // 浮动操作区域
            HStack {
                Button("取消") { }
                    .buttonStyle(.bordered)
                Spacer()
                Button("确认") { }
                    .buttonStyle(.borderedProminent)
            }
            .padding()
            .background(.regularMaterial)
        }
    }
}
```

### 自适应布局

```swift
struct AdaptiveGridView: View {
    @Environment(\.horizontalSizeClass) private var sizeClass

    private var columns: [GridItem] {
        switch sizeClass {
        case .compact:
            return [GridItem(.flexible())]
        case .regular:
            return [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ]
        default:
            return [GridItem(.flexible())]
        }
    }

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(items) { item in
                    ItemCard(item: item)
                }
            }
            .padding()
        }
    }
}
```

## 字体层级

### 系统字体样式

```swift
// 符合 HIG 的字体比例
struct Typography {
    // 标题
    static let largeTitle = Font.largeTitle.weight(.bold)      // 34pt 粗体
    static let title = Font.title.weight(.semibold)            // 28pt 半粗体
    static let title2 = Font.title2.weight(.semibold)          // 22pt 半粗体
    static let title3 = Font.title3.weight(.semibold)          // 20pt 半粗体

    // 标题和正文
    static let headline = Font.headline                         // 17pt 半粗体
    static let body = Font.body                                 // 17pt 常规
    static let callout = Font.callout                          // 16pt 常规

    // 辅助文本
    static let subheadline = Font.subheadline                  // 15pt 常规
    static let footnote = Font.footnote                        // 13pt 常规
    static let caption = Font.caption                          // 12pt 常规
    static let caption2 = Font.caption2                        // 11pt 常规
}
```

### 支持动态类型的自定义字体

```swift
extension Font {
    static func customBody(_ name: String) -> Font {
        .custom(name, size: 17, relativeTo: .body)
    }

    static func customHeadline(_ name: String) -> Font {
        .custom(name, size: 17, relativeTo: .headline)
            .weight(.semibold)
    }
}

// 使用示例
Text("自定义样式文本")
    .font(.customBody("Avenir Next"))
```

## 颜色系统

### 语义化颜色

```swift
// 使用语义化颜色以自动支持浅色/深色模式
extension Color {
    // 标签
    static let primaryLabel = Color.primary
    static let secondaryLabel = Color.secondary
    static let tertiaryLabel = Color(uiColor: .tertiaryLabel)

    // 背景
    static let systemBackground = Color(uiColor: .systemBackground)
    static let secondaryBackground = Color(uiColor: .secondarySystemBackground)
    static let groupedBackground = Color(uiColor: .systemGroupedBackground)

    // 填充
    static let primaryFill = Color(uiColor: .systemFill)
    static let secondaryFill = Color(uiColor: .secondarySystemFill)

    // 分隔线
    static let separator = Color(uiColor: .separator)
    static let opaqueSeparator = Color(uiColor: .opaqueSeparator)
}
```

### 色调颜色

```swift
// 全应用色调
struct AppColors {
    static let primary = Color.blue
    static let secondary = Color.purple
    static let success = Color.green
    static let warning = Color.orange
    static let error = Color.red

    // 语义化色调
    static let interactive = Color.accentColor
    static let destructive = Color.red
}

// 将色调应用于视图
ContentView()
    .tint(AppColors.primary)
```

## 导航模式

### 层级导航

```swift
struct MasterDetailView: View {
    @State private var selectedItem: Item?
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        NavigationSplitView {
            // 侧边栏
            List(items, selection: $selectedItem) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationTitle("项目")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("添加", systemImage: "plus") { }
                }
            }
        } detail: {
            // 详情视图
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView(
                    "选择一个项目",
                    systemImage: "sidebar.leading"
                )
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

### 标签页导航

```swift
struct MainTabView: View {
    @State private var selectedTab: Tab = .home

    enum Tab: String, CaseIterable {
        case home, explore, notifications, profile

        var title: String {
            rawValue.capitalized
        }

        var systemImage: String {
            switch self {
            case .home: return "house"
            case .explore: return "magnifyingglass"
            case .notifications: return "bell"
            case .profile: return "person"
            }
        }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(Tab.allCases, id: \.self) { tab in
                NavigationStack {
                    tabContent(for: tab)
                }
                .tabItem {
                    Label(tab.title, systemImage: tab.systemImage)
                }
                .tag(tab)
            }
        }
    }

    @ViewBuilder
    private func tabContent(for tab: Tab) -> some View {
        switch tab {
        case .home:
            HomeView()
        case .explore:
            ExploreView()
        case .notifications:
            NotificationsView()
        case .profile:
            ProfileView()
        }
    }
}
```

## 工具栏模式

### 标准工具栏项

```swift
struct ContentView: View {
    @State private var isEditing = false

    var body: some View {
        NavigationStack {
            List { /* 内容 */ }
            .navigationTitle("项目")
            .toolbar {
                // 前导项
                ToolbarItem(placement: .topBarLeading) {
                    EditButton()
                }

                // 尾随项
                ToolbarItemGroup(placement: .topBarTrailing) {
                    Button("筛选", systemImage: "line.3.horizontal.decrease.circle") { }
                    Button("添加", systemImage: "plus") { }
                }

                // 底部栏
                ToolbarItemGroup(placement: .bottomBar) {
                    Button("归档", systemImage: "archivebox") { }
                    Spacer()
                    Text("\(itemCount) 个项目")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    Spacer()
                    Button("分享", systemImage: "square.and.arrow.up") { }
                }
            }
            .toolbarBackground(.visible, for: .bottomBar)
        }
    }
}
```

### 搜索集成

```swift
struct SearchableView: View {
    @State private var searchText = ""
    @State private var searchScope: SearchScope = .all
    @State private var isSearching = false

    enum SearchScope: String, CaseIterable {
        case all, titles, content
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                ItemRow(item: item)
            }
            .navigationTitle("资料库")
            .searchable(
                text: $searchText,
                isPresented: $isSearching,
                placement: .navigationBarDrawer(displayMode: .always)
            )
            .searchScopes($searchScope) {
                ForEach(SearchScope.allCases, id: \.self) { scope in
                    Text(scope.rawValue.capitalized).tag(scope)
                }
            }
        }
    }
}
```

## 反馈模式

### 触觉反馈

```swift
struct HapticFeedback {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle = .medium) {
        let generator = UIImpactFeedbackGenerator(style: style)
        generator.impactOccurred()
    }

    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(type)
    }

    static func selection() {
        let generator = UISelectionFeedbackGenerator()
        generator.selectionChanged()
    }
}

// 使用示例
Button("提交") {
    HapticFeedback.notification(.success)
    submit()
}
```

### 视觉反馈

```swift
struct FeedbackButton: View {
    let title: String
    let action: () -> Void

    @State private var showSuccess = false

    var body: some View {
        Button(title) {
            action()
            withAnimation {
                showSuccess = true
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                withAnimation {
                    showSuccess = false
                }
            }
        }
        .overlay(alignment: .trailing) {
            if showSuccess {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundStyle(.green)
                    .transition(.scale.combined(with: .opacity))
            }
        }
    }
}
```

## 辅助功能

### VoiceOver 支持

```swift
struct AccessibleCard: View {
    let item: Item

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(item.title)
                .font(.headline)
            Text(item.subtitle)
                .font(.subheadline)
                .foregroundStyle(.secondary)

            HStack {
                Image(systemName: "star.fill")
                Text("\(item.rating, specifier: "%.1f")")
            }
        }
        .padding()
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.title), \(item.subtitle)")
        .accessibilityValue("评分: \(item.rating) 星")
        .accessibilityHint("双击查看详情")
        .accessibilityAddTraits(.isButton)
    }
}
```

### 动态类型支持

```swift
struct DynamicTypeView: View {
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        Group {
            if dynamicTypeSize.isAccessibilitySize {
                // 辅助功能尺寸时垂直堆叠
                VStack(alignment: .leading, spacing: 12) {
                    leadingContent
                    trailingContent
                }
            } else {
                // 标准尺寸时并排显示
                HStack {
                    leadingContent
                    Spacer()
                    trailingContent
                }
            }
        }
    }

    var leadingContent: some View {
        Label("项目", systemImage: "folder")
    }

    var trailingContent: some View {
        Text("12")
            .foregroundStyle(.secondary)
    }
}
```

## 错误处理界面

### 错误状态

```swift
struct ErrorView: View {
    let error: Error
    let retryAction: () async -> Void

    var body: some View {
        ContentUnavailableView {
            Label("无法加载", systemImage: "exclamationmark.triangle")
        } description: {
            Text(error.localizedDescription)
        } actions: {
            Button("重试") {
                Task {
                    await retryAction()
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

### 空状态

```swift
struct EmptyStateView: View {
    let title: String
    let description: String
    let systemImage: String
    let action: (() -> Void)?
    let actionTitle: String?

    var body: some View {
        ContentUnavailableView {
            Label(title, systemImage: systemImage)
        } description: {
            Text(description)
        } actions: {
            if let action, let actionTitle {
                Button(actionTitle, action: action)
                    .buttonStyle(.borderedProminent)
            }
        }
    }
}

// 使用示例
EmptyStateView(
    title: "无照片",
    description: "拍摄你的第一张照片以开始使用。",
    systemImage: "camera",
    action: { showCamera = true },
    actionTitle: "拍照"
)
```
