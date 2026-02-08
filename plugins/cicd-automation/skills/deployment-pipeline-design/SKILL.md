---
name: deployment-pipeline-design
description: 设计具有审批网关、安全检查和部署编排的多阶段 CI/CD 流水线。用于架构部署工作流、设置持续交付或实施 GitOps 实践。
---

# 部署流水线设计

具有审批网关和部署策略的多阶段 CI/CD 流水线架构模式。

## 目的

设计健壮、安全的部署流水线,通过合理的阶段组织和审批工作流程在速度与安全性之间取得平衡。

## 何时使用

- 设计 CI/CD 架构
- 实施部署网关
- 配置多环境流水线
- 建立部署最佳实践
- 实施渐进式交付

## 流水线阶段

### 标准流水线流程

```
┌─────────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────────┐
│  构建   │ → │ 测试 │ → │ 预发布  │ → │  审批  │ → │ 生产环境 │
└─────────┘   └──────┘   └─────────┘   └────────┘   └──────────┘
```

### 详细阶段分解

1. **源代码** - 代码检出
2. **构建** - 编译、打包、容器化
3. **测试** - 单元测试、集成测试、安全扫描
4. **预发布部署** - 部署到预发布环境
5. **集成测试** - 端到端测试、冒烟测试
6. **审批网关** - 需要手动审批
7. **生产部署** - 金丝雀、蓝绿、滚动更新
8. **验证** - 健康检查、监控
9. **回滚** - 失败时自动回滚

## 审批网关模式

### 模式 1: 手动审批

```yaml
# GitHub Actions
production-deploy:
  needs: staging-deploy
  environment:
    name: production
    url: https://app.example.com
  runs-on: ubuntu-latest
  steps:
    - name: 部署到生产环境
      run: |
        # 部署命令
```

### 模式 2: 基于时间的审批

```yaml
# GitLab CI
deploy:production:
  stage: deploy
  script:
    - deploy.sh production
  environment:
    name: production
  when: delayed
  start_in: 30 minutes
  only:
    - main
```

### 模式 3: 多人审批

```yaml
# Azure Pipelines
stages:
  - stage: Production
    dependsOn: Staging
    jobs:
      - deployment: Deploy
        environment:
          name: production
          resourceType: Kubernetes
        strategy:
          runOnce:
            preDeploy:
              steps:
                - task: ManualValidation@0
                  inputs:
                    notifyUsers: "team-leads@example.com"
                    instructions: "审批前审查预发布指标"
```

**参考:** 参见 `assets/approval-gate-template.yml`

## 部署策略

### 1. 滚动部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**特性:**

- 逐步推出
- 零停机
- 易于回滚
- 适用于大多数应用程序

### 2. 蓝绿部署

```yaml
# 蓝环境(当前)
kubectl apply -f blue-deployment.yaml
kubectl label service my-app version=blue

# 绿环境(新)
kubectl apply -f green-deployment.yaml
# 测试绿环境
kubectl label service my-app version=green

# 需要时回滚
kubectl label service my-app version=blue
```

**特性:**

- 瞬间切换
- 易于回滚
- 临时翻倍基础设施成本
- 适用于高风险部署

### 3. 金丝雀部署

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - setWeight: 25
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 5m }
        - setWeight: 100
```

**特性:**

- 渐进式流量转移
- 降低风险
- 真实用户测试
- 需要服务网格或类似技术

### 4. 功能开关

```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key="API_KEY")

if flagsmith.has_feature("new_checkout_flow"):
    # 新代码路径
    process_checkout_v2()
else:
    # 现有代码路径
    process_checkout_v1()
```

**特性:**

- 部署而不发布
- A/B 测试
- 瞬间回滚
- 精细控制

## 流水线编排

### 多阶段流水线示例

```yaml
name: 生产流水线

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 构建应用
        run: make build
      - name: 构建 Docker 镜像
        run: docker build -t myapp:${{ github.sha }} .
      - name: 推送到镜像仓库
        run: docker push myapp:${{ github.sha }}

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: 单元测试
        run: make test
      - name: 安全扫描
        run: trivy image myapp:${{ github.sha }}

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: staging
    steps:
      - name: 部署到预发布环境
        run: kubectl apply -f k8s/staging/

  integration-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: 运行端到端测试
        run: npm run test:e2e

  deploy-production:
    needs: integration-test
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: 金丝雀部署
        run: |
          kubectl apply -f k8s/production/
          kubectl argo rollouts promote my-app

  verify:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: 健康检查
        run: curl -f https://app.example.com/health
      - name: 通知团队
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"生产部署成功!"}'
```

## 流水线最佳实践

1. **快速失败** - 先运行快速测试
2. **并行执行** - 并发运行独立任务
3. **缓存** - 在运行之间缓存依赖
4. **制品管理** - 存储构建制品
5. **环境一致性** - 保持环境一致
6. **密钥管理** - 使用密钥存储(Vault 等)
7. **部署窗口** - 合理安排部署时间
8. **监控集成** - 跟踪部署指标
9. **回滚自动化** - 失败时自动回滚
10. **文档** - 记录流水线阶段

## 回滚策略

### 自动回滚

```yaml
deploy-and-verify:
  steps:
    - name: 部署新版本
      run: kubectl apply -f k8s/

    - name: 等待推出完成
      run: kubectl rollout status deployment/my-app

    - name: 健康检查
      id: health
      run: |
        for i in {1..10}; do
          if curl -sf https://app.example.com/health; then
            exit 0
          fi
          sleep 10
        done
        exit 1

    - name: 失败时回滚
      if: failure()
      run: kubectl rollout undo deployment/my-app
```

### 手动回滚

```bash
# 列出修订历史
kubectl rollout history deployment/my-app

# 回滚到上一个版本
kubectl rollout undo deployment/my-app

# 回滚到特定修订
kubectl rollout undo deployment/my-app --to-revision=3
```

## 监控和指标

### 关键流水线指标

- **部署频率** - 部署发生的频率
- **前置时间** - 从提交到生产的时间
- **变更失败率** - 失败部署的百分比
- **平均恢复时间(MTTR)** - 从失败中恢复的时间
- **流水线成功率** - 成功运行的百分比
- **平均流水线持续时间** - 完成流水线的时间

### 与监控集成

```yaml
- name: 部署后验证
  run: |
    # 等待指标稳定
    sleep 60

    # 检查错误率
    ERROR_RATE=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=rate(http_errors_total[5m])" | jq '.data.result[0].value[1]')

    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "错误率过高: $ERROR_RATE"
      exit 1
    fi
```

## 参考文件

- `references/pipeline-orchestration.md` - 复杂流水线模式
- `assets/approval-gate-template.yml` - 审批工作流模板

## 相关技能

- `github-actions-templates` - GitHub Actions 实现
- `gitlab-ci-patterns` - GitLab CI 实现
- `secrets-management` - 密钥处理
