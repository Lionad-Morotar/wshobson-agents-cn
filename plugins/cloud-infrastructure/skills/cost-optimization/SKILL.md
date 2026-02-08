---
name: cost-optimization
description: 通过资源调整、标签策略、预留实例和支出分析优化云成本。用于降低云费用、分析基础设施成本或实施成本治理策略时。
---

# 云成本优化

跨 AWS、Azure 和 GCP 优化云成本的策略和模式。

## 目的

实施系统性的成本优化策略，在保持性能和可靠性的同时降低云支出。

## 使用场景

- 降低云支出
- 调整资源规模
- 实施成本治理
- 优化多云成本
- 满足预算约束

## 成本优化框架

### 1. 可视化

- 实施成本分配标签
- 使用云成本管理工具
- 设置预算告警
- 创建成本仪表板

### 2. 资源调整

- 分析资源利用率
- 缩减过度配置的资源
- 使用自动扩缩容
- 移除空闲资源

### 3. 定价模型

- 使用预留容量
- 利用 Spot/抢占式实例
- 实施节省计划
- 使用承诺使用折扣

### 4. 架构优化

- 使用托管服务
- 实施缓存
- 优化数据传输
- 使用生命周期策略

## AWS 成本优化

### 预留实例

```
节省：比按需高 30-72%
期限：1 年或 3 年
付款：全预付/部分预付/无预付
灵活性：标准版或可转换版
```

### 节省计划

```
计算节省计划：节省 66%
EC2 实例节省计划：节省 72%
适用于：EC2、Fargate、Lambda
跨：实例系列、区域、操作系统灵活应用
```

### Spot 实例

```
节省：比按需高达 90%
最适合：批处理作业、CI/CD、无状态工作负载
风险：2 分钟中断通知
策略：与按需实例混合以提高韧性
```

### S3 成本优化

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

## Azure 成本优化

### 预留 VM 实例

- 1 年或 3 年期限
- 高达 72% 节省
- 灵活调整大小
- 可交换

### Azure 混合权益

- 使用现有的 Windows Server 许可证
- 结合预留实例高达 80% 节省
- 适用于 Windows 和 SQL Server

### Azure 顾问建议

- 调整 VM 大小
- 删除未使用的资源
- 使用预留容量
- 优化存储

## GCP 成本优化

### 承诺使用折扣

- 1 年或 3 年承诺
- 高达 57% 节省
- 适用于 vCPU 和内存
- 基于资源或基于支出

### 持续使用折扣

- 自动折扣
- 运行实例高达 30% 折扣
- 无需承诺
- 适用于 Compute Engine、GKE

### 抢占式 VM

- 高达 80% 节省
- 最长 24 小时运行时间
- 最适合批处理工作负载

## 标签策略

### AWS 标签

```hcl
locals {
  common_tags = {
    Environment = "production"
    Project     = "my-project"
    CostCenter  = "engineering"
    Owner       = "team@example.com"
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"

  tags = merge(
    local.common_tags,
    {
      Name = "web-server"
    }
  )
}
```

**参考：**参见 `references/tagging-standards.md`

## 成本监控

### 预算告警

```hcl
# AWS 预算
resource "aws_budgets_budget" "monthly" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "1000"
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["team@example.com"]
  }
}
```

### 成本异常检测

- AWS 成本异常检测
- Azure 成本管理告警
- GCP 预算告警

## 架构模式

### 模式 1：无服务器优先

- 使用 Lambda/Functions 处理事件驱动
- 仅按执行时间付费
- 包含自动扩缩容
- 无空闲成本

### 模式 2：调整数据库规模

```
开发环境：t3.small RDS
预发布环境：t3.large RDS
生产环境：r6g.2xlarge RDS 配合只读副本
```

### 模式 3：多层存储

```
热数据：S3 Standard
温数据：S3 Standard-IA（30 天）
冷数据：S3 Glacier（90 天）
归档：S3 Deep Archive（365 天）
```

### 模式 4：自动扩缩容

```hcl
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = "80"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
}
```

## 成本优化清单

- [ ] 实施成本分配标签
- [ ] 删除未使用的资源（EBS、EIP、快照）
- [ ] 根据利用率调整实例规模
- [ ] 为稳定工作负载使用预留容量
- [ ] 实施自动扩缩容
- [ ] 优化存储类别
- [ ] 使用生命周期策略
- [ ] 启用成本异常检测
- [ ] 设置预算告警
- [ ] 每周审查成本
- [ ] 使用 Spot/抢占式实例
- [ ] 优化数据传输成本
- [ ] 实施缓存层
- [ ] 使用托管服务
- [ ] 持续监控和优化

## 工具

- **AWS：** Cost Explorer、Cost Anomaly Detection、Compute Optimizer
- **Azure：** Cost Management、Advisor
- **GCP：** Cost Management、Recommender
- **多云：** CloudHealth、Cloudability、Kubecost

## 参考文件

- `references/tagging-standards.md` - 标签规范
- `assets/cost-analysis-template.xlsx` - 成本分析电子表格

## 相关技能

- `terraform-module-library` - 用于资源配置
- `multi-cloud-architecture` - 用于云平台选择
