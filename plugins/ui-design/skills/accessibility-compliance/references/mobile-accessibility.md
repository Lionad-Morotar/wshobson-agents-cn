# 移动端无障碍

## 概述

移动端无障碍确保应用在 iOS 和 Android 设备上为残障用户工作。这包括对屏幕阅读器(VoiceOver、TalkBack)、运动障碍和各种视觉障碍的支持。

## 触摸目标尺寸

### 最小尺寸

```css
/* WCAG 2.2 AA 级:最小 24x24px */
.interactive-element {
  min-width: 24px;
  min-height: 24px;
}

/* WCAG 2.2 AAA 级 / Apple HIG / Material Design: 44x44dp */
.touch-target {
  min-width: 44px;
  min-height: 44px;
}

/* Android Material Design:推荐 48x48dp */
.android-touch-target {
  min-width: 48px;
  min-height: 48px;
}
```

### 触摸目标间距

```tsx
// 确保触摸目标之间有足够的间距
function ButtonGroup({ buttons }) {
  return (
    <div className="flex gap-3">
      {" "}
      {/* 最小间距 12px */}
      {buttons.map((btn) => (
        <button key={btn.id} className="min-w-[44px] min-h-[44px] px-4 py-2">
          {btn.label}
        </button>
      ))}
    </div>
  );
}

// 在不改变视觉大小的情况下扩展点击区域
function IconButton({ icon, label, onClick }) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="relative p-3" // 创建 44x44 触摸区域
    >
      <span className="block w-5 h-5">{icon}</span>
    </button>
  );
}
```

## iOS VoiceOver

### React Native 无障碍属性

```tsx
import { View, Text, TouchableOpacity, AccessibilityInfo } from "react-native";

// 基本的可访问按钮
function AccessibleButton({ onPress, title, hint }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      accessible={true}
      accessibilityLabel={title}
      accessibilityHint={hint}
      accessibilityRole="button"
    >
      <Text>{title}</Text>
    </TouchableOpacity>
  );
}

// 具有分组内容的复杂组件
function ProductCard({ product }) {
  return (
    <View
      accessible={true}
      accessibilityLabel={`${product.name}, ${product.price}, ${product.rating} 星`}
      accessibilityRole="button"
      accessibilityActions={[
        { name: "activate", label: "查看详情" },
        { name: "addToCart", label: "加入购物车" },
      ]}
      onAccessibilityAction={(event) => {
        switch (event.nativeEvent.actionName) {
          case "addToCart":
            addToCart(product);
            break;
          case "activate":
            viewDetails(product);
            break;
        }
      }}
    >
      <Image source={product.image} accessibilityIgnoresInvertColors />
      <Text>{product.name}</Text>
      <Text>{product.price}</Text>
    </View>
  );
}

// 宣布动态变化
function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount((prev) => prev + 1);
    AccessibilityInfo.announceForAccessibility(`计数现在是 ${count + 1}`);
  };

  return (
    <View>
      <Text accessibilityRole="text" accessibilityLiveRegion="polite">
        计数:{count}
      </Text>
      <TouchableOpacity
        onPress={increment}
        accessibilityLabel="增加"
        accessibilityHint="将计数器加一"
      >
        <Text>+</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### SwiftUI 无障碍

```swift
import SwiftUI

struct AccessibleButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
        }
        .accessibilityLabel(title)
        .accessibilityHint("双击以激活")
        .accessibilityAddTraits(.isButton)
    }
}

struct ProductCard: View {
    let product: Product

    var body: some View {
        VStack {
            AsyncImage(url: product.imageURL)
                .accessibilityHidden(true) // 图片是装饰性的

            Text(product.name)
            Text(product.price.formatted(.currency(code: "USD")))
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(product.name), \(product.price.formatted(.currency(code: "USD")))")
        .accessibilityHint("双击查看详情")
        .accessibilityAction(named: "加入购物车") {
            addToCart(product)
        }
    }
}

// 自定义无障碍转子
struct DocumentView: View {
    let sections: [Section]

    var body: some View {
        ScrollView {
            ForEach(sections) { section in
                Text(section.title)
                    .font(.headline)
                    .accessibilityAddTraits(.isHeader)
                Text(section.content)
            }
        }
        .accessibilityRotor("标题") {
            ForEach(sections) { section in
                AccessibilityRotorEntry(section.title, id: section.id)
            }
        }
    }
}
```

## Android TalkBack

### Jetpack Compose 无障碍

```kotlin
import androidx.compose.ui.semantics.*

@Composable
fun AccessibleButton(
    onClick: () -> Unit,
    text: String,
    enabled: Boolean = true
) {
    Button(
        onClick = onClick,
        enabled = enabled,
        modifier = Modifier.semantics {
            contentDescription = text
            role = Role.Button
            if (!enabled) {
                disabled()
            }
        }
    ) {
        Text(text)
    }
}

@Composable
fun ProductCard(product: Product) {
    Card(
        modifier = Modifier
            .semantics(mergeDescendants = true) {
                contentDescription = "${product.name}, ${product.formattedPrice}"
                customActions = listOf(
                    CustomAccessibilityAction("加入购物车") {
                        addToCart(product)
                        true
                    }
                )
            }
            .clickable { navigateToDetails(product) }
    ) {
        Image(
            painter = painterResource(product.imageRes),
            contentDescription = null, // 装饰性
            modifier = Modifier.semantics { invisibleToUser() }
        )
        Text(product.name)
        Text(product.formattedPrice)
    }
}

// 动态内容的实时区域
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text(
            text = "计数: $count",
            modifier = Modifier.semantics {
                liveRegion = LiveRegionMode.Polite
            }
        )
        Button(onClick = { count++ }) {
            Text("增加")
        }
    }
}

// 标题级别
@Composable
fun SectionHeader(title: String, level: Int) {
    Text(
        text = title,
        style = MaterialTheme.typography.headlineMedium,
        modifier = Modifier.semantics {
            heading()
            // 自定义标题级别(非内置)
            testTag = "heading-$level"
        }
    )
}
```

### Android XML 视图

```xml
<!-- 可访问按钮 -->
<Button
    android:id="@+id/submit_button"
    android:layout_width="wrap_content"
    android:layout_height="48dp"
    android:minWidth="48dp"
    android:text="@string/submit"
    android:contentDescription="@string/submit_form" />

<!-- 分组内容 -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:importantForAccessibility="yes"
    android:focusable="true"
    android:contentDescription="@string/product_description">

    <ImageView
        android:importantForAccessibility="no"
        android:src="@drawable/product" />

    <TextView
        android:text="@string/product_name"
        android:importantForAccessibility="no" />
</LinearLayout>

<!-- 实时区域 -->
<TextView
    android:id="@+id/status"
    android:accessibilityLiveRegion="polite" />
```

```kotlin
// Kotlin 无障碍
binding.submitButton.apply {
    contentDescription = getString(R.string.submit_form)
    accessibilityDelegate = object : View.AccessibilityDelegate() {
        override fun onInitializeAccessibilityNodeInfo(
            host: View,
            info: AccessibilityNodeInfo
        ) {
            super.onInitializeAccessibilityNodeInfo(host, info)
            info.addAction(
                AccessibilityNodeInfo.AccessibilityAction(
                    AccessibilityNodeInfo.ACTION_CLICK,
                    getString(R.string.submit_action)
                )
            )
        }
    }
}

// 宣布变化
binding.counter.announceForAccessibility("计数已更新为 $count")
```

## 手势无障碍

### 替代手势

```tsx
// React Native:为复杂手势提供替代方案
function SwipeableCard({ item, onDelete }) {
  const [showDelete, setShowDelete] = useState(false);

  return (
    <View
      accessible={true}
      accessibilityActions={[{ name: "delete", label: "删除项目" }]}
      onAccessibilityAction={(event) => {
        if (event.nativeEvent.actionName === "delete") {
          onDelete(item);
        }
      }}
    >
      <Swipeable
        renderRightActions={() => (
          <TouchableOpacity
            onPress={() => onDelete(item)}
            accessibilityLabel="删除"
          >
            <Text>删除</Text>
          </TouchableOpacity>
        )}
      >
        <Text>{item.title}</Text>
      </Swipeable>

      {/* 屏幕阅读器用户的替代方案 */}
      <TouchableOpacity
        accessibilityLabel={`删除 ${item.title}`}
        onPress={() => onDelete(item)}
        style={{ position: "absolute", right: 0 }}
      >
        <Text>删除</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### 运动和动画

```tsx
// 尊重减少动画偏好
import { AccessibilityInfo } from "react-native";

function AnimatedComponent() {
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);

    const subscription = AccessibilityInfo.addEventListener(
      "reduceMotionChanged",
      setReduceMotion,
    );

    return () => subscription.remove();
  }, []);

  return (
    <Animated.View
      style={{
        transform: reduceMotion ? [] : [{ translateX: animatedValue }],
        opacity: reduceMotion ? 1 : animatedOpacity,
      }}
    >
      <Content />
    </Animated.View>
  );
}
```

## 动态类型 / 文本缩放

### iOS 动态类型

```swift
// SwiftUI
Text("你好,世界!")
    .font(.body) // 随动态类型自动缩放

Text("固定大小")
    .font(.system(size: 16, design: .default))
    .dynamicTypeSize(.large) // 限制为大

// 允许无限缩放
Text("可缩放")
    .font(.body)
    .minimumScaleFactor(0.5)
    .lineLimit(nil)
```

### Android 文本缩放

```xml
<!-- 使用 sp 作为文本大小 -->
<TextView
    android:textSize="16sp"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content" />

<!-- 在 styles.xml 中 -->
<style name="TextAppearance.Body">
    <item name="android:textSize">16sp</item>
    <item name="android:lineHeight">24sp</item>
</style>
```

```kotlin
// Compose:文本自动缩放
Text(
    text = "你好,世界!",
    style = MaterialTheme.typography.bodyLarge
)

// 如果需要,限制缩放
Text(
    text = "限制缩放",
    fontSize = 16.sp,
    maxLines = 2,
    overflow = TextOverflow.Ellipsis
)
```

### React Native 文本缩放

```tsx
import { Text, PixelRatio } from 'react-native';

// 允许文本缩放(默认)
<Text allowFontScaling={true}>可缩放文本</Text>

// 限制最大缩放
<Text maxFontSizeMultiplier={1.5}>限制缩放</Text>

// 禁用缩放(谨慎使用)
<Text allowFontScaling={false}>固定大小</Text>

// 响应式字体大小
const scaledFontSize = (size: number) => {
  const scale = PixelRatio.getFontScale();
  return size * Math.min(scale, 1.5); // 限制在 1.5x
};
```

## 测试检查清单

```markdown
## VoiceOver (iOS) 测试

- [ ] 所有交互元素都有标签
- [ ] 滑动导航以逻辑顺序覆盖所有内容
- [ ] 自定义操作可用于复杂交互
- [ ] 为动态内容发布公告
- [ ] 标题可通过转子导航
- [ ] 图片有适当的描述或被隐藏

## TalkBack (Android) 测试

- [ ] 焦点顺序符合逻辑
- [ ] 触摸探索正常工作
- [ ] 自定义操作可用
- [ ] 实时区域宣布更新
- [ ] 标题正确标记
- [ ] 分组内容一起读取

## 运动无障碍

- [ ] 触摸目标至少 44x44 点
- [ ] 目标之间有足够的间距(最小 8dp)
- [ ] 复杂手势的替代方案
- [ ] 没有时间限制的交互

## 视觉无障碍

- [ ] 文本可缩放到 200% 而无损失
- [ ] 内容在高对比度模式下可见
- [ ] 颜色不是唯一指示器
- [ ] 动画尊重减少动画偏好
```

## 资源

- [Apple 无障碍编程指南](https://developer.apple.com/accessibility/)
- [Android 无障碍开发者指南](https://developer.android.com/guide/topics/ui/accessibility)
- [React Native 无障碍](https://reactnative.dev/docs/accessibility)
- [移动端无障碍 WCAG](https://www.w3.org/TR/mobile-accessibility-mapping/)
