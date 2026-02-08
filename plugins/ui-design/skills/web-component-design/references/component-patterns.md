# 组件模式参考

## 复合组件深入

复合组件共享隐式状态，同时允许灵活组合。

### 使用 Context 实现

```tsx
import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
  type Dispatch,
  type SetStateAction,
} from "react";

// 类型定义
interface TabsContextValue {
  activeTab: string;
  setActiveTab: Dispatch<SetStateAction<string>>;
}

interface TabsProps {
  defaultValue: string;
  children: ReactNode;
  onChange?: (value: string) => void;
}

interface TabListProps {
  children: ReactNode;
  className?: string;
}

interface TabProps {
  value: string;
  children: ReactNode;
  disabled?: boolean;
}

interface TabPanelProps {
  value: string;
  children: ReactNode;
}

// Context
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error("Tabs 组件必须在 <Tabs> 内使用");
  }
  return context;
}

// 根组件
export function Tabs({ defaultValue, children, onChange }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  const handleChange: Dispatch<SetStateAction<string>> = useCallback(
    (value) => {
      const newValue = typeof value === "function" ? value(activeTab) : value;
      setActiveTab(newValue);
      onChange?.(newValue);
    },
    [activeTab, onChange],
  );

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleChange }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// 标签列表（标签触发器的容器）
Tabs.List = function TabList({ children, className }: TabListProps) {
  return (
    <div role="tablist" className={`flex border-b ${className}`}>
      {children}
    </div>
  );
};

// 单个标签（触发器）
Tabs.Tab = function Tab({ value, children, disabled }: TabProps) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`panel-${value}`}
      tabIndex={isActive ? 0 : -1}
      disabled={disabled}
      onClick={() => setActiveTab(value)}
      className={`
        px-4 py-2 font-medium transition-colors
        ${
          isActive
            ? "border-b-2 border-blue-600 text-blue-600"
            : "text-gray-600 hover:text-gray-900"
        }
        ${disabled ? "opacity-50 cursor-not-allowed" : ""}
      `}
    >
      {children}
    </button>
  );
};

// 标签面板（内容）
Tabs.Panel = function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabs();

  if (activeTab !== value) return null;

  return (
    <div
      role="tabpanel"
      id={`panel-${value}`}
      aria-labelledby={`tab-${value}`}
      tabIndex={0}
      className="py-4"
    >
      {children}
    </div>
  );
};
```

### 使用方式

```tsx
<Tabs defaultValue="overview" onChange={console.log}>
  <Tabs.List>
    <Tabs.Tab value="overview">概览</Tabs.Tab>
    <Tabs.Tab value="features">功能</Tabs.Tab>
    <Tabs.Tab value="pricing" disabled>
      定价
    </Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="overview">
    <h2>产品概览</h2>
    <p>描述内容...</p>
  </Tabs.Panel>
  <Tabs.Panel value="features">
    <h2>核心功能</h2>
    <ul>...</ul>
  </Tabs.Panel>
</Tabs>
```

## 渲染属性模式

将渲染控制权委托给使用者，同时提供状态和辅助方法。

```tsx
interface DataLoaderRenderProps<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

interface DataLoaderProps<T> {
  url: string;
  children: (props: DataLoaderRenderProps<T>) => ReactNode;
}

function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("获取失败");
      const data = await response.json();
      setState({ data, loading: false, error: null });
    } catch (error) {
      setState((prev) => ({ ...prev, loading: false, error: error as Error }));
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return <>{children({ ...state, refetch: fetchData })}</>;
}

// 使用示例
<DataLoader<User[]> url="/api/users">
  {({ data, loading, error, refetch }) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} onRetry={refetch} />;
    return <UserList users={data!} />;
  }}
</DataLoader>;
```

## 多态组件

可以渲染为不同 HTML 元素的组件。

```tsx
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

interface TextOwnProps {
  variant?: 'body' | 'heading' | 'label';
  size?: 'sm' | 'md' | 'lg';
}

type TextProps<C extends React.ElementType> = PolymorphicComponentProp<C, TextOwnProps>;

function Text<C extends React.ElementType = 'span'>({
  as,
  variant = 'body',
  size = 'md',
  className,
  children,
  ...props
}: TextProps<C>) {
  const Component = as || 'span';

  const variantClasses = {
    body: 'font-normal',
    heading: 'font-bold',
    label: 'font-medium uppercase tracking-wide',
  };

  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };

  return (
    <Component
      className={`${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
}

// 使用示例
<Text>默认 span</Text>
<Text as="p" variant="body" size="lg">段落</Text>
<Text as="h1" variant="heading" size="lg">标题</Text>
<Text as="label" variant="label" htmlFor="input">标签</Text>
```

## 受控与非受控模式

同时支持两种模式以获得最大灵活性。

```tsx
interface InputProps {
  // 受控
  value?: string;
  onChange?: (value: string) => void;
  // 非受控
  defaultValue?: string;
  // 通用
  placeholder?: string;
  disabled?: boolean;
}

function Input({
  value: controlledValue,
  onChange,
  defaultValue = '',
  ...props
}: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue);

  // 确定是否为受控
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }

    onChange?.(newValue);
  };

  return (
    <input
      type="text"
      value={value}
      onChange={handleChange}
      {...props}
    />
  );
}

// 受控用法
const [search, setSearch] = useState('');
<Input value={search} onChange={setSearch} />

// 非受控用法
<Input defaultValue="初始值" onChange={console.log} />
```

## 插槽模式

允许使用者替换内部部分。

```tsx
interface CardProps {
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  media?: ReactNode;
}

function Card({ children, header, footer, media }: CardProps) {
  return (
    <article className="rounded-lg border bg-white shadow-sm">
      {media && (
        <div className="aspect-video overflow-hidden rounded-t-lg">{media}</div>
      )}
      {header && <header className="border-b px-4 py-3">{header}</header>}
      <div className="px-4 py-4">{children}</div>
      {footer && (
        <footer className="border-t px-4 py-3 bg-gray-50 rounded-b-lg">
          {footer}
        </footer>
      )}
    </article>
  );
}

// 使用插槽
<Card
  media={<img src="/image.jpg" alt="" />}
  header={<h2 className="font-semibold">卡片标题</h2>}
  footer={<Button>操作</Button>}
>
  <p>卡片内容放在这里。</p>
</Card>;
```

## 转发 Ref 模式

允许父组件访问底层 DOM 节点。

```tsx
import { forwardRef, useRef, useImperativeHandle } from "react";

interface InputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

interface FancyInputProps {
  label: string;
  placeholder?: string;
}

const FancyInput = forwardRef<InputHandle, FancyInputProps>(
  ({ label, placeholder }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => {
        if (inputRef.current) inputRef.current.value = "";
      },
      getValue: () => inputRef.current?.value ?? "",
    }));

    return (
      <div>
        <label className="block text-sm font-medium mb-1">{label}</label>
        <input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          className="w-full px-3 py-2 border rounded-md"
        />
      </div>
    );
  },
);

FancyInput.displayName = "FancyInput";

// 使用示例
function Form() {
  const inputRef = useRef<InputHandle>(null);

  const handleSubmit = () => {
    console.log(inputRef.current?.getValue());
    inputRef.current?.clear();
  };

  return (
    <form onSubmit={handleSubmit}>
      <FancyInput ref={inputRef} label="姓名" />
      <button type="button" onClick={() => inputRef.current?.focus()}>
        聚焦输入框
      </button>
    </form>
  );
}
```
