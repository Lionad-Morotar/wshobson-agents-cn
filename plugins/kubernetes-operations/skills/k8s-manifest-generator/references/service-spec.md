# Kubernetes Service 规范参考

Kubernetes Service 资源的全面参考，涵盖服务类型、网络、负载均衡和服务发现模式。

## 概述

Service 为访问 Pod 提供稳定的网络端点。服务通过提供服务发现和负载均衡，实现微服务之间的松耦合。

## 服务类型

### 1. ClusterIP（默认）

在内部集群 IP 上暴露服务。仅可从集群内访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
  sessionAffinity: None
```

**使用场景：**

- 内部微服务通信
- 数据库服务
- 内部 API
- 消息队列

### 2. NodePort

在每个节点的 IP 上以静态端口（30000-32767 范围）暴露服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - name: http
      port: 80
      targetPort: 8080
      nodePort: 30080 # 可选，省略时自动分配
      protocol: TCP
```

**使用场景：**

- 开发/测试外部访问
- 没有负载均衡器的小型部署
- 直接节点访问需求

**限制：**

- 端口范围有限（30000-32767）
- 必须处理节点故障
- 跨节点没有内置负载均衡

### 3. LoadBalancer

使用云提供商的负载均衡器暴露服务。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
    - name: https
      port: 443
      targetPort: 8443
      protocol: TCP
  loadBalancerSourceRanges:
    - 203.0.113.0/24
```

**云特定的注解：**

**AWS：**

```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: "nlb" # 或 "external"
  service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
  service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
  service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
```

**Azure：**

```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "true"
  service.beta.kubernetes.io/azure-pip-name: "my-public-ip"
```

**GCP：**

```yaml
annotations:
  cloud.google.com/load-balancer-type: "Internal"
  cloud.google.com/backend-config: '{"default": "my-backend-config"}'
```

### 4. ExternalName

将服务映射到外部 DNS 名称（CNAME 记录）。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.external.example.com
  ports:
    - port: 5432
```

**使用场景：**

- 访问外部服务
- 服务迁移场景
- 多集群服务引用

## 完整 Service 规范

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: production
  labels:
    app: my-app
    tier: backend
  annotations:
    description: "主应用服务"
    prometheus.io/scrape: "true"
spec:
  # 服务类型
  type: ClusterIP

  # Pod 选择器
  selector:
    app: my-app
    version: v1

  # 端口配置
  ports:
    - name: http
      port: 80 # 服务端口
      targetPort: 8080 # 容器端口（或命名端口）
      protocol: TCP # TCP、UDP 或 SCTP

  # 会话亲和性
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

  # IP 配置
  clusterIP: 10.0.0.10 # 可选：特定 IP
  clusterIPs:
    - 10.0.0.10
  ipFamilies:
    - IPv4
  ipFamilyPolicy: SingleStack

  # 外部流量策略
  externalTrafficPolicy: Local

  # 内部流量策略
  internalTrafficPolicy: Local

  # 健康检查
  healthCheckNodePort: 30000

  # 负载均衡器配置（用于 type: LoadBalancer）
  loadBalancerIP: 203.0.113.100
  loadBalancerSourceRanges:
    - 203.0.113.0/24

  # 外部 IP
  externalIPs:
    - 80.11.12.10

  # 发布策略
  publishNotReadyAddresses: false
```

## 端口配置

### 命名端口

在 Pod 中使用命名端口以提高灵活性：

**Deployment：**

```yaml
spec:
  template:
    spec:
      containers:
        - name: app
          ports:
            - name: http
              containerPort: 8080
            - name: metrics
              containerPort: 9090
```

**Service：**

```yaml
spec:
  ports:
    - name: http
      port: 80
      targetPort: http # 引用命名端口
    - name: metrics
      port: 9090
      targetPort: metrics
```

### 多端口

```yaml
spec:
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
    - name: https
      port: 443
      targetPort: 8443
      protocol: TCP
    - name: grpc
      port: 9090
      targetPort: 9090
      protocol: TCP
```

## 会话亲和性

### None（默认）

在 Pod 之间随机分发请求。

```yaml
spec:
  sessionAffinity: None
```

### ClientIP

将来自同一客户端 IP 的请求路由到同一 Pod。

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800 # 3 小时
```

**使用场景：**

- 有状态应用
- 基于会话的应用
- WebSocket 连接

## 流量策略

### 外部流量策略

**Cluster（默认）：**

```yaml
spec:
  externalTrafficPolicy: Cluster
```

- 跨所有节点负载均衡
- 可能增加额外的网络跳数
- 源 IP 被屏蔽

**Local：**

```yaml
spec:
  externalTrafficPolicy: Local
```

- 流量仅到达接收节点上的 Pod
- 保留客户端源 IP
- 更好的性能（无额外跳数）
- 可能导致负载不均衡

### 内部流量策略

```yaml
spec:
  internalTrafficPolicy: Local # 或 Cluster
```

控制集群内部客户端的流量路由。

## Headless 服务

没有集群 IP 的服务，用于直接访问 Pod。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  clusterIP: None # Headless
  selector:
    app: database
  ports:
    - port: 5432
      targetPort: 5432
```

**使用场景：**

- StatefulSet Pod 发现
- Pod 到 Pod 直接通信
- 自定义负载均衡
- 数据库集群

**DNS 返回：**

- 单个 Pod IP 而非服务 IP
- 格式：`<pod-name>.<service-name>.<namespace>.svc.cluster.local`

## 服务发现

### DNS

**ClusterIP 服务：**

```
<service-name>.<namespace>.svc.cluster.local
```

示例：

```bash
curl http://backend-service.production.svc.cluster.local
```

**在同一命名空间内：**

```bash
curl http://backend-service
```

**Headless 服务（返回 Pod IP）：**

```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### 环境变量

Kubernetes 将服务信息注入到 Pod 中：

```bash
# 服务主机和端口
BACKEND_SERVICE_SERVICE_HOST=10.0.0.100
BACKEND_SERVICE_SERVICE_PORT=80

# 对于命名端口
BACKEND_SERVICE_SERVICE_PORT_HTTP=80
```

**注意：** Pod 必须在服务之后创建才能注入环境变量。

## 负载均衡

### 算法

Kubernetes 默认使用随机选择。对于高级负载均衡：

**服务网格（Istio 示例）：**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST # 或 ROUND_ROBIN、RANDOM、PASSTHROUGH
    connectionPool:
      tcp:
        maxConnections: 100
```

### 连接限制

使用 Pod 中断预算和资源限制：

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

## 服务网格集成

### Istio Virtual Service

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - match:
        - headers:
            version:
              exact: v2
      route:
        - destination:
            host: my-service
            subset: v2
    - route:
        - destination:
            host: my-service
            subset: v1
          weight: 90
        - destination:
            host: my-service
            subset: v2
          weight: 10
```

## 常见模式

### 模式 1：内部微服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: backend
  labels:
    app: user-service
    tier: backend
spec:
  type: ClusterIP
  selector:
    app: user-service
  ports:
    - name: http
      port: 8080
      targetPort: http
      protocol: TCP
    - name: grpc
      port: 9090
      targetPort: grpc
      protocol: TCP
```

### 模式 2：带负载均衡器的公共 API

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: api-gateway
  ports:
    - name: https
      port: 443
      targetPort: 8443
      protocol: TCP
  loadBalancerSourceRanges:
    - 0.0.0.0/0
```

### 模式 3：StatefulSet 与 Headless 服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cassandra
spec:
  clusterIP: None
  selector:
    app: cassandra
  ports:
    - port: 9042
      targetPort: 9042
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      containers:
        - name: cassandra
          image: cassandra:4.0
```

### 模式 4：外部服务映射

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-database
spec:
  type: ExternalName
  externalName: prod-db.cxyz.us-west-2.rds.amazonaws.com
---
# 或使用 Endpoints 实现基于 IP 的外部服务
apiVersion: v1
kind: Service
metadata:
  name: external-api
spec:
  ports:
    - port: 443
      targetPort: 443
      protocol: TCP
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-api
subsets:
  - addresses:
      - ip: 203.0.113.100
    ports:
      - port: 443
```

### 模式 5：带指标的多端口服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090
```

## 网络策略

控制服务的流量：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

## 最佳实践

### 服务配置

1. **使用命名端口**以提高灵活性
2. **根据暴露需求设置适当的服务类型**
3. **在 Deployment 和 Service 之间一致使用标签和选择器**
4. **为有状态应用配置会话亲和性**
5. **将外部流量策略设置为 Local** 以保留 IP
6. **为 StatefulSet 使用 headless 服务**
7. **实施网络策略**以增强安全性
8. **添加监控注解**以提高可观测性

### 生产检查清单

- [ ] 服务类型适用于用例
- [ ] 选择器与 Pod 标签匹配
- [ ] 使用命名端口以提高清晰度
- [ ] 如需要则配置会话亲和性
- [ ] 适当设置流量策略
- [ ] 配置负载均衡器注解（如适用）
- [ ] 限制源 IP 范围（对于公共服务）
- [ ] 验证健康检查配置
- [ ] 添加监控注解
- [ ] 定义网络策略

### 性能调优

**对于高流量：**

```yaml
spec:
  externalTrafficPolicy: Local
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

**对于 WebSocket/长连接：**

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 86400 # 24 小时
```

## 故障排查

### 服务无法访问

```bash
# 检查服务是否存在
kubectl get service <service-name>

# 检查端点（应显示 Pod IP）
kubectl get endpoints <service-name>

# 描述服务
kubectl describe service <service-name>

# 检查 Pod 是否匹配选择器
kubectl get pods -l app=<app-name>
```

**常见问题：**

- 选择器与 Pod 标签不匹配
- 没有 Pod 在运行（端点为空）
- 端口配置错误
- 网络策略阻止流量

### DNS 解析失败

```bash
# 从 Pod 测试 DNS
kubectl run debug --rm -it --image=busybox -- nslookup <service-name>

# 检查 CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### 负载均衡器问题

```bash
# 检查负载均衡器状态
kubectl describe service <service-name>

# 检查事件
kubectl get events --sort-by='.lastTimestamp'

# 验证云提供商配置
kubectl describe node
```

## 相关资源

- [Kubernetes Service API 参考](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#service-v1-core)
- [服务网络](https://kubernetes.io/docs/concepts/services-networking/service/)
- [服务和 Pod 的 DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
