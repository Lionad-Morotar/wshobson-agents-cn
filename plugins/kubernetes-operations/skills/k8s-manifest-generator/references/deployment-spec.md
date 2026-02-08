# Kubernetes Deployment 规范参考

Kubernetes Deployment 资源的全面参考，涵盖所有关键字段、最佳实践和常见模式。

## 概述

Deployment 为 Pod 和 ReplicaSet 提供声明式更新。它管理应用程序的期望状态，处理部署、回滚和扩缩容操作。

## 完整 Deployment 规范

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
  annotations:
    description: "主应用部署"
    contact: "backend-team@example.com"
spec:
  # 副本管理
  replicas: 3
  revisionHistoryLimit: 10

  # Pod 选择
  selector:
    matchLabels:
      app: my-app
      version: v1

  # 更新策略
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  # Pod 就绪的最小时间
  minReadySeconds: 10

  # 部署在此时间内未进展将失败
  progressDeadlineSeconds: 600

  # Pod 模板
  template:
    metadata:
      labels:
        app: my-app
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      # RBAC 的服务账户
      serviceAccountName: my-app

      # Pod 的安全上下文
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      # Init 容器在主容器之前运行
      initContainers:
        - name: init-db
          image: busybox:1.36
          command: ["sh", "-c", "until nc -z db-service 5432; do sleep 1; done"]
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            runAsUser: 1000

      # 主容器
      containers:
        - name: app
          image: myapp:1.0.0
          imagePullPolicy: IfNotPresent

          # 容器端口
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
            - name: metrics
              containerPort: 9090
              protocol: TCP

          # 环境变量
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url

          # ConfigMap 和 Secret 引用
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets

          # 资源请求和限制
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"

          # 存活探针
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
              httpHeaders:
                - name: Custom-Header
                  value: Awesome
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            successThreshold: 1
            failureThreshold: 3

          # 就绪探针
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            successThreshold: 1
            failureThreshold: 3

          # 启动探针（用于启动缓慢的容器）
          startupProbe:
            httpGet:
              path: /health/startup
              port: http
            initialDelaySeconds: 0
            periodSeconds: 10
            timeoutSeconds: 3
            successThreshold: 1
            failureThreshold: 30

          # 卷挂载
          volumeMounts:
            - name: data
              mountPath: /var/lib/app
            - name: config
              mountPath: /etc/app
              readOnly: true
            - name: tmp
              mountPath: /tmp

          # 容器的安全上下文
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
            capabilities:
              drop:
                - ALL

          # 生命周期钩子
          lifecycle:
            postStart:
              exec:
                command:
                  ["/bin/sh", "-c", "echo Container started > /tmp/started"]
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]

      # 卷
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: app-data
        - name: config
          configMap:
            name: app-config
        - name: tmp
          emptyDir: {}

      # DNS 配置
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
          - name: ndots
            value: "2"

      # 调度
      nodeSelector:
        disktype: ssd

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - my-app
                topologyKey: kubernetes.io/hostname

      tolerations:
        - key: "app"
          operator: "Equal"
          value: "my-app"
          effect: "NoSchedule"

      # 终止
      terminationGracePeriodSeconds: 30

      # 镜像拉取密钥
      imagePullSecrets:
        - name: regcred
```

## 字段参考

### 元数据字段

#### 必需字段

- `apiVersion`: `apps/v1`（当前稳定版本）
- `kind`: `Deployment`
- `metadata.name`: 命名空间内的唯一名称

#### 推荐元数据

- `metadata.namespace`: 目标命名空间（默认为 `default`）
- `metadata.labels`: 用于组织的键值对
- `metadata.annotations`: 非标识元数据

### Spec 字段

#### 副本管理

**`replicas`**（整数，默认：1）

- 期望的 Pod 实例数量
- 最佳实践：生产环境高可用使用 3+
- 可以手动扩缩容或通过 HorizontalPodAutoscaler

**`revisionHistoryLimit`**（整数，默认：10）

- 为回滚保留的旧 ReplicaSet 数量
- 设置为 0 以禁用回滚功能
- 减少长时间运行的部署的存储开销

#### 更新策略

**`strategy.type`**（字符串）

- `RollingUpdate`（默认）：渐进式 Pod 替换
- `Recreate`：在创建新 Pod 之前删除所有 Pod

**`strategy.rollingUpdate.maxSurge`**（整数或百分比，默认：25%）

- 更新期间期望副本数之上的最大 Pod 数
- 示例：3 个副本且 maxSurge=1，更新期间最多 4 个 Pod

**`strategy.rollingUpdate.maxUnavailable`**（整数或百分比，默认：25%）

- 更新期间期望副本数之下的最大 Pod 数
- 设置为 0 以实现零停机部署
- 如果 maxSurge 为 0，则不能为 0

**最佳实践：**

```yaml
# 零停机部署
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# 快速部署（可能有短暂停机）
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 2
    maxUnavailable: 1

# 完全替换
strategy:
  type: Recreate
```

#### Pod 模板

**`template.metadata.labels`**

- 必须包含与 `spec.selector.matchLabels` 匹配的标签
- 添加版本标签用于蓝绿部署
- 包含标准 Kubernetes 标签

**`template.spec.containers`**（必需）

- 容器规范数组
- 至少需要一个容器
- 每个容器需要唯一名称

#### 容器配置

**镜像管理：**

```yaml
containers:
  - name: app
    image: registry.example.com/myapp:1.0.0
    imagePullPolicy: IfNotPresent # 或 Always、Never
```

镜像拉取策略：

- `IfNotPresent`：如果未缓存则拉取（带标签镜像的默认值）
- `Always`：始终拉取（:latest 的默认值）
- `Never`：永不拉取，如果未缓存则失败

**端口声明：**

```yaml
ports:
  - name: http # 命名以便在 Service 中引用
    containerPort: 8080
    protocol: TCP # TCP（默认）、UDP 或 SCTP
    hostPort: 8080 # 可选：绑定到主机端口（很少使用）
```

#### 资源管理

**请求 vs 限制：**

```yaml
resources:
  requests:
    memory: "256Mi" # 保证资源
    cpu: "250m" # 0.25 CPU 核心
  limits:
    memory: "512Mi" # 最大允许值
    cpu: "500m" # 0.5 CPU 核心
```

**QoS 类（自动确定）：**

1. **Guaranteed**：所有容器的请求 = 限制
   - 最高优先级
   - 最后被驱逐

2. **Burstable**：请求 < 限制或仅设置了请求
   - 中等优先级
   - 在 Guaranteed 之前被驱逐

3. **BestEffort**：未设置请求或限制
   - 最低优先级
   - 首先被驱逐

**最佳实践：**

- 生产环境始终设置请求
- 设置限制以防止资源垄断
- 内存限制应为请求的 1.5-2 倍
- CPU 限制可以更高用于突发工作负载

#### 健康检查

**探针类型：**

1. **startupProbe** - 用于启动缓慢的应用程序

   ```yaml
   startupProbe:
     httpGet:
       path: /health/startup
       port: 8080
     initialDelaySeconds: 0
     periodSeconds: 10
     failureThreshold: 30 # 5 分钟启动时间（10s * 30）
   ```

2. **livenessProbe** - 重启不健康的容器

   ```yaml
   livenessProbe:
     httpGet:
       path: /health/live
       port: 8080
     initialDelaySeconds: 30
     periodSeconds: 10
     timeoutSeconds: 5
     failureThreshold: 3 # 3 次失败后重启
   ```

3. **readinessProbe** - 控制流量路由

   ```yaml
   readinessProbe:
     httpGet:
       path: /health/ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 5
     failureThreshold: 3 # 3 次失败后从服务中移除
   ```

**探针机制：**

```yaml
# HTTP GET
httpGet:
  path: /health
  port: 8080
  httpHeaders:
    - name: Authorization
      value: Bearer token

# TCP Socket
tcpSocket:
  port: 3306

# 命令执行
exec:
  command:
    - cat
    - /tmp/healthy

# gRPC（Kubernetes 1.24+）
grpc:
  port: 9090
  service: my.service.health.v1.Health
```

**探针时间参数：**

- `initialDelaySeconds`：首次探针前的等待时间
- `periodSeconds`：探针频率
- `timeoutSeconds`：探针超时
- `successThreshold`：标记健康所需的成功次数（存活/启动为 1）
- `failureThreshold`：采取操作前的失败次数

#### 安全上下文

**Pod 级安全上下文：**

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    fsGroupChangePolicy: OnRootMismatch
    seccompProfile:
      type: RuntimeDefault
```

**容器级安全上下文：**

```yaml
containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE # 仅在需要时
```

**安全最佳实践：**

- 始终以非 root 用户运行（`runAsNonRoot: true`）
- 删除所有能力并仅添加需要的
- 尽可能使用只读根文件系统
- 启用 seccomp 配置文件
- 禁用权限提升

#### 卷

**卷类型：**

```yaml
volumes:
  # PersistentVolumeClaim
  - name: data
    persistentVolumeClaim:
      claimName: app-data

  # ConfigMap
  - name: config
    configMap:
      name: app-config
      items:
        - key: app.properties
          path: application.properties

  # Secret
  - name: secrets
    secret:
      secretName: app-secrets
      defaultMode: 0400

  # EmptyDir（临时）
  - name: cache
    emptyDir:
      sizeLimit: 1Gi

  # HostPath（生产环境避免使用）
  - name: host-data
    hostPath:
      path: /data
      type: DirectoryOrCreate
```

#### 调度

**节点选择：**

```yaml
# 简单节点选择器
nodeSelector:
  disktype: ssd
  zone: us-west-1a

# 节点亲和性（更具表达力）
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/arch
              operator: In
              values:
                - amd64
                - arm64
```

**Pod 亲和性/反亲和性：**

```yaml
# 跨节点分散 Pod
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: my-app
      topologyKey: kubernetes.io/hostname

# 与数据库共置
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: database
        topologyKey: kubernetes.io/hostname
```

**容忍度：**

```yaml
tolerations:
  - key: "node.kubernetes.io/unreachable"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 30
  - key: "dedicated"
    operator: "Equal"
    value: "database"
    effect: "NoSchedule"
```

## 常见模式

### 高可用部署

```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: my-app
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-app
```

### Sidecar 容器模式

```yaml
spec:
  template:
    spec:
      containers:
        - name: app
          image: myapp:1.0.0
          volumeMounts:
            - name: shared-logs
              mountPath: /var/log
        - name: log-forwarder
          image: fluent-bit:2.0
          volumeMounts:
            - name: shared-logs
              mountPath: /var/log
              readOnly: true
      volumes:
        - name: shared-logs
          emptyDir: {}
```

### 依赖项的 Init 容器

```yaml
spec:
  template:
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.36
          command:
            - sh
            - -c
            - |
              until nc -z database-service 5432; do
                echo "Waiting for database..."
                sleep 2
              done
        - name: run-migrations
          image: myapp:1.0.0
          command: ["./migrate", "up"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
      containers:
        - name: app
          image: myapp:1.0.0
```

## 最佳实践

### 生产检查清单

- [ ] 设置资源请求和限制
- [ ] 实现所有三种探针类型（启动、存活、就绪）
- [ ] 使用特定的镜像标签（不是 :latest）
- [ ] 配置安全上下文（非 root、只读文件系统）
- [ ] 设置副本数 >= 3 以实现高可用
- [ ] 配置 Pod 反亲和性以分散
- [ ] 设置适当的更新策略（maxUnavailable: 0 实现零停机）
- [ ] 使用 ConfigMaps 和 Secrets 进行配置
- [ ] 添加标准标签和注解
- [ ] 配置优雅关闭（preStop 钩子、terminationGracePeriodSeconds）
- [ ] 设置 revisionHistoryLimit 以支持回滚
- [ ] 使用具有最小 RBAC 权限的 ServiceAccount

### 性能调优

**快速启动：**

```yaml
spec:
  minReadySeconds: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**零停机更新：**

```yaml
spec:
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**优雅关闭：**

```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: app
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15 && kill -SIGTERM 1"]
```

## 故障排查

### 常见问题

**Pod 无法启动：**

```bash
kubectl describe deployment <name>
kubectl get pods -l app=<app-name>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**ImagePullBackOff：**

- 检查镜像名称和标签
- 验证 imagePullSecrets
- 检查注册表凭据

**CrashLoopBackOff：**

- 检查容器日志
- 验证存活探针是否过于激进
- 检查资源限制
- 验证应用程序依赖项

**部署卡在进展中：**

- 检查 progressDeadlineSeconds
- 验证就绪探针
- 检查资源可用性

## 相关资源

- [Kubernetes Deployment API 参考](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#deployment-v1-apps)
- [Pod 安全标准](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [资源管理](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
