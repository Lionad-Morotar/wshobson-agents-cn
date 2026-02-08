# Material Design 3 主题系统

## 颜色系统

### 动态颜色（Material You）

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        shapes = AppShapes,
        content = content
    )
}
```

### 自定义颜色方案

```kotlin
// 定义调色板
val md_theme_light_primary = Color(0xFF6750A4)
val md_theme_light_onPrimary = Color(0xFFFFFFFF)
val md_theme_light_primaryContainer = Color(0xFFEADDFF)
val md_theme_light_onPrimaryContainer = Color(0xFF21005D)
val md_theme_light_secondary = Color(0xFF625B71)
val md_theme_light_onSecondary = Color(0xFFFFFFFF)
val md_theme_light_secondaryContainer = Color(0xFFE8DEF8)
val md_theme_light_onSecondaryContainer = Color(0xFF1D192B)
val md_theme_light_tertiary = Color(0xFF7D5260)
val md_theme_light_onTertiary = Color(0xFFFFFFFF)
val md_theme_light_tertiaryContainer = Color(0xFFFFD8E4)
val md_theme_light_onTertiaryContainer = Color(0xFF31111D)
val md_theme_light_error = Color(0xFFB3261E)
val md_theme_light_onError = Color(0xFFFFFFFF)
val md_theme_light_errorContainer = Color(0xFFF9DEDC)
val md_theme_light_onErrorContainer = Color(0xFF410E0B)
val md_theme_light_background = Color(0xFFFFFBFE)
val md_theme_light_onBackground = Color(0xFF1C1B1F)
val md_theme_light_surface = Color(0xFFFFFBFE)
val md_theme_light_onSurface = Color(0xFF1C1B1F)
val md_theme_light_surfaceVariant = Color(0xFFE7E0EC)
val md_theme_light_onSurfaceVariant = Color(0xFF49454F)
val md_theme_light_outline = Color(0xFF79747E)
val md_theme_light_outlineVariant = Color(0xFFCAC4D0)

val LightColorScheme = lightColorScheme(
    primary = md_theme_light_primary,
    onPrimary = md_theme_light_onPrimary,
    primaryContainer = md_theme_light_primaryContainer,
    onPrimaryContainer = md_theme_light_onPrimaryContainer,
    secondary = md_theme_light_secondary,
    onSecondary = md_theme_light_onSecondary,
    secondaryContainer = md_theme_light_secondaryContainer,
    onSecondaryContainer = md_theme_light_onSecondaryContainer,
    tertiary = md_theme_light_tertiary,
    onTertiary = md_theme_light_onTertiary,
    tertiaryContainer = md_theme_light_tertiaryContainer,
    onTertiaryContainer = md_theme_light_onTertiaryContainer,
    error = md_theme_light_error,
    onError = md_theme_light_onError,
    errorContainer = md_theme_light_errorContainer,
    onErrorContainer = md_theme_light_onErrorContainer,
    background = md_theme_light_background,
    onBackground = md_theme_light_onBackground,
    surface = md_theme_light_surface,
    onSurface = md_theme_light_onSurface,
    surfaceVariant = md_theme_light_surfaceVariant,
    onSurfaceVariant = md_theme_light_onSurfaceVariant,
    outline = md_theme_light_outline,
    outlineVariant = md_theme_light_outlineVariant
)

// 深色模式颜色遵循相同的模式
val DarkColorScheme = darkColorScheme(
    primary = md_theme_dark_primary,
    // ... 其他颜色
)
```

### 颜色角色使用

```kotlin
@Composable
fun ColorRolesExample() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Primary - 关键操作、悬浮操作按钮
        Button(onClick = { }) {
            Text("主要操作")
        }

        // Primary Container - 次要突出的容器
        Surface(
            color = MaterialTheme.colorScheme.primaryContainer,
            shape = RoundedCornerShape(12.dp)
        ) {
            Text(
                "主色容器",
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }

        // Secondary - 较不突出的操作
        FilledTonalButton(onClick = { }) {
            Text("次要操作")
        }

        // Tertiary - 对比强调色
        Badge(
            containerColor = MaterialTheme.colorScheme.tertiaryContainer,
            contentColor = MaterialTheme.colorScheme.onTertiaryContainer
        ) {
            Text("新")
        }

        // Error - 破坏性操作
        Button(
            onClick = { },
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        ) {
            Text("删除")
        }

        // Surface 变体
        Surface(
            color = MaterialTheme.colorScheme.surfaceVariant,
            shape = RoundedCornerShape(8.dp)
        ) {
            Text(
                "表面变体",
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
```

### 扩展颜色

```kotlin
// 超出 M3 默认值的自定义语义颜色
data class ExtendedColors(
    val success: Color,
    val onSuccess: Color,
    val successContainer: Color,
    val onSuccessContainer: Color,
    val warning: Color,
    val onWarning: Color,
    val warningContainer: Color,
    val onWarningContainer: Color
)

val LocalExtendedColors = staticCompositionLocalOf {
    ExtendedColors(
        success = Color(0xFF4CAF50),
        onSuccess = Color.White,
        successContainer = Color(0xFFE8F5E9),
        onSuccessContainer = Color(0xFF1B5E20),
        warning = Color(0xFFFF9800),
        onWarning = Color.White,
        warningContainer = Color(0xFFFFF3E0),
        onWarningContainer = Color(0xFFE65100)
    )
}

@Composable
fun AppTheme(
    content: @Composable () -> Unit
) {
    val extendedColors = ExtendedColors(
        // ... 基于浅色/深色主题定义颜色
    )

    CompositionLocalProvider(
        LocalExtendedColors provides extendedColors
    ) {
        MaterialTheme(
            colorScheme = colorScheme,
            content = content
        )
    }
}

// 使用示例
@Composable
fun SuccessBanner() {
    val extendedColors = LocalExtendedColors.current

    Surface(
        color = extendedColors.successContainer,
        shape = RoundedCornerShape(8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Icon(
                Icons.Default.CheckCircle,
                contentDescription = null,
                tint = extendedColors.success
            )
            Text(
                "操作成功！",
                color = extendedColors.onSuccessContainer
            )
        }
    }
}
```

## 排版系统

### Material 3 字体比例

```kotlin
val AppTypography = Typography(
    // Display 样式 - 英雄文本、大号数字
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    displaySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 36.sp,
        lineHeight = 44.sp,
        letterSpacing = 0.sp
    ),

    // Headline 样式 - 高强调、短文本
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    headlineSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp,
        lineHeight = 32.sp,
        letterSpacing = 0.sp
    ),

    // Title 样式 - 中等强调标题
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    titleSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),

    // Body 样式 - 长文本
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    bodySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.4.sp
    ),

    // Label 样式 - 按钮、标签、导航
    labelLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    labelMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
```

### 自定义字体

```kotlin
// 加载自定义字体
val Inter = FontFamily(
    Font(R.font.inter_regular, FontWeight.Normal),
    Font(R.font.inter_medium, FontWeight.Medium),
    Font(R.font.inter_semibold, FontWeight.SemiBold),
    Font(R.font.inter_bold, FontWeight.Bold)
)

val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = Inter,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    // 应用到所有样式...
)

// 可变字体（Android 12+）
val InterVariable = FontFamily(
    Font(
        R.font.inter_variable,
        variationSettings = FontVariation.Settings(
            FontVariation.weight(400)
        )
    )
)
```

## 形状系统

### Material 3 形状

```kotlin
val AppShapes = Shapes(
    // 超小 - 芯片、小按钮
    extraSmall = RoundedCornerShape(4.dp),

    // 小 - 文本字段、小卡片
    small = RoundedCornerShape(8.dp),

    // 中 - 卡片、对话框
    medium = RoundedCornerShape(12.dp),

    // 大 - 大卡片、底部抽屉
    large = RoundedCornerShape(16.dp),

    // 超大 - 全屏对话框
    extraLarge = RoundedCornerShape(28.dp)
)
```

### 自定义形状使用

```kotlin
@Composable
fun ShapedComponents() {
    Column(
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // 文本字段使用小形状
        OutlinedTextField(
            value = "",
            onValueChange = {},
            shape = MaterialTheme.shapes.small,
            label = { Text("输入") }
        )

        // 卡片使用中形状
        Card(
            shape = MaterialTheme.shapes.medium
        ) {
            Text("卡片内容", modifier = Modifier.padding(16.dp))
        }

        // 突出容器使用大形状
        Surface(
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Text("精选", modifier = Modifier.padding(24.dp))
        }

        // 自定义非对称形状
        Surface(
            shape = RoundedCornerShape(
                topStart = 24.dp,
                topEnd = 24.dp,
                bottomStart = 0.dp,
                bottomEnd = 0.dp
            ),
            color = MaterialTheme.colorScheme.surface
        ) {
            Text("底部抽屉样式", modifier = Modifier.padding(16.dp))
        }
    }
}
```

## 高程和阴影

### 色调高程

```kotlin
@Composable
fun ElevationExample() {
    Column(
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Level 0 - 无高程
        Surface(
            tonalElevation = 0.dp,
            shadowElevation = 0.dp
        ) {
            Text("Level 0", modifier = Modifier.padding(16.dp))
        }

        // Level 1 - 低强调表面
        Surface(
            tonalElevation = 1.dp,
            shadowElevation = 1.dp
        ) {
            Text("Level 1", modifier = Modifier.padding(16.dp))
        }

        // Level 2 - 卡片、开关
        Surface(
            tonalElevation = 3.dp,
            shadowElevation = 2.dp
        ) {
            Text("Level 2", modifier = Modifier.padding(16.dp))
        }

        // Level 3 - 导航组件
        Surface(
            tonalElevation = 6.dp,
            shadowElevation = 4.dp
        ) {
            Text("Level 3", modifier = Modifier.padding(16.dp))
        }

        // Level 4 - 导航栏
        Surface(
            tonalElevation = 8.dp,
            shadowElevation = 6.dp
        ) {
            Text("Level 4", modifier = Modifier.padding(16.dp))
        }

        // Level 5 - 悬浮操作按钮
        Surface(
            tonalElevation = 12.dp,
            shadowElevation = 8.dp
        ) {
            Text("Level 5", modifier = Modifier.padding(16.dp))
        }
    }
}
```

## 响应式设计

### 窗口大小类别

```kotlin
@Composable
fun AdaptiveLayout() {
    val windowSizeClass = calculateWindowSizeClass(LocalContext.current as Activity)

    when (windowSizeClass.widthSizeClass) {
        WindowWidthSizeClass.Compact -> {
            // 手机竖屏 - 单列、底部导航
            CompactLayout()
        }
        WindowWidthSizeClass.Medium -> {
            // 平板竖屏、手机横屏 - 导航栏
            MediumLayout()
        }
        WindowWidthSizeClass.Expanded -> {
            // 平板横屏、桌面 - 导航抽屉、多窗格
            ExpandedLayout()
        }
    }
}

@Composable
fun CompactLayout() {
    Scaffold(
        bottomBar = { NavigationBar { /* 项 */ } }
    ) { padding ->
        Content(modifier = Modifier.padding(padding))
    }
}

@Composable
fun MediumLayout() {
    Row {
        NavigationRail { /* 项 */ }
        Content(modifier = Modifier.weight(1f))
    }
}

@Composable
fun ExpandedLayout() {
    PermanentNavigationDrawer(
        drawerContent = {
            PermanentDrawerSheet { /* 项 */ }
        }
    ) {
        Row {
            ListPane(modifier = Modifier.weight(0.4f))
            DetailPane(modifier = Modifier.weight(0.6f))
        }
    }
}
```

### 可折叠设备支持

```kotlin
@Composable
fun FoldableAwareLayout() {
    val foldingFeature = LocalFoldingFeature.current

    when {
        foldingFeature?.state == FoldingFeature.State.HALF_OPENED -> {
            // 设备半折叠（桌面模式）
            TwoHingeLayout(
                top = { CameraPreview() },
                bottom = { CameraControls() }
            )
        }
        foldingFeature?.orientation == FoldingFeature.Orientation.VERTICAL -> {
            // 垂直折叠（书本模式）
            TwoPaneLayout(
                first = { NavigationPane() },
                second = { ContentPane() }
            )
        }
        else -> {
            // 常规或完全展开
            SinglePaneLayout()
        }
    }
}
```
