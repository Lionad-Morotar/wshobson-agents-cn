# RBAC 模式和最佳实践

## 常见 RBAC 模式

### 模式 1: 只读访问

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only
rules:
  - apiGroups: ["", "apps", "batch"]
    resources: ["*"]
    verbs: ["get", "list", "watch"]
```

### 模式 2: 命名空间管理员

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: namespace-admin
  namespace: production
rules:
  - apiGroups: ["", "apps", "batch", "extensions"]
    resources: ["*"]
    verbs: ["*"]
```

### 模式 3: 部署管理器

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

### 模式 4: 密钥读取器(ServiceAccount)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["app-secrets"] # 仅限特定密钥
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-secret-reader
  namespace: production
subjects:
  - kind: ServiceAccount
    name: my-app
    namespace: production
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### 模式 5: CI/CD 流水线访问

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cicd-deployer
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services", "configmaps"]
    verbs: ["get", "list", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
```

## ServiceAccount 最佳实践

### 创建专用 ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      serviceAccountName: my-app
      automountServiceAccountToken: false # 如不需要则禁用
```

### 最小权限 ServiceAccount

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get"]
    resourceNames: ["my-app-config"]
```

## 安全最佳实践

1. **尽可能使用 Roles 而非 ClusterRoles**
2. **指定 resourceNames** 以实现细粒度访问
3. **避免生产环境中的通配符权限** (`*`)
4. **为每个应用创建专用 ServiceAccount**
5. **如不需要则禁用令牌自动挂载**
6. **定期 RBAC 审计** 以删除未使用的权限
7. **使用组** 进行用户管理
8. **实施命名空间隔离**
9. **使用审计日志监控 RBAC 使用情况**
10. **在元数据中记录角色用途**

## RBAC 故障排查

### 检查用户权限

```bash
kubectl auth can-i list pods --as john@example.com
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-app
```

### 查看有效权限

```bash
kubectl describe clusterrole cluster-admin
kubectl describe rolebinding -n production
```

### 调试访问问题

```bash
kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide | grep my-user
```

## 常见 RBAC 动词

- `get` - 读取特定资源
- `list` - 列出某种类型的所有资源
- `watch` - 监视资源更改
- `create` - 创建新资源
- `update` - 更新现有资源
- `patch` - 部分更新资源
- `delete` - 删除资源
- `deletecollection` - 删除多个资源
- `*` - 所有动词(生产环境中避免使用)

## 资源范围

### 集群范围资源

- Nodes
- PersistentVolumes
- ClusterRoles
- ClusterRoleBindings
- Namespaces

### 命名空间范围资源

- Pods
- Services
- Deployments
- ConfigMaps
- Secrets
- Roles
- RoleBindings
