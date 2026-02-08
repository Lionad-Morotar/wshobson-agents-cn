---
name: code-review-excellence
description: 掌握有效的代码评审实践，提供建设性反馈，及早发现错误，并在保持团队士气的同时促进知识共享。在评审拉取请求、建立评审标准或指导开发人员时使用。
---

# 代码评审卓越

通过建设性反馈、系统分析和协作改进，将代码评审从守门转变为知识共享。

## 何时使用此技能

- 评审拉取请求和代码变更
- 为团队建立代码评审标准
- 通过评审指导初级开发人员
- 进行架构评审
- 创建评审清单和指南
- 改善团队协作
- 减少代码评审周期时间
- 维护代码质量标准

## 核心原则

### 1. 评审思维

**代码评审的目标：**

- 捕获错误和边缘情况
- 确保代码可维护性
- 在团队间共享知识
- 强制执行编码标准
- 改进设计和架构
- 建立团队文化

**不是目标：**

- 炫耀知识
- 挑剔格式（使用 linter）
- 不必要地阻止进度
- 按您的偏好重写

### 2. 有效反馈

**好的反馈是：**

- 具体且可操作
- 教育性，而非评判性
- 专注于代码，而非个人
- 平衡（也要表扬好的工作）
- 有优先级（关键 vs 有则更好）

```markdown
❌ 差："这是错的。"
✅ 好："当多个用户同时访问时，这可能导致竞态条件。
考虑在这里使用互斥锁。"

❌ 差："你为什么不使用 X 模式？"
✅ 好："你考虑过仓储模式吗？这会让测试更容易。
这里有一个示例：[链接]"

❌ 差："重命名这个变量。"
✅ 好："[nit] 考虑使用 `userCount` 而不是 `uc` 以提高清晰度。
如果您想保留它，不是阻塞问题。"
```

### 3. 评审范围

**要评审什么：**

- 逻辑正确性和边缘情况
- 安全漏洞
- 性能影响
- 测试覆盖率和质量
- 错误处理
- 文档和注释
- API 设计和命名
- 架构适配度

**不要手动评审什么：**

- 代码格式化（使用 Prettier、Black 等）
- 导入组织
- Linting 违规
- 简单的拼写错误

## 评审流程

### 阶段 1：上下文收集（2-3 分钟）

```markdown
在深入代码之前，了解：

1. 阅读 PR 描述和关联的问题
2. 检查 PR 大小（>400 行？要求拆分）
3. 评审 CI/CD 状态（测试通过了吗？）
4. 理解业务需求
5. 注意任何相关的架构决策
```

### 阶段 2：高层评审（5-10 分钟）

```markdown
1. **架构和设计**
   - 解决方案是否适合问题？
   - 有更简单的方法吗？
   - 它是否与现有模式一致？
   - 它能扩展吗？

2. **文件组织**
   - 新文件是否在正确的位置？
   - 代码是否按逻辑分组？
   - 有重复的文件吗？

3. **测试策略**
   - 有测试吗？
   - 测试是否覆盖边缘情况？
   - 测试是否可读？
```

### 阶段 3：逐行评审（10-20 分钟）

```markdown
对于每个文件：

1. **逻辑和正确性**
   - 处理了边缘情况吗？
   - 差一错误？
   - 空/未定义检查？
   - 竞态条件？

2. **安全性**
   - 输入验证？
   - SQL 注入风险？
   - XSS 漏洞？
   - 敏感数据暴露？

3. **性能**
   - N+1 查询？
   - 不必要的循环？
   - 内存泄漏？
   - 阻塞操作？

4. **可维护性**
   - 清晰的变量名？
   - 函数只做一件事？
   - 复杂代码有注释？
   - 魔术数字提取了吗？
```

### 阶段 4：总结和决策（2-3 分钟）

```markdown
1. 总结关键问题
2. 突出您喜欢的内容
3. 做出明确决策：
   - ✅ 批准
   - 💬 评论（小建议）
   - 🔄 请求更改（必须处理）
4. 如果复杂，提议结对编程
```

## 评审技术

### 技术 1：清单方法

```markdown
## 安全清单

- [ ] 用户输入已验证和清理
- [ ] SQL 查询使用参数化
- [ ] 已检查身份验证/授权
- [ ] 机密未硬编码
- [ ] 错误消息不泄露信息

## 性能清单

- [ ] 没有 N+1 查询
- [ ] 数据库查询已索引
- [ ] 大列表已分页
- [ ] 昂贵的操作已缓存
- [ ] 热路径中没有阻塞 I/O

## 测试清单

- [ ] 已测试快乐路径
- [ ] 已覆盖边缘情况
- [ ] 已测试错误情况
- [ ] 测试名称具有描述性
- [ ] 测试是确定性的
```

### 技术 2：提问方法

与其陈述问题，不如提问以鼓励思考：

```markdown
❌ "如果列表为空，这将失败。"
✅ "如果 `items` 是空数组会发生什么？"

❌ "你需要在这里进行错误处理。"
✅ "如果 API 调用失败，这应该如何表现？"

❌ "这是低效的。"
✅ "我看到这会遍历所有用户。我们考虑过 10 万用户的性能影响吗？"
```

### 技术 3：建议，而不是命令

````markdown
## 使用协作语言

❌ "你必须将其更改为使用 async/await"
✅ "建议：async/await 可能会让这更具可读性：
`typescript
    async function fetchUser(id: string) {
        const user = await db.query('SELECT * FROM users WHERE id = ?', id);
        return user;
    }
    `
您觉得怎么样？"

❌ "将其提取为函数"
✅ "这个逻辑出现在 3 个地方。将其提取为共享工具函数有意义吗？"
````

### 技术 4：区分严重性

```markdown
使用标签指示优先级：

🔴 [blocking] - 必须在合并前修复
🟡 [important] - 应该修复，如果有分歧请讨论
🟢 [nit] - 有则更好，不阻塞
💡 [suggestion] - 考虑的替代方法
📚 [learning] - 教育性评论，无需操作
🎉 [praise] - 做得好，继续保持！

示例：
"🔴 [blocking] 此 SQL 查询易受注入攻击。
请使用参数化查询。"

"🟢 [nit] 考虑将 `data` 重命名为 `userData` 以提高清晰度。"

"🎉 [praise] 出色的测试覆盖率！这将捕获边缘情况。"
```

## 语言特定模式

### Python 代码评审

```python
# 检查 Python 特定问题

# ❌ 可变默认参数
def add_item(item, items=[]):  # Bug! 在调用间共享
    items.append(item)
    return items

# ✅ 使用 None 作为默认值
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ❌ 捕获范围太广
try:
    result = risky_operation()
except:  # 捕获所有内容，甚至 KeyboardInterrupt！
    pass

# ✅ 捕获特定异常
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"无效值：{e}")
    raise

# ❌ 使用可变类属性
class User:
    permissions = []  # 在所有实例间共享！

# ✅ 在 __init__ 中初始化
class User:
    def __init__(self):
        self.permissions = []
```

### TypeScript/JavaScript 代码评审

```typescript
// 检查 TypeScript 特定问题

// ❌ 使用 any 会破坏类型安全
function processData(data: any) {  // 避免使用 any
    return data.value;
}

// ✅ 使用适当的类型
interface DataPayload {
    value: string;
}
function processData(data: DataPayload) {
    return data.value;
}

// ❌ 未处理异步错误
async function fetchUser(id: string) {
    const response = await fetch(`/api/users/${id}`);
    return response.json();  // 如果网络失败怎么办？
}

// ✅ 正确处理错误
async function fetchUser(id: string): Promise<User> {
    try {
        const response = await fetch(`/api/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('获取用户失败：', error);
        throw error;
    }
}

// ❌ props 变异
function UserProfile({ user }: Props) {
    user.lastViewed = new Date();  // 变异 prop！
    return <div>{user.name}</div>;
}

// ✅ 不要变异 props
function UserProfile({ user, onView }: Props) {
    useEffect(() => {
        onView(user.id);  // 通知父级更新
    }, [user.id]);
    return <div>{user.name}</div>;
}
```

## 高级评审模式

### 模式 1：架构评审

```markdown
评审重大变更时：

1. **首先编写设计文档**
   - 对于大型功能，在代码之前请求设计文档
   - 在实施前与团队评审设计
   - 就方法达成一致以避免返工

2. **分阶段评审**
   - 第一个 PR：核心抽象和接口
   - 第二个 PR：实施
   - 第三个 PR：集成和测试
   - 更容易评审，更快迭代

3. **考虑替代方案**
   - "我们考虑过使用 [模式/库] 吗？"
   - "与更简单的方法相比有什么权衡？"
   - "当需求变化时，这将如何演变？"
```

### 模式 2：测试质量评审

```typescript
// ❌ 差的测试：实施细节测试
test('计数器变量递增', () => {
    const component = render(<Counter />);
    const button = component.getByRole('button');
    fireEvent.click(button);
    expect(component.state.counter).toBe(1);  // 测试内部状态
});

// ✅ 好的测试：行为测试
test('点击时显示递增计数', () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// 测试评审问题：
// - 测试是否描述行为，而非实施？
// - 测试名称是否清晰且具有描述性？
// - 测试是否覆盖边缘情况？
// - 测试是否独立（无共享状态）？
// - 测试是否可以按任何顺序运行？
```

### 模式 3：安全评审

```markdown
## 安全评审清单

### 身份验证和授权

- [ ] 在需要的地方要求身份验证？
- [ ] 在每个操作之前进行授权检查？
- [ ] JWT 验证是否正确（签名、过期）？
- [ ] API 密钥/机密是否正确保护？

### 输入验证

- [ ] 所有用户输入都已验证？
- [ ] 文件上传受限（大小、类型）？
- [ ] SQL 查询已参数化？
- [ ] XSS 保护（转义输出）？

### 数据保护

- [ ] 密码已哈希（bcrypt/argon2）？
- [ ] 敏感数据静态加密？
- [ ] 对敏感数据强制使用 HTTPS？
- [ ] 根据法规处理 PII？

### 常见漏洞

- [ ] 没有 eval() 或类似的动态执行？
- [ ] 没有硬编码的机密？
- [ ] 状态变更操作的 CSRF 保护？
- [ ] 公共端点的速率限制？
```

## 给予困难的反馈

### 模式：三明治方法（改进版）

```markdown
传统：表扬 + 批评 + 表扬（感觉虚假）

更好：上下文 + 具体问题 + 有用的解决方案

示例：
"我注意到支付处理逻辑内联在控制器中。
这使其更难测试和重用。

[具体问题]
calculateTotal() 函数混合了税收计算、
折扣逻辑和数据库查询，使其难以
单元测试和推理。

[有用的解决方案]
我们可以将其提取为 PaymentService 类吗？
这将使其可测试和可重用。如果有帮助，我可以与您结对。"
```

### 处理分歧

```markdown
当作者不同意您的反馈时：

1. **寻求理解**
   "帮助我理解您的方法。什么导致您
   选择这种模式？"

2. **承认有效的观点**
   "关于 X 这是一个很好的观点。我没有考虑到这一点。"

3. **提供数据**
   "我担心性能。我们可以添加基准测试
   来验证方法吗？"

4. **必要时升级**
   "让我们让 [架构师/高级开发人员] 对此进行权衡。"

5. **知道何时放手**
   如果它工作正常且不是关键问题，请批准它。
   完美是进步的敌人。
```

## 最佳实践

1. **及时评审**：24 小时内，最好是当天
2. **限制 PR 大小**：有效评审最多 200-400 行
3. **按时间段评审**：最多 60 分钟，休息一下
4. **使用评审工具**：GitHub、GitLab 或专用工具
5. **自动化所有可以自动化的内容**：Linter、格式化程序、安全扫描
6. **建立融洽关系**：表情符号、表扬和同理心很重要
7. **保持可用**：提议结对处理复杂问题
8. **向他人学习**：评审他人的评审评论

## 常见陷阱

- **完美主义**：为次要的风格偏好阻止 PR
- **范围蔓延**："既然你在做这个，能不能也..."
- **不一致**：对不同的人有不同的标准
- **延迟评审**：让 PR 停留数天
- **消失**：请求更改然后消失
- **橡皮图章**：未经实际评审就批准
- **过分关注琐事**：广泛辩论琐碎细节

## 模板

### PR 评审评论模板

```markdown
## 摘要

[评审内容的简要概述]

## 优势

- [做得好的地方]
- [好的模式或方法]

## 必要的更改

🔴 [阻塞问题 1]
🔴 [阻塞问题 2]

## 建议

💡 [改进 1]
💡 [改进 2]

## 问题

❓ [需要对 X 进行澄清]
❓ [替代方法考虑]

## 结论

✅ 在处理必要的更改后批准
```

## 资源

- **references/code-review-best-practices.md**：综合评审指南
- **references/common-bugs-checklist.md**：需要注意的语言特定错误
- **references/security-review-guide.md**：以安全为重点的评审清单
- **assets/pr-review-template.md**：标准评审评论模板
- **assets/review-checklist.md**：快速参考清单
- **scripts/pr-analyzer.py**：分析 PR 复杂性并建议评审者
