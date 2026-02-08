# Jetpack Compose 组件库

## 列表和集合

### 基础 LazyColumn

```kotlin
@Composable
fun ItemList(
    items: List<Item>,
    onItemClick: (Item) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(
            items = items,
            key = { it.id }
        ) { item ->
            ItemRow(
                item = item,
                onClick = { onItemClick(item) }
            )
        }
    }
}
```

### 下拉刷新

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RefreshableList(
    items: List<Item>,
    isRefreshing: Boolean,
    onRefresh: () -> Unit
) {
    val pullToRefreshState = rememberPullToRefreshState()

    PullToRefreshBox(
        state = pullToRefreshState,
        isRefreshing = isRefreshing,
        onRefresh = onRefresh
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxSize()
        ) {
            items(items) { item ->
                ItemRow(item = item)
            }
        }
    }
}
```

### 滑动删除

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SwipeableItem(
    item: Item,
    onDelete: () -> Unit
) {
    val dismissState = rememberSwipeToDismissBoxState(
        confirmValueChange = { value ->
            if (value == SwipeToDismissBoxValue.EndToStart) {
                onDelete()
                true
            } else {
                false
            }
        }
    )

    SwipeToDismissBox(
        state = dismissState,
        backgroundContent = {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.errorContainer)
                    .padding(horizontal = 20.dp),
                contentAlignment = Alignment.CenterEnd
            ) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = "删除",
                    tint = MaterialTheme.colorScheme.onErrorContainer
                )
            }
        }
    ) {
        ItemRow(item = item)
    }
}
```

### 粘性标题

```kotlin
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun GroupedList(
    groups: Map<String, List<Item>>
) {
    LazyColumn {
        groups.forEach { (header, items) ->
            stickyHeader {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceVariant
                ) {
                    Text(
                        text = header,
                        modifier = Modifier.padding(16.dp),
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            items(items, key = { it.id }) { item ->
                ItemRow(item = item)
            }
        }
    }
}
```

## 表单和输入

### 文本字段

```kotlin
@Composable
fun LoginForm(
    onLogin: (email: String, password: String) -> Unit
) {
    var email by rememberSaveable { mutableStateOf("") }
    var password by rememberSaveable { mutableStateOf("") }
    var passwordVisible by rememberSaveable { mutableStateOf(false) }
    var emailError by remember { mutableStateOf<String?>(null) }

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        OutlinedTextField(
            value = email,
            onValueChange = {
                email = it
                emailError = if (it.isValidEmail()) null else "无效的邮箱地址"
            },
            label = { Text("邮箱") },
            placeholder = { Text("name@example.com") },
            leadingIcon = { Icon(Icons.Default.Email, null) },
            isError = emailError != null,
            supportingText = emailError?.let { { Text(it) } },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("密码") },
            leadingIcon = { Icon(Icons.Default.Lock, null) },
            trailingIcon = {
                IconButton(onClick = { passwordVisible = !passwordVisible }) {
                    Icon(
                        if (passwordVisible) Icons.Default.VisibilityOff
                        else Icons.Default.Visibility,
                        contentDescription = "切换密码可见性"
                    )
                }
            },
            visualTransformation = if (passwordVisible)
                VisualTransformation.None
            else
                PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { onLogin(email, password) },
            modifier = Modifier.fillMaxWidth(),
            enabled = email.isNotEmpty() && password.isNotEmpty() && emailError == null
        ) {
            Text("登录")
        }
    }
}
```

### 搜索栏

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchableScreen(
    items: List<Item>,
    onItemClick: (Item) -> Unit
) {
    var query by rememberSaveable { mutableStateOf("") }
    var expanded by rememberSaveable { mutableStateOf(false) }

    val filteredItems = remember(query, items) {
        if (query.isEmpty()) items
        else items.filter { it.name.contains(query, ignoreCase = true) }
    }

    SearchBar(
        query = query,
        onQueryChange = { query = it },
        onSearch = { expanded = false },
        active = expanded,
        onActiveChange = { expanded = it },
        placeholder = { Text("搜索项目") },
        leadingIcon = { Icon(Icons.Default.Search, null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { query = "" }) {
                    Icon(Icons.Default.Clear, "清除搜索")
                }
            }
        },
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = if (expanded) 0.dp else 16.dp)
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(16.dp)
        ) {
            items(filteredItems) { item ->
                ListItem(
                    headlineContent = { Text(item.name) },
                    supportingContent = { Text(item.description) },
                    modifier = Modifier.clickable {
                        onItemClick(item)
                        expanded = false
                    }
                )
            }
        }
    }
}
```

### 选择控件

```kotlin
@Composable
fun SettingsScreen() {
    var notificationsEnabled by rememberSaveable { mutableStateOf(true) }
    var selectedOption by rememberSaveable { mutableStateOf(0) }
    var expandedDropdown by remember { mutableStateOf(false) }
    var selectedLanguage by rememberSaveable { mutableStateOf("English") }
    val languages = listOf("English", "Spanish", "French", "German")

    Column {
        // 开关
        ListItem(
            headlineContent = { Text("启用通知") },
            supportingContent = { Text("接收推送通知") },
            trailingContent = {
                Switch(
                    checked = notificationsEnabled,
                    onCheckedChange = { notificationsEnabled = it }
                )
            }
        )

        HorizontalDivider()

        // 单选按钮
        Column {
            Text(
                "主题",
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.titleSmall
            )
            listOf("System", "Light", "Dark").forEachIndexed { index, option ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .selectable(
                            selected = selectedOption == index,
                            onClick = { selectedOption = index },
                            role = Role.RadioButton
                        )
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RadioButton(
                        selected = selectedOption == index,
                        onClick = null
                    )
                    Spacer(Modifier.width(16.dp))
                    Text(option)
                }
            }
        }

        HorizontalDivider()

        // 下拉菜单
        ExposedDropdownMenuBox(
            expanded = expandedDropdown,
            onExpandedChange = { expandedDropdown = it },
            modifier = Modifier.padding(16.dp)
        ) {
            OutlinedTextField(
                value = selectedLanguage,
                onValueChange = {},
                readOnly = true,
                label = { Text("语言") },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedDropdown) },
                modifier = Modifier
                    .fillMaxWidth()
                    .menuAnchor()
            )
            ExposedDropdownMenu(
                expanded = expandedDropdown,
                onDismissRequest = { expandedDropdown = false }
            ) {
                languages.forEach { language ->
                    DropdownMenuItem(
                        text = { Text(language) },
                        onClick = {
                            selectedLanguage = language
                            expandedDropdown = false
                        },
                        contentPadding = ExposedDropdownMenuDefaults.ItemContentPadding
                    )
                }
            }
        }
    }
}
```

## 对话框和底部表单

### 警告对话框

```kotlin
@Composable
fun DeleteConfirmationDialog(
    itemName: String,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        icon = {
            Icon(
                Icons.Default.Warning,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.error
            )
        },
        title = {
            Text("删除项目?")
        },
        text = {
            Text("确定要删除 \"$itemName\" 吗? 此操作无法撤销。")
        },
        confirmButton = {
            TextButton(
                onClick = onConfirm,
                colors = ButtonDefaults.textButtonColors(
                    contentColor = MaterialTheme.colorScheme.error
                )
            ) {
                Text("删除")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("取消")
            }
        }
    )
}
```

### 模态底部表单

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OptionsBottomSheet(
    onDismiss: () -> Unit,
    onOptionSelected: (String) -> Unit
) {
    val sheetState = rememberModalBottomSheetState()

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        dragHandle = { BottomSheetDefaults.DragHandle() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 32.dp)
        ) {
            Text(
                "选项",
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                style = MaterialTheme.typography.titleMedium
            )

            listOf(
                Triple(Icons.Default.Share, "分享", "share"),
                Triple(Icons.Default.Edit, "编辑", "edit"),
                Triple(Icons.Default.FileCopy, "复制", "duplicate"),
                Triple(Icons.Default.Delete, "删除", "delete")
            ).forEach { (icon, label, action) ->
                ListItem(
                    headlineContent = { Text(label) },
                    leadingContent = {
                        Icon(
                            icon,
                            contentDescription = null,
                            tint = if (action == "delete")
                                MaterialTheme.colorScheme.error
                            else
                                MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    },
                    modifier = Modifier.clickable { onOptionSelected(action) }
                )
            }
        }
    }
}
```

### 日期和时间选择器

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateTimePickerExample() {
    var showDatePicker by remember { mutableStateOf(false) }
    var showTimePicker by remember { mutableStateOf(false) }
    val datePickerState = rememberDatePickerState()
    val timePickerState = rememberTimePickerState()

    Column(modifier = Modifier.padding(16.dp)) {
        OutlinedButton(onClick = { showDatePicker = true }) {
            Icon(Icons.Default.CalendarToday, null)
            Spacer(Modifier.width(8.dp))
            Text(
                datePickerState.selectedDateMillis?.let {
                    SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
                        .format(Date(it))
                } ?: "选择日期"
            )
        }

        Spacer(Modifier.height(16.dp))

        OutlinedButton(onClick = { showTimePicker = true }) {
            Icon(Icons.Default.Schedule, null)
            Spacer(Modifier.width(8.dp))
            Text(
                String.format("%02d:%02d", timePickerState.hour, timePickerState.minute)
            )
        }
    }

    if (showDatePicker) {
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = { showDatePicker = false }) {
                    Text("确定")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDatePicker = false }) {
                    Text("取消")
                }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }

    if (showTimePicker) {
        AlertDialog(
            onDismissRequest = { showTimePicker = false },
            confirmButton = {
                TextButton(onClick = { showTimePicker = false }) {
                    Text("确定")
                }
            },
            dismissButton = {
                TextButton(onClick = { showTimePicker = false }) {
                    Text("取消")
                }
            },
            text = {
                TimePicker(state = timePickerState)
            }
        )
    }
}
```

## 加载状态

### 进度指示器

```kotlin
@Composable
fun LoadingStates() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        // 不确定圆形进度
        CircularProgressIndicator()

        // 确定圆形进度
        CircularProgressIndicator(
            progress = { 0.7f },
            strokeWidth = 4.dp
        )

        // 不确定线性进度
        LinearProgressIndicator(modifier = Modifier.fillMaxWidth())

        // 确定线性进度
        LinearProgressIndicator(
            progress = { 0.7f },
            modifier = Modifier.fillMaxWidth()
        )
    }
}
```

### 骨架屏加载

```kotlin
@Composable
fun SkeletonLoader(
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "skeleton")
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 0.7f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "alpha"
    )

    Column(
        modifier = modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        repeat(5) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = alpha))
                )
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Box(
                        modifier = Modifier
                            .height(16.dp)
                            .fillMaxWidth(0.7f)
                            .clip(RoundedCornerShape(4.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = alpha))
                    )
                    Box(
                        modifier = Modifier
                            .height(12.dp)
                            .fillMaxWidth(0.5f)
                            .clip(RoundedCornerShape(4.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = alpha))
                    )
                }
            }
        }
    }
}
```

### 内容加载模式

```kotlin
@Composable
fun <T> AsyncContent(
    state: AsyncState<T>,
    onRetry: () -> Unit,
    content: @Composable (T) -> Unit
) {
    when (state) {
        is AsyncState.Loading -> {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        }
        is AsyncState.Success -> {
            content(state.data)
        }
        is AsyncState.Error -> {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(
                    Icons.Default.Error,
                    contentDescription = null,
                    modifier = Modifier.size(64.dp),
                    tint = MaterialTheme.colorScheme.error
                )
                Spacer(Modifier.height(16.dp))
                Text(
                    "出错了",
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    state.message,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.height(24.dp))
                Button(onClick = onRetry) {
                    Text("重试")
                }
            }
        }
    }
}

sealed class AsyncState<out T> {
    object Loading : AsyncState<Nothing>()
    data class Success<T>(val data: T) : AsyncState<T>()
    data class Error(val message: String) : AsyncState<Nothing>()
}
```

## 动画

### 动画可见性

```kotlin
@Composable
fun ExpandableCard(
    title: String,
    content: String
) {
    var expanded by rememberSaveable { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .clickable { expanded = !expanded }
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                Icon(
                    if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                    contentDescription = if (expanded) "收起" else "展开"
                )
            }

            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically() + fadeIn(),
                exit = shrinkVertically() + fadeOut()
            ) {
                Text(
                    text = content,
                    modifier = Modifier.padding(top = 12.dp),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
```

### 动画内容

```kotlin
@Composable
fun AnimatedCounter(count: Int) {
    AnimatedContent(
        targetState = count,
        transitionSpec = {
            if (targetState > initialState) {
                slideInVertically { -it } + fadeIn() togetherWith
                    slideOutVertically { it } + fadeOut()
            } else {
                slideInVertically { it } + fadeIn() togetherWith
                    slideOutVertically { -it } + fadeOut()
            }.using(SizeTransform(clip = false))
        },
        label = "counter"
    ) { targetCount ->
        Text(
            text = "$targetCount",
            style = MaterialTheme.typography.displayMedium
        )
    }
}
```

### 手势动画

```kotlin
@Composable
fun SwipeableCard(
    onSwipeLeft: () -> Unit,
    onSwipeRight: () -> Unit,
    content: @Composable () -> Unit
) {
    var offsetX by remember { mutableFloatStateOf(0f) }
    val animatedOffset by animateFloatAsState(
        targetValue = offsetX,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy),
        label = "offset"
    )

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .offset { IntOffset(animatedOffset.roundToInt(), 0) }
            .pointerInput(Unit) {
                detectHorizontalDragGestures(
                    onDragEnd = {
                        when {
                            offsetX > 200f -> {
                                onSwipeRight()
                                offsetX = 0f
                            }
                            offsetX < -200f -> {
                                onSwipeLeft()
                                offsetX = 0f
                            }
                            else -> offsetX = 0f
                        }
                    },
                    onHorizontalDrag = { _, dragAmount ->
                        offsetX += dragAmount
                    }
                )
            }
    ) {
        content()
    }
}
```
