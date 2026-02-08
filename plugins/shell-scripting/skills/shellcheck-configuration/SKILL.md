---
name: shellcheck-configuration
description: 掌握 ShellCheck 静态分析配置和使用，提升 Shell 脚本质量。在设置代码检查基础设施、修复代码问题或确保脚本可移植性时使用。
---

# ShellCheck 配置与静态分析

配置和使用 ShellCheck 的综合指南，通过静态代码分析提升 Shell 脚本质量，捕获常见陷阱，并强制执行最佳实践。

## 何时使用此技能

- 在 CI/CD 流水线中为 Shell 脚本设置代码检查
- 分析现有 Shell 脚本的问题
- 理解 ShellCheck 错误代码和警告
- 为特定项目需求配置 ShellCheck
- 将 ShellCheck 集成到开发工作流中
- 抑制误报并配置规则集
- 强制执行一致的代码质量标准
- 迁移脚本以满足质量门禁

## ShellCheck 基础

### 什么是 ShellCheck？

ShellCheck 是一个静态分析工具，用于分析 Shell 脚本并检测问题模式。它支持：

- Bash、sh、dash、ksh 和其他 POSIX shell
- 超过 100 种不同的警告和错误
- 针对目标 shell 和标志的配置
- 与编辑器和 CI/CD 系统集成

### 安装

```bash
# macOS 使用 Homebrew
brew install shellcheck

# Ubuntu/Debian
apt-get install shellcheck

# 从源码安装
git clone https://github.com/koalaman/shellcheck.git
cd shellcheck
make build
make install

# 验证安装
shellcheck --version
```

## 配置文件

### .shellcheckrc（项目级别）

在项目根目录创建 `.shellcheckrc`：

```
# 指定目标 shell
shell=bash

# 启用可选检查
enable=avoid-nullary-conditions
enable=require-variable-braces

# 禁用特定警告
disable=SC1091
disable=SC2086
```

### 环境变量

```bash
# 设置默认 shell 目标
export SHELLCHECK_SHELL=bash

# 启用严格模式
export SHELLCHECK_STRICT=true

# 指定配置文件位置
export SHELLCHECK_CONFIG=~/.shellcheckrc
```

## 常见 ShellCheck 错误代码

### SC1000-1099：解析器错误

```bash
# SC1004：反斜杠续行后未跟换行符
echo hello\
world  # 错误 - 需要行续行

# SC1008：运算符 `==' 的无效数据
if [[ $var =  "value" ]]; then  # == 前的空格
    true
fi
```

### SC2000-2099：Shell 问题

```bash
# SC2009：考虑使用 pgrep 或 pidof 而非 grep|grep
ps aux | grep -v grep | grep myprocess  # 改用 pgrep

# SC2012：仅将 `ls` 用于查看。使用 `find` 获得可靠输出
for file in $(ls -la)  # 更好：使用 find 或 globbing

# SC2015：避免使用 && 和 || 代替 if-then-else
[[ -f "$file" ]] && echo "found" || echo "not found"  # 不够清晰

# SC2016：表达式在单引号中不会展开
echo '$VAR'  # 字面量 $VAR，不是变量展开

# SC2026：此单词是非标准的。在使用其他 shell 的脚本时
# 设置 POSIXLY_CORRECT
```

### SC2100-2199：引号问题

```bash
# SC2086：使用双引号防止 globbing 和单词分割
for i in $list; do  # 应该是：for i in $list 或 for i in "$list"
    echo "$i"
done

# SC2115：路径中的字面量波浪号未展开。使用 $HOME 代替
~/.bashrc  # 在字符串中，使用 "$HOME/.bashrc"

# SC2181：直接使用 `if` 检查退出码，而非间接检查
some_command
if [ $? -eq 0 ]; then  # 更好：if some_command; then

# SC2206：使用引号防止单词分割或设置 IFS
array=( $items )  # 应该使用：array=( $items )
```

### SC3000-3999：POSIX 兼容性问题

```bash
# SC3010：在 POSIX sh 中，使用 'case' 而非 'cond && foo'
[[ $var == "value" ]] && do_something  # 非 POSIX

# SC3043：在 POSIX sh 中，'local' 未定义
function my_func() {
    local var=value  # 在某些 shell 中非 POSIX
}
```

## 实用配置示例

### 最小配置（严格 POSIX）

```bash
#!/bin/bash
# 配置以实现最大可移植性

shellcheck \
  --shell=sh \
  --external-sources \
  --check-sourced \
  script.sh
```

### 开发配置（Bash 放宽规则）

```bash
#!/bin/bash
# 为 Bash 开发配置

shellcheck \
  --shell=bash \
  --exclude=SC1091,SC2119 \
  --enable=all \
  script.sh
```

### CI/CD 集成配置

```bash
#!/bin/bash
set -Eeuo pipefail

# 分析所有 shell 脚本，发现问题则失败
find . -type f -name "*.sh" | while read -r script; do
    echo "Checking: $script"
    shellcheck \
        --shell=bash \
        --format=gcc \
        --exclude=SC1091 \
        "$script" || exit 1
done
```

### 项目 .shellcheckrc

```
# 分析的目标 shell 方言
shell=bash

# 启用可选检查
enable=avoid-nullary-conditions,require-variable-braces,check-unassigned-uppercase

# 禁用特定警告
# SC1091：不跟踪源文件（许多误报）
disable=SC1091

# SC2119：使用 function_name 而非 function_name -- (arguments)
disable=SC2119

# 为上下文引入的外部文件
external-sources=true
```

## 集成模式

### Pre-commit Hook 配置

```bash
#!/bin/bash
# .git/hooks/pre-commit

#!/bin/bash
set -e

# 查找此提交中更改的所有 shell 脚本
git diff --cached --name-only | grep '\.sh$' | while read -r script; do
    echo "Linting: $script"

    if ! shellcheck "$script"; then
        echo "ShellCheck failed on $script"
        exit 1
    fi
done
```

### GitHub Actions 工作流

```yaml
name: ShellCheck

on: [push, pull_request]

jobs:
  shellcheck:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run ShellCheck
        run: |
          sudo apt-get install shellcheck
          find . -type f -name "*.sh" -exec shellcheck {} \;
```

### GitLab CI 流水线

```yaml
shellcheck:
  stage: lint
  image: koalaman/shellcheck-alpine
  script:
    - find . -type f -name "*.sh" -exec shellcheck {} \;
  allow_failure: false
```

## 处理 ShellCheck 违规

### 抑制特定警告

```bash
#!/bin/bash

# 禁用整行的警告
# shellcheck disable=SC2086
for file in $(ls -la); do
    echo "$file"
done

# 禁用整个脚本的警告
# shellcheck disable=SC1091,SC2119

# 禁用多个警告（格式不同）
command_that_fails() {
    # shellcheck disable=SC2015
    [ -f "$1" ] && echo "found" || echo "not found"
}

# 禁用源指令的特定检查
# shellcheck source=./helper.sh
source helper.sh
```

### 常见违规和修复

#### SC2086：使用双引号防止单词分割

```bash
# 问题
for i in $list; do done

# 解决方案
for i in $list; do done  # 如果 $list 已加引号，或
for i in "${list[@]}"; do done  # 如果 list 是数组
```

#### SC2181：直接检查退出码

```bash
# 问题
some_command
if [ $? -eq 0 ]; then
    echo "success"
fi

# 解决方案
if some_command; then
    echo "success"
fi
```

#### SC2015：使用 if-then 而非 && ||

```bash
# 问题
[ -f "$file" ] && echo "exists" || echo "not found"

# 解决方案 - 意图更清晰
if [ -f "$file" ]; then
    echo "exists"
else
    echo "not found"
fi
```

#### SC2016：表达式在单引号中不会展开

```bash
# 问题
echo 'Variable value: $VAR'

# 解决方案
echo "Variable value: $VAR"
```

#### SC2009：使用 pgrep 而非 grep

```bash
# 问题
ps aux | grep -v grep | grep myprocess

# 解决方案
pgrep -f myprocess
```

## 性能优化

### 检查多个文件

```bash
#!/bin/bash

# 顺序检查
for script in *.sh; do
    shellcheck "$script"
done

# 并行检查（更快）
find . -name "*.sh" -print0 | \
    xargs -0 -P 4 -n 1 shellcheck
```

### 缓存结果

```bash
#!/bin/bash

CACHE_DIR=".shellcheck_cache"
mkdir -p "$CACHE_DIR"

check_script() {
    local script="$1"
    local hash
    local cache_file

    hash=$(sha256sum "$script" | cut -d' ' -f1)
    cache_file="$CACHE_DIR/$hash"

    if [[ ! -f "$cache_file" ]]; then
        if shellcheck "$script" > "$cache_file" 2>&1; then
            touch "$cache_file.ok"
        else
            return 1
        fi
    fi

    [[ -f "$cache_file.ok" ]]
}

find . -name "*.sh" | while read -r script; do
    check_script "$script" || exit 1
done
```

## 输出格式

### 默认格式

```bash
shellcheck script.sh

# 输出：
# script.sh:1:3: warning: foo is referenced but not assigned. [SC2154]
```

### GCC 格式（用于 CI/CD）

```bash
shellcheck --format=gcc script.sh

# 输出：
# script.sh:1:3: warning: foo is referenced but not assigned.
```

### JSON 格式（用于解析）

```bash
shellcheck --format=json script.sh

# 输出：
# [{"file": "script.sh", "line": 1, "column": 3, "level": "warning", "code": 2154, "message": "..."}]
```

### 静默格式

```bash
shellcheck --format=quiet script.sh

# 如果发现问题则返回非零值，否则无输出
```

## 最佳实践

1. **在 CI/CD 中运行 ShellCheck** - 在合并前捕获问题
2. **为目标 shell 配置** - 不要将 bash 作为 sh 分析
3. **记录排除项** - 解释为什么抑制违规
4. **解决违规** - 不要只是禁用警告
5. **启用严格模式** - 使用 `--enable=all` 并小心排除
6. **定期更新** - 保持 ShellCheck 最新以获得新检查
7. **使用 pre-commit hooks** - 在推送前本地捕获问题
8. **与编辑器集成** - 在开发期间获得实时反馈

## 资源

- **ShellCheck GitHub**: https://github.com/koalaman/shellcheck
- **ShellCheck Wiki**: https://www.shellcheck.net/wiki/
- **错误代码参考**: https://www.shellcheck.net/
