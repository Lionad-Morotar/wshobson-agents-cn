---
name: github-actions-templates
description: 创建用于自动化测试、构建和部署应用程序的生产级 GitHub Actions 工作流。用于使用 GitHub Actions 设置 CI/CD、自动化开发工作流或创建可重用的工作流模板。
---

# GitHub Actions 模板

用于测试、构建和部署应用程序的生产级 GitHub Actions 工作流模式。

## 目的

为各种技术栈的持续集成和部署创建高效、安全的 GitHub Actions 工作流。

## 何时使用

- 自动化测试和部署
- 构建 Docker 镜像并推送到镜像仓库
- 部署到 Kubernetes 集群
- 运行安全扫描
- 为多个环境实施矩阵构建

## 常见工作流模式

### 模式 1: 测试工作流

```yaml
name: 测试

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: 使用 Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - name: 安装依赖
        run: npm ci

      - name: 运行 linter
        run: npm run lint

      - name: 运行测试
        run: npm test

      - name: 上传覆盖率
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

**参考:** 参见 `assets/test-workflow.yml`

### 模式 2: 构建并推送 Docker 镜像

```yaml
name: 构建并推送

on:
  push:
    branches: [main]
    tags: ["v*"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: 登录到容器镜像仓库
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: 提取元数据
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: 构建并推送
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**参考:** 参见 `assets/deploy-workflow.yml`

### 模式 3: 部署到 Kubernetes

```yaml
name: 部署到 Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: 配置 AWS 凭证
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - name: 更新 kubeconfig
        run: |
          aws eks update-kubeconfig --name production-cluster --region us-west-2

      - name: 部署到 Kubernetes
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/my-app -n production
          kubectl get services -n production

      - name: 验证部署
        run: |
          kubectl get pods -n production
          kubectl describe deployment my-app -n production
```

### 模式 4: 矩阵构建

```yaml
name: 矩阵构建

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 运行测试
        run: pytest
```

**参考:** 参见 `assets/matrix-build.yml`

## 工作流最佳实践

1. **使用特定的 action 版本** (@v4,而不是 @latest)
2. **缓存依赖** 以加速构建
3. **使用密钥** 处理敏感数据
4. **在 PR 上实施状态检查**
5. **使用矩阵构建** 进行多版本测试
6. **设置适当的权限**
7. **使用可重用工作流** 处理常见模式
8. **为生产环境实施审批网关**
9. **添加通知步骤** 处理失败
10. **使用自托管运行器** 处理敏感工作负载

## 可重用工作流

```yaml
# .github/workflows/reusable-test.yml
name: 可重用测试工作流

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

**使用可重用工作流:**

```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "20.x"
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 安全扫描

```yaml
name: 安全扫描

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: 运行 Trivy 漏洞扫描器
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: "fs"
          scan-ref: "."
          format: "sarif"
          output: "trivy-results.sarif"

      - name: 上传 Trivy 结果到 GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: "trivy-results.sarif"

      - name: 运行 Snyk 安全扫描
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## 带审批的部署

```yaml
name: 部署到生产环境

on:
  push:
    tags: ["v*"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com

    steps:
      - uses: actions/checkout@v4

      - name: 部署应用
        run: |
          echo "正在部署到生产环境..."
          # 部署命令

      - name: 通知 Slack
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "生产环境部署成功完成!"
            }
```

## 参考文件

- `assets/test-workflow.yml` - 测试工作流模板
- `assets/deploy-workflow.yml` - 部署工作流模板
- `assets/matrix-build.yml` - 矩阵构建模板
- `references/common-workflows.md` - 常见工作流模式

## 相关技能

- `gitlab-ci-patterns` - GitLab CI 工作流
- `deployment-pipeline-design` - 流水线架构
- `secrets-management` - 密钥处理
