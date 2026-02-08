借助全面的测试安全网，自信地重构代码：

[扩展思考：此工具使用 tdd-orchestrator 智能体（opus 模型）进行复杂的重构，同时保持所有测试通过。它应用设计模式、改进代码质量，并在全面测试覆盖的安全保障下优化性能。]

## 使用方法

使用 Task 工具并设置 subagent_type="tdd-orchestrator" 来执行安全重构。

提示词："在保持所有测试通过的情况下重构此代码：$ARGUMENTS。应用 TDD 重构阶段：

## 核心流程

**1. 预评估**

- 运行测试以建立通过的基线
- 分析代码异味和测试覆盖率
- 记录当前性能指标
- 制定增量重构计划

**2. 代码异味检测**

- 重复代码 → 提取方法/类
- 长方法 → 分解为专注的函数
- 大型类 → 拆分职责
- 长参数列表 → 参数对象
- 特性依恋 → 将方法移至合适的类
- 基本类型偏执 → 值对象
- Switch 语句 → 多态
- 死代码 → 删除

**3. 设计模式**

- 应用创建型模式（工厂、建造者、单例）
- 应用结构型模式（适配器、外观、装饰器）
- 应用行为型模式（策略、观察者、命令）
- 应用领域模式（仓储、服务、值对象）
- 仅在能带来明确价值的地方使用模式

**4. SOLID 原则**

- 单一职责原则：只有一个改变的理由
- 开闭原则：对扩展开放，对修改封闭
- 里氏替换原则：子类型可替换
- 接口隔离原则：小而专注的接口
- 依赖倒置原则：依赖抽象

**5. 重构技术**

- 提取方法/变量/接口
- 内联不必要的间接层
- 重命名以提高清晰度
- 将方法/字段移至合适的类
- 用常量替换魔术数字
- 封装字段
- 用多态替换条件表达式
- 引入空对象

**6. 性能优化**

- 性能分析以识别瓶颈
- 优化算法和数据结构
- 在有益的地方实现缓存
- 减少数据库查询（消除 N+1）
- 延迟加载和分页
- 始终在优化前后进行测量

**7. 增量步骤**

- 进行小的、原子性的更改
- 每次修改后运行测试
- 每次成功重构后提交
- 将重构与行为更改分离
- 需要时使用脚手架

**8. 架构演进**

- 分层分离和依赖管理
- 模块边界和接口定义
- 用于解耦的事件驱动模式
- 数据库访问模式优化

**9. 安全验证**

- 每次更改后运行完整测试套件
- 性能回归测试
- 变异测试以评估测试有效性
- 重大更改的回滚计划

**10. 高级模式**

- 绞杀者模式：渐进式遗留系统替换
- 抽象分支：大规模更改
- 并行更改：扩展-收缩模式
- Mikado 方法：依赖图导航

## 输出要求

- 应用了改进的重构代码
- 测试结果（全部通过）
- 优化前后指标对比
- 已应用的重构技术列表
- 性能改进测量
- 剩余技术债务评估

## 安全检查清单

提交之前：

- ✓ 所有测试通过（100% 通过）
- ✓ 无功能回归
- ✓ 性能指标可接受
- ✓ 代码覆盖率保持/提升
- ✓ 文档已更新

## 恢复协议

如果测试失败：

- 立即回滚最后的更改
- 识别破坏性的重构
- 应用更小的增量更改
- 使用版本控制进行安全实验

## 示例：提取方法模式

**之前：**

```typescript
class OrderProcessor {
  processOrder(order: Order): ProcessResult {
    // 验证
    if (!order.customerId || order.items.length === 0) {
      return { success: false, error: "Invalid order" };
    }

    // 计算总计
    let subtotal = 0;
    for (const item of order.items) {
      subtotal += item.price * item.quantity;
    }
    let total = subtotal + subtotal * 0.08 + (subtotal > 100 ? 0 : 15);

    // 处理支付...
    // 更新库存...
    // 发送确认...
  }
}
```

**之后：**

```typescript
class OrderProcessor {
  async processOrder(order: Order): Promise<ProcessResult> {
    const validation = this.validateOrder(order);
    if (!validation.isValid) return ProcessResult.failure(validation.error);

    const orderTotal = OrderTotal.calculate(order);
    const inventoryCheck = await this.inventoryService.checkAvailability(
      order.items,
    );
    if (!inventoryCheck.available)
      return ProcessResult.failure(inventoryCheck.reason);

    await this.paymentService.processPayment(
      order.paymentMethod,
      orderTotal.total,
    );
    await this.inventoryService.reserveItems(order.items);
    await this.notificationService.sendOrderConfirmation(order, orderTotal);

    return ProcessResult.success(order.id, orderTotal.total);
  }

  private validateOrder(order: Order): ValidationResult {
    if (!order.customerId)
      return ValidationResult.invalid("Customer ID required");
    if (order.items.length === 0)
      return ValidationResult.invalid("Order must contain items");
    return ValidationResult.valid();
  }
}
```

**已应用：** 提取方法、值对象、依赖注入、异步模式

待重构代码：$ARGUMENTS"
