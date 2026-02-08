---
name: modern-javascript-patterns
description: 掌握 ES6+ 特性，包括 async/await、解构、展开运算符、箭头函数、promise、模块、迭代器、生成器和函数式编程模式，以编写整洁、高效的 JavaScript 代码。在重构遗留代码、实施现代模式或优化 JavaScript 应用程序时使用。
---

# 现代 JavaScript 模式

掌握现代 JavaScript (ES6+) 特性、函数式编程模式和编写整洁、可维护和高性能代码最佳实践的综合指南。

## 何时使用此技能

- 将遗留 JavaScript 重构为现代语法
- 实施函数式编程模式
- 优化 JavaScript 性能
- 编写可维护和可读的代码
- 处理异步操作
- 构建现代 Web 应用程序
- 从回调迁移到 Promises/async-await
- 实施数据转换流水线

## ES6+ 核心特性

### 1. 箭头函数

**语法和用例：**

```javascript
// 传统函数
function add(a, b) {
  return a + b;
}

// 箭头函数
const add = (a, b) => a + b;

// 单个参数（括号可选）
const double = (x) => x * 2;

// 无参数
const getRandom = () => Math.random();

// 多条语句（需要花括号）
const processUser = (user) => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// 返回对象（用括号包裹）
const createUser = (name, age) => ({ name, age });
```

**词法 'this' 绑定：**

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // 箭头函数保留 'this' 上下文
  increment = () => {
    this.count++;
  };

  // 传统函数在回调中丢失 'this'
  incrementTraditional() {
    setTimeout(function () {
      this.count++; // 'this' 是 undefined
    }, 1000);
  }

  // 箭头函数维持 'this'
  incrementArrow() {
    setTimeout(() => {
      this.count++; // 'this' 指向 Counter 实例
    }, 1000);
  }
}
```

### 2. 解构

**对象解构：**

```javascript
const user = {
  id: 1,
  name: "John Doe",
  email: "john@example.com",
  address: {
    city: "New York",
    country: "USA",
  },
};

// 基本解构
const { name, email } = user;

// 重命名变量
const { name: userName, email: userEmail } = user;

// 默认值
const { age = 25 } = user;

// 嵌套解构
const {
  address: { city, country },
} = user;

// 剩余运算符
const { id, ...userWithoutId } = user;

// 函数参数
function greet({ name, age = 18 }) {
  console.log(`Hello ${name}, you are ${age}`);
}
greet(user);
```

**数组解构：**

```javascript
const numbers = [1, 2, 3, 4, 5];

// 基本解构
const [first, second] = numbers;

// 跳过元素
const [, , third] = numbers;

// 剩余运算符
const [head, ...tail] = numbers;

// 交换变量
let a = 1,
  b = 2;
[a, b] = [b, a];

// 函数返回值
function getCoordinates() {
  return [10, 20];
}
const [x, y] = getCoordinates();

// 默认值
const [one, two, three = 0] = [1, 2];
```

### 3. 展开和剩余运算符

**展开运算符：**

```javascript
// 数组展开
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];

// 对象展开
const defaults = { theme: "dark", lang: "en" };
const userPrefs = { theme: "light" };
const settings = { ...defaults, ...userPrefs };

// 函数参数
const numbers = [1, 2, 3];
Math.max(...numbers);

// 复制数组/对象（浅拷贝）
const copy = [...arr1];
const objCopy = { ...user };

// 不可变地添加项目
const newArr = [...arr1, 4, 5];
const newObj = { ...user, age: 30 };
```

**剩余参数：**

```javascript
// 收集函数参数
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}
sum(1, 2, 3, 4, 5);

// 与常规参数结合
function greet(greeting, ...names) {
  return `${greeting} ${names.join(", ")}`;
}
greet("Hello", "John", "Jane", "Bob");

// 对象剩余
const { id, ...userData } = user;

// 数组剩余
const [first, ...rest] = [1, 2, 3, 4, 5];
```

### 4. 模板字面量

```javascript
// 基本用法
const name = "John";
const greeting = `Hello, ${name}!`;

// 多行字符串
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// 表达式求值
const price = 19.99;
const total = `Total: $${(price * 1.2).toFixed(2)}`;

// 标签模板字面量
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] || "";
    return result + str + `<mark>${value}</mark>`;
  }, "");
}

const name = "John";
const age = 30;
const html = highlight`Name: ${name}, Age: ${age}`;
// 输出: "Name: <mark>John</mark>, Age: <mark>30</mark>"
```

### 5. 增强的对象字面量

```javascript
const name = "John";
const age = 30;

// 简写属性名
const user = { name, age };

// 简写方法名
const calculator = {
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
};

// 计算属性名
const field = "email";
const user = {
  name: "John",
  [field]: "john@example.com",
  [`get${field.charAt(0).toUpperCase()}${field.slice(1)}`]() {
    return this[field];
  },
};

// 动态属性创建
const createUser = (name, ...props) => {
  return props.reduce(
    (user, [key, value]) => ({
      ...user,
      [key]: value,
    }),
    { name },
  );
};

const user = createUser("John", ["age", 30], ["email", "john@example.com"]);
```

## 异步模式

### 1. Promises

**创建和使用 Promises：**

```javascript
// 创建 promise
const fetchUser = (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: "John" });
      } else {
        reject(new Error("Invalid ID"));
      }
    }, 1000);
  });
};

// 使用 promises
fetchUser(1)
  .then((user) => console.log(user))
  .catch((error) => console.error(error))
  .finally(() => console.log("Done"));

// 链式 promises
fetchUser(1)
  .then((user) => fetchUserPosts(user.id))
  .then((posts) => processPosts(posts))
  .then((result) => console.log(result))
  .catch((error) => console.error(error));
```

**Promise 组合器：**

```javascript
// Promise.all - 等待所有 promises
const promises = [fetchUser(1), fetchUser(2), fetchUser(3)];

Promise.all(promises)
  .then((users) => console.log(users))
  .catch((error) => console.error("At least one failed:", error));

// Promise.allSettled - 等待所有，无论结果如何
Promise.allSettled(promises).then((results) => {
  results.forEach((result) => {
    if (result.status === "fulfilled") {
      console.log("Success:", result.value);
    } else {
      console.log("Error:", result.reason);
    }
  });
});

// Promise.race - 第一个完成的
Promise.race(promises)
  .then((winner) => console.log("First:", winner))
  .catch((error) => console.error(error));

// Promise.any - 第一个成功的
Promise.any(promises)
  .then((first) => console.log("First success:", first))
  .catch((error) => console.error("All failed:", error));
```

### 2. Async/Await

**基本用法：**

```javascript
// Async 函数总是返回 Promise
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user;
}

// 使用 try/catch 进行错误处理
async function getUserData(id) {
  try {
    const user = await fetchUser(id);
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

// 串行 vs 并行执行
async function sequential() {
  const user1 = await fetchUser(1); // 等待
  const user2 = await fetchUser(2); // 然后等待
  return [user1, user2];
}

async function parallel() {
  const [user1, user2] = await Promise.all([fetchUser(1), fetchUser(2)]);
  return [user1, user2];
}
```

**高级模式：**

```javascript
// Async IIFE
(async () => {
  const result = await someAsyncOperation();
  console.log(result);
})();

// Async 迭代
async function processUsers(userIds) {
  for (const id of userIds) {
    const user = await fetchUser(id);
    await processUser(user);
  }
}

// 顶层 await (ES2022)
const config = await fetch("/config.json").then((r) => r.json());

// 重试逻辑
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}

// 超时包装器
async function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), ms),
  );
  return Promise.race([promise, timeout]);
}
```

## 函数式编程模式

### 1. 数组方法

**Map、Filter、Reduce：**

```javascript
const users = [
  { id: 1, name: "John", age: 30, active: true },
  { id: 2, name: "Jane", age: 25, active: false },
  { id: 3, name: "Bob", age: 35, active: true },
];

// Map - 转换数组
const names = users.map((user) => user.name);
const upperNames = users.map((user) => user.name.toUpperCase());

// Filter - 选择元素
const activeUsers = users.filter((user) => user.active);
const adults = users.filter((user) => user.age >= 18);

// Reduce - 聚合数据
const totalAge = users.reduce((sum, user) => sum + user.age, 0);
const avgAge = totalAge / users.length;

// 按属性分组
const byActive = users.reduce((groups, user) => {
  const key = user.active ? "active" : "inactive";
  return {
    ...groups,
    [key]: [...(groups[key] || []), user],
  };
}, {});

// 链式方法
const result = users
  .filter((user) => user.active)
  .map((user) => user.name)
  .sort()
  .join(", ");
```

**高级数组方法：**

```javascript
// Find - 第一个匹配的元素
const user = users.find((u) => u.id === 2);

// FindIndex - 第一个匹配的索引
const index = users.findIndex((u) => u.name === "Jane");

// Some - 至少一个匹配
const hasActive = users.some((u) => u.active);

// Every - 全部匹配
const allAdults = users.every((u) => u.age >= 18);

// FlatMap - 映射并展平
const userTags = [
  { name: "John", tags: ["admin", "user"] },
  { name: "Jane", tags: ["user"] },
];
const allTags = userTags.flatMap((u) => u.tags);

// From - 从可迭代对象创建数组
const str = "hello";
const chars = Array.from(str);
const numbers = Array.from({ length: 5 }, (_, i) => i + 1);

// Of - 从参数创建数组
const arr = Array.of(1, 2, 3);
```

### 2. 高阶函数

**函数作为参数：**

```javascript
// 自定义 forEach
function forEach(array, callback) {
  for (let i = 0; i < array.length; i++) {
    callback(array[i], i, array);
  }
}

// 自定义 map
function map(array, transform) {
  const result = [];
  for (const item of array) {
    result.push(transform(item));
  }
  return result;
}

// 自定义 filter
function filter(array, predicate) {
  const result = [];
  for (const item of array) {
    if (predicate(item)) {
      result.push(item);
    }
  }
  return result;
}
```

**返回函数的函数：**

```javascript
// 柯里化
const multiply = (a) => (b) => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15

// 偏应用
function partial(fn, ...args) {
  return (...moreArgs) => fn(...args, ...moreArgs);
}

const add = (a, b, c) => a + b + c;
const add5 = partial(add, 5);
console.log(add5(3, 2)); // 10

// 记忆化
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize((n) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 3. 组合和管道

```javascript
// 函数组合
const compose =
  (...fns) =>
  (x) =>
    fns.reduceRight((acc, fn) => fn(acc), x);

const pipe =
  (...fns) =>
  (x) =>
    fns.reduce((acc, fn) => fn(acc), x);

// 示例用法
const addOne = (x) => x + 1;
const double = (x) => x * 2;
const square = (x) => x * x;

const composed = compose(square, double, addOne);
console.log(composed(3)); // ((3 + 1) * 2)^2 = 64

const piped = pipe(addOne, double, square);
console.log(piped(3)); // ((3 + 1) * 2)^2 = 64

// 实际示例
const processUser = pipe(
  (user) => ({ ...user, name: user.name.trim() }),
  (user) => ({ ...user, email: user.email.toLowerCase() }),
  (user) => ({ ...user, age: parseInt(user.age) }),
);

const user = processUser({
  name: "  John  ",
  email: "JOHN@EXAMPLE.COM",
  age: "30",
});
```

### 4. 纯函数和不可变性

```javascript
// 非纯函数（修改输入）
function addItemImpure(cart, item) {
  cart.items.push(item);
  cart.total += item.price;
  return cart;
}

// 纯函数（无副作用）
function addItemPure(cart, item) {
  return {
    ...cart,
    items: [...cart.items, item],
    total: cart.total + item.price,
  };
}

// 不可变数组操作
const numbers = [1, 2, 3, 4, 5];

// 添加到数组
const withSix = [...numbers, 6];

// 从数组中删除
const withoutThree = numbers.filter((n) => n !== 3);

// 更新数组元素
const doubled = numbers.map((n) => (n === 3 ? n * 2 : n));

// 不可变对象操作
const user = { name: "John", age: 30 };

// 更新属性
const olderUser = { ...user, age: 31 };

// 添加属性
const withEmail = { ...user, email: "john@example.com" };

// 删除属性
const { age, ...withoutAge } = user;

// 深拷贝（简单方法）
const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

// 更好的深拷贝
const structuredClone = (obj) => globalThis.structuredClone(obj);
```

## 现代类特性

```javascript
// 类语法
class User {
  // 私有字段
  #password;

  // 公共字段
  id;
  name;

  // 静态字段
  static count = 0;

  constructor(id, name, password) {
    this.id = id;
    this.name = name;
    this.#password = password;
    User.count++;
  }

  // 公共方法
  greet() {
    return `Hello, ${this.name}`;
  }

  // 私有方法
  #hashPassword(password) {
    return `hashed_${password}`;
  }

  // Getter
  get displayName() {
    return this.name.toUpperCase();
  }

  // Setter
  set password(newPassword) {
    this.#password = this.#hashPassword(newPassword);
  }

  // 静态方法
  static create(id, name, password) {
    return new User(id, name, password);
  }
}

// 继承
class Admin extends User {
  constructor(id, name, password, role) {
    super(id, name, password);
    this.role = role;
  }

  greet() {
    return `${super.greet()}, I'm an admin`;
  }
}
```

## 模块 (ES6)

```javascript
// 导出
// math.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export class Calculator {
  // ...
}

// 默认导出
export default function multiply(a, b) {
  return a * b;
}

// 导入
// app.js
import multiply, { PI, add, Calculator } from "./math.js";

// 重命名导入
import { add as sum } from "./math.js";

// 导入所有
import * as Math from "./math.js";

// 动态导入
const module = await import("./math.js");
const { add } = await import("./math.js");

// 条件加载
if (condition) {
  const module = await import("./feature.js");
  module.init();
}
```

## 迭代器和生成器

```javascript
// 自定义迭代器
const range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() {
    return {
      current: this.from,
      last: this.to,

      next() {
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      },
    };
  },
};

for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}

// 生成器函数
function* rangeGenerator(from, to) {
  for (let i = from; i <= to; i++) {
    yield i;
  }
}

for (const num of rangeGenerator(1, 5)) {
  console.log(num);
}

// 无限生成器
function* fibonacci() {
  let [prev, curr] = [0, 1];
  while (true) {
    yield curr;
    [prev, curr] = [curr, prev + curr];
  }
}

// Async 生成器
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

for await (const page of fetchPages("/api/users")) {
  console.log(page);
}
```

## 现代运算符

```javascript
// 可选链
const user = { name: "John", address: { city: "NYC" } };
const city = user?.address?.city;
const zipCode = user?.address?.zipCode; // undefined

// 函数调用
const result = obj.method?.();

// 数组访问
const first = arr?.[0];

// 空值合并
const value = null ?? "default"; // 'default'
const value = undefined ?? "default"; // 'default'
const value = 0 ?? "default"; // 0 (not 'default')
const value = "" ?? "default"; // '' (not 'default')

// 逻辑赋值
let a = null;
a ??= "default"; // a = 'default'

let b = 5;
b ??= 10; // b = 5 (unchanged)

let obj = { count: 0 };
obj.count ||= 1; // obj.count = 1
obj.count &&= 2; // obj.count = 2
```

## 性能优化

```javascript
// 防抖
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const searchDebounced = debounce(search, 300);

// 节流
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

const scrollThrottled = throttle(handleScroll, 100);

// 惰性求值
function* lazyMap(iterable, transform) {
  for (const item of iterable) {
    yield transform(item);
  }
}

// 只使用你需要的
const numbers = [1, 2, 3, 4, 5];
const doubled = lazyMap(numbers, (x) => x * 2);
const first = doubled.next().value; // 只计算第一个值
```

## 最佳实践

1. **默认使用 const**：只在需要重新赋值时使用 let
2. **首选箭头函数**：特别是用于回调
3. **使用模板字面量**：而不是字符串拼接
4. **解构对象和数组**：为了更整洁的代码
5. **使用 async/await**：而不是 Promise 链
6. **避免数据变异**：使用展开运算符和数组方法
7. **使用可选链**：防止 "Cannot read property of undefined"
8. **使用空值合并**：用于默认值
9. **首选数组方法**：而不是传统循环
10. **使用模块**：为了更好的代码组织
11. **编写纯函数**：更容易测试和推理
12. **使用有意义的变量名**：自文档化代码
13. **保持函数小**：单一职责原则
14. **正确处理错误**：在 async/await 中使用 try/catch
15. **使用严格模式**：`'use strict'` 用于更好的错误捕获

## 常见陷阱

1. **this 绑定混淆**：使用箭头函数或 bind()
2. **没有错误处理的 Async/await**：始终使用 try/catch
3. **不必要的 Promise 创建**：不要包装已经是异步的函数
4. **对象变异**：使用展开运算符或 Object.assign()
5. **忘记 await**：Async 函数返回 promises
6. **阻塞事件循环**：避免同步操作
7. **内存泄漏**：清理事件监听器和定时器
8. **不处理 promise 拒绝**：使用 catch() 或 try/catch

## 资源

- **MDN Web Docs**：https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **JavaScript.info**：https://javascript.info/
- **You Don't Know JS**：https://github.com/getify/You-Dont-Know-JS
- **Eloquent JavaScript**：https://eloquentjavascript.net/
- **ES6 Features**：http://es6-features.org/
