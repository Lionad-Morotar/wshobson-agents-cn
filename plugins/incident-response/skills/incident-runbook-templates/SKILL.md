---
name: incident-runbook-templates
description: 创建结构化的事件响应运行手册，包含逐步程序、升级路径和恢复操作。在构建运行手册、响应事件或建立事件响应程序时使用。
---

# 事件运行手册模板

生产就绪的事件响应运行手册模板，涵盖检测、分类、缓解、解决和沟通。

## 何时使用此技能

- 创建事件响应程序
- 构建特定服务的运行手册
- 建立升级路径
- 记录恢复程序
- 响应活跃事件
- 值班工程师入职培训

## 核心概念

### 1. 事件严重程度级别

| 严重程度 | 影响 | 响应时间 | 示例 |
| -------- | -------------------------- | ----------------- | ----------------------- |
| **SEV1** | 完全中断、数据丢失 | 15 分钟 | 生产环境宕机 |
| **SEV2** | 严重降级 | 30 分钟 | 关键功能故障 |
| **SEV3** | 轻微影响 | 2 小时 | 非关键 bug |
| **SEV4** | 最小影响 | 下一个工作日 | 外观问题 |

### 2. 运行手册结构

```
1. 概述与影响
2. 检测与警报
3. 初步分类
4. 缓解步骤
5. 根因调查
6. 解决程序
7. 验证与回滚
8. 沟通模板
9. 升级矩阵
```

## 运行手册模板

### 模板 1：服务中断运行手册

````markdown
# [服务名称] 中断运行手册

## 概述

**服务**：支付处理服务
**负责人**：平台团队
**Slack**：#payments-incidents
**PagerDuty**：payments-oncall

## 影响评估

- [ ] 哪些客户受到影响？
- [ ] 百分之多少的流量受到影响？
- [ ] 是否有财务影响？
- [ ] 爆炸半径有多大？

## 检测

### 警报

- `payment_error_rate > 5%` (PagerDuty)
- `payment_latency_p99 > 2s` (Slack)
- `payment_success_rate < 95%` (PagerDuty)

### 仪表板

- [支付服务仪表板](https://grafana/d/payments)
- [错误跟踪](https://sentry.io/payments)
- [依赖状态](https://status.stripe.com)

## 初步分类（前 5 分钟）

### 1. 评估范围

```bash
# 检查服务健康状况
kubectl get pods -n payments -l app=payment-service

# 检查最近的部署
kubectl rollout history deployment/payment-service -n payments

# 检查错误率
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))"
````

### 2. 快速健康检查

- [ ] 可以访问服务吗？ `curl -I https://api.company.com/payments/health`
- [ ] 数据库连接？检查连接池指标
- [ ] 外部依赖？检查 Stripe、银行 API 状态
- [ ] 最近的更改？检查部署历史

### 3. 初步分类

| 症状 | 可能原因 | 转到章节 |
| -------------------- | ------------------- | ------------- |
| 所有请求失败 | 服务宕机 | 章节 4.1 |
| 高延迟 | 数据库/依赖 | 章节 4.2 |
| 部分失败 | 代码 bug | 章节 4.3 |
| 错误激增 | 流量激增 | 章节 4.4 |

## 缓解程序

### 4.1 服务完全宕机

```bash
# 步骤 1：检查 Pod 状态
kubectl get pods -n payments

# 步骤 2：如果 Pod 处于崩溃循环，检查日志
kubectl logs -n payments -l app=payment-service --tail=100

# 步骤 3：检查最近的部署
kubectl rollout history deployment/payment-service -n payments

# 步骤 4：如果最近的部署可疑，则回滚
kubectl rollout undo deployment/payment-service -n payments

# 步骤 5：如果资源受限，则扩容
kubectl scale deployment/payment-service -n payments --replicas=10

# 步骤 6：验证恢复
kubectl rollout status deployment/payment-service -n payments
```

### 4.2 高延迟

```bash
# 步骤 1：检查数据库连接
kubectl exec -n payments deploy/payment-service -- \
  curl localhost:8080/metrics | grep db_pool

# 步骤 2：检查慢查询（如果是数据库问题）
psql -h $DB_HOST -U $DB_USER -c "
  SELECT pid, now() - query_start AS duration, query
  FROM pg_stat_activity
  WHERE state = 'active' AND duration > interval '5 seconds'
  ORDER BY duration DESC;"

# 步骤 3：如需要，终止长时间运行的查询
psql -h $DB_HOST -U $DB_USER -c "SELECT pg_terminate_backend(pid);"

# 步骤 4：检查外部依赖延迟
curl -w "@curl-format.txt" -o /dev/null -s https://api.stripe.com/v1/health

# 步骤 5：如果依赖缓慢，启用断路器
kubectl set env deployment/payment-service \
  STRIPE_CIRCUIT_BREAKER_ENABLED=true -n payments
```

### 4.3 部分失败（特定错误）

```bash
# 步骤 1：识别错误模式
kubectl logs -n payments -l app=payment-service --tail=500 | \
  grep -i error | sort | uniq -c | sort -rn | head -20

# 步骤 2：检查错误跟踪
# 前往 Sentry：https://sentry.io/payments

# 步骤 3：如果是特定端点，启用功能标志禁用
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "DISABLE_PROBLEMATIC_FEATURE", "enabled": true}'

# 步骤 4：如果是数据问题，检查最近的数据更改
psql -h $DB_HOST -c "
  SELECT * FROM audit_log
  WHERE table_name = 'payment_methods'
  AND created_at > now() - interval '1 hour';"
```

### 4.4 流量激增

```bash
# 步骤 1：检查当前请求率
kubectl top pods -n payments

# 步骤 2：水平扩容
kubectl scale deployment/payment-service -n payments --replicas=20

# 步骤 3：启用速率限制
kubectl set env deployment/payment-service \
  RATE_LIMIT_ENABLED=true \
  RATE_LIMIT_RPS=1000 -n payments

# 步骤 4：如果是攻击，阻止可疑 IP
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-suspicious
  namespace: payments
spec:
  podSelector:
    matchLabels:
      app: payment-service
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 192.168.1.0/24  # 可疑范围
EOF
```

## 验证步骤

```bash
# 验证服务健康
curl -s https://api.company.com/payments/health | jq

# 验证错误率恢复正常
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))" | jq '.data.result[0].value[1]'

# 验证延迟可接受
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))" | jq

# 冒烟测试关键流程
./scripts/smoke-test-payments.sh
```

## 回滚程序

```bash
# 回滚 Kubernetes 部署
kubectl rollout undo deployment/payment-service -n payments

# 回滚数据库迁移（如适用）
./scripts/db-rollback.sh $MIGRATION_VERSION

# 回滚功能标志
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "NEW_PAYMENT_FLOW", "enabled": false}'
```

## 升级矩阵

| 条件 | 升级到 | 联系方式 |
| ----------------------------- | ------------------- | ------------------- |
| SEV1 超过 15 分钟未解决 | 工程经理 | @manager (Slack) |
| 疑似数据泄露 | 安全团队 | #security-incidents |
| 财务影响 > $10k | 财务 + 法务 | @finance-oncall |
| 需要客户沟通 | 支持负责人 | @support-lead |

## 沟通模板

### 初始通知（内部）

```
🚨 事件：支付服务降级

严重程度：SEV2
状态：调查中
影响：约 20% 的支付请求失败
开始时间：[时间]
事件指挥：[姓名]

当前操作：
- 调查根本原因
- 扩容服务
- 监控仪表板

更新在 #payments-incidents
```

### 状态更新

```
📊 更新：支付服务事件

状态：缓解中
影响：失败率降至约 5%
持续时间：25 分钟

已采取的操作：
- 回滚部署 v2.3.4 → v2.3.3
- 服务从 5 个副本扩容到 10 个副本

下一步：
- 继续监控
- 根因分析进行中

预计解决时间：约 15 分钟
```

### 解决通知

```
✅ 已解决：支付服务事件

持续时间：45 分钟
影响：约 5,000 笔受影响的交易
根本原因：v2.3.4 中的内存泄漏

解决方案：
- 回滚到 v2.3.3
- 交易自动重试成功

后续：
- 事后分析安排于 [日期]
- Bug 修复进行中
```

````

### 模板 2：数据库事件运行手册

```markdown
# 数据库事件运行手册

## 快速参考
| 问题 | 命令 |
|-------|---------|
| 检查连接 | `SELECT count(*) FROM pg_stat_activity;` |
| 终止查询 | `SELECT pg_terminate_backend(pid);` |
| 检查复制延迟 | `SELECT extract(epoch from (now() - pg_last_xact_replay_timestamp()));` |
| 检查锁 | `SELECT * FROM pg_locks WHERE NOT granted;` |

## 连接池耗尽
```sql
-- 检查当前连接
SELECT datname, usename, state, count(*)
FROM pg_stat_activity
GROUP BY datname, usename, state
ORDER BY count(*) DESC;

-- 识别长时间运行的连接
SELECT pid, usename, datname, state, query_start, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- 终止空闲连接
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '10 minutes';
````

## 复制延迟

```sql
-- 检查副本上的延迟
SELECT
  CASE
    WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
    ELSE extract(epoch from now() - pg_last_xact_replay_timestamp())
  END AS lag_seconds;

-- 如果延迟 > 60 秒，考虑：
-- 1. 检查主/副本之间的网络
-- 2. 检查副本磁盘 I/O
-- 3. 如果无法恢复，考虑故障转移
```

## 磁盘空间危急

```bash
# 检查磁盘使用情况
df -h /var/lib/postgresql/data

# 查找大表
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;"

# VACUUM 回收空间
psql -c "VACUUM FULL large_table;"

# 如果紧急，删除旧数据或扩展磁盘
```

```

## 最佳实践

### 应该做的
- **保持运行手册更新** - 每次事件后审查
- **定期测试运行手册** - 游戏日、混沌工程
- **包含回滚步骤** - 始终有逃生通道
- **记录假设** - 步骤工作必须满足的条件
- **链接到仪表板** - 压力期间快速访问

### 不应该做的
- **不要假设知识** - 为凌晨 3 点的大脑编写
- **不要跳过验证** - 确认每个步骤都有效
- **不要忘记沟通** - 让利益相关者知情
- **不要独自工作** - 尽早升级
- **不要跳过事后分析** - 从每个事件中学习

## 资源

- [Google SRE 手册 - 事件管理](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty 事件响应](https://response.pagerduty.com/)
- [Atlassian 事件管理](https://www.atlassian.com/incident-management)
```
