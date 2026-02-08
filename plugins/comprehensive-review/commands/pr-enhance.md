# Pull Request 增强

你是一位 PR 优化专家，专门创建高质量的 pull request，以促进高效的代码审查。生成全面的 PR 描述，自动化审查流程，并确保 PR 遵循清晰度、规模和可审查性的最佳实践。

## 上下文

用户需要创建或改进具有详细描述、适当文档、测试覆盖率分析和审查便利性的 pull request。专注于使 PR 易于审查、文档齐全，并包含所有必要的上下文。

## 要求

$ARGUMENTS

## 指令

### 1. PR 分析

分析变更并生成洞察：

**变更摘要生成器**

```python
import subprocess
import re
from collections import defaultdict

class PRAnalyzer:
    def analyze_changes(self, base_branch='main'):
        """
        分析当前分支与基础分支之间的变更
        """
        analysis = {
            'files_changed': self._get_changed_files(base_branch),
            'change_statistics': self._get_change_stats(base_branch),
            'change_categories': self._categorize_changes(base_branch),
            'potential_impacts': self._assess_impacts(base_branch),
            'dependencies_affected': self._check_dependencies(base_branch)
        }

        return analysis

    def _get_changed_files(self, base_branch):
        """获取变更文件列表及统计信息"""
        cmd = f"git diff --name-status {base_branch}...HEAD"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                status, filename = line.split('\t', 1)
                files.append({
                    'filename': filename,
                    'status': self._parse_status(status),
                    'category': self._categorize_file(filename)
                })

        return files

    def _get_change_stats(self, base_branch):
        """获取详细变更统计"""
        cmd = f"git diff --shortstat {base_branch}...HEAD"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        # 解析输出如："10 files changed, 450 insertions(+), 123 deletions(-)"
        stats_pattern = r'(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?'
        match = re.search(stats_pattern, result.stdout)

        if match:
            files, insertions, deletions = match.groups()
            return {
                'files_changed': int(files),
                'insertions': int(insertions or 0),
                'deletions': int(deletions or 0),
                'net_change': int(insertions or 0) - int(deletions or 0)
            }

        return {'files_changed': 0, 'insertions': 0, 'deletions': 0, 'net_change': 0}

    def _categorize_file(self, filename):
        """按类型分类文件"""
        categories = {
            'source': ['.js', '.ts', '.py', '.java', '.go', '.rs'],
            'test': ['test', 'spec', '.test.', '.spec.'],
            'config': ['config', '.json', '.yml', '.yaml', '.toml'],
            'docs': ['.md', 'README', 'CHANGELOG', '.rst'],
            'styles': ['.css', '.scss', '.less'],
            'build': ['Makefile', 'Dockerfile', '.gradle', 'pom.xml']
        }

        for category, patterns in categories.items():
            if any(pattern in filename for pattern in patterns):
                return category

        return 'other'
```

### 2. PR 描述生成

创建全面的 PR 描述：

**描述模板生成器**

```python
def generate_pr_description(analysis, commits):
    """
    从分析生成详细的 PR 描述
    """
    description = f"""
## 摘要

{generate_summary(analysis, commits)}

## 变更内容

{generate_change_list(analysis)}

## 变更原因

{extract_why_from_commits(commits)}

## 变更类型

{determine_change_types(analysis)}

## 测试方法

{generate_test_section(analysis)}

## 视觉变更

{generate_visual_section(analysis)}

## 性能影响

{analyze_performance_impact(analysis)}

## 破坏性变更

{identify_breaking_changes(analysis)}

## 依赖项

{list_dependency_changes(analysis)}

## 检查清单

{generate_review_checklist(analysis)}

## 附加说明

{generate_additional_notes(analysis)}
"""
    return description

def generate_summary(analysis, commits):
    """生成执行摘要"""
    stats = analysis['change_statistics']

    # 从提交中提取主要目的
    main_purpose = extract_main_purpose(commits)

    summary = f"""
此 PR {main_purpose}。

**影响**：{stats['files_changed']} 个文件变更（{stats['insertions']} 行添加，{stats['deletions']} 行删除）
**风险级别**：{calculate_risk_level(analysis)}
**审查时间**：约 {estimate_review_time(stats)} 分钟
"""
    return summary

def generate_change_list(analysis):
    """生成分类变更列表"""
    changes_by_category = defaultdict(list)

    for file in analysis['files_changed']:
        changes_by_category[file['category']].append(file)

    change_list = ""
    icons = {
        'source': '🔧',
        'test': '✅',
        'docs': '📝',
        'config': '⚙️',
        'styles': '🎨',
        'build': '🏗️',
        'other': '📁'
    }

    for category, files in changes_by_category.items():
        change_list += f"\n### {icons.get(category, '📁')} {category.title()} 变更\n"
        for file in files[:10]:  # 每个类别限制 10 个文件
            change_list += f"- {file['status']}: `{file['filename']}`\n"
        if len(files) > 10:
            change_list += f"- ...以及 {len(files) - 10} 个其他文件\n"

    return change_list
```

### 3. 审查清单生成

创建自动化审查清单：

**智能清单生成器**

```python
def generate_review_checklist(analysis):
    """
    生成上下文感知的审查清单
    """
    checklist = ["## 审查清单\n"]

    # 通用项目
    general_items = [
        "代码遵循项目样式指南",
        "已完成自我审查",
        "为复杂逻辑添加了注释",
        "没有遗留调试代码",
        "没有暴露敏感数据"
    ]

    # 添加通用项目
    checklist.append("### 通用")
    for item in general_items:
        checklist.append(f"- [ ] {item}")

    # 特定文件检查
    file_types = {file['category'] for file in analysis['files_changed']}

    if 'source' in file_types:
        checklist.append("\n### 代码质量")
        checklist.extend([
            "- [ ] 没有代码重复",
            "- [ ] 函数专注且简短",
            "- [ ] 变量名具有描述性",
            "- [ ] 错误处理全面",
            "- [ ] 没有引入性能瓶颈"
        ])

    if 'test' in file_types:
        checklist.append("\n### 测试")
        checklist.extend([
            "- [ ] 所有新代码都有测试覆盖",
            "- [ ] 测试有意义而非仅仅为了覆盖率",
            "- [ ] 边界情况已测试",
            "- [ ] 测试遵循 AAA 模式（Arrange、Act、Assert）",
            "- [ ] 没有引入不稳定的测试"
        ])

    if 'config' in file_types:
        checklist.append("\n### 配置")
        checklist.extend([
            "- [ ] 没有硬编码值",
            "- [ ] 环境变量已记录",
            "- [ ] 维持了向后兼容性",
            "- [ ] 安全影响已审查",
            "- [ ] 默认值合理"
        ])

    if 'docs' in file_types:
        checklist.append("\n### 文档")
        checklist.extend([
            "- [ ] 文档清晰准确",
            "- [ ] 在有帮助的地方提供了示例",
            "- [ ] API 变更已记录",
            "- [ ] 必要时更新了 README",
            "- [ ] 更新了变更日志"
        ])

    # 安全检查
    if has_security_implications(analysis):
        checklist.append("\n### 安全")
        checklist.extend([
            "- [ ] 没有 SQL 注入漏洞",
            "- [ ] 实现了输入验证",
            "- [ ] 身份验证/授权正确",
            "- [ ] 日志中没有敏感数据",
            "- [ ] 依赖项安全"
        ])

    return '\n'.join(checklist)
```

### 4. 代码审查自动化

自动化常见审查任务：

**自动化审查机器人**

```python
class ReviewBot:
    def perform_automated_checks(self, pr_diff):
        """
        执行自动化代码审查检查
        """
        findings = []

        # 检查常见问题
        checks = [
            self._check_console_logs,
            self._check_commented_code,
            self._check_large_functions,
            self._check_todo_comments,
            self._check_hardcoded_values,
            self._check_missing_error_handling,
            self._check_security_issues
        ]

        for check in checks:
            findings.extend(check(pr_diff))

        return findings

    def _check_console_logs(self, diff):
        """检查 console.log 语句"""
        findings = []
        pattern = r'\+.*console\.(log|debug|info|warn|error)'

        for file, content in diff.items():
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                findings.append({
                    'type': 'warning',
                    'file': file,
                    'line': self._get_line_number(match, content),
                    'message': '发现 console 语句 - 合并前请移除',
                    'suggestion': '请使用适当的日志框架'
                })

        return findings

    def _check_large_functions(self, diff):
        """检查过大的函数"""
        findings = []

        # 简单启发式：计算函数开始和结束之间的行数
        for file, content in diff.items():
            if file.endswith(('.js', '.ts', '.py')):
                functions = self._extract_functions(content)
                for func in functions:
                    if func['lines'] > 50:
                        findings.append({
                            'type': 'suggestion',
                            'file': file,
                            'line': func['start_line'],
                            'message': f"函数 '{func['name']}' 有 {func['lines']} 行",
                            'suggestion': '考虑拆分为更小的函数'
                        })

        return findings
```

### 5. PR 规模优化

帮助拆分大型 PR：

**PR 拆分建议**

```python
def suggest_pr_splits(analysis):
    """
    建议如何拆分大型 PR
    """
    stats = analysis['change_statistics']

    # 检查 PR 是否过大
    if stats['files_changed'] > 20 or stats['insertions'] + stats['deletions'] > 1000:
        suggestions = analyze_split_opportunities(analysis)

        return f"""
## ⚠️ 检测到大型 PR

此 PR 变更了 {stats['files_changed']} 个文件，总计 {stats['insertions'] + stats['deletions']} 处变更。
大型 PR 更难审查，更有可能引入 Bug。

### 建议的拆分方案：

{format_split_suggestions(suggestions)}

### 拆分方法：

1. 从当前分支创建功能分支
2. 为第一个逻辑单元挑选提交
3. 为第一个单元创建 PR
4. 对剩余单元重复此操作

```bash
# 示例拆分工作流
git checkout -b feature/part-1
git cherry-pick <part-1 的提交哈希>
git push origin feature/part-1
# 为第 1 部分创建 PR

git checkout -b feature/part-2
git cherry-pick <part-2 的提交哈希>
git push origin feature/part-2
# 为第 2 部分创建 PR
```

"""

    return ""

def analyze_split_opportunities(analysis):
    """查找拆分的逻辑单元"""
    suggestions = []

    # 按功能区域分组
    feature_groups = defaultdict(list)
    for file in analysis['files_changed']:
        feature = extract_feature_area(file['filename'])
        feature_groups[feature].append(file)

    # 建议拆分
    for feature, files in feature_groups.items():
        if len(files) >= 5:
            suggestions.append({
                'name': f"{feature} 变更",
                'files': files,
                'reason': f"隔离的 {feature} 功能变更"
            })

    return suggestions
```

### 6. 视觉差异增强

生成可视化表示：

**Mermaid 图表生成器**

```python
def generate_architecture_diff(analysis):
    """
    生成显示架构变更的图表
    """
    if has_architectural_changes(analysis):
        return f"""
## 架构变更

```mermaid
graph LR
    subgraph "变更前"
        A1[组件 A] --> B1[组件 B]
        B1 --> C1[数据库]
    end

    subgraph "变更后"
        A2[组件 A] --> B2[组件 B]
        B2 --> C2[数据库]
        B2 --> D2[新增缓存层]
        A2 --> E2[新增 API 网关]
    end

    style D2 fill:#90EE90
    style E2 fill:#90EE90
```

### 关键变更：

1. 添加了缓存层以提高性能
2. 引入了 API 网关以改善路由
3. 重构了组件通信
   """
    return ""
```

### 7. 测试覆盖率报告

包含测试覆盖率分析：

**覆盖率报告生成器**

```python
def generate_coverage_report(base_branch='main'):
    """
    生成测试覆盖率对比
    """
    # 获取前后的覆盖率
    before_coverage = get_coverage_for_branch(base_branch)
    after_coverage = get_coverage_for_branch('HEAD')

    coverage_diff = after_coverage - before_coverage

    report = f"""
## 测试覆盖率

| 指标 | 变更前 | 变更后 | 变化 |
|--------|--------|-------|--------|
| 行数 | {before_coverage['lines']:.1f}% | {after_coverage['lines']:.1f}% | {format_diff(coverage_diff['lines'])} |
| 函数 | {before_coverage['functions']:.1f}% | {after_coverage['functions']:.1f}% | {format_diff(coverage_diff['functions'])} |
| 分支 | {before_coverage['branches']:.1f}% | {after_coverage['branches']:.1f}% | {format_diff(coverage_diff['branches'])} |

### 未覆盖的文件
"""

    # 列出低覆盖率的文件
    for file in get_low_coverage_files():
        report += f"- `{file['name']}`: {file['coverage']:.1f}% 覆盖率\n"

    return report

def format_diff(value):
    """格式化覆盖率差异"""
    if value > 0:
        return f"<span style='color: green'>+{value:.1f}%</span> ✅"
    elif value < 0:
        return f"<span style='color: red'>{value:.1f}%</span> ⚠️"
    else:
        return "无变化"
```

### 8. 风险评估

评估 PR 风险：

**风险计算器**

```python
def calculate_pr_risk(analysis):
    """
    计算 PR 的风险分数
    """
    risk_factors = {
        'size': calculate_size_risk(analysis),
        'complexity': calculate_complexity_risk(analysis),
        'test_coverage': calculate_test_risk(analysis),
        'dependencies': calculate_dependency_risk(analysis),
        'security': calculate_security_risk(analysis)
    }

    overall_risk = sum(risk_factors.values()) / len(risk_factors)

    risk_report = f"""
## 风险评估

**整体风险级别**: {get_risk_level(overall_risk)} ({overall_risk:.1f}/10)

### 风险因素

| 因素 | 分数 | 详情 |
|--------|-------|---------|
| 规模 | {risk_factors['size']:.1f}/10 | {get_size_details(analysis)} |
| 复杂度 | {risk_factors['complexity']:.1f}/10 | {get_complexity_details(analysis)} |
| 测试覆盖率 | {risk_factors['test_coverage']:.1f}/10 | {get_test_details(analysis)} |
| 依赖项 | {risk_factors['dependencies']:.1f}/10 | {get_dependency_details(analysis)} |
| 安全性 | {risk_factors['security']:.1f}/10 | {get_security_details(analysis)} |

### 缓解策略

{generate_mitigation_strategies(risk_factors)}
"""

    return risk_report

def get_risk_level(score):
    """将分数转换为风险级别"""
    if score < 3:
        return "🟢 低"
    elif score < 6:
        return "🟡 中"
    elif score < 8:
        return "🟠 高"
    else:
        return "🔴 严重"
```

### 9. PR 模板

生成特定上下文的模板：

```python
def generate_pr_template(pr_type, analysis):
    """
    根据类型生成 PR 模板
    """
    templates = {
        'feature': f"""
## 功能: {extract_feature_name(analysis)}

### 描述
{generate_feature_description(analysis)}

### 用户故事
作为 [用户类型]
我想要 [功能]
以便 [受益]

### 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

### 演示
[演示链接或截图]

### 技术实现
{generate_technical_summary(analysis)}

### 测试策略
{generate_test_strategy(analysis)}
""",
        'bugfix': f"""
## Bug 修复: {extract_bug_description(analysis)}

### 问题
- **报告来源**: #[问题编号]
- **严重性**: {determine_severity(analysis)}
- **影响版本**: {get_affected_versions(analysis)}

### 根本原因
{analyze_root_cause(analysis)}

### 解决方案
{describe_solution(analysis)}

### 测试
- [ ] 修复前 Bug 可复现
- [ ] 修复后 Bug 已解决
- [ ] 未引入回归
- [ ] 已测试边界情况

### 验证步骤
1. 复现原始问题的步骤
2. 应用此修复
3. 验证问题已解决
""",
        'refactor': f"""
## 重构: {extract_refactor_scope(analysis)}

### 动机
{describe_refactor_motivation(analysis)}

### 变更内容
{list_refactor_changes(analysis)}

### 收益
- 改进了 {list_improvements(analysis)}
- 减少了 {list_reductions(analysis)}

### 兼容性
- [ ] 无破坏性变更
- [ ] API 保持不变
- [ ] 性能维持或改善

### 指标
| 指标 | 变更前 | 变更后 |
|--------|--------|-------|
| 复杂度 | X | Y |
| 测试覆盖率 | X% | Y% |
| 性能 | Xms | Yms |
"""
    }

    return templates.get(pr_type, templates['feature'])
```

### 10. 审查响应模板

帮助处理审查响应：

```python
review_response_templates = {
    'acknowledge_feedback': """
感谢您的详细审查！我将处理这些要点。
""",

    'explain_decision': """
很好的问题！我选择这种方法是因为：
1. [原因 1]
2. [原因 2]

考虑的替代方案：
- [替代方案 1]: [未选择的原因]
- [替代方案 2]: [未选择的原因]

如有疑虑，我很乐意进一步讨论。
""",

    'request_clarification': """
感谢您的反馈。能否澄清您对 [具体要点] 的意思？
我想在做出更改之前确保正确理解您的关注点。
""",

    'disagree_respectfully': """
我感谢您对此的看法。我有略有不同的观点：

[您的理由]

但是，我愿意进一步讨论此事。您认为 [折衷方案/中间立场] 如何？
""",

    'commit_to_change': """
好发现！我将更新为 [具体变更]。
这应该解决 [关注点]，同时保持 [其他要求]。
"""
}
```

## 输出格式

1. **PR 摘要**: 包含关键指标的执行摘要
2. **详细描述**: 全面的 PR 描述
3. **审查清单**: 上下文感知的审查项目
4. **风险评估**: 包含缓解策略的风险分析
5. **测试覆盖率**: 变更前/后的覆盖率对比
6. **视觉辅助**: 适用的图表和视觉差异
7. **规模建议**: 拆分大型 PR 的建议
8. **审查自动化**: 自动化检查和发现

专注于创建令人愉悦的 PR，包含所有必要的上下文和文档，以实现高效的代码审查流程。
