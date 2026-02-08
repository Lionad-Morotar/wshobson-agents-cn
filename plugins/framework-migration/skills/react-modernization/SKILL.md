---
name: react-modernization
description: 升级 React 应用到最新版本，从类组件迁移到 hooks，并采用并发特性。用于现代化 React 代码库、迁移到 React Hooks 或升级到最新 React 版本时使用。
---

# React 现代化

精通 React 版本升级、类到 hooks 迁移、并发特性采用以及用于自动转换的 codemods。

## 何时使用此技能

- 升级 React 应用到最新版本
- 将类组件迁移到带 hooks 的函数组件
- 采用并发 React 特性（Suspense、transitions）
- 应用 codemods 进行自动重构
- 现代化状态管理模式
- 更新到 TypeScript
- 使用 React 18+ 特性改进性能

## 版本升级路径

### React 16 → 17 → 18

**各版本的破坏性变更：**

**React 17:**

- 事件委托变更
- 无事件池
- Effect 清理时序
- JSX 转换（无需 React 导入）

**React 18:**

- 自动批处理
- 并发渲染
- 严格模式变更（双重调用）
- 新的根 API
- 服务端 Suspense

## 类到 Hooks 迁移

### 状态管理

```javascript
// 之前：类组件
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0,
      name: "",
    };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

// 之后：带 hooks 的函数组件
function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState("");

  const increment = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

### 生命周期方法到 Hooks

```javascript
// 之前：生命周期方法
class DataFetcher extends React.Component {
  state = { data: null, loading: true };

  componentDidMount() {
    this.fetchData();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.fetchData();
    }
  }

  componentWillUnmount() {
    this.cancelRequest();
  }

  fetchData = async () => {
    const data = await fetch(`/api/${this.props.id}`);
    this.setState({ data, loading: false });
  };

  cancelRequest = () => {
    // 清理
  };

  render() {
    if (this.state.loading) return <div>Loading...</div>;
    return <div>{this.state.data}</div>;
  }
}

// 之后：useEffect hook
function DataFetcher({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${id}`);
        const result = await response.json();

        if (!cancelled) {
          setData(result);
          setLoading(false);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
        }
      }
    };

    fetchData();

    // 清理函数
    return () => {
      cancelled = true;
    };
  }, [id]); // id 变化时重新运行

  if (loading) return <div>Loading...</div>;
  return <div>{data}</div>;
}
```

### Context 和 HOC 到 Hooks

```javascript
// 之前：Context 消费者和 HOC
const ThemeContext = React.createContext();

class ThemedButton extends React.Component {
  static contextType = ThemeContext;

  render() {
    return (
      <button style={{ background: this.context.theme }}>
        {this.props.children}
      </button>
    );
  }
}

// 之后：useContext hook
function ThemedButton({ children }) {
  const { theme } = useContext(ThemeContext);

  return <button style={{ background: theme }}>{children}</button>;
}

// 之前：用于数据获取的 HOC
function withUser(Component) {
  return class extends React.Component {
    state = { user: null };

    componentDidMount() {
      fetchUser().then((user) => this.setState({ user }));
    }

    render() {
      return <Component {...this.props} user={this.state.user} />;
    }
  };
}

// 之后：自定义 hook
function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser().then(setUser);
  }, []);

  return user;
}

function UserProfile() {
  const user = useUser();
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## React 18 并发特性

### 新的根 API

```javascript
// 之前：React 17
import ReactDOM from "react-dom";

ReactDOM.render(<App />, document.getElementById("root"));

// 之后：React 18
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

### 自动批处理

```javascript
// React 18：所有更新都被批处理
function handleClick() {
  setCount((c) => c + 1);
  setFlag((f) => !f);
  // 仅一次重新渲染（已批处理）
}

// 即使在异步中：
setTimeout(() => {
  setCount((c) => c + 1);
  setFlag((f) => !f);
  // 在 React 18 中仍然批处理！
}, 1000);

// 如需要则退出
import { flushSync } from "react-dom";

flushSync(() => {
  setCount((c) => c + 1);
});
// 重新渲染发生在这里
setFlag((f) => !f);
// 另一次重新渲染
```

### Transitions

```javascript
import { useState, useTransition } from "react";

function SearchResults() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // 紧急：立即更新输入
    setQuery(e.target.value);

    // 非紧急：更新结果（可中断）
    startTransition(() => {
      setResults(searchResults(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={results} />
    </>
  );
}
```

### 用于数据获取的 Suspense

```javascript
import { Suspense } from "react";

// 基于资源的数据获取（React 18）
const resource = fetchProfileData();

function ProfilePage() {
  return (
    <Suspense fallback={<Loading />}>
      <ProfileDetails />
      <Suspense fallback={<Loading />}>
        <ProfileTimeline />
      </Suspense>
    </Suspense>
  );
}

function ProfileDetails() {
  // 如果数据未准备好会暂停
  const user = resource.user.read();
  return <h1>{user.name}</h1>;
}

function ProfileTimeline() {
  const posts = resource.posts.read();
  return <Timeline posts={posts} />;
}
```

## 自动化 Codemods

### 运行 React Codemods

```bash
# 重命名不安全生命周期方法
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js src/

# 更新 React 导入（React 17+）
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/update-react-imports.js src/
```

### 自定义 Codemod 示例

```javascript
// custom-codemod.js
module.exports = function (file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  // 查找 setState 调用
  root
    .find(j.CallExpression, {
      callee: {
        type: "MemberExpression",
        property: { name: "setState" },
      },
    })
    .forEach((path) => {
      // 转换为 useState
      // ... 转换逻辑
    });

  return root.toSource();
};

// 运行：jscodeshift -t custom-codemod.js src/
```

## 性能优化

### useMemo 和 useCallback

```javascript
function ExpensiveComponent({ items, filter }) {
  // 缓存昂贵的计算
  const filteredItems = useMemo(() => {
    return items.filter((item) => item.category === filter);
  }, [items, filter]);

  // 缓存回调以防止子组件重新渲染
  const handleClick = useCallback((id) => {
    console.log("Clicked:", id);
  }, []); // 无依赖，永不改变

  return <List items={filteredItems} onClick={handleClick} />;
}

// 带有 memo 的子组件
const List = React.memo(({ items, onClick }) => {
  return items.map((item) => (
    <Item key={item.id} item={item} onClick={onClick} />
  ));
});
```

### 代码分割

```javascript
import { lazy, Suspense } from "react";

// 懒加载组件
const Dashboard = lazy(() => import("./Dashboard"));
const Settings = lazy(() => import("./Settings"));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## TypeScript 迁移

```typescript
// 之前：JavaScript
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// 之后：TypeScript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// 泛型组件
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>;
}
```

## 迁移检查清单

```markdown
### 迁移前

- [ ] 增量更新依赖（不要一次性）
- [ ] 查看发行说明中的破坏性变更
- [ ] 设置测试套件
- [ ] 创建功能分支

### 类 → Hooks 迁移

- [ ] 识别要迁移的类组件
- [ ] 从叶子组件开始（无子组件）
- [ ] 转换状态到 useState
- [ ] 转换生命周期到 useEffect
- [ ] 转换 context 到 useContext
- [ ] 提取自定义 hooks
- [ ] 彻底测试

### React 18 升级

- [ ] 首先更新到 React 17（如需要）
- [ ] 更新 react 和 react-dom 到 18
- [ ] 如果使用 TypeScript，更新 @types/react
- [ ] 更改到 createRoot API
- [ ] 使用 StrictMode 测试（双重调用）
- [ ] 解决并发渲染问题
- [ ] 在有益处的地方采用 Suspense/Transitions

### 性能

- [ ] 识别性能瓶颈
- [ ] 在适当的地方添加 React.memo
- [ ] 对昂贵操作使用 useMemo/useCallback
- [ ] 实现代码分割
- [ ] 优化重新渲染

### 测试

- [ ] 更新测试工具（React Testing Library）
- [ ] 使用 React 18 特性测试
- [ ] 检查控制台警告
- [ ] 性能测试
```

## 资源

- **references/breaking-changes.md**：特定版本的破坏性变更
- **references/codemods.md**：Codemod 使用指南
- **references/hooks-migration.md**：全面的 hooks 模式
- **references/concurrent-features.md**：React 18 并发特性
- **assets/codemod-config.json**：Codemod 配置
- **assets/migration-checklist.md**：分步检查清单
- **scripts/apply-codemods.sh**：自动化 codemod 脚本

## 最佳实践

1. **增量迁移**：不要一次性迁移所有内容
2. **彻底测试**：每一步都要全面测试
3. **使用 Codemods**：自动化重复性转换
4. **从简单开始**：从叶子组件开始
5. **利用 StrictMode**：尽早发现问题
6. **监控性能**：迁移前后测量
7. **文档变更**：保留迁移日志

## 常见陷阱

- 忘记 useEffect 依赖
- 过度使用 useMemo/useCallback
- 不在 useEffect 中处理清理
- 混合类和函数模式
- 忽略 StrictMode 警告
- 破坏性变更假设
