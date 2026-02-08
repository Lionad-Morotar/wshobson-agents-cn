---
name: memory-safety-patterns
description: Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing safe systems code, managing resources, or preventing memory bugs.
---

# 内存安全模式

跨语言内存安全编程模式,包括 RAII、所有权、智能指针和资源管理。

## 何时使用此技能

- 编写内存安全的系统代码
- 管理资源(文件、套接字、内存)
- 防止释放后使用和内存泄漏
- 实现 RAII 模式
- 为安全性选择语言
- 调试内存问题

## 核心概念

### 1. 内存漏洞分类

| 漏洞类型            | 描述                    | 预防方法          |
| -------------------- | -------------------------------- | ----------------- |
| **释放后使用**   | 访问已释放的内存              | 所有权、RAII   |
| **重复释放**      | 两次释放同一块内存           | 智能指针    |
| **内存泄漏**      | 从未释放内存                | RAII、GC          |
| **缓冲区溢出**  | 写入超出缓冲区末尾            | 边界检查   |
| **悬空指针** | 指向已释放内存的指针          | 生命周期跟踪 |
| **数据竞争**        | 并发未同步访问                 | 所有权、同步   |

### 2. 安全性谱系

```
手动管理(C) → 智能指针(C++) → 所有权(Rust) → 垃圾回收(Go、Java)
安全性较低                                              安全性较高
控制力较强                                              控制力较弱
```

## 各语言模式

### 模式 1:C++ 中的 RAII

```cpp
// RAII:资源获取即初始化
// 资源生命周期与对象生命周期绑定

#include <memory>
#include <fstream>
#include <mutex>

// 带 RAII 的文件句柄
class FileHandle {
public:
    explicit FileHandle(const std::string& path)
        : file_(path) {
        if (!file_.is_open()) {
            throw std::runtime_error("Failed to open file");
        }
    }

    // 析构函数自动关闭文件
    ~FileHandle() = default; // fstream 在其析构函数中关闭

    // 删除拷贝(防止重复关闭)
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // 允许移动
    FileHandle(FileHandle&&) = default;
    FileHandle& operator=(FileHandle&&) = default;

    void write(const std::string& data) {
        file_ << data;
    }

private:
    std::fstream file_;
};

// 锁守护(互斥锁的 RAII)
class Database {
public:
    void update(const std::string& key, const std::string& value) {
        std::lock_guard<std::mutex> lock(mutex_); // 退出作用域时释放
        data_[key] = value;
    }

    std::string get(const std::string& key) {
        std::shared_lock<std::shared_mutex> lock(shared_mutex_);
        return data_[key];
    }

private:
    std::mutex mutex_;
    std::shared_mutex shared_mutex_;
    std::map<std::string, std::string> data_;
};

// 带回滚的事务(RAII)
template<typename T>
class Transaction {
public:
    explicit Transaction(T& target)
        : target_(target), backup_(target), committed_(false) {}

    ~Transaction() {
        if (!committed_) {
            target_ = backup_; // 回滚
        }
    }

    void commit() { committed_ = true; }

    T& get() { return target_; }

private:
    T& target_;
    T backup_;
    bool committed_;
};
```

### 模式 2:C++ 中的智能指针

```cpp
#include <memory>

// unique_ptr:单一所有权
class Engine {
public:
    void start() { /* ... */ }
};

class Car {
public:
    Car() : engine_(std::make_unique<Engine>()) {}

    void start() {
        engine_->start();
    }

    // 转移所有权
    std::unique_ptr<Engine> extractEngine() {
        return std::move(engine_);
    }

private:
    std::unique_ptr<Engine> engine_;
};

// shared_ptr:共享所有权
class Node {
public:
    std::string data;
    std::shared_ptr<Node> next;

    // 使用 weak_ptr 打破循环
    std::weak_ptr<Node> parent;
};

void sharedPtrExample() {
    auto node1 = std::make_shared<Node>();
    auto node2 = std::make_shared<Node>();

    node1->next = node2;
    node2->parent = node1; // 弱引用防止循环

    // 访问 weak_ptr
    if (auto parent = node2->parent.lock()) {
        // parent 是有效的 shared_ptr
    }
}

// 资源自定义删除器
class Socket {
public:
    static void close(int* fd) {
        if (fd && *fd >= 0) {
            ::close(*fd);
            delete fd;
        }
    }
};

auto createSocket() {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    return std::unique_ptr<int, decltype(&Socket::close)>(
        new int(fd),
        &Socket::close
    );
}

// make_unique/make_shared 最佳实践
void bestPractices() {
    // 好:异常安全,单次分配
    auto ptr = std::make_shared<Widget>();

    // 坏:两次分配,非异常安全
    std::shared_ptr<Widget> ptr2(new Widget());

    // 对于数组
    auto arr = std::make_unique<int[]>(10);
}
```

### 模式 3:Rust 中的所有权

```rust
// 移动语义(默认)
fn move_example() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 被移动,不再有效

    // println!("{}", s1); // 编译错误!
    println!("{}", s2);
}

// 借用(引用)
fn borrow_example() {
    let s = String::from("hello");

    // 不可变借用(允许多个)
    let len = calculate_length(&s);
    println!("{} has length {}", s, len);

    // 可变借用(仅允许一个)
    let mut s = String::from("hello");
    change(&mut s);
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s 离开作用域,但不释放因为是借用的

fn change(s: &mut String) {
    s.push_str(", world");
}

// 生命周期:编译器跟踪引用有效性
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 包含引用的结构体需要生命周期标注
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }

    // 生命周期省略:编译器推断 &self 为 'a
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}

// 内部可变性
use std::cell::{Cell, RefCell};
use std::rc::Rc;

struct Stats {
    count: Cell<i32>,           // 拷贝类型
    data: RefCell<Vec<String>>, // 非拷贝类型
}

impl Stats {
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }

    fn add_data(&self, item: String) {
        self.data.borrow_mut().push(item);
    }
}

// Rc 用于共享所有权(单线程)
fn rc_example() {
    let data = Rc::new(vec![1, 2, 3]);
    let data2 = Rc::clone(&data); // 增加引用计数

    println!("Count: {}", Rc::strong_count(&data)); // 2
}

// Arc 用于共享所有权(线程安全)
use std::sync::Arc;
use std::thread;

fn arc_example() {
    let data = Arc::new(vec![1, 2, 3]);

    let handles: Vec<_> = (0..3)
        .map(|_| {
            let data = Arc::clone(&data);
            thread::spawn(move || {
                println!("{:?}", data);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
}
```

### 模式 4:C 中的安全资源管理

```c
// C 没有 RAII,但我们可以使用模式

#include <stdlib.h>
#include <stdio.h>

// 模式:goto 清理
int process_file(const char* path) {
    FILE* file = NULL;
    char* buffer = NULL;
    int result = -1;

    file = fopen(path, "r");
    if (!file) {
        goto cleanup;
    }

    buffer = malloc(1024);
    if (!buffer) {
        goto cleanup;
    }

    // 处理文件...
    result = 0;

cleanup:
    if (buffer) free(buffer);
    if (file) fclose(file);
    return result;
}

// 模式:带创建/销毁的不透明指针
typedef struct Context Context;

Context* context_create(void);
void context_destroy(Context* ctx);
int context_process(Context* ctx, const char* data);

// 实现
struct Context {
    int* data;
    size_t size;
    FILE* log;
};

Context* context_create(void) {
    Context* ctx = calloc(1, sizeof(Context));
    if (!ctx) return NULL;

    ctx->data = malloc(100 * sizeof(int));
    if (!ctx->data) {
        free(ctx);
        return NULL;
    }

    ctx->log = fopen("log.txt", "w");
    if (!ctx->log) {
        free(ctx->data);
        free(ctx);
        return NULL;
    }

    return ctx;
}

void context_destroy(Context* ctx) {
    if (ctx) {
        if (ctx->log) fclose(ctx->log);
        if (ctx->data) free(ctx->data);
        free(ctx);
    }
}

// 模式:清理属性(GCC/Clang 扩展)
#define AUTO_FREE __attribute__((cleanup(auto_free_func)))

void auto_free_func(void** ptr) {
    free(*ptr);
}

void auto_free_example(void) {
    AUTO_FREE char* buffer = malloc(1024);
    // buffer 在作用域结束时自动释放
}
```

### 模式 5:边界检查

```cpp
// C++:使用容器而非原始数组
#include <vector>
#include <array>
#include <span>

void safe_array_access() {
    std::vector<int> vec = {1, 2, 3, 4, 5};

    // 安全:抛出 std::out_of_range
    try {
        int val = vec.at(10);
    } catch (const std::out_of_range& e) {
        // 处理错误
    }

    // 不安全但更快(无边界检查)
    int val = vec[2];

    // 现代 C++20:用于数组视图的 std::span
    std::span<int> view(vec);
    // 迭代器是边界安全的
    for (int& x : view) {
        x *= 2;
    }
}

// 固定大小数组
void fixed_array() {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};

    // 编译时大小已知
    static_assert(arr.size() == 5);

    // 安全访问
    int val = arr.at(2);
}
```

```rust
// Rust:默认进行边界检查

fn rust_bounds_checking() {
    let vec = vec![1, 2, 3, 4, 5];

    // 运行时边界检查(越界时 panic)
    let val = vec[2];

    // 显式选项(不 panic)
    match vec.get(10) {
        Some(val) => println!("Got {}", val),
        None => println!("Index out of bounds"),
    }

    // 迭代器(无需边界检查)
    for val in &vec {
        println!("{}", val);
    }

    // 切片进行边界检查
    let slice = &vec[1..3]; // [2, 3]
}
```

### 模式 6:防止数据竞争

```cpp
// C++:线程安全的共享状态
#include <mutex>
#include <shared_mutex>
#include <atomic>

class ThreadSafeCounter {
public:
    void increment() {
        // 原子操作
        count_.fetch_add(1, std::memory_order_relaxed);
    }

    int get() const {
        return count_.load(std::memory_order_relaxed);
    }

private:
    std::atomic<int> count_{0};
};

class ThreadSafeMap {
public:
    void write(const std::string& key, int value) {
        std::unique_lock lock(mutex_);
        data_[key] = value;
    }

    std::optional<int> read(const std::string& key) {
        std::shared_lock lock(mutex_);
        auto it = data_.find(key);
        if (it != data_.end()) {
            return it->second;
        }
        return std::nullopt;
    }

private:
    mutable std::shared_mutex mutex_;
    std::map<std::string, int> data_;
};
```

```rust
// Rust:编译时防止数据竞争

use std::sync::{Arc, Mutex, RwLock};
use std::sync::atomic::{AtomicI32, Ordering};
use std::thread;

// 简单类型使用原子
fn atomic_example() {
    let counter = Arc::new(AtomicI32::new(0));

    let handles: Vec<_> = (0..10)
        .map(|_| {
            let counter = Arc::clone(&counter);
            thread::spawn(move || {
                counter.fetch_add(1, Ordering::SeqCst);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Counter: {}", counter.load(Ordering::SeqCst));
}

// 复杂类型使用 Mutex
fn mutex_example() {
    let data = Arc::new(Mutex::new(vec![]));

    let handles: Vec<_> = (0..10)
        .map(|i| {
            let data = Arc::clone(&data);
            thread::spawn(move || {
                let mut vec = data.lock().unwrap();
                vec.push(i);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
}

// 读密集型工作负载使用 RwLock
fn rwlock_example() {
    let data = Arc::new(RwLock::new(HashMap::new()));

    // 多个读者可以
    let read_guard = data.read().unwrap();

    // 写者阻塞读者
    let write_guard = data.write().unwrap();
}
```

## 最佳实践

### 应该做的

- **优先使用 RAII** - 将资源生命周期与作用域绑定
- **使用智能指针** - 在 C++ 中避免原始指针
- **理解所有权** - 知道谁拥有什么
- **检查边界** - 使用安全访问方法
- **使用工具** - AddressSanitizer、Valgrind、Miri

### 不应该做的

- **不要使用原始指针** - 除非与 C 接口
- **不要返回局部引用** - 会导致悬空指针
- **不要忽略编译器警告** - 它们能捕获漏洞
- **不要随意使用 `unsafe`** - 在 Rust 中,尽量减少使用
- **不要假设线程安全** - 要显式说明

## 调试工具

```bash
# AddressSanitizer(Clang/GCC)
clang++ -fsanitize=address -g source.cpp

# Valgrind
valgrind --leak-check=full ./program

# Rust Miri(未定义行为检测器)
cargo +nightly miri run

# ThreadSanitizer
clang++ -fsanitize=thread -g source.cpp
```

## 资源

- [C++ 核心指南](https://isocpp.github.io/CppCoreGuidelines/)
- [Rust 所有权](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)
