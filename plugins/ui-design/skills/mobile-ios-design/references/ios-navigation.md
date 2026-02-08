# iOS 导航模式

## NavigationStack (iOS 16+)

### 基础导航

```swift
struct BasicNavigationView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.title, value: item)
            }
            .navigationTitle("项目")
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
        }
    }
}
```

### 编程式导航

```swift
struct ProgrammaticNavigationView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Button("前往设置") {
                    path.append(Destination.settings)
                }

                Button("前往个人资料") {
                    path.append(Destination.profile)
                }

                Button("深度链接到项目 123") {
                    path.append(Destination.settings)
                    path.append(Destination.itemDetail(id: 123))
                }
            }
            .navigationTitle("主页")
            .navigationDestination(for: Destination.self) { destination in
                switch destination {
                case .settings:
                    SettingsView()
                case .profile:
                    ProfileView()
                case .itemDetail(let id):
                    ItemDetailView(itemId: id)
                }
            }
        }
    }

    enum Destination: Hashable {
        case settings
        case profile
        case itemDetail(id: Int)
    }
}
```

### 导航状态持久化

```swift
struct PersistentNavigationView: View {
    @SceneStorage("navigationPath") private var pathData: Data?
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            ContentView()
                .navigationDestination(for: Item.self) { item in
                    ItemDetailView(item: item)
                }
        }
        .onAppear {
            restorePath()
        }
        .onChange(of: path) { _, newPath in
            savePath(newPath)
        }
    }

    private func savePath(_ path: NavigationPath) {
        guard let representation = path.codable else { return }
        pathData = try? JSONEncoder().encode(representation)
    }

    private func restorePath() {
        guard let data = pathData,
              let representation = try? JSONDecoder().decode(
                NavigationPath.CodableRepresentation.self,
                from: data
              ) else { return }
        path = NavigationPath(representation)
    }
}
```

## NavigationSplitView

### 双栏布局

```swift
struct TwoColumnView: View {
    @State private var selectedCategory: Category?
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            // 侧边栏
            List(categories, selection: $selectedCategory) { category in
                NavigationLink(value: category) {
                    Label(category.name, systemImage: category.icon)
                }
            }
            .navigationTitle("分类")
        } detail: {
            // 详情
            if let category = selectedCategory {
                CategoryDetailView(category: category)
            } else {
                ContentUnavailableView(
                    "选择一个分类",
                    systemImage: "sidebar.leading"
                )
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

### 三栏布局

```swift
struct ThreeColumnView: View {
    @State private var selectedFolder: Folder?
    @State private var selectedDocument: Document?

    var body: some View {
        NavigationSplitView {
            // 侧边栏
            List(folders, selection: $selectedFolder) { folder in
                NavigationLink(value: folder) {
                    Label(folder.name, systemImage: "folder")
                }
            }
            .navigationTitle("文件夹")
        } content: {
            // 内容栏
            if let folder = selectedFolder {
                List(folder.documents, selection: $selectedDocument) { document in
                    NavigationLink(value: document) {
                        DocumentRow(document: document)
                    }
                }
                .navigationTitle(folder.name)
            } else {
                Text("选择一个文件夹")
            }
        } detail: {
            // 详情栏
            if let document = selectedDocument {
                DocumentDetailView(document: document)
            } else {
                ContentUnavailableView(
                    "选择一个文档",
                    systemImage: "doc"
                )
            }
        }
    }
}
```

## Sheet 导航

### 模态 Sheet

```swift
struct SheetNavigationView: View {
    @State private var showSettings = false
    @State private var showNewItem = false
    @State private var editingItem: Item?

    var body: some View {
        NavigationStack {
            ContentView()
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button("添加", systemImage: "plus") {
                            showNewItem = true
                        }
                    }
                    ToolbarItem(placement: .topBarLeading) {
                        Button("设置", systemImage: "gear") {
                            showSettings = true
                        }
                    }
                }
        }
        // 基于布尔值的 sheet
        .sheet(isPresented: $showSettings) {
            SettingsSheet()
        }
        // 基于布尔值的全屏覆盖
        .fullScreenCover(isPresented: $showNewItem) {
            NewItemView()
        }
        // 基于项目的 sheet
        .sheet(item: $editingItem) { item in
            EditItemSheet(item: item)
        }
    }
}
```

### 带导航的 Sheet

```swift
struct NavigableSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("通用") {
                    NavigationLink("账户") {
                        AccountSettingsView()
                    }
                    NavigationLink("通知") {
                        NotificationSettingsView()
                    }
                }

                Section("高级") {
                    NavigationLink("隐私") {
                        PrivacySettingsView()
                    }
                }
            }
            .navigationTitle("设置")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }
}
```

### Sheet 自定义

```swift
struct CustomSheetView: View {
    @State private var showSheet = false

    var body: some View {
        Button("显示 Sheet") {
            showSheet = true
        }
        .sheet(isPresented: $showSheet) {
            SheetContent()
                // 可用的停靠高度
                .presentationDetents([
                    .medium,
                    .large,
                    .height(200),
                    .fraction(0.75)
                ])
                // 选定的停靠高度绑定
                .presentationDetents([.medium, .large], selection: $selectedDetent)
                // 拖动指示器可见性
                .presentationDragIndicator(.visible)
                // 圆角半径
                .presentationCornerRadius(24)
                // 背景交互
                .presentationBackgroundInteraction(.enabled(upThrough: .medium))
                // 禁用交互式关闭
                .interactiveDismissDisabled(hasUnsavedChanges)
        }
    }
}
```

## 标签页导航

### 基础 TabView

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("主页", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("搜索", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("个人资料", systemImage: "person")
                }
                .tag(2)
                .badge(unreadCount)
        }
    }
}
```

### 带自定义徽标的标签页

```swift
struct BadgedTabView: View {
    @State private var selectedTab: Tab = .home
    @State private var cartCount = 3

    enum Tab: String, CaseIterable {
        case home, search, cart, profile

        var icon: String {
            switch self {
            case .home: return "house"
            case .search: return "magnifyingglass"
            case .cart: return "cart"
            case .profile: return "person"
            }
        }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(Tab.allCases, id: \.self) { tab in
                NavigationStack {
                    contentView(for: tab)
                }
                .tabItem {
                    Label(tab.rawValue.capitalized, systemImage: tab.icon)
                }
                .tag(tab)
                .badge(tab == .cart ? cartCount : 0)
            }
        }
    }
}
```

## 深度链接

### 基于 URL 的导航

```swift
struct DeepLinkableApp: App {
    @StateObject private var router = NavigationRouter()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(router)
                .onOpenURL { url in
                    router.handle(url: url)
                }
        }
    }
}

class NavigationRouter: ObservableObject {
    @Published var path = NavigationPath()
    @Published var selectedTab: Tab = .home

    func handle(url: URL) {
        guard url.scheme == "myapp" else { return }

        switch url.host {
        case "item":
            if let id = Int(url.lastPathComponent) {
                selectedTab = .home
                path = NavigationPath()
                path.append(Destination.itemDetail(id: id))
            }
        case "settings":
            selectedTab = .profile
            path = NavigationPath()
            path.append(Destination.settings)
        default:
            break
        }
    }
}
```

### 通用链接

```swift
struct UniversalLinkHandler: View {
    @EnvironmentObject private var router: NavigationRouter

    var body: some View {
        ContentView()
            .onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
                guard let url = activity.webpageURL else { return }
                handleUniversalLink(url)
            }
    }

    private func handleUniversalLink(_ url: URL) {
        // 解析 URL 路径并相应导航
        let pathComponents = url.pathComponents

        if pathComponents.contains("product"),
           let idString = pathComponents.last,
           let id = Int(idString) {
            router.navigate(to: .product(id: id))
        }
    }
}
```

## 导航协调器模式

```swift
@MainActor
class NavigationCoordinator: ObservableObject {
    @Published var path = NavigationPath()
    @Published var sheet: Sheet?
    @Published var fullScreenCover: FullScreenCover?

    enum Sheet: Identifiable {
        case settings
        case newItem
        case editItem(Item)

        var id: String {
            switch self {
            case .settings: return "settings"
            case .newItem: return "newItem"
            case .editItem(let item): return "editItem-\(item.id)"
            }
        }
    }

    enum FullScreenCover: Identifiable {
        case onboarding
        case camera

        var id: String {
            switch self {
            case .onboarding: return "onboarding"
            case .camera: return "camera"
            }
        }
    }

    func push(_ destination: Destination) {
        path.append(destination)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path = NavigationPath()
    }

    func present(_ sheet: Sheet) {
        self.sheet = sheet
    }

    func presentFullScreen(_ cover: FullScreenCover) {
        self.fullScreenCover = cover
    }

    func dismiss() {
        if fullScreenCover != nil {
            fullScreenCover = nil
        } else if sheet != nil {
            sheet = nil
        }
    }
}
```

## 导航过渡 (iOS 18+)

### 自定义导航过渡

```swift
struct CustomTransitionView: View {
    @Namespace private var namespace

    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                        .matchedTransitionSource(id: item.id, in: namespace)
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
                    .navigationTransition(.zoom(sourceID: item.id, in: namespace))
            }
        }
    }
}
```

### Hero 过渡

```swift
struct HeroTransitionView: View {
    @Namespace private var animation
    @State private var selectedItem: Item?

    var body: some View {
        ZStack {
            ScrollView {
                LazyVGrid(columns: columns) {
                    ForEach(items) { item in
                        if selectedItem?.id != item.id {
                            ItemCard(item: item)
                                .matchedGeometryEffect(id: item.id, in: animation)
                                .onTapGesture {
                                    withAnimation(.spring(response: 0.3)) {
                                        selectedItem = item
                                    }
                                }
                        }
                    }
                }
            }

            if let item = selectedItem {
                ItemDetailView(item: item)
                    .matchedGeometryEffect(id: item.id, in: animation)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.3)) {
                            selectedItem = nil
                        }
                    }
            }
        }
    }
}
```
