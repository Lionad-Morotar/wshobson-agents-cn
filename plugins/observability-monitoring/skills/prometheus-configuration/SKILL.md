---
name: prometheus-configuration
description: 设置 Prometheus 以实现基础设施和应用程序的全面指标采集、存储和监控。在实施指标采集、设置监控基础设施或配置告警系统时使用。
---

# Prometheus 配置

Prometheus 设置、指标采集、抓取配置和记录规则的完整指南。

## 目的

配置 Prometheus 以实现对基础设施和应用程序的全面指标采集、告警和监控。

## 何时使用

- 设置 Prometheus 监控
- 配置指标抓取
- 创建记录规则
- 设计告警规则
- 实现服务发现

## Prometheus 架构

```
┌──────────────┐
│ 应用程序     │ ← 使用客户端库进行埋点
└──────┬───────┘
       │ /metrics 端点
       ↓
┌──────────────┐
│  Prometheus  │ ← 定期抓取指标
│    服务器    │
└──────┬───────┘
       │
       ├─→ AlertManager (告警)
       ├─→ Grafana (可视化)
       └─→ 长期存储 (Thanos/Cortex)
```

## 安装

### 使用 Helm 在 Kubernetes 上安装

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageVolumeSize=50Gi
```

### 使用 Docker Compose

```yaml
version: "3.8"
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--storage.tsdb.retention.time=30d"

volumes:
  prometheus-data:
```

## 配置文件

**prometheus.yml:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: "production"
    region: "us-west-2"

# Alertmanager 配置
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# 加载规则文件
rule_files:
  - /etc/prometheus/rules/*.yml

# 抓取配置
scrape_configs:
  # Prometheus 自身
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  # Node exporters
  - job_name: "node-exporter"
    static_configs:
      - targets:
          - "node1:9100"
          - "node2:9100"
          - "node3:9100"
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: "([^:]+)(:[0-9]+)?"
        replacement: "${1}"

  # 带注解的 Kubernetes Pods
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod

  # 应用程序指标
  - job_name: "my-app"
    static_configs:
      - targets:
          - "app1.example.com:9090"
          - "app2.example.com:9090"
    metrics_path: "/metrics"
    scheme: "https"
    tls_config:
      ca_file: /etc/prometheus/ca.crt
      cert_file: /etc/prometheus/client.crt
      key_file: /etc/prometheus/client.key
```

**参考：** 参见 `assets/prometheus.yml.template`

## 抓取配置

### 静态目标

```yaml
scrape_configs:
  - job_name: "static-targets"
    static_configs:
      - targets: ["host1:9100", "host2:9100"]
        labels:
          env: "production"
          region: "us-west-2"
```

### 基于文件的服务发现

```yaml
scrape_configs:
  - job_name: "file-sd"
    file_sd_configs:
      - files:
          - /etc/prometheus/targets/*.json
          - /etc/prometheus/targets/*.yml
        refresh_interval: 5m
```

**targets/production.json:**

```json
[
  {
    "targets": ["app1:9090", "app2:9090"],
    "labels": {
      "env": "production",
      "service": "api"
    }
  }
]
```

### Kubernetes 服务发现

```yaml
scrape_configs:
  - job_name: "kubernetes-services"
    kubernetes_sd_configs:
      - role: service
    relabel_configs:
      - source_labels:
          [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels:
          [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

**参考：** 参见 `references/scrape-configs.md`

## 记录规则

为频繁查询的表达式创建预计算指标：

```yaml
# /etc/prometheus/rules/recording_rules.yml
groups:
  - name: api_metrics
    interval: 15s
    rules:
      # 每个服务的 HTTP 请求速率
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      # 错误率百分比
      - record: job:http_requests_errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      - record: job:http_requests_error_rate:percentage
        expr: |
          (job:http_requests_errors:rate5m / job:http_requests:rate5m) * 100

      # P95 延迟
      - record: job:http_request_duration:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

  - name: resource_metrics
    interval: 30s
    rules:
      # CPU 利用率百分比
      - record: instance:node_cpu:utilization
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

      # 内存利用率百分比
      - record: instance:node_memory:utilization
        expr: |
          100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)

      # 磁盘使用率百分比
      - record: instance:node_disk:utilization
        expr: |
          100 - ((node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)
```

**参考：** 参见 `references/recording-rules.md`

## 告警规则

```yaml
# /etc/prometheus/rules/alert_rules.yml
groups:
  - name: availability
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "服务 {{ $labels.instance }} 已宕机"
          description: "{{ $labels.job }} 已宕机超过 1 分钟"

      - alert: HighErrorRate
        expr: job:http_requests_error_rate:percentage > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.job }} 错误率过高"
          description: "错误率为 {{ $value }}%（阈值：5%）"

      - alert: HighLatency
        expr: job:http_request_duration:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.job }} 延迟过高"
          description: "P95 延迟为 {{ $value }}s（阈值：1s）"

  - name: resources
    interval: 1m
    rules:
      - alert: HighCPUUsage
        expr: instance:node_cpu:utilization > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.instance }} CPU 使用率过高"
          description: "CPU 使用率为 {{ $value }}%"

      - alert: HighMemoryUsage
        expr: instance:node_memory:utilization > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.instance }} 内存使用率过高"
          description: "内存使用率为 {{ $value }}%"

      - alert: DiskSpaceLow
        expr: instance:node_disk:utilization > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.instance }} 磁盘空间不足"
          description: "磁盘使用率为 {{ $value }}%"
```

## 验证

```bash
# 验证配置
promtool check config prometheus.yml

# 验证规则
promtool check rules /etc/prometheus/rules/*.yml

# 测试查询
promtool query instant http://localhost:9090 'up'
```

**参考：** 参见 `scripts/validate-prometheus.sh`

## 最佳实践

1. **使用一致的命名**规范（前缀_名称_单位）
2. **设置适当的抓取间隔**（通常 15-60 秒）
3. **对昂贵的查询使用记录规则**
4. **实现高可用性**（多个 Prometheus 实例）
5. **根据存储容量配置保留时间**
6. **使用重标签**进行指标清理
7. **监控 Prometheus 自身**
8. **实现联邦**用于大规模部署
9. **使用 Thanos/Cortex**进行长期存储
10. **记录自定义指标**文档

## 故障排查

**检查抓取目标：**

```bash
curl http://localhost:9090/api/v1/targets
```

**检查配置：**

```bash
curl http://localhost:9090/api/v1/status/config
```

**测试查询：**

```bash
curl 'http://localhost:9090/api/v1/query?query=up'
```

## 参考文件

- `assets/prometheus.yml.template` - 完整配置模板
- `references/scrape-configs.md` - 抓取配置模式
- `references/recording-rules.md` - 记录规则示例
- `scripts/validate-prometheus.sh` - 验证脚本

## 相关技能

- `grafana-dashboards` - 用于可视化
- `slo-implementation` - 用于 SLO 监控
- `distributed-tracing` - 用于请求追踪
