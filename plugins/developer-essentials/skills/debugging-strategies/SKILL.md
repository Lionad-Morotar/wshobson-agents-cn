---
name: debugging-strategies
description: 掌握系统调试技术、分析工具和根本原因分析，以高效跟踪任何代码库或技术堆栈中的错误。在调查错误、性能问题或意外行为时使用。
---

# 调试策略

通过经过验证的策略、强大的工具和有条理的方法，将调试从令人沮丧的猜测转变为系统的问题解决。

## 何时使用此技能

- 跟踪难以捉摸的错误
- 调查性能问题
- 理解不熟悉的代码库
- 调试生产问题
- 分析崩溃转储和堆栈跟踪
- 分析应用程序性能
- 调查内存泄漏
- 调试分布式系统

## 核心原则

### 1. 科学方法

**1. 观察**：实际行为是什么？
**2. 假设**：可能是什么原因造成的？
**3. 实验**：测试您的假设
**4. 分析**：是否证明/反驳了您的理论？
**5. 重复**：直到找到根本原因

### 2. 调试思维

**不要假设：**

- "不可能是 X" - 是的，它可能
- "我没有更改 Y" - 无论如何要检查
- "我的机器上可以工作" - 找出原因

**要：**

- 一致地复现
- 隔离问题
- 保留详细记录
- 质疑一切
- 遇到困难时休息一下

### 3. 橡皮鸭调试

大声解释您的代码和问题（给橡皮鸭、同事或您自己）。通常会发现问题。

## 系统调试流程

### 阶段 1：复现

```markdown
## 复现清单

1. **您能复现它吗？**
   - 总是？有时？随机？
   - 需要特定条件吗？
   - 其他人能复现吗？

2. **创建最小复现**
   - 简化为最小的示例
   - 删除不相关的代码
   - 隔离问题

3. **记录步骤**
   - 写下确切的步骤
   - 注意环境细节
   - 捕获错误消息
```

### 阶段 2：收集信息

```markdown
## 信息收集

1. **错误消息**
   - 完整堆栈跟踪
   - 错误代码
   - 控制台/日志输出

2. **环境**
   - 操作系统版本
   - 语言/运行时版本
   - 依赖版本
   - 环境变量

3. **最近的更改**
   - Git 历史
   - 部署时间线
   - 配置更改

4. **范围**
   - 影响所有用户还是特定用户？
   - 所有浏览器还是特定浏览器？
   - 仅生产环境还是开发环境也有？
```

### 阶段 3：形成假设

```markdown
## 假设形成

基于收集的信息，询问：

1. **什么改变了？**
   - 最近的代码更改
   - 依赖更新
   - 基础设施更改

2. **有什么不同？**
   - 工作环境 vs 损坏环境
   - 工作用户 vs 损坏用户
   - 之前 vs 之后

3. **哪里可能失败？**
   - 输入验证
   - 业务逻辑
   - 数据层
   - 外部服务
```

### 阶段 4：测试和验证

```markdown
## 测试策略

1. **二分搜索**
   - 注释掉一半代码
   - 缩小问题部分
   - 重复直到找到

2. **添加日志**
   - 有策略的 console.log/print
   - 跟踪变量值
   - 跟踪执行流程

3. **隔离组件**
   - 分别测试每个部分
   - 模拟依赖
   - 删除复杂性

4. **比较工作 vs 损坏**
   - 比较配置
   - 比较环境
   - 比较数据
```

## 调试工具

### JavaScript/TypeScript 调试

```typescript
// Chrome DevTools 调试器
function processOrder(order: Order) {
  debugger; // 在此处暂停执行

  const total = calculateTotal(order);
  console.log("总计：", total);

  // 条件断点
  if (order.items.length > 10) {
    debugger; // 仅在条件为真时中断
  }

  return total;
}

// 控制台调试技术
console.log("值：", value); // 基本
console.table(arrayOfObjects); // 表格格式
console.time("operation");
/* 代码 */ console.timeEnd("operation"); // 计时
console.trace(); // 堆栈跟踪
console.assert(value > 0, "值必须为正"); // 断言

// 性能分析
performance.mark("start-operation");
// ... 操作代码
performance.mark("end-operation");
performance.measure("operation", "start-operation", "end-operation");
console.log(performance.getEntriesByType("measure"));
```

**VS Code 调试器配置：**

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "调试程序",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "node",
      "request": "launch",
      "name": "调试测试",
      "program": "${workspaceFolder}/node_modules/jest/bin/jest",
      "args": ["--runInBand", "--no-cache"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Python 调试

```python
# 内置调试器 (pdb)
import pdb

def calculate_total(items):
    total = 0
    pdb.set_trace()  # 调试器从此处开始

    for item in items:
        total += item.price * item.quantity

    return total

# 断点 (Python 3.7+)
def process_order(order):
    breakpoint()  # 比 pdb.set_trace() 更方便
    # ... 代码

# 事后调试
try:
    risky_operation()
except Exception:
    import pdb
    pdb.post_mortem()  # 在异常点调试

# IPython 调试 (ipdb)
from ipdb import set_trace
set_trace()  # 比 pdb 更好的界面

# 用于调试的日志记录
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_user(user_id):
    logger.debug(f'正在获取用户：{user_id}')
    user = db.query(User).get(user_id)
    logger.debug(f'找到用户：{user}')
    return user

# 性能分析
import cProfile
import pstats

cProfile.run('slow_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # 最慢的前 10 个
```

### Go 调试

```go
// Delve 调试器
// 安装：go install github.com/go-delve/delve/cmd/dlv@latest
// 运行：dlv debug main.go

import (
    "fmt"
    "runtime"
    "runtime/debug"
)

// 打印堆栈跟踪
func debugStack() {
    debug.PrintStack()
}

// 带调试的恐慌恢复
func processRequest() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("恐慌：", r)
            debug.PrintStack()
        }
    }()

    // ... 可能恐慌的代码
}

// 内存分析
import _ "net/http/pprof"
// 访问 http://localhost:6060/debug/pprof/

// CPU 分析
import (
    "os"
    "runtime/pprof"
)

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... 要分析的代码
```

## 高级调试技术

### 技术 1：二分搜索调试

```bash
# 用于查找回归的 Git bisect
git bisect start
git bisect bad                    # 当前提交是坏的
git bisect good v1.0.0            # v1.0.0 是好的

# Git 检出中间提交
# 测试它，然后：
git bisect good   # 如果它工作
git bisect bad    # 如果它损坏

# 继续直到发现错误
git bisect reset  # 完成后
```

### 技术 2：差异调试

比较工作 vs 损坏：

```markdown
## 有什么不同？

| 方面       | 工作        | 损坏        |
| ---------- | ----------- | ----------- |
| 环境       | 开发        | 生产        |
| Node 版本  | 18.16.0     | 18.15.0     |
| 数据       | 空 DB       | 100 万条记录 |
| 用户       | 管理员      | 普通用户    |
| 浏览器     | Chrome      | Safari      |
| 时间       | 白天        | 午夜之后    |

假设：基于时间的问题？检查时区处理。
```

### 技术 3：跟踪调试

```typescript
// 函数调用跟踪
function trace(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor,
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`正在调用 ${propertyKey}，参数：`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} 返回：`, result);
    return result;
  };

  return descriptor;
}

class OrderService {
  @trace
  calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

### 技术 4：内存泄漏检测

```typescript
// Chrome DevTools 内存分析器
// 1. 获取堆快照
// 2. 执行操作
// 3. 获取另一个快照
// 4. 比较快照

// Node.js 内存调试
if (process.memoryUsage().heapUsed > 500 * 1024 * 1024) {
  console.warn("高内存使用：", process.memoryUsage());

  // 生成堆转储
  require("v8").writeHeapSnapshot();
}

// 在测试中发现内存泄漏
let beforeMemory: number;

beforeEach(() => {
  beforeMemory = process.memoryUsage().heapUsed;
});

afterEach(() => {
  const afterMemory = process.memoryUsage().heapUsed;
  const diff = afterMemory - beforeMemory;

  if (diff > 10 * 1024 * 1024) {
    // 10MB 阈值
    console.warn(`可能的内存泄漏：${diff / 1024 / 1024}MB`);
  }
});
```

## 按问题类型的调试模式

### 模式 1：间歇性错误

```markdown
## 不稳定错误的策略

1. **添加大量日志**
   - 记录时序信息
   - 记录所有状态转换
   - 记录外部交互

2. **查找竞态条件**
   - 对共享状态的并发访问
   - 异步操作乱序完成
   - 缺少同步

3. **检查时序依赖**
   - setTimeout/setInterval
   - Promise 解析顺序
   - 动画帧时序

4. **压力测试**
   - 运行多次
   - 改变时序
   - 模拟负载
```

### 模式 2：性能问题

```markdown
## 性能调试

1. **首先分析**
   - 不要盲目优化
   - 优化前后测量
   - 找到瓶颈

2. **常见罪魁祸首**
   - N+1 查询
   - 不必要的重渲染
   - 大数据处理
   - 同步 I/O

3. **工具**
   - 浏览器 DevTools 性能选项卡
   - Lighthouse
   - Python: cProfile, line_profiler
   - Node: clinic.js, 0x
```

### 模式 3：生产错误

```markdown
## 生产调试

1. **收集证据**
   - 错误跟踪 (Sentry, Bugsnag)
   - 应用程序日志
   - 用户报告
   - 指标/监控

2. **本地复现**
   - 使用生产数据（匿名化）
   - 匹配环境
   - 遵循确切的步骤

3. **安全调查**
   - 不要更改生产环境
   - 使用功能标志
   - 添加监控/日志
   - 在暂存中测试修复
```

## 最佳实践

1. **首先复现**：无法复现就无法修复
2. **隔离问题**：删除复杂性直到最小情况
3. **阅读错误消息**：它们通常有帮助
4. **检查最近的更改**：大多数错误是最近的
5. **使用版本控制**：Git bisect、blame、历史
6. **休息一下**：新鲜的眼睛看得更清楚
7. **记录发现**：帮助未来的您
8. **修复根本原因**：而不仅仅是症状

## 常见调试错误

- **进行多项更改**：一次更改一件事
- **不阅读错误消息**：阅读完整的堆栈跟踪
- **假设它很复杂**：通常它很简单
- **生产中的调试日志**：发布前删除
- **不使用调试器**：console.log 并不总是最好的
- **过早放弃**：坚持会有回报
- **不测试修复**：验证它真的有效

## 快速调试清单

```markdown
## 遇到困难时，检查：

- [ ] 拼写错误（变量名中的拼写错误）
- [ ] 大小写敏感（fileName vs filename）
- [ ] 空/未定义值
- [ ] 数组索引差一
- [ ] 异步时序（竞态条件）
- [ ] 范围问题（闭包、提升）
- [ ] 类型不匹配
- [ ] 缺少依赖
- [ ] 环境变量
- [ ] 文件路径（绝对 vs 相对）
- [ ] 缓存问题（清除缓存）
- [ ] 陈旧数据（刷新数据库）
```

## 资源

- **references/debugging-tools-guide.md**：综合工具文档
- **references/performance-profiling.md**：性能调试指南
- **references/production-debugging.md**：调试实时系统
- **assets/debugging-checklist.md**：快速参考清单
- **assets/common-bugs.md**：常见错误模式
- **scripts/debug-helper.ts**：调试实用函数
