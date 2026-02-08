---
name: threat-mitigation-mapping
description: 将识别的威胁映射到适当的安全控制措施和缓解方案。用于优先级排序安全投资、制定补救计划或验证控制措施有效性。
---

# 威胁缓解映射

将威胁与控制措施关联起来,实现有效的安全规划。

## 何时使用本技能

- 优先级排序安全投资
- 制定补救路线图
- 验证控制措施覆盖范围
- 设计纵深防御
- 安全架构审查
- 风险处置规划

## 核心概念

### 1. 控制措施类别

```
预防性 ────► 在攻击发生前阻止攻击
   │              (防火墙、输入验证)
   │
检测性 ─────► 识别正在进行的攻击
   │              (IDS、日志监控)
   │
纠正性 ────► 响应攻击并从攻击中恢复
                  (事件响应、备份恢复)
```

### 2. 控制措施层级

| 层级           | 示例                             |
| --------------- | ------------------------------------ |
| **网络层**     | 防火墙、WAF、DDoS 防护       |
| **应用层** | 输入验证、身份认证     |
| **数据层**        | 加密、访问控制          |
| **终端层**    | EDR、补丁管理                |
| **流程层**     | 安全培训、事件响应 |

### 3. 纵深防御

```
                    ┌──────────────────────┐
                    │      边界防护       │ ← 防火墙、WAF
                    │   ┌──────────────┐   │
                    │   │   网络层    │   │ ← 网络分段、IDS
                    │   │  ┌────────┐  │   │
                    │   │  │  主机  │  │   │ ← EDR、加固
                    │   │  │ ┌────┐ │  │   │
                    │   │  │ │应用 │ │  │   │ ← 认证、验证
                    │   │  │ │数据│ │  │   │ ← 加密
                    │   │  │ └────┘ │  │   │
                    │   │  └────────┘  │   │
                    │   └──────────────┘   │
                    └──────────────────────┘
```

## 模板

### 模板 1: 缓解模型

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set
from datetime import datetime

class ControlType(Enum):
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"


class ControlLayer(Enum):
    NETWORK = "network"
    APPLICATION = "application"
    DATA = "data"
    ENDPOINT = "endpoint"
    PROCESS = "process"
    PHYSICAL = "physical"


class ImplementationStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIAL = "partial"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"


class Effectiveness(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


@dataclass
class SecurityControl:
    id: str
    name: str
    description: str
    control_type: ControlType
    layer: ControlLayer
    effectiveness: Effectiveness
    implementation_cost: str  # Low, Medium, High
    maintenance_cost: str
    status: ImplementationStatus = ImplementationStatus.NOT_IMPLEMENTED
    mitigates_threats: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    compliance_refs: List[str] = field(default_factory=list)

    def coverage_score(self) -> float:
        """根据状态和有效性计算覆盖分数。"""
        status_multiplier = {
            ImplementationStatus.NOT_IMPLEMENTED: 0.0,
            ImplementationStatus.PARTIAL: 0.5,
            ImplementationStatus.IMPLEMENTED: 0.8,
            ImplementationStatus.VERIFIED: 1.0,
        }
        return self.effectiveness.value * status_multiplier[self.status]


@dataclass
class Threat:
    id: str
    name: str
    category: str  # STRIDE category
    description: str
    impact: str  # Critical, High, Medium, Low
    likelihood: str
    risk_score: float


@dataclass
class MitigationMapping:
    threat: Threat
    controls: List[SecurityControl]
    residual_risk: str = "Unknown"
    notes: str = ""

    def calculate_coverage(self) -> float:
        """计算控制措施对威胁的覆盖程度。"""
        if not self.controls:
            return 0.0

        total_score = sum(c.coverage_score() for c in self.controls)
        max_possible = len(self.controls) * Effectiveness.VERY_HIGH.value

        return (total_score / max_possible) * 100 if max_possible > 0 else 0

    def has_defense_in_depth(self) -> bool:
        """检查是否覆盖了多个层级。"""
        layers = set(c.layer for c in self.controls if c.status != ImplementationStatus.NOT_IMPLEMENTED)
        return len(layers) >= 2

    def has_control_diversity(self) -> bool:
        """检查是否存在多种控制措施类型。"""
        types = set(c.control_type for c in self.controls if c.status != ImplementationStatus.NOT_IMPLEMENTED)
        return len(types) >= 2


@dataclass
class MitigationPlan:
    name: str
    threats: List[Threat] = field(default_factory=list)
    controls: List[SecurityControl] = field(default_factory=list)
    mappings: List[MitigationMapping] = field(default_factory=list)

    def get_unmapped_threats(self) -> List[Threat]:
        """查找没有缓解措施的威胁。"""
        mapped_ids = {m.threat.id for m in self.mappings}
        return [t for t in self.threats if t.id not in mapped_ids]

    def get_control_coverage(self) -> Dict[str, float]:
        """获取每个威胁的覆盖百分比。"""
        return {
            m.threat.id: m.calculate_coverage()
            for m in self.mappings
        }

    def get_gaps(self) -> List[Dict]:
        """识别缓解措施的缺口。"""
        gaps = []
        for mapping in self.mappings:
            coverage = mapping.calculate_coverage()
            if coverage < 50:
                gaps.append({
                    "threat": mapping.threat.id,
                    "threat_name": mapping.threat.name,
                    "coverage": coverage,
                    "issue": "控制措施覆盖不足",
                    "recommendation": "增加更多控制措施或改进现有措施"
                })
            if not mapping.has_defense_in_depth():
                gaps.append({
                    "threat": mapping.threat.id,
                    "threat_name": mapping.threat.name,
                    "coverage": coverage,
                    "issue": "缺乏纵深防御",
                    "recommendation": "在不同层级添加控制措施"
                })
            if not mapping.has_control_diversity():
                gaps.append({
                    "threat": mapping.threat.id,
                    "threat_name": mapping.threat.name,
                    "coverage": coverage,
                    "issue": "缺乏控制措施多样性",
                    "recommendation": "添加检测性或纠正性控制措施"
                })
        return gaps
```

### 模板 2: 控制措施库

```python
class ControlLibrary:
    """标准安全控制措施库。"""

    STANDARD_CONTROLS = {
        # Authentication Controls
        "AUTH-001": SecurityControl(
            id="AUTH-001",
            name="Multi-Factor Authentication",
            description="Require MFA for all user authentication",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="Medium",
            maintenance_cost="Low",
            mitigates_threats=["SPOOFING"],
            technologies=["TOTP", "WebAuthn", "SMS OTP"],
            compliance_refs=["PCI-DSS 8.3", "NIST 800-63B"]
        ),
        "AUTH-002": SecurityControl(
            id="AUTH-002",
            name="Account Lockout Policy",
            description="Lock accounts after failed authentication attempts",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.MEDIUM,
            implementation_cost="Low",
            maintenance_cost="Low",
            mitigates_threats=["SPOOFING"],
            technologies=["Custom implementation"],
            compliance_refs=["PCI-DSS 8.1.6"]
        ),

        # Input Validation Controls
        "VAL-001": SecurityControl(
            id="VAL-001",
            name="Input Validation Framework",
            description="Validate and sanitize all user input",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="Medium",
            maintenance_cost="Medium",
            mitigates_threats=["TAMPERING", "INJECTION"],
            technologies=["Joi", "Yup", "Pydantic"],
            compliance_refs=["OWASP ASVS V5"]
        ),
        "VAL-002": SecurityControl(
            id="VAL-002",
            name="Web Application Firewall",
            description="Deploy WAF to filter malicious requests",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.NETWORK,
            effectiveness=Effectiveness.MEDIUM,
            implementation_cost="Medium",
            maintenance_cost="Medium",
            mitigates_threats=["TAMPERING", "INJECTION", "DOS"],
            technologies=["AWS WAF", "Cloudflare", "ModSecurity"],
            compliance_refs=["PCI-DSS 6.6"]
        ),

        # Encryption Controls
        "ENC-001": SecurityControl(
            id="ENC-001",
            name="Data Encryption at Rest",
            description="Encrypt sensitive data in storage",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.DATA,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="Medium",
            maintenance_cost="Low",
            mitigates_threats=["INFORMATION_DISCLOSURE"],
            technologies=["AES-256", "KMS", "HSM"],
            compliance_refs=["PCI-DSS 3.4", "GDPR Art. 32"]
        ),
        "ENC-002": SecurityControl(
            id="ENC-002",
            name="TLS Encryption",
            description="Encrypt data in transit using TLS 1.3",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.NETWORK,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="Low",
            maintenance_cost="Low",
            mitigates_threats=["INFORMATION_DISCLOSURE", "TAMPERING"],
            technologies=["TLS 1.3", "Certificate management"],
            compliance_refs=["PCI-DSS 4.1", "HIPAA"]
        ),

        # Logging Controls
        "LOG-001": SecurityControl(
            id="LOG-001",
            name="Security Event Logging",
            description="Log all security-relevant events",
            control_type=ControlType.DETECTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.MEDIUM,
            implementation_cost="Low",
            maintenance_cost="Medium",
            mitigates_threats=["REPUDIATION"],
            technologies=["ELK Stack", "Splunk", "CloudWatch"],
            compliance_refs=["PCI-DSS 10.2", "SOC2"]
        ),
        "LOG-002": SecurityControl(
            id="LOG-002",
            name="Log Integrity Protection",
            description="Protect logs from tampering",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.DATA,
            effectiveness=Effectiveness.MEDIUM,
            implementation_cost="Medium",
            maintenance_cost="Low",
            mitigates_threats=["REPUDIATION", "TAMPERING"],
            technologies=["Immutable storage", "Log signing"],
            compliance_refs=["PCI-DSS 10.5"]
        ),

        # Access Control
        "ACC-001": SecurityControl(
            id="ACC-001",
            name="Role-Based Access Control",
            description="Implement RBAC for authorization",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="Medium",
            maintenance_cost="Medium",
            mitigates_threats=["ELEVATION_OF_PRIVILEGE", "INFORMATION_DISCLOSURE"],
            technologies=["RBAC", "ABAC", "Policy engines"],
            compliance_refs=["PCI-DSS 7.1", "SOC2"]
        ),

        # Availability Controls
        "AVL-001": SecurityControl(
            id="AVL-001",
            name="Rate Limiting",
            description="Limit request rates to prevent abuse",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.APPLICATION,
            effectiveness=Effectiveness.MEDIUM,
            implementation_cost="Low",
            maintenance_cost="Low",
            mitigates_threats=["DENIAL_OF_SERVICE"],
            technologies=["API Gateway", "Redis", "Token bucket"],
            compliance_refs=["OWASP API Security"]
        ),
        "AVL-002": SecurityControl(
            id="AVL-002",
            name="DDoS Protection",
            description="Deploy DDoS mitigation services",
            control_type=ControlType.PREVENTIVE,
            layer=ControlLayer.NETWORK,
            effectiveness=Effectiveness.HIGH,
            implementation_cost="High",
            maintenance_cost="Medium",
            mitigates_threats=["DENIAL_OF_SERVICE"],
            technologies=["Cloudflare", "AWS Shield", "Akamai"],
            compliance_refs=["NIST CSF"]
        ),
    }

    def get_controls_for_threat(self, threat_category: str) -> List[SecurityControl]:
        """获取缓解特定威胁类别的所有控制措施。"""
        return [
            c for c in self.STANDARD_CONTROLS.values()
            if threat_category in c.mitigates_threats
        ]

    def get_controls_by_layer(self, layer: ControlLayer) -> List[SecurityControl]:
        """获取特定层级的控制措施。"""
        return [c for c in self.STANDARD_CONTROLS.values() if c.layer == layer]

    def get_control(self, control_id: str) -> Optional[SecurityControl]:
        """根据 ID 获取特定控制措施。"""
        return self.STANDARD_CONTROLS.get(control_id)

    def recommend_controls(
        self,
        threat: Threat,
        existing_controls: List[str]
    ) -> List[SecurityControl]:
        """为威胁推荐额外的控制措施。"""
        available = self.get_controls_for_threat(threat.category)
        return [c for c in available if c.id not in existing_controls]
```

### 模板 3: 缓解分析

```python
class MitigationAnalyzer:
    """分析和优化缓解策略。"""

    def __init__(self, plan: MitigationPlan, library: ControlLibrary):
        self.plan = plan
        self.library = library

    def calculate_overall_risk_reduction(self) -> float:
        """计算总体风险降低百分比。"""
        if not self.plan.mappings:
            return 0.0

        weighted_coverage = 0
        total_weight = 0

        for mapping in self.plan.mappings:
            # 按威胁风险评分加权
            weight = mapping.threat.risk_score
            coverage = mapping.calculate_coverage()
            weighted_coverage += weight * coverage
            total_weight += weight

        return weighted_coverage / total_weight if total_weight > 0 else 0

    def get_critical_gaps(self) -> List[Dict]:
        """查找需要立即关注的关键缺口。"""
        gaps = self.plan.get_gaps()
        critical_threats = {t.id for t in self.plan.threats if t.impact == "Critical"}

        return [g for g in gaps if g["threat"] in critical_threats]

    def optimize_budget(
        self,
        budget: float,
        cost_map: Dict[str, float]
    ) -> List[SecurityControl]:
        """在预算范围内选择能最大化风险降低的控制措施。"""
        # 简单的贪心算法 - 可替换为优化算法
        recommended = []
        remaining_budget = budget
        unmapped = self.plan.get_unmapped_threats()

        # 按有效性/成本比率排序控制措施
        all_controls = list(self.library.STANDARD_CONTROLS.values())
        controls_with_value = []

        for control in all_controls:
            if control.status == ImplementationStatus.NOT_IMPLEMENTED:
                cost = cost_map.get(control.id, float('inf'))
                if cost <= remaining_budget:
                    # 计算价值为覆盖的威胁数 * 有效性 / 成本
                    threats_covered = len([
                        t for t in unmapped
                        if t.category in control.mitigates_threats
                    ])
                    if threats_covered > 0:
                        value = (threats_covered * control.effectiveness.value) / cost
                        controls_with_value.append((control, value, cost))

        # 按价值排序(越高越好)
        controls_with_value.sort(key=lambda x: x[1], reverse=True)

        for control, value, cost in controls_with_value:
            if cost <= remaining_budget:
                recommended.append(control)
                remaining_budget -= cost

        return recommended

    def generate_roadmap(self) -> List[Dict]:
        """按优先级生成实施路线图。"""
        roadmap = []
        gaps = self.plan.get_gaps()

        # 阶段 1: 低覆盖率的关键威胁
        phase1 = []
        for gap in gaps:
            mapping = next(
                (m for m in self.plan.mappings if m.threat.id == gap["threat"]),
                None
            )
            if mapping and mapping.threat.impact == "Critical":
                controls = self.library.get_controls_for_threat(mapping.threat.category)
                phase1.extend([
                    {
                        "threat": gap["threat"],
                        "control": c.id,
                        "control_name": c.name,
                        "phase": 1,
                        "priority": "Critical"
                    }
                    for c in controls
                    if c.status == ImplementationStatus.NOT_IMPLEMENTED
                ])

        roadmap.extend(phase1[:5])  # 阶段 1 的前 5 个

        # 阶段 2: 高影响威胁
        phase2 = []
        for gap in gaps:
            mapping = next(
                (m for m in self.plan.mappings if m.threat.id == gap["threat"]),
                None
            )
            if mapping and mapping.threat.impact == "High":
                controls = self.library.get_controls_for_threat(mapping.threat.category)
                phase2.extend([
                    {
                        "threat": gap["threat"],
                        "control": c.id,
                        "control_name": c.name,
                        "phase": 2,
                        "priority": "High"
                    }
                    for c in controls
                    if c.status == ImplementationStatus.NOT_IMPLEMENTED
                ])

        roadmap.extend(phase2[:5])  # 阶段 2 的前 5 个

        return roadmap

    def defense_in_depth_analysis(self) -> Dict[str, List[str]]:
        """分析纵深防御覆盖情况。"""
        layer_coverage = {layer.value: [] for layer in ControlLayer}

        for mapping in self.plan.mappings:
            for control in mapping.controls:
                if control.status in [ImplementationStatus.IMPLEMENTED, ImplementationStatus.VERIFIED]:
                    layer_coverage[control.layer.value].append(control.id)

        return layer_coverage

    def generate_report(self) -> str:
        """生成综合缓解报告。"""
        risk_reduction = self.calculate_overall_risk_reduction()
        gaps = self.plan.get_gaps()
        critical_gaps = self.get_critical_gaps()
        layer_coverage = self.defense_in_depth_analysis()

        report = f"""
# 威胁缓解报告

## 执行摘要
- **总体风险降低:** {risk_reduction:.1f}%
- **威胁总数:** {len(self.plan.threats)}
- **控制措施总数:** {len(self.plan.controls)}
- **已识别缺口:** {len(gaps)}
- **关键缺口:** {len(critical_gaps)}

## 纵深防御覆盖情况
{self._format_layer_coverage(layer_coverage)}

## 需要立即采取行动的关键缺口
{self._format_gaps(critical_gaps)}

## 建议
{self._format_recommendations()}

## 实施路线图
{self._format_roadmap()}
"""
        return report

    def _format_layer_coverage(self, coverage: Dict[str, List[str]]) -> str:
        lines = []
        for layer, controls in coverage.items():
            status = "✓" if controls else "✗"
            lines.append(f"- {layer}: {status} ({len(controls)} 个控制措施)")
        return "\n".join(lines)

    def _format_gaps(self, gaps: List[Dict]) -> str:
        if not gaps:
            return "未识别到关键缺口。"
        lines = []
        for gap in gaps:
            lines.append(f"- **{gap['threat_name']}**: {gap['issue']}")
            lines.append(f"  - 覆盖率: {gap['coverage']:.1f}%")
            lines.append(f"  - 建议: {gap['recommendation']}")
        return "\n".join(lines)

    def _format_recommendations(self) -> str:
        recommendations = []
        layer_coverage = self.defense_in_depth_analysis()

        for layer, controls in layer_coverage.items():
            if not controls:
                recommendations.append(f"- 在 {layer} 层添加控制措施")

        gaps = self.plan.get_gaps()
        if any(g["issue"] == "No control diversity" for g in gaps):
            recommendations.append("- 添加更多检测性和纠正性控制措施")

        return "\n".join(recommendations) if recommendations else "当前覆盖范围充足。"

    def _format_roadmap(self) -> str:
        roadmap = self.generate_roadmap()
        if not roadmap:
            return "目前无需推荐额外的控制措施。"

        lines = []
        current_phase = 0
        for item in roadmap:
            if item["phase"] != current_phase:
                current_phase = item["phase"]
                lines.append(f"\n### 阶段 {current_phase}")
            lines.append(f"- [{item['priority']}] {item['control_name']} (针对 {item['threat']})")

        return "\n".join(lines)
```

### 模板 4: 控制措施有效性测试

```python
from dataclasses import dataclass
from typing import List, Callable, Any
import asyncio

@dataclass
class ControlTest:
    control_id: str
    test_name: str
    test_function: Callable[[], bool]
    expected_result: bool
    description: str


class ControlTester:
    """测试控制措施有效性。"""

    def __init__(self):
        self.tests: List[ControlTest] = []
        self.results: List[Dict] = []

    def add_test(self, test: ControlTest) -> None:
        self.tests.append(test)

    async def run_tests(self) -> List[Dict]:
        """运行所有控制措施测试。"""
        self.results = []

        for test in self.tests:
            try:
                result = test.test_function()
                passed = result == test.expected_result
                self.results.append({
                    "control_id": test.control_id,
                    "test_name": test.test_name,
                    "passed": passed,
                    "actual_result": result,
                    "expected_result": test.expected_result,
                    "description": test.description,
                    "error": None
                })
            except Exception as e:
                self.results.append({
                    "control_id": test.control_id,
                    "test_name": test.test_name,
                    "passed": False,
                    "actual_result": None,
                    "expected_result": test.expected_result,
                    "description": test.description,
                    "error": str(e)
                })

        return self.results

    def get_effectiveness_score(self, control_id: str) -> float:
        """计算控制措施的有效性评分。"""
        control_results = [r for r in self.results if r["control_id"] == control_id]
        if not control_results:
            return 0.0

        passed = sum(1 for r in control_results if r["passed"])
        return (passed / len(control_results)) * 100

    def generate_test_report(self) -> str:
        """生成测试结果报告。"""
        if not self.results:
            return "尚未运行测试。"

        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])

        report = f"""
# 控制措施有效性测试报告

## 摘要
- **测试总数:** {total}
- **通过:** {passed}
- **失败:** {total - passed}
- **通过率:** {(passed/total)*100:.1f}%

## 按控制措施分组的结果
"""
        # 按控制措施分组
        controls = {}
        for result in self.results:
            cid = result["control_id"]
            if cid not in controls:
                controls[cid] = []
            controls[cid].append(result)

        for control_id, results in controls.items():
            score = self.get_effectiveness_score(control_id)
            report += f"\n### {control_id} (有效性: {score:.1f}%)\n"
            for r in results:
                status = "✓" if r["passed"] else "✗"
                report += f"- {status} {r['test_name']}\n"
                if r["error"]:
                    report += f"  - 错误: {r['error']}\n"

        return report
```

## 最佳实践

### 应该做

- **映射所有威胁** - 不应存在未映射的威胁
- **分层部署控制措施** - 纵深防御至关重要
- **混合控制措施类型** - 预防性、检测性、纠正性相结合
- **跟踪有效性** - 衡量并持续改进
- **定期审查** - 控制措施会随时间衰减

### 不应该做

- **不要依赖单一控制措施** - 避免单点故障
- **不要忽视成本** - 投资回报率很重要
- **不要跳过测试** - 未经测试的控制措施可能失效
- **不要设置后遗忘** - 持续改进是关键
- **不要忽视人员/流程** - 仅靠技术是不够的

## 参考资料

- [NIST 网络安全框架](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)
- [MITRE D3FEND](https://d3fend.mitre.org/)
