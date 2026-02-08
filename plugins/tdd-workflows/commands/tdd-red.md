编写符合 TDD 红色阶段原则的全面失败测试。

[扩展思考：使用 test-automator 智能体生成能够正确定义预期行为的失败测试。]

## 角色

使用 Task 工具生成失败测试，设置 subagent_type="unit-testing::test-automator"。

## 提示词模板

"为以下内容生成全面的失败测试：$ARGUMENTS

## 核心要求

1. **测试结构**
   - 框架适配的设置（Jest/pytest/JUnit/Go/RSpec）
   - 安排-执行-断言模式（Arrange-Act-Assert）
   - should_X_when_Y 命名规范
   - 无相互依赖的独立测试夹具

2. **行为覆盖**
   - 正常路径场景（Happy path）
   - 边界情况（空值、null、边界值）
   - 错误处理和异常
   - 并发访问（如适用）

3. **失败验证**
   - 测试运行时必须失败
   - 因正确原因失败（非语法/导入错误）
   - 有意义的诊断错误消息
   - 无级联失败

4. **测试类别**
   - 单元测试：隔离的组件行为
   - 集成测试：组件交互
   - 契约测试：API/接口契约
   - 属性测试：数学不变式

## 框架模式

**JavaScript/TypeScript (Jest/Vitest)**

- 使用 `vi.fn()` 或 `jest.fn()` 模拟依赖
- 使用 `@testing-library` 测试 React 组件
- 使用 `fast-check` 进行属性测试

**Python (pytest)**

- 使用适当作用域的 fixtures
- 使用参数化处理多个测试用例
- 使用 Hypothesis 进行基于属性的测试

**Go**

- 使用子测试进行表驱动测试
- 使用 `t.Parallel()` 进行并行执行
- 使用 `testify/assert` 获得更清晰的断言

**Ruby (RSpec)**

- 使用 `let` 进行延迟加载，`let!` 进行立即加载
- 使用 contexts 描述不同场景
- 使用 shared examples 描述通用行为

## 质量检查清单

- 可读的测试名称，能够记录意图
- 每个测试一个行为
- 无实现细节泄露
- 有意义的测试数据（而非 'foo'/'bar'）
- 测试作为活文档

## 应避免的反模式

- 测试立即通过
- 测试实现而非行为
- 复杂的设置代码
- 每个测试多个职责
- 脆弱的测试与具体实现强耦合

## 边界情况类别

- **空值/Null**：undefined、null、空字符串/数组/对象
- **边界**：最小/最大值、单个元素、容量限制
- **特殊情况**：Unicode、空白字符、特殊字符
- **状态**：无效转换、并发修改
- **错误**：网络故障、超时、权限

## 输出要求

- 包含导入的完整测试文件
- 测试目的文档
- 运行和验证失败的命令
- 指标：测试数量、覆盖区域
- 绿色阶段的后续步骤"

## 验证

生成后：

1. 运行测试 - 确认它们失败
2. 验证失败消息是否有帮助
3. 检查测试独立性
4. 确保全面覆盖

## 示例（最小化）

```typescript
// auth.service.test.ts
describe("AuthService", () => {
  let authService: AuthService;
  let mockUserRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepo = { findByEmail: jest.fn() } as any;
    authService = new AuthService(mockUserRepo);
  });

  it("should_return_token_when_valid_credentials", async () => {
    const user = { id: "1", email: "test@example.com", passwordHash: "hashed" };
    mockUserRepo.findByEmail.mockResolvedValue(user);

    const result = await authService.authenticate("test@example.com", "pass");

    expect(result.success).toBe(true);
    expect(result.token).toBeDefined();
  });

  it("should_fail_when_user_not_found", async () => {
    mockUserRepo.findByEmail.mockResolvedValue(null);

    const result = await authService.authenticate("none@example.com", "pass");

    expect(result.success).toBe(false);
    expect(result.error).toBe("INVALID_CREDENTIALS");
  });
});
```

测试要求：$ARGUMENTS
