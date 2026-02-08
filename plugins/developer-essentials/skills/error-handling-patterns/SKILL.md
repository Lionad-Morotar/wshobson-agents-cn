---
name: error-handling-patterns
description: 掌握跨语言的错误处理模式，包括异常、Result 类型、错误传播和优雅降级，以构建弹性应用程序。在实施错误处理、设计 API 或提高应用程序可靠性时使用。
---

# 错误处理模式

使用强大的错误处理策略构建弹性应用程序，优雅地处理故障并提供出色的调试体验。

## 何时使用此技能

- 在新功能中实施错误处理
- 设计错误弹性 API
- 调试生产问题
- 提高应用程序可靠性
- 为用户和开发人员创建更好的错误消息
- 实施重试和断路器模式
- 处理异步/并发错误
- 构建容错分布式系统

## 核心概念

### 1. 错误处理理念

**异常 vs Result 类型：**

- **异常**：传统 try-catch，中断控制流
- **Result 类型**：显式成功/失败，函数式方法
- **错误代码**：C 风格，需要纪律
- **Option/Maybe 类型**：用于可空值

**何时使用每种：**

- 异常：意外错误、异常条件
- Result 类型：预期错误、验证失败
- Panics/崩溃：不可恢复错误、编程错误

### 2. 错误类别

**可恢复错误：**

- 网络超时
- 缺失文件
- 无效用户输入
- API 速率限制

**不可恢复错误：**

- 内存不足
- 栈溢出
- 编程错误（空指针等）

## 语言特定模式

### Python 错误处理

**自定义异常层次结构：**

```python
class ApplicationError(Exception):
    """所有应用程序错误的基本异常。"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationError(ApplicationError):
    """验证失败时引发。"""
    pass

class NotFoundError(ApplicationError):
    """未找到资源时引发。"""
    pass

class ExternalServiceError(ApplicationError):
    """外部服务失败时引发。"""
    def __init__(self, message: str, service: str, **kwargs):
        super().__init__(message, **kwargs)
        self.service = service

# 使用
def get_user(user_id: str) -> User:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise NotFoundError(
            f"User not found",
            code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )
    return user
```

**清理的上下文管理器：**

```python
from contextlib import contextmanager

@contextmanager
def database_transaction(session):
    """确保事务已提交或回滚。"""
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

# 使用
with database_transaction(db.session) as session:
    user = User(name="Alice")
    session.add(user)
    # 自动提交或回滚
```

**指数退避重试：**

```python
import time
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar('T')

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """带有指数退避的重试装饰器。"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        time.sleep(sleep_time)
                        continue
                    raise
            raise last_exception
        return wrapper
    return decorator

# 使用
@retry(max_attempts=3, exceptions=(NetworkError,))
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### TypeScript/JavaScript 错误处理

**自定义错误类：**

```typescript
// 自定义错误类
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: Record<string, any>,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends ApplicationError {
  constructor(message: string, details?: Record<string, any>) {
    super(message, "VALIDATION_ERROR", 400, details);
  }
}

class NotFoundError extends ApplicationError {
  constructor(resource: string, id: string) {
    super(`${resource} not found`, "NOT_FOUND", 404, { resource, id });
  }
}

// 使用
function getUser(id: string): User {
  const user = users.find((u) => u.id === id);
  if (!user) {
    throw new NotFoundError("User", id);
  }
  return user;
}
```

**Result 类型模式：**

```typescript
// 用于显式错误处理的 Result 类型
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

// 辅助函数
function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// 使用
function parseJSON<T>(json: string): Result<T, SyntaxError> {
  try {
    const value = JSON.parse(json) as T;
    return Ok(value);
  } catch (error) {
    return Err(error as SyntaxError);
  }
}

// 消费 Result
const result = parseJSON<User>(userJson);
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error("Parse failed:", result.error.message);
}

// 链接 Results
function chain<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>,
): Result<U, E> {
  return result.ok ? fn(result.value) : result;
}
```

**异步错误处理：**

```typescript
// 带适当错误处理的 async/await
async function fetchUserOrders(userId: string): Promise<Order[]> {
  try {
    const user = await getUser(userId);
    const orders = await getOrders(user.id);
    return orders;
  } catch (error) {
    if (error instanceof NotFoundError) {
      return []; // 为未找到返回空数组
    }
    if (error instanceof NetworkError) {
      // 重试逻辑
      return retryFetchOrders(userId);
    }
    // 重新抛出意外错误
    throw error;
  }
}

// Promise 错误处理
function fetchData(url: string): Promise<Data> {
  return fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new NetworkError(`HTTP ${response.status}`);
      }
      return response.json();
    })
    .catch((error) => {
      console.error("Fetch failed:", error);
      throw error;
    });
}
```

### Rust 错误处理

**Result 和 Option 类型：**

```rust
use std::fs::File;
use std::io::{self, Read};

// 用于可能失败的操作的 Result 类型
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // ? 运算符传播错误
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// 自定义错误类型
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    NotFound(String),
    Validation(String),
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::Io(error)
    }
}

// 使用自定义错误类型
fn read_number_from_file(path: &str) -> Result<i32, AppError> {
    let contents = read_file(path)?;  // 自动转换 io::Error
    let number = contents.trim().parse()
        .map_err(AppError::Parse)?;   // 显式转换 ParseIntError
    Ok(number)
}

// Option 用于可空值
fn find_user(id: &str) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// 组合 Option 和 Result
fn get_user_age(id: &str) -> Result<u32, AppError> {
    find_user(id)
        .ok_or_else(|| AppError::NotFound(id.to_string()))
        .map(|user| user.age)
}
```

### Go 错误处理

**显式错误返回：**

```go
// 基本错误处理
func getUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to query user: %w", err)
    }
    if user == nil {
        return nil, errors.New("user not found")
    }
    return user, nil
}

// 自定义错误类型
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

// 用于比较的哨兵错误
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

// 错误检查
user, err := getUser("123")
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // 处理未找到
    } else {
        // 处理其他错误
    }
}

// 错误包装和解包
func processUser(id string) error {
    user, err := getUser(id)
    if err != nil {
        return fmt.Errorf("process user failed: %w", err)
    }
    // 处理用户
    return nil
}

// 解包错误
err := processUser("123")
if err != nil {
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Printf("Validation error: %s\n", valErr.Field)
    }
}
```

## 通用模式

### 模式 1：断路器

防止分布式系统中的级联故障。

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, TypeVar

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"       # 正常操作
    OPEN = "open"          # 失败，拒绝请求
    HALF_OPEN = "half_open"  # 测试是否恢复

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: timedelta = timedelta(seconds=60),
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func: Callable[[], T]) -> T:
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# 使用
circuit_breaker = CircuitBreaker()

def fetch_data():
    return circuit_breaker.call(lambda: external_api.get_data())
```

### 模式 2：错误聚合

收集多个错误而不是在第一个错误时失败。

```typescript
class ErrorCollector {
  private errors: Error[] = [];

  add(error: Error): void {
    this.errors.push(error);
  }

  hasErrors(): boolean {
    return this.errors.length > 0;
  }

  getErrors(): Error[] {
    return [...this.errors];
  }

  throw(): never {
    if (this.errors.length === 1) {
      throw this.errors[0];
    }
    throw new AggregateError(
      this.errors,
      `${this.errors.length} errors occurred`,
    );
  }
}

// 使用：验证多个字段
function validateUser(data: any): User {
  const errors = new ErrorCollector();

  if (!data.email) {
    errors.add(new ValidationError("Email is required"));
  } else if (!isValidEmail(data.email)) {
    errors.add(new ValidationError("Email is invalid"));
  }

  if (!data.name || data.name.length < 2) {
    errors.add(new ValidationError("Name must be at least 2 characters"));
  }

  if (!data.age || data.age < 18) {
    errors.add(new ValidationError("Age must be 18 or older"));
  }

  if (errors.hasErrors()) {
    errors.throw();
  }

  return data as User;
}
```

### 模式 3：优雅降级

当错误发生时提供后备功能。

```python
from typing import Optional, Callable, TypeVar

T = TypeVar('T')

def with_fallback(
    primary: Callable[[], T],
    fallback: Callable[[], T],
    log_error: bool = True
) -> T:
    """尝试主函数，错误时回退到后备函数。"""
    try:
        return primary()
    except Exception as e:
        if log_error:
            logger.error(f"Primary function failed: {e}")
        return fallback()

# 使用
def get_user_profile(user_id: str) -> UserProfile:
    return with_fallback(
        primary=lambda: fetch_from_cache(user_id),
        fallback=lambda: fetch_from_database(user_id)
    )

# 多个后备
def get_exchange_rate(currency: str) -> float:
    return (
        try_function(lambda: api_provider_1.get_rate(currency))
        or try_function(lambda: api_provider_2.get_rate(currency))
        or try_function(lambda: cache.get_rate(currency))
        or DEFAULT_RATE
    )

def try_function(func: Callable[[], Optional[T]]) -> Optional[T]:
    try:
        return func()
    except Exception:
        return None
```

## 最佳实践

1. **快速失败**：尽早验证输入，快速失败
2. **保留上下文**：包括堆栈跟踪、元数据、时间戳
3. **有意义的消息**：解释发生了什么以及如何修复
4. **适当日志记录**：错误 = 日志，预期失败 = 不滥用日志
5. **在正确的级别处理**：在可以有意义的处理的地方捕获
6. **清理资源**：使用 try-finally、上下文管理器、defer
7. **不要吞并错误**：记录或重新抛出，不要静默忽略
8. **类型安全错误**：尽可能使用类型化错误

```python
# 好的错误处理示例
def process_order(order_id: str) -> Order:
    """处理订单的综合错误处理。"""
    try:
        # 验证输入
        if not order_id:
            raise ValidationError("Order ID is required")

        # 获取订单
        order = db.get_order(order_id)
        if not order:
            raise NotFoundError("Order", order_id)

        # 处理支付
        try:
            payment_result = payment_service.charge(order.total)
        except PaymentServiceError as e:
            # 记录并包装外部服务错误
            logger.error(f"Payment failed for order {order_id}: {e}")
            raise ExternalServiceError(
                f"Payment processing failed",
                service="payment_service",
                details={"order_id": order_id, "amount": order.total}
            ) from e

        # 更新订单
        order.status = "completed"
        order.payment_id = payment_result.id
        db.save(order)

        return order

    except ApplicationError:
        # 重新抛出已知的应用程序错误
        raise
    except Exception as e:
        # 记录意外错误
        logger.exception(f"Unexpected error processing order {order_id}")
        raise ApplicationError(
            "Order processing failed",
            code="INTERNAL_ERROR"
        ) from e
```

## 常见陷阱

- **捕获过于广泛**：`except Exception` 隐藏错误
- **空 Catch 块**：静默吞并错误
- **记录并重新抛出**：创建重复的日志条目
- **不清理**：忘记关闭文件、连接
- **糟糕的错误消息**："Error occurred" 没有帮助
- **返回错误代码**：使用异常或 Result 类型
- **忽略异步错误**：未处理的 Promise 拒绝

## 资源

- **references/exception-hierarchy-design.md**：设计错误类层次结构
- **references/error-recovery-strategies.md**：不同场景的恢复模式
- **references/async-error-handling.md**：处理并发代码中的错误
- **assets/error-handling-checklist.md**：错误处理审查清单
- **assets/error-message-guide.md**：编写有用的错误消息
- **scripts/error-analyzer.py**：分析日志中的错误模式
