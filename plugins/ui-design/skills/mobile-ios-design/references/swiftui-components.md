# SwiftUI 组件库

## 列表和集合

### 基础列表

```swift
struct ItemListView: View {
    @State private var items: [Item] = []

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
            }
            .onDelete(perform: deleteItems)
            .onMove(perform: moveItems)
        }
        .listStyle(.insetGrouped)
        .refreshable {
            await loadItems()
        }
    }

    private func deleteItems(at offsets: IndexSet) {
        items.remove(atOffsets: offsets)
    }

    private func moveItems(from source: IndexSet, to destination: Int) {
        items.move(fromOffsets: source, toOffset: destination)
    }
}
```

### 分组列表

```swift
struct SectionedListView: View {
    let groupedItems: [String: [Item]]

    var body: some View {
        List {
            ForEach(groupedItems.keys.sorted(), id: \.self) { key in
                Section(header: Text(key)) {
                    ForEach(groupedItems[key] ?? []) { item in
                        ItemRow(item: item)
                    }
                }
            }
        }
        .listStyle(.sidebar)
    }
}
```

### 搜索集成

```swift
struct SearchableListView: View {
    @State private var searchText = ""
    @State private var items: [Item] = []

    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.name.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                ItemRow(item: item)
            }
            .searchable(text: $searchText, prompt: "搜索项目")
            .searchSuggestions {
                ForEach(searchSuggestions, id: \.self) { suggestion in
                    Text(suggestion)
                        .searchCompletion(suggestion)
                }
            }
            .navigationTitle("项目")
        }
    }
}
```

## 表单和输入

### 设置表单

```swift
struct SettingsView: View {
    @AppStorage("notifications") private var notificationsEnabled = true
    @AppStorage("soundEnabled") private var soundEnabled = true
    @State private var selectedTheme = Theme.system
    @State private var username = ""

    var body: some View {
        Form {
            Section("账户") {
                TextField("用户名", text: $username)
                    .textContentType(.username)
                    .autocorrectionDisabled()
            }

            Section("偏好设置") {
                Toggle("启用通知", isOn: $notificationsEnabled)
                Toggle("音效", isOn: $soundEnabled)

                Picker("主题", selection: $selectedTheme) {
                    ForEach(Theme.allCases) { theme in
                        Text(theme.rawValue).tag(theme)
                    }
                }
            }

            Section("关于") {
                LabeledContent("版本", value: "1.0.0")

                Link(destination: URL(string: "https://example.com/privacy")!) {
                    Text("隐私政策")
                }
            }
        }
        .navigationTitle("设置")
    }
}
```

### 自定义输入字段

```swift
struct ValidatedTextField: View {
    let title: String
    @Binding var text: String
    let validation: (String) -> Bool

    @State private var isValid = true
    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundStyle(.secondary)

            TextField(title, text: $text)
                .textFieldStyle(.roundedBorder)
                .focused($isFocused)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(borderColor, lineWidth: 1)
                )
                .onChange(of: text) { _, newValue in
                    isValid = validation(newValue)
                }

            if !isValid && !text.isEmpty {
                Text("无效输入")
                    .font(.caption)
                    .foregroundStyle(.red)
            }
        }
    }

    private var borderColor: Color {
        if isFocused {
            return isValid ? .blue : .red
        }
        return .clear
    }
}
```

## 按钮和操作

### 按钮样式

```swift
// 主要填充按钮
Button("继续") {
    // 操作
}
.buttonStyle(.borderedProminent)
.controlSize(.large)

// 次要按钮
Button("取消") {
    // 操作
}
.buttonStyle(.bordered)

// 删除按钮
Button("删除", role: .destructive) {
    // 操作
}
.buttonStyle(.bordered)

// 自定义按钮样式
struct ScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}
```

### 菜单和上下文菜单

```swift
// 菜单按钮
Menu {
    Button("编辑", systemImage: "pencil") { }
    Button("复制", systemImage: "doc.on.doc") { }
    Divider()
    Button("删除", systemImage: "trash", role: .destructive) { }
} label: {
    Image(systemName: "ellipsis.circle")
}

// 任何视图上的上下文菜单
Text("长按我")
    .contextMenu {
        Button("复制", systemImage: "doc.on.doc") { }
        Button("分享", systemImage: "square.and.arrow.up") { }
    } preview: {
        ItemPreviewView()
    }
```

## Sheet 和模态视图

### Sheet 展示

```swift
struct ParentView: View {
    @State private var showSettings = false
    @State private var selectedItem: Item?

    var body: some View {
        VStack {
            Button("设置") {
                showSettings = true
            }
        }
        .sheet(isPresented: $showSettings) {
            SettingsSheet()
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
        }
        .sheet(item: $selectedItem) { item in
            ItemDetailSheet(item: item)
                .presentationDetents([.height(300), .large])
                .presentationCornerRadius(24)
        }
    }
}

struct SettingsSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            SettingsContent()
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

### 确认对话框

```swift
struct DeleteConfirmationView: View {
    @State private var showConfirmation = false

    var body: some View {
        Button("删除账户", role: .destructive) {
            showConfirmation = true
        }
        .confirmationDialog(
            "删除账户",
            isPresented: $showConfirmation,
            titleVisibility: .visible
        ) {
            Button("删除", role: .destructive) {
                deleteAccount()
            }
            Button("取消", role: .cancel) { }
        } message: {
            Text("此操作无法撤销。")
        }
    }
}
```

## 加载和进度

### 进度指示器

```swift
// 不确定的旋转指示器
ProgressView()
    .progressViewStyle(.circular)

// 确定的进度条
ProgressView(value: downloadProgress, total: 1.0) {
    Text("下载中...")
} currentValueLabel: {
    Text("\(Int(downloadProgress * 100))%")
}

// 自定义加载视图
struct LoadingOverlay: View {
    let message: String

    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                ProgressView()
                    .scaleEffect(1.5)
                    .tint(.white)

                Text(message)
                    .font(.subheadline)
                    .foregroundStyle(.white)
            }
            .padding(24)
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
        }
    }
}
```

### 骨架屏加载

```swift
struct SkeletonRow: View {
    @State private var isAnimating = false

    var body: some View {
        HStack(spacing: 12) {
            Circle()
                .fill(.gray.opacity(0.3))
                .frame(width: 44, height: 44)

            VStack(alignment: .leading, spacing: 8) {
                RoundedRectangle(cornerRadius: 4)
                    .fill(.gray.opacity(0.3))
                    .frame(height: 14)
                    .frame(maxWidth: 200)

                RoundedRectangle(cornerRadius: 4)
                    .fill(.gray.opacity(0.2))
                    .frame(height: 12)
                    .frame(maxWidth: 150)
            }
        }
        .opacity(isAnimating ? 0.5 : 1.0)
        .animation(.easeInOut(duration: 0.8).repeatForever(), value: isAnimating)
        .onAppear { isAnimating = true }
    }
}
```

## 异步内容加载

### AsyncImage

```swift
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image
            .resizable()
            .aspectRatio(contentMode: .fill)
    case .failure:
        Image(systemName: "photo")
            .foregroundStyle(.secondary)
    @unknown default:
        EmptyView()
    }
}
.frame(width: 100, height: 100)
.clipShape(RoundedRectangle(cornerRadius: 8))
```

### 基于任务的加载

```swift
struct AsyncContentView: View {
    @State private var items: [Item] = []
    @State private var isLoading = true
    @State private var error: Error?

    var body: some View {
        Group {
            if isLoading {
                ProgressView("加载中...")
            } else if let error {
                ContentUnavailableView(
                    "加载失败",
                    systemImage: "exclamationmark.triangle",
                    description: Text(error.localizedDescription)
                )
            } else if items.isEmpty {
                ContentUnavailableView(
                    "无项目",
                    systemImage: "tray",
                    description: Text("添加你的第一个项目以开始使用。")
                )
            } else {
                List(items) { item in
                    ItemRow(item: item)
                }
            }
        }
        .task {
            await loadItems()
        }
    }

    private func loadItems() async {
        do {
            items = try await api.fetchItems()
            isLoading = false
        } catch {
            self.error = error
            isLoading = false
        }
    }
}
```

## 动画

### 隐式动画

```swift
struct AnimatedCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("点击展开")

            if isExpanded {
                Text("此处为附加内容")
                    .transition(.move(edge: .top).combined(with: .opacity))
            }
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(.blue.opacity(0.1), in: RoundedRectangle(cornerRadius: 12))
        .onTapGesture {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                isExpanded.toggle()
            }
        }
    }
}
```

### 自定义过渡

```swift
extension AnyTransition {
    static var slideAndFade: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        )
    }

    static var scaleAndFade: AnyTransition {
        .scale(scale: 0.8).combined(with: .opacity)
    }
}
```

### 相位动画器 (iOS 17+)

```swift
struct PulsingButton: View {
    var body: some View {
        Button("点击我") { }
            .buttonStyle(.borderedProminent)
            .phaseAnimator([false, true]) { content, phase in
                content
                    .scaleEffect(phase ? 1.05 : 1.0)
            } animation: { _ in
                .easeInOut(duration: 0.5)
            }
    }
}
```

## 手势

### 拖动手势

```swift
struct DraggableCard: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false

    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(.blue)
            .frame(width: 200, height: 150)
            .offset(offset)
            .scaleEffect(isDragging ? 1.05 : 1.0)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                        isDragging = true
                    }
                    .onEnded { _ in
                        withAnimation(.spring()) {
                            offset = .zero
                            isDragging = false
                        }
                    }
            )
    }
}
```

### 同时手势

```swift
struct ZoomableImage: View {
    @State private var scale: CGFloat = 1.0
    @State private var lastScale: CGFloat = 1.0

    var body: some View {
        Image("photo")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .scaleEffect(scale)
            .gesture(
                MagnificationGesture()
                    .onChanged { value in
                        scale = lastScale * value
                    }
                    .onEnded { _ in
                        lastScale = scale
                    }
            )
            .gesture(
                TapGesture(count: 2)
                    .onEnded {
                        withAnimation {
                            scale = 1.0
                            lastScale = 1.0
                        }
                    }
            )
    }
}
```
