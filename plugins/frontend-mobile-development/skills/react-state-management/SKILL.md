---
name: react-state-management
description: 精通使用 Redux Toolkit、Zustand、Jotai 和 React Query 的现代 React 状态管理。在设置全局状态、管理服务端状态或在状态管理解决方案之间选择时使用。
---

# React 状态管理

现代 React 状态管理模式的综合指南，从本地组件状态到全局存储和服务端状态同步。

## 何时使用此技能

- 在 React 应用中设置全局状态管理
- 在 Redux Toolkit、Zustand 或 Jotai 之间选择
- 使用 React Query 或 SWR 管理服务端状态
- 实现乐观更新
- 调试与状态相关的问题
- 从遗留 Redux 迁移到现代模式

## 核心概念

### 1. 状态分类

| 类型             | 描述                  | 解决方案                     |
| ---------------- | ---------------------------- | ----------------------------- |
| **本地状态**  | 组件特定、UI 状态 | useState, useReducer          |
| **全局状态** | 跨组件共享     | Redux Toolkit, Zustand, Jotai |
| **服务端状态** | 远程数据、缓存         | React Query, SWR, RTK Query   |
| **URL 状态**    | 路由参数、搜索     | React Router, nuqs            |
| **表单状态**   | 输入值、验证     | React Hook Form, Formik       |

### 2. 选择标准

```
小型应用、简单状态 → Zustand 或 Jotai
大型应用、复杂状态 → Redux Toolkit
重度服务端交互 → React Query + 轻量客户端状态
原子/细粒度更新 → Jotai
```

## 快速开始

### Zustand（最简单）

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// 在组件中使用
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>切换主题</button>
    </header>
  )
}
```

## 模式

### 模式 1：Redux Toolkit with TypeScript

```typescript
// store/index.ts
import { configureStore } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import userReducer from "./slices/userSlice";
import cartReducer from "./slices/cartSlice";

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ["persist/PERSIST"],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// 类型化 hooks
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

```typescript
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: string;
  email: string;
  name: string;
}

interface UserState {
  current: User | null;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: UserState = {
  current: null,
  status: "idle",
  error: null,
};

export const fetchUser = createAsyncThunk(
  "user/fetchUser",
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error("获取用户失败");
      return await response.json();
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  },
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.current = action.payload;
      state.status = "succeeded";
    },
    clearUser: (state) => {
      state.current = null;
      state.status = "idle";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.current = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload as string;
      });
  },
});

export const { setUser, clearUser } = userSlice.actions;
export default userSlice.reducer;
```

### 模式 2：Zustand with Slices（可扩展）

```typescript
// store/slices/createUserSlice.ts
import { StateCreator } from "zustand";

export interface UserSlice {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice, // 组合存储类型
  [],
  [],
  UserSlice
> = (set, get) => ({
  user: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const user = await authApi.login(credentials);
    set({ user, isAuthenticated: true });
  },
  logout: () => {
    set({ user: null, isAuthenticated: false });
    // 可以访问其他 slices
    // get().clearCart()
  },
});

// store/index.ts
import { create } from "zustand";
import { createUserSlice, UserSlice } from "./slices/createUserSlice";
import { createCartSlice, CartSlice } from "./slices/createCartSlice";

type StoreState = UserSlice & CartSlice;

export const useStore = create<StoreState>()((...args) => ({
  ...createUserSlice(...args),
  ...createCartSlice(...args),
}));

// 选择性订阅（防止不必要的重新渲染）
export const useUser = () => useStore((state) => state.user);
export const useCart = () => useStore((state) => state.cart);
```

### 模式 3：Jotai 用于原子状态

```typescript
// atoms/userAtoms.ts
import { atom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'

// 基础 atom
export const userAtom = atom<User | null>(null)

// 派生 atom（计算）
export const isAuthenticatedAtom = atom((get) => get(userAtom) !== null)

// 带持久化的 atom
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light')

// 异步 atom
export const userProfileAtom = atom(async (get) => {
  const user = get(userAtom)
  if (!user) return null
  const response = await fetch(`/api/users/${user.id}/profile`)
  return response.json()
})

// 只写 atom（action）
export const logoutAtom = atom(null, (get, set) => {
  set(userAtom, null)
  set(cartAtom, [])
  localStorage.removeItem('token')
})

// 使用
function Profile() {
  const [user] = useAtom(userAtom)
  const [, logout] = useAtom(logoutAtom)
  const [profile] = useAtom(userProfileAtom) // 支持 Suspense

  return (
    <Suspense fallback={<Skeleton />}>
      <ProfileContent profile={profile} onLogout={logout} />
    </Suspense>
  )
}
```

### 模式 4：React Query 用于服务端状态

```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Query keys 工厂
export const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, "detail"] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

// 获取 hook
export function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    staleTime: 5 * 60 * 1000, // 5 分钟
    gcTime: 30 * 60 * 1000, // 30 分钟（原 cacheTime）
  });
}

// 单个用户 hook
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    enabled: !!id, // 如果没有 id 则不获取
  });
}

// 带乐观更新的 mutation
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // 取消正在进行的重新获取
      await queryClient.cancelQueries({
        queryKey: userKeys.detail(newUser.id),
      });

      // 快照之前的值
      const previousUser = queryClient.getQueryData(
        userKeys.detail(newUser.id),
      );

      // 乐观更新
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser);

      return { previousUser };
    },
    onError: (err, newUser, context) => {
      // 出错时回滚
      queryClient.setQueryData(
        userKeys.detail(newUser.id),
        context?.previousUser,
      );
    },
    onSettled: (data, error, variables) => {
      // mutation 后重新获取
      queryClient.invalidateQueries({
        queryKey: userKeys.detail(variables.id),
      });
    },
  });
}
```

### 模式 5：组合客户端 + 服务端状态

```typescript
// Zustand 用于客户端状态
const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  modal: null,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  openModal: (modal) => set({ modal }),
  closeModal: () => set({ modal: null }),
}))

// React Query 用于服务端状态
function Dashboard() {
  const { sidebarOpen, toggleSidebar } = useUIStore()
  const { data: users, isLoading } = useUsers({ active: true })
  const { data: stats } = useStats()

  if (isLoading) return <DashboardSkeleton />

  return (
    <div className={sidebarOpen ? 'with-sidebar' : ''}>
      <Sidebar open={sidebarOpen} onToggle={toggleSidebar} />
      <main>
        <StatsCards stats={stats} />
        <UserTable users={users} />
      </main>
    </div>
  )
}
```

## 最佳实践

### 应该做的

- **就近存储状态** - 尽可能将状态保持在靠近使用它的地方
- **使用选择器** - 通过选择性订阅防止不必要的重新渲染
- **规范化数据** - 展平嵌套结构以便更容易更新
- **类型化一切** - 完整的 TypeScript 覆盖防止运行时错误
- **分离关注点** - 服务端状态（React Query）vs 客户端状态（Zustand）

### 不应该做的

- **不要过度全局化** - 并不是所有东西都需要在全局状态中
- **不要重复服务端状态** - 让 React Query 管理它
- **不要直接突变** - 始终使用不可变更新
- **不要存储派生数据** - 改为计算它
- **不要混合范式** - 为每个类别选择一个主要解决方案

## 迁移指南

### 从遗留 Redux 到 RTK

```typescript
// 之前（遗留 Redux）
const ADD_TODO = "ADD_TODO";
const addTodo = (text) => ({ type: ADD_TODO, payload: text });
function todosReducer(state = [], action) {
  switch (action.type) {
    case ADD_TODO:
      return [...state, { text: action.payload, completed: false }];
    default:
      return state;
  }
}

// 之后（Redux Toolkit）
const todosSlice = createSlice({
  name: "todos",
  initialState: [],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      // Immer 允许"突变"
      state.push({ text: action.payload, completed: false });
    },
  },
});
```

## 资源

- [Redux Toolkit 文档](https://redux-toolkit.js.org/)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [Jotai 文档](https://jotai.org/)
- [TanStack Query](https://tanstack.com/query)
