# 依赖升级策略

你是一位依赖管理专家，专精于项目依赖的安全、渐进式升级。规划和执行依赖更新，最小化风险、进行适当测试，并为破坏性变更提供清晰的迁移路径。

## 上下文

用户需要安全地升级项目依赖，处理破坏性变更，确保兼容性，并保持稳定性。重点关注风险评估、渐进式升级、自动化测试和回滚策略。

## 需求

$ARGUMENTS

## 说明

### 1. 依赖更新分析

评估当前依赖状态和升级需求：

**全面依赖审计**

```python
import json
import subprocess
from datetime import datetime, timedelta
from packaging import version

class DependencyAnalyzer:
    def analyze_update_opportunities(self):
        """
        分析所有依赖的更新机会
        """
        analysis = {
            'dependencies': self._analyze_dependencies(),
            'update_strategy': self._determine_strategy(),
            'risk_assessment': self._assess_risks(),
            'priority_order': self._prioritize_updates()
        }

        return analysis

    def _analyze_dependencies(self):
        """分析每个依赖"""
        deps = {}

        # NPM 分析
        if self._has_npm():
            npm_output = subprocess.run(
                ['npm', 'outdated', '--json'],
                capture_output=True,
                text=True
            )
            if npm_output.stdout:
                npm_data = json.loads(npm_output.stdout)
                for pkg, info in npm_data.items():
                    deps[pkg] = {
                        'current': info['current'],
                        'wanted': info['wanted'],
                        'latest': info['latest'],
                        'type': info.get('type', 'dependencies'),
                        'ecosystem': 'npm',
                        'update_type': self._categorize_update(
                            info['current'],
                            info['latest']
                        )
                    }

        # Python 分析
        if self._has_python():
            pip_output = subprocess.run(
                ['pip', 'list', '--outdated', '--format=json'],
                capture_output=True,
                text=True
            )
            if pip_output.stdout:
                pip_data = json.loads(pip_output.stdout)
                for pkg_info in pip_data:
                    deps[pkg_info['name']] = {
                        'current': pkg_info['version'],
                        'latest': pkg_info['latest_version'],
                        'ecosystem': 'pip',
                        'update_type': self._categorize_update(
                            pkg_info['version'],
                            pkg_info['latest_version']
                        )
                    }

        return deps

    def _categorize_update(self, current_ver, latest_ver):
        """按 semver 分类更新"""
        try:
            current = version.parse(current_ver)
            latest = version.parse(latest_ver)

            if latest.major > current.major:
                return 'major'
            elif latest.minor > current.minor:
                return 'minor'
            elif latest.micro > current.micro:
                return 'patch'
            else:
                return 'none'
        except:
            return 'unknown'
```

### 2. 破坏性变更检测

识别潜在的破坏性变更：

**破坏性变更扫描器**

```python
class BreakingChangeDetector:
    def detect_breaking_changes(self, package_name, current_version, target_version):
        """
        检测版本之间的破坏性变更
        """
        breaking_changes = {
            'api_changes': [],
            'removed_features': [],
            'changed_behavior': [],
            'migration_required': False,
            'estimated_effort': 'low'
        }

        # 获取变更日志
        changelog = self._fetch_changelog(package_name, current_version, target_version)

        # 解析破坏性变更
        breaking_patterns = [
            r'BREAKING CHANGE:',
            r'BREAKING:',
            r'removed',
            r'deprecated',
            r'no longer',
            r'renamed',
            r'moved to',
            r'replaced by'
        ]

        for pattern in breaking_patterns:
            matches = re.finditer(pattern, changelog, re.IGNORECASE)
            for match in matches:
                context = self._extract_context(changelog, match.start())
                breaking_changes['api_changes'].append(context)

        # 检查特定模式
        if package_name == 'react':
            breaking_changes.update(self._check_react_breaking_changes(
                current_version, target_version
            ))
        elif package_name == 'webpack':
            breaking_changes.update(self._check_webpack_breaking_changes(
                current_version, target_version
            ))

        # 估算迁移工作量
        breaking_changes['estimated_effort'] = self._estimate_effort(breaking_changes)

        return breaking_changes

    def _check_react_breaking_changes(self, current, target):
        """React 特定的破坏性变更"""
        changes = {
            'api_changes': [],
            'migration_required': False
        }

        # React 15 到 16
        if current.startswith('15') and target.startswith('16'):
            changes['api_changes'].extend([
                'PropTypes 移至单独的包',
                'React.createClass 已弃用',
                'String refs 已弃用'
            ])
            changes['migration_required'] = True

        # React 16 到 17
        elif current.startswith('16') and target.startswith('17'):
            changes['api_changes'].extend([
                '事件委托变更',
                '无事件池',
                'useEffect 清理时序变更'
            ])

        # React 17 到 18
        elif current.startswith('17') and target.startswith('18'):
            changes['api_changes'].extend([
                '自动批处理',
                '更严格的严格模式',
                'Suspense 变更',
                '新的根 API'
            ])
            changes['migration_required'] = True

        return changes
```

### 3. 迁移指南生成

创建详细的迁移指南：

**迁移指南生成器**

```python
def generate_migration_guide(package_name, current_version, target_version, breaking_changes):
    """
    生成分步迁移指南
    """
    guide = f"""
# 迁移指南：{package_name} {current_version} → {target_version}

## 概述
本指南将帮助你将 {package_name} 从版本 {current_version} 升级到 {target_version}。

**预计时间**：{estimate_migration_time(breaking_changes)}
**风险级别**：{assess_risk_level(breaking_changes)}
**破坏性变更**：{len(breaking_changes['api_changes'])}

## 迁移前检查清单

- [ ] 当前测试套件通过
- [ ] 已创建备份/标记 Git 提交点
- [ ] 已检查依赖兼容性
- [ ] 已通知团队升级

## 迁移步骤

### 步骤 1：更新依赖

```bash
# 创建新分支
git checkout -b upgrade/{package_name}-{target_version}

# 更新包
npm install {package_name}@{target_version}

# 如需要，更新对等依赖
{generate_peer_deps_commands(package_name, target_version)}
```

### 步骤 2：处理破坏性变更

{generate_breaking_change_fixes(breaking_changes)}

### 步骤 3：更新代码模式

{generate_code_updates(package_name, current_version, target_version)}

### 步骤 4：运行 Codemods（如果可用）

{generate_codemod_commands(package_name, target_version)}

### 步骤 5：测试与验证

```bash
# 运行 linter 以发现问题
npm run lint

# 运行测试
npm test

# 运行类型检查
npm run type-check

# 手动测试检查清单
```

{generate_test_checklist(package_name, breaking_changes)}

### 步骤 6：性能验证

{generate_performance_checks(package_name)}

## 回滚计划

如果出现问题，按照以下步骤回滚：

```bash
# 恢复包版本
git checkout package.json package-lock.json
npm install

# 或使用备份分支
git checkout main
git branch -D upgrade/{package_name}-{target_version}
```

## 常见问题与解决方案

{generate_common_issues(package_name, target_version)}

## 资源

- [官方迁移指南]({get_official_guide_url(package_name, target_version)})
- [变更日志]({get_changelog_url(package_name, target_version)})
- [社区讨论]({get_community_url(package_name)})
  """
      return guide
```

### 4. 渐进式升级策略

规划安全的渐进式升级：

**渐进式升级规划器**

```python
class IncrementalUpgrader:
    def plan_incremental_upgrade(self, package_name, current, target):
        """
        规划渐进式升级路径
        """
        # 获取当前和目标之间的所有版本
        all_versions = self._get_versions_between(package_name, current, target)

        # 识别安全的停止点
        safe_versions = self._identify_safe_versions(all_versions)

        # 创建升级路径
        upgrade_path = self._create_upgrade_path(current, target, safe_versions)

        plan = f"""
## 渐进式升级计划：{package_name}

### 当前状态
- 版本：{current}
- 目标：{target}
- 总步骤：{len(upgrade_path)}

### 升级路径

"""
        for i, step in enumerate(upgrade_path, 1):
            plan += f"""
#### 步骤 {i}：升级到 {step['version']}

**风险级别**：{step['risk_level']}
**破坏性变更**：{step['breaking_changes']}

```bash
# 升级命令
npm install {package_name}@{step['version']}

# 测试命令
npm test -- --updateSnapshot

# 验证
npm run integration-tests
```

**关键变更**：
{self._summarize_changes(step)}

**测试重点**：
{self._get_test_focus(step)}

---

"""

        return plan

    def _identify_safe_versions(self, versions):
        """识别安全的中间版本"""
        safe_versions = []

        for v in versions:
            # 安全版本通常是：
            # - 每个次版本的最后一个补丁版本
            # - 具有长期稳定期的版本
            # - 重大 API 变更之前的版本
            if (self._is_last_patch(v, versions) or
                self._has_stability_period(v) or
                self._is_pre_breaking_change(v)):
                safe_versions.append(v)

        return safe_versions
```

### 5. 自动化测试策略

确保升级不会破坏功能：

**升级测试套件**

```javascript
// upgrade-tests.js
const { runUpgradeTests } = require('./upgrade-test-framework');

async function testDependencyUpgrade(packageName, targetVersion) {
    const testSuite = {
        preUpgrade: async () => {
            // 捕获基线
            const baseline = {
                unitTests: await runTests('unit'),
                integrationTests: await runTests('integration'),
                e2eTests: await runTests('e2e'),
                performance: await capturePerformanceMetrics(),
                bundleSize: await measureBundleSize()
            };

            return baseline;
        },

        postUpgrade: async (baseline) => {
            // 升级后运行相同测试
            const results = {
                unitTests: await runTests('unit'),
                integrationTests: await runTests('integration'),
                e2eTests: await runTests('e2e'),
                performance: await capturePerformanceMetrics(),
                bundleSize: await measureBundleSize()
            };

            // 比较结果
            const comparison = compareResults(baseline, results);

            return {
                passed: comparison.passed,
                failures: comparison.failures,
                regressions: comparison.regressions,
                improvements: comparison.improvements
            };
        },

        smokeTests: [
            async () => {
                // 关键路径测试
                await testCriticalUserFlows();
            },
            async () => {
                // API 兼容性
                await testAPICompatibility();
            },
            async () => {
                // 构建过程
                await testBuildProcess();
            }
        ]
    };

    return runUpgradeTests(testSuite);
}
```

### 6. 兼容性矩阵

检查依赖之间的兼容性：

**兼容性检查器**

```python
def generate_compatibility_matrix(dependencies):
    """
    生成依赖的兼容性矩阵
    """
    matrix = {}

    for dep_name, dep_info in dependencies.items():
        matrix[dep_name] = {
            'current': dep_info['current'],
            'target': dep_info['latest'],
            'compatible_with': check_compatibility(dep_name, dep_info['latest']),
            'conflicts': find_conflicts(dep_name, dep_info['latest']),
            'peer_requirements': get_peer_requirements(dep_name, dep_info['latest'])
        }

    # 生成报告
    report = """
## 依赖兼容性矩阵

| 包 | 当前版本 | 目标版本 | 兼容 | 冲突 | 需要操作 |
|---------|---------|--------|-----------------|-----------|-----------------|
"""

    for pkg, info in matrix.items():
        compatible = '✅' if not info['conflicts'] else '⚠️'
        conflicts = ', '.join(info['conflicts']) if info['conflicts'] else '无'
        action = '可安全升级' if not info['conflicts'] else '先解决冲突'

        report += f"| {pkg} | {info['current']} | {info['target']} | {compatible} | {conflicts} | {action} |\n"

    return report

def check_compatibility(package_name, version):
    """检查此包与什么兼容"""
    # 检查 package.json 或 requirements.txt
    peer_deps = get_peer_dependencies(package_name, version)
    compatible_packages = []

    for peer_pkg, peer_version_range in peer_deps.items():
        if is_installed(peer_pkg):
            current_peer_version = get_installed_version(peer_pkg)
            if satisfies_version_range(current_peer_version, peer_version_range):
                compatible_packages.append(f"{peer_pkg}@{current_peer_version}")

    return compatible_packages
```

### 7. 回滚策略

实现安全的回滚程序：

**回滚管理器**

```bash
#!/bin/bash
# rollback-dependencies.sh

# 创建回滚点
create_rollback_point() {
    echo "📌 正在创建回滚点..."

    # 保存当前状态
    cp package.json package.json.backup
    cp package-lock.json package-lock.json.backup

    # Git 标签
    git tag -a "pre-upgrade-$(date +%Y%m%d-%H%M%S)" -m "升级前快照"

    # 如需要，数据库快照
    if [ -f "database-backup.sh" ]; then
        ./database-backup.sh
    fi

    echo "✅ 回滚点已创建"
}

# 执行回滚
rollback() {
    echo "🔄 正在执行回滚..."

    # 恢复包文件
    mv package.json.backup package.json
    mv package-lock.json.backup package-lock.json

    # 重新安装依赖
    rm -rf node_modules
    npm ci

    # 运行回滚后测试
    npm test

    echo "✅ 回滚完成"
}

# 验证回滚
verify_rollback() {
    echo "🔍 正在验证回滚..."

    # 检查关键功能
    npm run test:critical

    # 检查服务健康
    curl -f http://localhost:3000/health || exit 1

    echo "✅ 回滚已验证"
}
```

### 8. 批量更新策略

高效处理多个更新：

**批量更新规划器**

```python
def plan_batch_updates(dependencies):
    """
    规划高效的批量更新
    """
    # 按更新类型分组
    groups = {
        'patch': [],
        'minor': [],
        'major': [],
        'security': []
    }

    for dep, info in dependencies.items():
        if info.get('has_security_vulnerability'):
            groups['security'].append(dep)
        else:
            groups[info['update_type']].append(dep)

    # 创建更新批次
    batches = []

    # 批次 1：安全更新（立即）
    if groups['security']:
        batches.append({
            'priority': 'CRITICAL',
            'name': '安全更新',
            'packages': groups['security'],
            'strategy': 'immediate',
            'testing': 'full'
        })

    # 批次 2：补丁更新（安全）
    if groups['patch']:
        batches.append({
            'priority': 'HIGH',
            'name': '补丁更新',
            'packages': groups['patch'],
            'strategy': 'grouped',
            'testing': 'smoke'
        })

    # 批次 3：次要更新（谨慎）
    if groups['minor']:
        batches.append({
            'priority': 'MEDIUM',
            'name': '次要更新',
            'packages': groups['minor'],
            'strategy': 'incremental',
            'testing': 'regression'
        })

    # 批次 4：主要更新（计划）
    if groups['major']:
        batches.append({
            'priority': 'LOW',
            'name': '主要更新',
            'packages': groups['major'],
            'strategy': 'individual',
            'testing': 'comprehensive'
        })

    return generate_batch_plan(batches)
```

### 9. 框架特定升级

处理框架升级：

**框架升级指南**

```python
framework_upgrades = {
    'angular': {
        'upgrade_command': 'ng update',
        'pre_checks': [
            'ng update @angular/core@{version} --dry-run',
            'npm audit',
            'ng lint'
        ],
        'post_upgrade': [
            'ng update @angular/cli',
            'npm run test',
            'npm run e2e'
        ],
        'common_issues': {
            'ivy_renderer': '在 tsconfig.json 中启用 Ivy',
            'strict_mode': '更新 TypeScript 配置',
            'deprecated_apis': '使用 Angular 迁移原理图'
        }
    },
    'react': {
        'upgrade_command': 'npm install react@{version} react-dom@{version}',
        'codemods': [
            'npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js src/',
            'npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/error-boundaries.js src/'
        ],
        'verification': [
            'npm run build',
            'npm test -- --coverage',
            'npm run analyze-bundle'
        ]
    },
    'vue': {
        'upgrade_command': 'npm install vue@{version}',
        'migration_tool': 'npx vue-codemod -t <transform> <path>',
        'breaking_changes': {
            '2_to_3': [
                '组合式 API',
                '多个根元素',
                'Teleport 组件',
                'Fragments'
            ]
        }
    }
}
```

### 10. 升级后监控

升级后监控应用程序：

```javascript
// post-upgrade-monitoring.js
const monitoring = {
  metrics: {
    performance: {
      page_load_time: { threshold: 3000, unit: "ms" },
      api_response_time: { threshold: 500, unit: "ms" },
      memory_usage: { threshold: 512, unit: "MB" },
    },
    errors: {
      error_rate: { threshold: 0.01, unit: "%" },
      console_errors: { threshold: 0, unit: "count" },
    },
    bundle: {
      size: { threshold: 5, unit: "MB" },
      gzip_size: { threshold: 1.5, unit: "MB" },
    },
  },

  checkHealth: async function () {
    const results = {};

    for (const [category, metrics] of Object.entries(this.metrics)) {
      results[category] = {};

      for (const [metric, config] of Object.entries(metrics)) {
        const value = await this.measureMetric(metric);
        results[category][metric] = {
          value,
          threshold: config.threshold,
          unit: config.unit,
          status: value <= config.threshold ? "PASS" : "FAIL",
        };
      }
    }

    return results;
  },

  generateReport: function (results) {
    let report = "## 升级后健康检查\n\n";

    for (const [category, metrics] of Object.entries(results)) {
      report += `### ${category}\n\n`;
      report += "| 指标 | 值 | 阈值 | 状态 |\n";
      report += "|--------|-------|-----------|--------|\n";

      for (const [metric, data] of Object.entries(metrics)) {
        const status = data.status === "PASS" ? "✅" : "❌";
        report += `| ${metric} | ${data.value}${data.unit} | ${data.threshold}${data.unit} | ${status} |\n`;
      }

      report += "\n";
    }

    return report;
  },
};
```

## 输出格式

1. **升级概览**：可用更新摘要及风险评估
2. **优先级矩阵**：按重要性和安全性排序的更新列表
3. **迁移指南**：每个主要升级的分步指南
4. **兼容性报告**：依赖兼容性分析
5. **测试策略**：用于验证升级的自动化测试
6. **回滚计划**：如需要时恢复的明确程序
7. **监控仪表板**：升级后健康指标
8. **时间表**：实施升级的现实计划

重点关注安全的、渐进式的升级，在保持依赖最新和安全的同时维持系统稳定性。
