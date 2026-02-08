# GitOps 同步策略

## ArgoCD 同步策略

### 自动同步

```yaml
syncPolicy:
  automated:
    prune: true # 删除从 Git 中移除的资源
    selfHeal: true # 协调手动更改
    allowEmpty: false # 防止空同步
```

### 手动同步

```yaml
syncPolicy:
  syncOptions:
    - PrunePropagationPolicy=foreground
    - CreateNamespace=true
```

### 同步窗口

```yaml
syncWindows:
  - kind: allow
    schedule: "0 8 * * *"
    duration: 1h
    applications:
      - my-app
  - kind: deny
    schedule: "0 22 * * *"
    duration: 8h
    applications:
      - "*"
```

### 重试策略

```yaml
syncPolicy:
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

## Flux 同步策略

### Kustomization 同步

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
spec:
  interval: 5m
  prune: true
  wait: true
  timeout: 5m
  retryInterval: 1m
  force: false
```

### 源同步间隔

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
spec:
  interval: 1m
  timeout: 60s
```

## 健康评估

### 自定义健康检查

```yaml
# ArgoCD
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.MyCustomResource: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "False" then
            hs.status = "Degraded"
            hs.message = condition.message
            return hs
          end
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for status"
    return hs
```

## 同步选项

### 常用同步选项

- `PrunePropagationPolicy=foreground` - 等待删除的资源被完全删除
- `CreateNamespace=true` - 自动创建命名空间
- `Validate=false` - 跳过 kubectl 验证
- `PruneLast=true` - 在同步后修剪资源
- `RespectIgnoreDifferences=true` - 遵循忽略差异配置
- `ApplyOutOfSyncOnly=true` - 仅应用不同步的资源

## 最佳实践

1. 在非生产环境使用自动同步
2. 生产环境需要手动批准
3. 为维护配置同步窗口
4. 为自定义资源实施健康检查
5. 对于大型应用使用选择性同步
6. 配置适当的重试策略
7. 使用警报监控同步失败
8. 在生产环境中谨慎使用修剪
9. 在暂存环境测试同步策略
10. 为团队记录同步行为
