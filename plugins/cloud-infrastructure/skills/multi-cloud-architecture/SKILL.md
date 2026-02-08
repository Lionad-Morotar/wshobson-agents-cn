---
name: multi-cloud-architecture
description: Design multi-cloud architectures using a decision framework to select and integrate services across AWS, Azure, and GCP. Use when building multi-cloud systems, avoiding vendor lock-in, or leveraging best-of-breed services from multiple providers.
---

# 多云架构

跨 AWS、Azure 和 GCP 构建应用程序的决策框架和模式。

## 目的

设计云无关的架构,并对跨云提供商的服务选择做出明智决策。

## 适用场景

- 设计多云策略
- 在云提供商之间迁移
- 为特定工作负载选择云服务
- 实现云无关架构
- 优化跨提供商的成本

## 云服务对比

### 计算服务

| AWS     | Azure               | GCP             | 用例               |
| ------- | ------------------- | --------------- | ------------------ |
| EC2     | Virtual Machines    | Compute Engine  | IaaS 虚拟机        |
| ECS     | Container Instances | Cloud Run       | 容器               |
| EKS     | AKS                 | GKE             | Kubernetes         |
| Lambda  | Functions           | Cloud Functions | 无服务器           |
| Fargate | Container Apps      | Cloud Run       | 托管容器           |

### 存储服务

| AWS     | Azure           | GCP             | 用例           |
| ------- | --------------- | --------------- | -------------- |
| S3      | Blob Storage    | Cloud Storage   | 对象存储       |
| EBS     | Managed Disks   | Persistent Disk | 块存储         |
| EFS     | Azure Files     | Filestore       | 文件存储       |
| Glacier | Archive Storage | Archive Storage | 冷存储         |

### 数据库服务

| AWS         | Azure            | GCP           | 用例             |
| ----------- | ---------------- | ------------- | ---------------- |
| RDS         | SQL Database     | Cloud SQL     | 托管 SQL         |
| DynamoDB    | Cosmos DB        | Firestore     | NoSQL            |
| Aurora      | PostgreSQL/MySQL | Cloud Spanner | 分布式 SQL       |
| ElastiCache | Cache for Redis  | Memorystore   | 缓存             |

**参考:** 完整对比请参阅 `references/service-comparison.md`

## 多云模式

### 模式 1: 单云带灾备

- 主工作负载在一个云中
- 灾难恢复在另一个云中
- 跨云数据库复制
- 自动故障转移

### 模式 2: 最佳组合

- 从每个提供商使用最佳服务
- AI/ML 在 GCP 上
- 企业应用在 Azure 上
- 通用计算在 AWS 上

### 模式 3: 地理分布

- 从最近的云区域为用户服务
- 数据主权合规
- 全局负载均衡
- 区域故障转移

### 模式 4: 云无关抽象

- Kubernetes 用于计算
- PostgreSQL 用于数据库
- S3 兼容存储(MinIO)
- 开源工具

## 云无关架构

### 使用云原生替代方案

- **计算:** Kubernetes (EKS/AKS/GKE)
- **数据库:** PostgreSQL/MySQL (RDS/SQL Database/Cloud SQL)
- **消息队列:** Apache Kafka (MSK/Event Hubs/Confluent)
- **缓存:** Redis (ElastiCache/Azure Cache/Memorystore)
- **对象存储:** S3 兼容 API
- **监控:** Prometheus/Grafana
- **服务网格:** Istio/Linkerd

### 抽象层

```
应用层
    ↓
基础设施抽象 (Terraform)
    ↓
云提供商 API
    ↓
AWS / Azure / GCP
```

## 成本对比

### 计算定价因素

- **AWS:** 按需、预留、Spot、节省计划
- **Azure:** 即用即付、预留、Spot
- **GCP:** 按需、承诺使用、可抢占

### 成本优化策略

1. 使用预留/承诺容量(节省 30-70%)
2. 利用 Spot/可抢占实例
3. 调整资源大小
4. 对可变工作负载使用无服务器
5. 优化数据传输成本
6. 实施生命周期策略
7. 使用成本分配标签
8. 使用云成本工具监控

**参考:** 请参阅 `references/multi-cloud-patterns.md`

## 迁移策略

### 阶段 1: 评估

- 清点当前基础设施
- 识别依赖关系
- 评估云兼容性
- 估算成本

### 阶段 2: 试点

- 选择试点工作负载
- 在目标云中实施
- 彻底测试
- 记录经验

### 阶段 3: 迁移

- 增量迁移工作负载
- 维护双运行期
- 监控性能
- 验证功能

### 阶段 4: 优化

- 调整资源大小
- 实施云原生服务
- 优化成本
- 增强安全性

## 最佳实践

1. **使用基础设施即代码**(Terraform/OpenTofu)
2. **实施 CI/CD 流水线**进行部署
3. **跨云设计故障容错**
4. **尽可能使用托管服务**
5. **实施全面监控**
6. **自动化成本优化**
7. **遵循安全最佳实践**
8. **记录云特定配置**
9. **测试灾难恢复**程序
10. **对多个云培训团队**

## 参考文件

- `references/service-comparison.md` - 完整服务对比
- `references/multi-cloud-patterns.md` - 架构模式

## 相关技能

- `terraform-module-library` - 用于 IaC 实施
- `cost-optimization` - 用于成本管理
- `hybrid-cloud-networking` - 用于连接
