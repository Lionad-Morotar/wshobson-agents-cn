---
name: bash-defensive-patterns
description: 掌握用于生产级脚本的防御性 Bash 编程技术。在编写稳健的 shell 脚本、CI/CD 流水线或需要容错和安全性的系统工具时使用。
---

# Bash 防御性模式

使用防御性编程技术、错误处理和安全最佳实践编写生产级 Bash 脚本的综合指南，以防止常见陷阱并确保可靠性。

## 何时使用此技能

- 编写生产自动化脚本
- 构建 CI/CD 流水线脚本
- 创建系统管理工具
- 开发具有容错能力的部署自动化
- 编写必须安全处理边缘情况的脚本
- 构建可维护的 shell 脚本库
- 实现全面的日志记录和监控
- 创建必须跨不同平台工作的脚本

## 核心防御原则

### 1. 严格模式

在每个脚本开头启用 bash 严格模式，以便及早捕获错误。

```bash
#!/bin/bash
set -Eeuo pipefail  # 遇到错误、未设置变量、管道失败时退出
```

**关键标志：**

- `set -E`: 在函数中继承 ERR 捕获
- `set -e`: 任何错误时退出（命令返回非零值）
- `set -u`: 未定义变量引用时退出
- `set -o pipefail`: 管道中任何命令失败时管道失败（不仅仅是最后一个）

### 2. 错误捕获和清理

在脚本退出或错误时实现适当的清理。

```bash
#!/bin/bash
set -Eeuo pipefail

trap 'echo "Error on line $LINENO"' ERR
trap 'echo "Cleaning up..."; rm -rf "$TMPDIR"' EXIT

TMPDIR=$(mktemp -d)
# 脚本代码在这里
```

### 3. 变量安全

始终引用变量以防止单词分割和通配符问题。

```bash
# 错误 - 不安全
cp $source $dest

# 正确 - 安全
cp "$source" "$dest"

# 必需变量 - 如果未设置则显示消息并失败
: "${REQUIRED_VAR:?REQUIRED_VAR is not set}"
```

### 4. 数组处理

安全地使用数组进行复杂数据处理。

```bash
# 安全的数组迭代
declare -a items=("item 1" "item 2" "item 3")

for item in "${items[@]}"; do
    echo "Processing: $item"
done

# 安全地将输出读取到数组
mapfile -t lines < <(some_command)
readarray -t numbers < <(seq 1 10)
```

### 5. 条件安全

使用 `[[ ]]` 进行 Bash 特定功能，使用 `[ ]` 进行 POSIX 兼容。

```bash
# Bash - 更安全
if [[ -f "$file" && -r "$file" ]]; then
    content=$(<"$file")
fi

# POSIX - 可移植
if [ -f "$file" ] && [ -r "$file" ]; then
    content=$(cat "$file")
fi

# 在操作之前测试是否存在
if [[ -z "${VAR:-}" ]]; then
    echo "VAR is not set or is empty"
fi
```

## 基本模式

### 模式 1：安全脚本目录检测

```bash
#!/bin/bash
set -Eeuo pipefail

# 正确确定脚本目录
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
SCRIPT_NAME="$(basename -- "${BASH_SOURCE[0]}")"

echo "Script location: $SCRIPT_DIR/$SCRIPT_NAME"
```

### 模式 2：综合函数模板

```bash
#!/bin/bash
set -Eeuo pipefail

# 函数前缀：handle_*、process_*、check_*、validate_*
# 包含文档和错误处理

validate_file() {
    local -r file="$1"
    local -r message="${2:-File not found: $file}"

    if [[ ! -f "$file" ]]; then
        echo "ERROR: $message" >&2
        return 1
    fi
    return 0
}

process_files() {
    local -r input_dir="$1"
    local -r output_dir="$2"

    # 验证输入
    [[ -d "$input_dir" ]] || { echo "ERROR: input_dir not a directory" >&2; return 1; }

    # 根据需要创建输出目录
    mkdir -p "$output_dir" || { echo "ERROR: Cannot create output_dir" >&2; return 1; }

    # 安全地处理文件
    while IFS= read -r -d '' file; do
        echo "Processing: $file"
        # 执行工作
    done < <(find "$input_dir" -maxdepth 1 -type f -print0)

    return 0
}
```

### 模式 3：安全临时文件处理

```bash
#!/bin/bash
set -Eeuo pipefail

trap 'rm -rf -- "$TMPDIR"' EXIT

# 创建临时目录
TMPDIR=$(mktemp -d) || { echo "ERROR: Failed to create temp directory" >&2; exit 1; }

# 在目录中创建临时文件
TMPFILE1="$TMPDIR/temp1.txt"
TMPFILE2="$TMPDIR/temp2.txt"

# 使用临时文件
touch "$TMPFILE1" "$TMPFILE2"

echo "Temp files created in: $TMPDIR"
```

### 模式 4：健壮的参数解析

```bash
#!/bin/bash
set -Eeuo pipefail

# 默认值
VERBOSE=false
DRY_RUN=false
OUTPUT_FILE=""
THREADS=4

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
    -v, --verbose       Enable verbose output
    -d, --dry-run       Run without making changes
    -o, --output FILE   Output file path
    -j, --jobs NUM      Number of parallel jobs
    -h, --help          Show this help message
EOF
    exit "${1:-0}"
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -j|--jobs)
            THREADS="$2"
            shift 2
            ;;
        -h|--help)
            usage 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            usage 1
            ;;
    esac
done

# 验证必需参数
[[ -n "$OUTPUT_FILE" ]] || { echo "ERROR: -o/--output is required" >&2; usage 1; }
```

### 模式 5：结构化日志记录

```bash
#!/bin/bash
set -Eeuo pipefail

# 日志函数
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2
}

log_warn() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] DEBUG: $*" >&2
    fi
}

# 使用
log_info "Starting script"
log_debug "Debug information"
log_warn "Warning message"
log_error "Error occurred"
```

### 模式 6：信号处理协调

```bash
#!/bin/bash
set -Eeuo pipefail

# 跟踪后台进程
PIDS=()

cleanup() {
    log_info "Shutting down..."

    # 终止所有后台进程
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    # 等待优雅关闭
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
}

trap cleanup SIGTERM SIGINT

# 启动后台任务
background_task &
PIDS+=($!)

another_task &
PIDS+=($!)

# 等待所有后台进程
wait
```

### 模式 7：安全文件操作

```bash
#!/bin/bash
set -Eeuo pipefail

# 使用 -i 标志安全移动而不覆盖
safe_move() {
    local -r source="$1"
    local -r dest="$2"

    if [[ ! -e "$source" ]]; then
        echo "ERROR: Source does not exist: $source" >&2
        return 1
    fi

    if [[ -e "$dest" ]]; then
        echo "ERROR: Destination already exists: $dest" >&2
        return 1
    fi

    mv "$source" "$dest"
}

# 安全目录清理
safe_rmdir() {
    local -r dir="$1"

    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Not a directory: $dir" >&2
        return 1
    fi

    # 使用 -I 标志在删除前提示（BSD/GNU 兼容）
    rm -rI -- "$dir"
}

# 原子文件写入
atomic_write() {
    local -r target="$1"
    local -r tmpfile
    tmpfile=$(mktemp) || return 1

    # 首先写入临时文件
    cat > "$tmpfile"

    # 原子重命名
    mv "$tmpfile" "$target"
}
```

### 模式 8：幂等脚本设计

```bash
#!/bin/bash
set -Eeuo pipefail

# 检查资源是否已存在
ensure_directory() {
    local -r dir="$1"

    if [[ -d "$dir" ]]; then
        log_info "Directory already exists: $dir"
        return 0
    fi

    mkdir -p "$dir" || {
        log_error "Failed to create directory: $dir"
        return 1
    }

    log_info "Created directory: $dir"
}

# 确保配置状态
ensure_config() {
    local -r config_file="$1"
    local -r default_value="$2"

    if [[ ! -f "$config_file" ]]; then
        echo "$default_value" > "$config_file"
        log_info "Created config: $config_file"
    fi
}

# 多次重新运行脚本应该是安全的
ensure_directory "/var/cache/myapp"
ensure_config "/etc/myapp/config" "DEBUG=false"
```

### 模式 9：安全命令替换

```bash
#!/bin/bash
set -Eeuo pipefail

# 使用 $() 而不是反引号
name=$(<"$file")  # 现代、安全的从文件变量赋值
output=$(command -v python3)  # 安全地获取命令位置

# 使用错误检查处理命令替换
result=$(command -v node) || {
    log_error "node command not found"
    return 1
}

# 对于多行
mapfile -t lines < <(grep "pattern" "$file")

# NUL 安全迭代
while IFS= read -r -d '' file; do
    echo "Processing: $file"
done < <(find /path -type f -print0)
```

### 模式 10：试运行支持

```bash
#!/bin/bash
set -Eeuo pipefail

DRY_RUN="${DRY_RUN:-false}"

run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Would execute: $*"
        return 0
    fi

    "$@"
}

# 使用
run_cmd cp "$source" "$dest"
run_cmd rm "$file"
run_cmd chown "$owner" "$target"
```

## 高级防御技术

### 命名参数模式

```bash
#!/bin/bash
set -Eeuo pipefail

process_data() {
    local input_file=""
    local output_dir=""
    local format="json"

    # 解析命名参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --input=*)
                input_file="${1#*=}"
                ;;
            --output=*)
                output_dir="${1#*=}"
                ;;
            --format=*)
                format="${1#*=}"
                ;;
            *)
                echo "ERROR: Unknown parameter: $1" >&2
                return 1
                ;;
        esac
        shift
    done

    # 验证必需参数
    [[ -n "$input_file" ]] || { echo "ERROR: --input is required" >&2; return 1; }
    [[ -n "$output_dir" ]] || { echo "ERROR: --output is required" >&2; return 1; }
}
```

### 依赖检查

```bash
#!/bin/bash
set -Eeuo pipefail

check_dependencies() {
    local -a missing_deps=()
    local -a required=("jq" "curl" "git")

    for cmd in "${required[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo "ERROR: Missing required commands: ${missing_deps[*]}" >&2
        return 1
    fi
}

check_dependencies
```

## 最佳实践总结

1. **始终使用严格模式** - `set -Eeuo pipefail`
2. **引用所有变量** - `"$variable"` 防止单词分割
3. **使用 [[]] 条件** - 比 [ ] 更健壮
4. **实现错误捕获** - 优雅地捕获和处理错误
5. **验证所有输入** - 检查文件存在性、权限、格式
6. **使用函数提高可重用性** - 使用有意义的前缀
7. **实现结构化日志记录** - 包含时间戳和级别
8. **支持试运行模式** - 允许用户预览更改
9. **安全处理临时文件** - 使用 mktemp、使用 trap 清理
10. **设计幂等性** - 脚本应该可以安全地重新运行
11. **记录需求** - 列出依赖项和最低版本
12. **测试错误路径** - 确保错误处理正常工作
13. **使用 `command -v`** - 检查可执行文件比 `which` 更安全
14. **优先使用 printf 而不是 echo** - 在不同系统上更可预测

## 资源

- **Bash Strict Mode**: http://redsymbol.net/articles/unofficial-bash-strict-mode/
- **Google Shell Style Guide**: https://google.github.io/styleguide/shellguide.html
- **Defensive BASH Programming**: https://www.lifepipe.net/
