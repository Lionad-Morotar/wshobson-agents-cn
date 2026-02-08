---
name: changelog-automation
description: 遵循 Keep a Changelog 格式自动从提交、PR 和发布生成变更日志。用于设置发布工作流、生成发布说明或标准化提交约定。
---

# 变更日志自动化

用于遵循行业标准自动生成变更日志、发布说明和版本管理的模式和工具。

## 何时使用此技能

- 设置自动化变更日志生成
- 实施约定式提交
- 创建发布说明工作流
- 标准化提交消息格式
- 生成 GitHub/GitLab 发布说明
- 管理语义版本控制

## 核心概念

### 1. Keep a Changelog 格式

```markdown
# Changelog

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
并且本项目遵循 [语义版本控制](https://semver.org/spec/v2.0.0.html)。

## [未发布]

### 新增

- 新功能 X

## [1.2.0] - 2024-01-15

### 新增

- 用户配置文件头像
- 深色模式支持

### 更改

- 加载性能提高 40%

### 已弃用

- 旧的身份验证 API（使用 v2）

### 已移除

- 旧的支付网关

### 修复

- 登录超时问题 (#123)

### 安全

- 为 CVE-2024-1234 更新依赖项

[未发布]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### 2. 约定式提交

```
<type>[可选范围]: <description>

[可选 body]

[可选 footer(s)]
```

| Type       | Description      | Changelog Section  |
| ---------- | ---------------- | ------------------ |
| `feat`     | 新功能           | 新增               |
| `fix`      | Bug 修复         | 修复               |
| `docs`     | 文档             | （通常排除）       |
| `style`    | 格式化           | （通常排除）       |
| `refactor` | 代码重构         | 更改               |
| `perf`     | 性能             | 更改               |
| `test`     | 测试             | （通常排除）       |
| `chore`    | 维护             | （通常排除）       |
| `ci`       | CI 更改          | （通常排除）       |
| `build`    | 构建系统         | （通常排除）       |
| `revert`   | 回滚提交         | 已移除             |

### 3. 语义版本控制

```
MAJOR.MINOR.PATCH

MAJOR：重大更改（feat! 或 BREAKING CHANGE）
MINOR：新功能（feat）
PATCH：Bug 修复（fix）
```

## 实现

### 方法 1：Conventional Changelog（Node.js）

```bash
# 安装工具
npm install -D @commitlint/cli @commitlint/config-conventional
npm install -D husky
npm install -D standard-version
# 或
npm install -D semantic-release

# 设置 commitlint
cat > commitlint.config.js << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'ci',
        'build',
        'revert',
      ],
    ],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'subject-max-length': [2, 'always', 72],
  },
};
EOF

# 设置 husky
npx husky init
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

### 方法 2：standard-version 配置

```javascript
// .versionrc.js
module.exports = {
  types: [
    { type: "feat", section: "Features" },
    { type: "fix", section: "Bug Fixes" },
    { type: "perf", section: "Performance Improvements" },
    { type: "revert", section: "Reverts" },
    { type: "docs", section: "Documentation", hidden: true },
    { type: "style", section: "Styles", hidden: true },
    { type: "chore", section: "Miscellaneous", hidden: true },
    { type: "refactor", section: "Code Refactoring", hidden: true },
    { type: "test", section: "Tests", hidden: true },
    { type: "build", section: "Build System", hidden: true },
    { type: "ci", section: "CI/CD", hidden: true },
  ],
  commitUrlFormat: "{{host}}/{{owner}}/{{repository}}/commit/{{hash}}",
  compareUrlFormat:
    "{{host}}/{{owner}}/{{repository}}/compare/{{previousTag}}...{{currentTag}}",
  issueUrlFormat: "{{host}}/{{owner}}/{{repository}}/issues/{{id}}",
  userUrlFormat: "{{host}}/{{user}}",
  releaseCommitMessageFormat: "chore(release): {{currentTag}}",
  scripts: {
    prebump: 'echo "Running prebump"',
    postbump: 'echo "Running postbump"',
    prechangelog: 'echo "Running prechangelog"',
    postchangelog: 'echo "Running postchangelog"',
  },
};
```

```json
// package.json scripts
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major",
    "release:patch": "standard-version --release-as patch",
    "release:dry": "standard-version --dry-run"
  }
}
```

### 方法 3：semantic-release（完全自动化）

```javascript
// release.config.js
module.exports = {
  branches: [
    "main",
    { name: "beta", prerelease: true },
    { name: "alpha", prerelease: true },
  ],
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        changelogFile: "CHANGELOG.md",
      },
    ],
    [
      "@semantic-release/npm",
      {
        npmPublish: true,
      },
    ],
    [
      "@semantic-release/github",
      {
        assets: ["dist/**/*.js", "dist/**/*.css"],
      },
    ],
    [
      "@semantic-release/git",
      {
        assets: ["CHANGELOG.md", "package.json"],
        message:
          "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}",
      },
    ],
  ],
};
```

### 方法 4：GitHub Actions 工作流

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      release_type:
        description: "Release type"
        required: true
        default: "patch"
        type: choice
        options:
          - patch
          - minor
          - major

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - run: npm ci

      - name: 配置 Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: 运行 semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release

  # 替代方案：使用 standard-version 的手动发布
  manual-release:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - run: npm ci

      - name: 配置 Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: 更新版本并生成变更日志
        run: npx standard-version --release-as ${{ inputs.release_type }}

      - name: 推送更改
        run: git push --follow-tags origin main

      - name: 创建 GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ steps.version.outputs.tag }}
          body_path: RELEASE_NOTES.md
          generate_release_notes: true
```

### 方法 5：git-cliff（基于 Rust，快速）

```toml
# cliff.toml
[changelog]
header = """
# Changelog

本项目的所有重要更改都将记录在此文件中。

"""
body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [未发布]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {% if commit.scope %}**{{ commit.scope }}:** {% endif %}\
            {{ commit.message | upper_first }}\
            {% if commit.github.pr_number %} ([#{{ commit.github.pr_number }}](https://github.com/owner/repo/pull/{{ commit.github.pr_number }})){% endif %}\
    {% endfor %}
{% endfor %}
"""
footer = """
{% for release in releases -%}
    {% if release.version -%}
        {% if release.previous.version -%}
            [{{ release.version | trim_start_matches(pat="v") }}]: \
                https://github.com/owner/repo/compare/{{ release.previous.version }}...{{ release.version }}
        {% endif -%}
    {% else -%}
        [unreleased]: https://github.com/owner/repo/compare/{{ release.previous.version }}...HEAD
    {% endif -%}
{% endfor %}
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = true
split_commits = false
commit_parsers = [
    { message = "^feat", group = "Features" },
    { message = "^fix", group = "Bug Fixes" },
    { message = "^doc", group = "Documentation" },
    { message = "^perf", group = "Performance" },
    { message = "^refactor", group = "Refactoring" },
    { message = "^style", group = "Styling" },
    { message = "^test", group = "Testing" },
    { message = "^chore\\(release\\)", skip = true },
    { message = "^chore", group = "Miscellaneous" },
]
filter_commits = false
tag_pattern = "v[0-9]*"
skip_tags = ""
ignore_tags = ""
topo_order = false
sort_commits = "oldest"

[github]
owner = "owner"
repo = "repo"
```

```bash
# 生成变更日志
git cliff -o CHANGELOG.md

# 为特定范围生成
git cliff v1.0.0..v2.0.0 -o RELEASE_NOTES.md

# 预览而不写入
git cliff --unreleased --dry-run
```

### 方法 6：Python（commitizen）

```toml
# pyproject.toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "1.0.0"
version_files = [
    "pyproject.toml:version",
    "src/__init__.py:__version__",
]
tag_format = "v$version"
update_changelog_on_bump = true
changelog_incremental = true
changelog_start_rev = "v0.1.0"

[tool.commitizen.customize]
message_template = "{{change_type}}{% if scope %}({{scope}}){% endif %}: {{message}}"
schema = "<type>(<scope>): <subject>"
schema_pattern = "^(feat|fix|docs|style|refactor|perf|test|chore)(\\(\\w+\\))?:\\s.*"
bump_pattern = "^(feat|fix|perf|refactor)"
bump_map = {"feat" = "MINOR", "fix" = "PATCH", "perf" = "PATCH", "refactor" = "PATCH"}
```

```bash
# 安装
pip install commitizen

# 交互式创建提交
cz commit

# 更新版本并更新变更日志
cz bump --changelog

# 检查提交
cz check --rev-range HEAD~5..HEAD
```

## 发布说明模板

### GitHub Release 模板

```markdown
## What's Changed

### 🚀 Features

{{ range .Features }}

- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
  {{ end }}

### 🐛 Bug Fixes

{{ range .Fixes }}

- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
  {{ end }}

### 📚 Documentation

{{ range .Docs }}

- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
  {{ end }}

### 🔧 Maintenance

{{ range .Chores }}

- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
  {{ end }}

## New Contributors

{{ range .NewContributors }}

- @{{ .Username }} made their first contribution in #{{ .PR }}
  {{ end }}

**Full Changelog**: https://github.com/owner/repo/compare/v{{ .Previous }}...v{{ .Current }}
```

### 内部发布说明

```markdown
# Release v2.1.0 - January 15, 2024

## 摘要

此版本引入了深色模式支持，并将结账性能提高了 40%。它还包括重要的安全更新。

## 亮点

### 🌙 深色模式

用户现在可以从设置切换到深色模式。该偏好设置会自动保存并在设备间同步。

### ⚡ 性能

- 结账流程快 40%
- 包大小减少 15%

## 重大更改

此版本中没有。

## 升级指南

不需要特殊步骤。应用标准部署流程。

## 已知问题

- 深色模式在初始加载时可能会闪烁（修复计划在 v2.1.1 中）

## 依赖项更新

| Package | From    | To      | Reason                   |
| ------- | ------- | ------- | ------------------------ |
| react   | 18.2.0  | 18.3.0  | Performance improvements |
| lodash  | 4.17.20 | 4.17.21 | Security patch           |
```

## 提交消息示例

```bash
# 带范围的功能
feat(auth): 为 Google 登录添加 OAuth2 支持

# 带问题引用的 Bug 修复
fix(checkout): 解决支付处理中的竞争条件

Closes #123

# 重大更改
feat(api)!: 更改用户端点响应格式

BREAKING CHANGE: 用户端点现在返回 `userId` 而不是 `id`。
迁移指南：更新所有 API 使用者以使用新的字段名称。

# 多段式
fix(database): 优雅地处理连接超时

以前，连接超时会导致整个请求在重试之前失败
此更改实现了指数退避，最多
在失败前重试 3 次。

超时阈值已从 5s 增加到 10s，基于 p99
延迟分析。

Fixes #456
Reviewed-by: @alice
```

## 最佳实践

### 应该做的

- **遵循约定式提交** - 启用自动化
- **编写清晰的消息** - 未来的你会感谢你
- **引用问题** - 将提交链接到票据
- **一致使用范围** - 定义团队约定
- **自动化发布** - 减少人为错误

### 不应该做的

- **不要混合更改** - 每次提交一个逻辑更改
- **不要跳过验证** - 使用 commitlint
- **不要手动编辑** - 仅生成的变更日志
- **不要忘记重大更改** - 使用 `!` 或页脚标记
- **不要忽略 CI** - 在管道中验证提交

## 资源

- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [semantic-release](https://semantic-release.gitbook.io/)
- [git-cliff](https://git-cliff.org/)
