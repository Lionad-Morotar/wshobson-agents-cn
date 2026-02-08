---
name: istio-traffic-management
description: Configure Istio traffic management including routing, load balancing, circuit breakers, and canary deployments. Use when implementing service mesh traffic policies, progressive delivery, or resilience patterns.
---

# Istio 流量管理

生产环境服务网格部署的 Istio 流量管理综合指南。

## 适用场景

- 配置服务间路由
- 实现金丝雀或蓝绿部署
- 设置熔断器和重试策略
- 负载均衡配置
- 用于测试的流量镜像
- 混沌工程的故障注入

## 核心概念

### 1. 流量管理资源

| 资源               | 用途                     | 作用域     |
| ------------------ | ------------------------ | ---------- |
| **VirtualService** | 将流量路由到目标服务     | 基于主机   |
| **DestinationRule**| 定义路由后的策略         | 基于服务   |
| **Gateway**        | 配置入口/出口流量        | 集群边缘   |
| **ServiceEntry**   | 添加外部服务到网格       | 整个网格   |

### 2. 流量流向

```
Client → Gateway → VirtualService → DestinationRule → Service
                   (路由)           (策略)            (Pod)
```

## 模板

### 模板 1: 基础路由

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-route
  namespace: bookinfo
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            end-user:
              exact: jason
      route:
        - destination:
            host: reviews
            subset: v2
    - route:
        - destination:
            host: reviews
            subset: v1
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-destination
  namespace: bookinfo
spec:
  host: reviews
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
    - name: v3
      labels:
        version: v3
```

### 模板 2: 金丝雀部署

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service-canary
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: stable
          weight: 90
        - destination:
            host: my-service
            subset: canary
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service-dr
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
  subsets:
    - name: stable
      labels:
        version: stable
    - name: canary
      labels:
        version: canary
```

### 模板 3: 熔断器

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: circuit-breaker
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

### 模板 4: 重试和超时

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ratings-retry
spec:
  hosts:
    - ratings
  http:
    - route:
        - destination:
            host: ratings
      timeout: 10s
      retries:
        attempts: 3
        perTryTimeout: 3s
        retryOn: connect-failure,refused-stream,unavailable,cancelled,retriable-4xx,503
        retryRemoteLocalities: true
```

### 模板 5: 流量镜像

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: mirror-traffic
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: v1
      mirror:
        host: my-service
        subset: v2
      mirrorPercentage:
        value: 100.0
```

### 模板 6: 故障注入

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: fault-injection
spec:
  hosts:
    - ratings
  http:
    - fault:
        delay:
          percentage:
            value: 10
          fixedDelay: 5s
        abort:
          percentage:
            value: 5
          httpStatus: 503
      route:
        - destination:
            host: ratings
```

### 模板 7: 入口网关

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: my-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: my-tls-secret
      hosts:
        - "*.example.com"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-vs
spec:
  hosts:
    - "api.example.com"
  gateways:
    - my-gateway
  http:
    - match:
        - uri:
            prefix: /api/v1
      route:
        - destination:
            host: api-service
            port:
              number: 8080
```

## 负载均衡策略

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: load-balancing
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN # 或 LEAST_CONN, RANDOM, PASSTHROUGH
---
# 用于会话保持的一致性哈希
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: sticky-sessions
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id
        # 或: httpCookie, useSourceIp, httpQueryParameterName
```

## 最佳实践

### 应该做

- **从简单开始** - 逐步增加复杂度
- **使用子集** - 清晰地对服务进行版本管理
- **设置超时** - 始终配置合理的超时时间
- **启用重试** - 但要使用退避策略和限制
- **监控** - 使用 Kiali 和 Jaeger 提高可观测性

### 不应该做

- **不要过度重试** - 可能导致级联故障
- **不要忽略异常检测** - 启用熔断器
- **不要镜像到生产环境** - 应镜像到测试环境
- **不要跳过金丝雀** - 先用小流量百分比进行测试

## 调试命令

```bash
# 检查 VirtualService 配置
istioctl analyze

# 查看生效的路由
istioctl proxy-config routes deploy/my-app -o json

# 检查端点发现
istioctl proxy-config endpoints deploy/my-app

# 调试流量
istioctl proxy-config log deploy/my-app --level debug
```

## 参考资料

- [Istio 流量管理](https://istio.io/latest/docs/concepts/traffic-management/)
- [虚拟服务参考](https://istio.io/latest/docs/reference/config/networking/virtual-service/)
- [目标规则参考](https://istio.io/latest/docs/reference/config/networking/destination-rule/)
