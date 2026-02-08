通过协调的多智能体编排，实施深度防御策略的综合安全加固：

[扩展思考：此工作流在所有应用层实施深度防御安全策略。它协调专业安全智能体进行全面评估、实施分层安全控制，并建立持续安全监控。该方法遵循现代 DevSecOps 原则，包括安全左移、自动扫描和合规性验证。每个阶段都基于前一个阶段的发现，从而建立能够应对当前漏洞和未来威胁的弹性安全态势。]

## 第一阶段：综合安全评估

### 1. 初始漏洞扫描

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："对以下目标执行综合安全评估：$ARGUMENTS。使用 Semgrep/SonarQube 执行 SAST 分析，使用 OWASP ZAP 进行 DAST 扫描，使用 Snyk/Trivy 进行依赖审计，使用 GitLeaks/TruffleHog 进行密钥检测。为供应链分析生成 SBOM。识别 OWASP Top 10 漏洞、CWE 弱点和 CVE 暴露。"
- 输出：包含 CVSS 评分、可利用性分析、攻击面映射、密钥暴露报告、SBOM 清单的详细漏洞报告
- 上下文：所有修复工作的初始基线

### 2. 威胁建模和风险分析

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："使用 STRIDE 方法论对以下目标进行威胁建模：$ARGUMENTS。分析攻击向量，创建攻击树，评估已识别漏洞的业务影响。将威胁映射到 MITRE ATT&CK 框架。根据可能性和影响确定风险优先级。"
- 输出：威胁模型图、包含优先级漏洞的风险矩阵、攻击场景文档、业务影响分析
- 上下文：使用漏洞扫描结果来指导威胁优先级

### 3. 架构安全审查

- 使用 Task 工具，设置 subagent_type="backend-api-security::backend-architect"
- 提示词："审查以下目标的架构安全弱点：$ARGUMENTS。评估服务边界、数据流安全、身份验证/授权架构、加密实施、网络分段。设计零信任架构模式。参考威胁模型和漏洞发现。"
- 输出：安全架构评估、零信任设计建议、服务网格安全要求、数据分类矩阵
- 上下文：结合威胁模型来解决架构漏洞

## 第二阶段：漏洞修复

### 4. 关键漏洞修复

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："协调以下目标中关键漏洞（CVSS 7+）的立即修复：$ARGUMENTS。使用参数化查询修复 SQL 注入，使用输出编码修复 XSS，使用安全会话管理修复身份验证绕过，使用输入验证修复不安全反序列化。为 CVE 应用安全补丁。"
- 输出：包含漏洞修复的补丁代码、安全补丁文档、回归测试要求
- 上下文：处理漏洞评估中的高优先级项目

### 5. 后端安全加固

- 使用 Task 工具，设置 subagent_type="backend-api-security::backend-security-coder"
- 提示词："为以下目标实施综合后端安全控制：$ARGUMENTS。使用 OWASP ESAPI 添加输入验证，实施速率限制和 DDoS 防护，使用 OAuth2/JWT 验证保护 API 端点，使用 AES-256/TLS 1.3 为静态/传输中的数据添加加密。实施不暴露 PII 的安全日志记录。"
- 输出：加固的 API 端点、验证中间件、加密实施、安全配置模板
- 上下文：在漏洞修复的基础上构建预防性控制

### 6. 前端安全实施

- 使用 Task 工具，设置 subagent_type="frontend-mobile-security::frontend-security-coder"
- 提示词："为以下目标实施前端安全措施：$ARGUMENTS。使用基于 nonce 的策略配置 CSP 头，使用 DOMPurify 实施 XSS 防护，使用 PKCE OAuth2 保护身份验证流程，为外部资源添加 SRI，使用 SameSite/HttpOnly/Secure 标志实施安全 Cookie 处理。"
- 输出：安全的前端组件、CSP 策略配置、身份验证流程实施、安全头配置
- 上下文：通过客户端防护补充后端安全

### 7. 移动安全加固

- 使用 Task 工具，设置 subagent_type="frontend-mobile-security::mobile-security-coder"
- 提示词："为以下目标实施移动应用安全：$ARGUMENTS。添加证书固定，实施生物识别身份验证，使用加密保护本地存储，使用 ProGuard/R8 混淆代码，实施防篡改和 root/越狱检测，保护 IPC 通信。"
- 输出：加固的移动应用、安全配置文件、混淆规则、证书固定实施
- 上下文：将安全扩展到移动平台（如适用）

## 第三阶段：安全控制实施

### 8. 身份验证和授权增强

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："为以下目标实施现代身份验证系统：$ARGUMENTS。部署带 PKCE 的 OAuth2/OIDC，使用 TOTP/WebAuthn/FIDO2 实施 MFA，添加基于风险的身份验证，使用最小权限原则实施 RBAC/ABAC，添加具有安全令牌轮换的会话管理。"
- 输出：身份验证服务配置、MFA 实施、授权策略、会话管理系统
- 上下文：根据架构审查加强访问控制

### 9. 基础设施安全控制

- 使用 Task 工具，设置 subagent_type="deployment-strategies::deployment-engineer"
- 提示词："为以下目标部署基础设施安全控制：$ARGUMENTS。为 OWASP 防护配置 WAF 规则，使用微分段实施网络分段，部署 IDS/IPS 系统，配置云安全组和 NACL，使用速率限制和地理阻止实施 DDoS 防护。"
- 输出：WAF 配置、网络安全策略、IDS/IPS 规则、云安全配置
- 上下文：实施网络级防御

### 10. 密钥管理实施

- 使用 Task 工具，设置 subagent_type="deployment-strategies::deployment-engineer"
- 提示词："为以下目标实施企业级密钥管理：$ARGUMENTS。部署 HashiCorp Vault 或 AWS Secrets Manager，实施密钥轮换策略，移除硬编码密钥，配置最小权限 IAM 角色，实施支持 HSM 的加密密钥管理。"
- 输出：密钥管理配置、轮换策略、IAM 角色定义、密钥管理流程
- 上下文：消除密钥暴露漏洞

## 第四阶段：验证和合规

### 11. 渗透测试和验证

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："对以下目标执行综合渗透测试：$ARGUMENTS。执行经过身份验证和未经身份验证的测试、API 安全测试、业务逻辑测试、权限提升尝试。使用 Burp Suite、Metasploit 和自定义漏洞利用。验证所有安全控制的有效性。"
- 输出：渗透测试报告、概念验证漏洞利用、修复验证、安全控制有效性指标
- 上下文：验证所有已实施的安全措施

### 12. 合规性和标准验证

- 使用 Task 工具，设置 subagent_type="security-auditor"
- 提示词："验证以下目标的安全框架合规性：$ARGUMENTS。根据 OWASP ASVS Level 2、CIS 基准、SOC2 Type II 要求、GDPR/CCPA 隐私控制（如适用还包括 HIPAA/PCI-DSS）进行验证。生成合规性证明报告。"
- 输出：合规性评估报告、差距分析、修复要求、审计证据收集
- 上下文：确保监管和行业标准合规

### 13. 安全监控和 SIEM 集成

- 使用 Task 工具，设置 subagent_type="incident-response::devops-troubleshooter"
- 提示词："为以下目标实施安全监控和 SIEM：$ARGUMENTS。部署 Splunk/ELK/Sentinel 集成，配置安全事件关联，实施用于异常检测的行为分析，设置自动事件响应手册，创建安全仪表板和告警。"
- 输出：SIEM 配置、关联规则、事件响应手册、安全仪表板、告警定义
- 上下文：建立持续安全监控

## 配置选项

- scanning_depth: "quick" | "standard" | "comprehensive"（默认：comprehensive）
- compliance_frameworks: ["OWASP", "CIS", "SOC2", "GDPR", "HIPAA", "PCI-DSS"]
- remediation_priority: "cvss_score" | "exploitability" | "business_impact"
- monitoring_integration: "splunk" | "elastic" | "sentinel" | "custom"
- authentication_methods: ["oauth2", "saml", "mfa", "biometric", "passwordless"]

## 成功标准

- 所有关键漏洞（CVSS 7+）已修复
- OWASP Top 10 漏洞已处理
- 渗透测试中零高风险发现
- 合规框架验证通过
- 安全监控检测并告警威胁
- 关键告警的事件响应时间 < 15 分钟
- 已生成 SBOM 并跟踪漏洞
- 所有密钥通过安全保险库管理
- 身份验证实施 MFA 和安全会话管理
- 安全测试集成到 CI/CD 流水线

## 协调说明

- 每个阶段提供详细发现，以指导后续阶段
- 安全审计智能体与特定域智能体协调进行修复
- 所有代码变更在实施前经过安全审查
- 评估和修复之间的持续反馈循环
- 安全发现跟踪在集中式漏洞管理系统中
- 实施后安排定期安全审查

安全加固目标：$ARGUMENTS
