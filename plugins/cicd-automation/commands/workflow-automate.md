# workflow-automate

使用工作流自动化命令简化开发工作流程、CI/CD 流水线和基础设施管理。

## 功能概述

工作流自动化命令提供全面的工具集用于：
- GitHub Actions 工作流分析
- CI/CD 流水线生成
- 发布自动化
- 开发工作流自动化
- 基础设施自动化
- 监控和可观测性
- 安全扫描集成
- 工作流编排

## 工作流分析

在实施自动化解决方案之前，分析当前的工作流和识别改进领域。

### workflow_analyzer.py

```python
#!/usr/bin/env python3
"""
工作流分析器 - 分析 GitHub Actions 工作流和识别自动化机会

分析 GitHub Actions 工作流文件、识别瓶颈、优化机会并提供改进建议。
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class WorkflowMetrics:
    """工作流指标"""
    name: str
    total_runs: int
    avg_duration: timedelta
    success_rate: float
    jobs_count: int
    critical_path: List[str]
    optimization_opportunities: List[str]


class WorkflowAnalyzer:
    """GitHub Actions 工作流分析器"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.workflows_dir = self.repo_path / ".github" / "workflows"
        
    def analyze_workflows(self) -> Dict[str, WorkflowMetrics]:
        """分析所有工作流并计算指标"""
        metrics = {}
        
        for workflow_file in self.workflows_dir.glob("*.yml"):
            workflow = self._parse_workflow(workflow_file)
            if workflow:
                workflow_name = workflow.get("name", workflow_file.stem)
                metrics[workflow_name] = self._calculate_metrics(workflow)
                
        return metrics
    
    def _parse_workflow(self, workflow_file: Path) -> Dict[str, Any]:
        """解析工作流 YAML 文件"""
        try:
            with open(workflow_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error parsing {workflow_file}: {e}")
            return None
    
    def _calculate_metrics(self, workflow: Dict[str, Any]) -> WorkflowMetrics:
        """计算工作流指标"""
        jobs = workflow.get("jobs", {})
        jobs_count = len(jobs)
        
        return WorkflowMetrics(
            name=workflow.get("name", "Unknown"),
            total_runs=0,  # 从 GitHub API 获取
            avg_duration=timedelta(minutes=5),
            success_rate=0.95,
            jobs_count=jobs_count,
            critical_path=self._identify_critical_path(jobs),
            optimization_opportunities=self._find_optimizations(jobs)
        )
    
    def _identify_critical_path(self, jobs: Dict[str, Any]) -> List[str]:
        """识别关键路径中的任务"""
        critical = []
        for job_name, job_config in jobs.items():
            needs = job_config.get("needs", [])
            if not needs:  # 起始任务
                critical.append(job_name)
        return critical
    
    def _find_optimizations(self, jobs: Dict[str, Any]) -> List[str]:
        """识别优化机会"""
        optimizations = []
        
        for job_name, job_config in jobs.items():
            steps = job_config.get("steps", [])
            
            # 检查缓存机会
            if any("npm install" in str(step) for step in steps):
                optimizations.append(f"{job_name}: 添加 npm 缓存")
            
            # 检查并行化机会
            if job_config.get("matrix"):
                optimizations.append(f"{job_name}: 优化矩阵策略")
                
        return optimizations
    
    def generate_report(self, metrics: Dict[str, WorkflowMetrics]) -> str:
        """生成分析报告"""
        report = ["# 工作流分析报告", ""]
        
        for workflow_name, metric in metrics.items():
            report.append(f"## {workflow_name}")
            report.append(f"- 任务数: {metric.jobs_count}")
            report.append(f"- 平均持续时间: {metric.avg_duration}")
            report.append(f"- 成功率: {metric.success_rate:.1%}")
            report.append(f"- 优化机会: {len(metric.optimization_opportunities)}")
            report.append("")
            
        return "\n".join(report)


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: workflow_analyzer.py <repo_path>")
        sys.exit(1)
    
    analyzer = WorkflowAnalyzer(sys.argv[1])
    metrics = analyzer.analyze_workflows()
    report = analyzer.generate_report(metrics)
    print(report)


if __name__ == "__main__":
    main()
```

## CI/CD 流水线

创建健壮的 CI/CD 流水线用于自动化测试、构建和部署。

### .github/workflows/ci-cd.yml

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 代码质量检查
  code-quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 设置 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: 安装依赖
        run: npm ci
      
      - name: 运行 Lint
        run: npm run lint
      
      - name: 运行类型检查
        run: npm run type-check
      
      - name: 代码格式检查
        run: npm run format:check

  # 安全扫描
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 Trivy 漏洞扫描
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: 上传 Trivy 结果到 GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  # 测试
  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 21]
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: 安装依赖
        run: npm ci
      
      - name: 运行单元测试
        run: npm run test:unit
      
      - name: 运行集成测试
        run: npm run test:integration
      
      - name: 生成覆盖率报告
        run: npm run test:coverage
      
      - name: 上传覆盖率到 Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella

  # 构建
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [code-quality, security-scan, test]
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: 安装依赖
        run: npm ci
      
      - name: 构建项目
        run: npm run build
      
      - name: 上传构建产物
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7

  # Docker 镜像构建和推送
  docker-build:
    name: Docker Build & Push
    runs-on: ubuntu-latest
    needs: [build]
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: 登录到 GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 提取 Docker 元数据
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
      
      - name: 构建并推送 Docker 镜像
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  # 部署到预发布环境
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [docker-build]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 kubectl
        uses: azure/setup-kubectl@v3
      
      - name: 配置 kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > $HOME/.kube/config
      
      - name: 部署到 Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/app -n staging

  # 部署到生产环境
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [docker-build]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 kubectl
        uses: azure/setup-kubectl@v3
      
      - name: 配置 kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG_PRODUCTION }}" | base64 -d > $HOME/.kube/config
      
      - name: 部署到 Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/app -n production
      
      - name: 验证部署
        run: |
          kubectl get pods -n production
          kubectl get services -n production

  # 性能测试
  performance-test:
    name: Performance Test
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://staging.example.com
          uploadArtifacts: true
          temporaryPublicStorage: true

  # 通知
  notify:
    name: Notify
    runs-on: ubuntu-latest
    needs: [deploy-production, performance-test]
    if: always()
    steps:
      - name: 发送 Slack 通知
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: '部署完成: ${{ github.ref }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 发布自动化

自动化语义化版本和发布管理。

### .github/workflows/release.yml

```yaml
name: Release Automation

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  release:
    name: Semantic Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      
      - name: 设置 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: 安装依赖
        run: npm ci
      
      - name: 运行测试
        run: npm test
      
      - name: 构建项目
        run: npm run build
      
      - name: 创建 Release
        id: release
        uses: semantic-release/semantic-release@v22
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        with:
          branches: ['main']
          plugins: |
            @semantic-release/commit-analyzer
            @semantic-release/release-notes-generator
            @semantic-release/github
            @semantic-release/npm
      
      - name: 上传 Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: release-artifacts
          path: |
            dist/
            package.json
            package-lock.json
          if-no-files-found: error
      
      - name: 创建 GitHub Release
        if: steps.release.outputs.new_release_published == 'true'
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ steps.release.outputs.git_tag }}
          release_name: Release ${{ steps.release.outputs.git_tag }}
          body: ${{ steps.release.outputs.notes }}
          draft: false
          prerelease: false
```

## 开发工作流自动化

自动化常见开发任务并强制执行最佳实践。

### .github/workflows/pr-automation.yml

```yaml
name: PR Automation

on:
  pull_request:
    types: [opened, synchronize, reopened, edited]
  pull_request_review:
    types: [submitted, edited, dismissed]

jobs:
  # 自动标签
  auto-label:
    name: Auto Label
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 自动标签
        uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml
          sync-labels: true

  # PR 验证
  pr-validation:
    name: PR Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 检查 PR 描述
        uses: techsteplez/pr-description-checker@v2
        with:
          fail_on_error: true
          min_length: 20
      
      - name: 检查链接任务
        uses: nearform/github-action-check-linked-issues@v1
        with:
          excludeFromBranch: main,develop
          customNotLinkedMessage: "请将此 PR 链接到一个 issue"
      
      - name: 检查提交签名
        uses: 1Francis1/commit-sign-check@v1
        with:
          allowed-actors: dependabot[bot], renovate[bot]

  # 代码审查分配
  assign-reviewers:
    name: Assign Reviewers
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 分配代码审查者
        uses: kentaro-m/auto-assign-action@v2
        with:
          configuration-path: .github/auto_assign.yml
          repo-token: ${{ secrets.GITHUB_TOKEN }}

  # 自动合并依赖更新
  auto-merge-dependencies:
    name: Auto Merge Dependencies
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]' || github.actor == 'renovate[bot]'
    steps:
      - name: 等待 CI 检查通过
        uses: lewagon/wait-on-check-action@v1.3.1
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          check-name: 'Code Quality'
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
      
      - name: 自动合并
        uses: ahmadnassri/action-dependabot-auto-merge@v2
        with:
          target: minor
          github-token: ${{ secrets.GITHUB_TOKEN }}

  # 大型 PR 警告
  large-pr-warning:
    name: Large PR Warning
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 检查 PR 大小
        uses: action-reviews/large-pr-warning@v2
        with:
          files_limit: 500
          lines_limit: 2000
          comment_message: "这个 PR 非常大，请考虑将其拆分为更小的 PR 以便于审查"
```

### pre-commit-config.yaml

```yaml
# Pre-commit 钩子配置
# 安装: pip install pre-commit
# 运行: pre-commit install

default_language_version:
  python: python3.11
  node: "20"

repos:
  # 通用文件检查
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key
      - id: mixed-line-ending

  # Python 特定检查
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-PyYAML

  # JavaScript/TypeScript 检查
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, css,scss, json, markdown]
        exclude: package-lock.json

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.57.0
    hooks:
      - id: eslint
        types_or: [javascript, jsx, ts, tsx]
        args: ['--fix']

  # 安全检查
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # Dockerfile 检查
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker
        args: ['--ignore', 'DL3008']

  # Markdown 检查
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: ['--fix']

  # Terraform 检查
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.2
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
        args: ['--args=--module']
      - id: terraform_docs
        args: ['--args=--sort-by-required']
      - id: terraform_tfsec
        args: ['--args=--exclude-downloaded-modules']

  # Kubernetes 清单检查
  - repo: https://github.com/instrumenta/kubeval
    rev: v0.16.1
    hooks:
      - id: kubeval
        files: .*\.yaml$
```

### scripts/setup-dev.sh

```bash
#!/bin/bash
# 开发环境自动化设置脚本

set -e

echo "🚀 开始设置开发环境..."

# 检测操作系统
OS="$(uname -s)"
echo "检测到操作系统: $OS"

# 安装 Homebrew (macOS)
if [[ "$OS" == "Darwin" ]]; then
    if ! command -v brew &> /dev/null; then
        echo "📦 安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "✅ Homebrew 已安装"
    fi
fi

# 安装依赖工具
echo "🔧 安装开发工具..."

if [[ "$OS" == "Darwin" ]]; then
    brew install node@20 python@3.11 git kubectl helm terraform vault jq
elif [[ "$OS" == "Linux" ]]; then
    sudo apt-get update
    sudo apt-get install -y nodejs npm python3.11 python3-pip git kubectl helm terraform vault jq
fi

# 安装 Node.js 依赖
if [ -f "package.json" ]; then
    echo "📦 安装 Node.js 依赖..."
    npm install
fi

# 安装 Python 依赖
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "📦 安装 Python 依赖..."
    pip install -r requirements.txt || pip install .
fi

# 安装 pre-commit 钩子
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🪝 安装 pre-commit 钩子..."
    pip install pre-commit
    pre-commit install
fi

# 安装 Husky (Node.js 钩子)
if [ -f "package.json" ]; then
    echo "🪝 安装 Husky 钩子..."
    npm install -g husky
    npx husky install
fi

# 设置 Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Docker 未安装。请从 https://www.docker.com/products/docker-desktop 下载"
fi

# 设置 kubectl 自动完成
if command -v kubectl &> /dev/null; then
    echo "⚡ 设置 kubectl 自动完成..."
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "source <(kubectl completion zsh)" >> ~/.zshrc
    elif [[ "$SHELL" == *"bash"* ]]; then
        echo "source <(kubectl completion bash)" >> ~/.bashrc
    fi
fi

# 设置 git 自动完成
if command -v git &> /dev/null; then
    echo "⚡ 设置 git 自动完成..."
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "autoload -Uz compinit && compinit" >> ~/.zshrc
    elif [[ "$SHELL" == *"bash"* ]]; then
        curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
        echo "source ~/.git-completion.bash" >> ~/.bashrc
    fi
fi

# 创建 .env 文件（如果不存在）
if [ ! -f ".env" ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env 2>/dev/null || echo "# 环境变量" > .env
fi

echo "✅ 开发环境设置完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件并添加必要的 API 密钥"
echo "2. 运行 'npm run dev' 或 'python main.py' 启动开发服务器"
echo "3. 运行 'npm test' 或 'pytest' 运行测试"
```

## 基础设施自动化

使用 Terraform 和其他工具自动化基础设施配置。

### .github/workflows/terraform.yml

```yaml
name: Infrastructure Automation

on:
  push:
    branches: [main]
    paths: ['terraform/**']
  pull_request:
    branches: [main]
    paths: ['terraform/**']
  workflow_dispatch:

jobs:
  # Terraform 格式化和验证
  terraform-format:
    name: Terraform Format
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0
      
      - name: Terraform Format
        run: terraform fmt -check
        working-directory: terraform

  # Terraform 安全扫描
  terraform-scan:
    name: Terraform Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 tfsec
        uses: aquasecurity/tfsec-sarif-action@v0.1.0
        with:
          sarif_file: tfsec-results.sarif
      
      - name: 上传 tfsec 结果到 GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: tfsec-results.sarif

  # Terraform 规划
  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    env:
      TF_VAR_environment: staging
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0
      
      - name: 配置 AWS 凭证
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Terraform Init
        run: terraform init
        working-directory: terraform
      
      - name: Terraform Validate
        run: terraform validate
        working-directory: terraform
      
      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        working-directory: terraform
        continue-on-error: true
      
      - name: 保存 Terraform 计划
        uses: actions/upload-artifact@v4
        with:
          name: terraform-plan
          path: terraform/tfplan
      
      - name: 评论 PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const output = `#### Terraform Format and Style 🖌️\`${{ steps.fmt.outcome }}\`
            #### Terraform Initialization ⚙️\`${{ steps.init.outcome }}\`
            #### Terraform Plan 📖\`${{ steps.plan.outcome }}\`
            #### Terraform Validation 🤖\`${{ steps.validate.outcome }}\`
            
            <details><summary>Show Plan</summary>
            
            \`\`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\`\`
            
            </details>
            
            *Pushed by: @${{ github.actor }}, Action: \`${{ github.event_name }}\`*`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

  # Terraform 应用
  terraform-apply:
    name: Terraform Apply
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: [terraform-format, terraform-scan]
    env:
      TF_VAR_environment: production
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0
      
      - name: 配置 AWS 凭证
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Terraform Init
        run: terraform init
        working-directory: terraform
      
      - name: Terraform Apply
        run: terraform apply -auto-approve
        working-directory: terraform
      
      - name: 输出资源信息
        id: output
        run: terraform output -json
        working-directory: terraform
```

### scripts/deploy-infrastructure.py

```python
#!/usr/bin/env python3
"""
基础设施部署自动化脚本

自动化 Terraform 部署、验证和后部署配置。
"""

import subprocess
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import argparse


class InfrastructureDeployer:
    """基础设施部署管理器"""
    
    def __init__(self, environment: str, terraform_dir: str = "terraform"):
        self.environment = environment
        self.terraform_dir = Path(terraform_dir)
        self.state_file = self.terraform_dir / "terraform.tfstate"
        
    def run_terraform(self, command: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """运行 Terraform 命令"""
        cmd = ["terraform", *command]
        print(f"运行: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=self.terraform_dir,
            capture_output=capture_output,
            text=True
        )
        
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            sys.exit(1)
            
        return result
    
    def initialize(self) -> None:
        """初始化 Terraform"""
        print(f"初始化 Terraform ({self.environment})...")
        self.run_terraform(["init", "-upgrade"])
    
    def validate(self) -> None:
        """验证 Terraform 配置"""
        print("验证 Terraform 配置...")
        self.run_terraform(["validate"])
    
    def plan(self, output_file: str = "tfplan") -> str:
        """生成执行计划"""
        print(f"生成执行计划 ({self.environment})...")
        result = self.run_terraform([
            "plan",
            "-out", output_file,
            "-var", f"environment={self.environment}"
        ])
        return result.stdout
    
    def apply(self, plan_file: str = "tfplan") -> Dict[str, Any]:
        """应用 Terraform 配置"""
        print(f"应用 Terraform 配置 ({self.environment})...")
        result = self.run_terraform(["apply", "-auto-approve", plan_file])
        
        # 获取输出
        output_result = self.run_terraform(["output", "-json"])
        return json.loads(output_result.stdout)
    
    def destroy(self) -> None:
        """销毁基础设施"""
        print(f"销毁基础设施 ({self.environment})...")
        self.run_terraform(["destroy", "-auto-approve"])
    
    def get_outputs(self) -> Dict[str, Any]:
        """获取 Terraform 输出"""
        result = self.run_terraform(["output", "-json"])
        return json.loads(result.stdout)
    
    def wait_for_service(self, url: str, timeout: int = 300) -> bool:
        """等待服务可用"""
        import requests
        
        print(f"等待服务 {url} 可用...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ 服务 {url} 已就绪")
                    return True
            except requests.RequestException:
                pass
            
            time.sleep(5)
        
        print(f"❌ 服务 {url} 未在 {timeout} 秒内就绪")
        return False
    
    def post_deploy_config(self, outputs: Dict[str, Any]) -> None:
        """后部署配置"""
        print("运行后部署配置...")
        
        # 配置 Kubernetes
        if "kube_config" in outputs:
            kubeconfig_path = Path.home() / ".kube" / f"config-{self.environment}"
            kubeconfig_path.write_text(outputs["kube_config"]["value"])
            print(f"Kubeconfig 保存到 {kubeconfig_path}")
        
        # 更新 DNS
        if "load_balancer_ip" in outputs:
            self.update_dns(outputs["load_balancer_ip"]["value"])
        
        # 配置监控
        if "monitoring_endpoint" in outputs:
            self.setup_monitoring(outputs["monitoring_endpoint"]["value"])
    
    def update_dns(self, ip: str) -> None:
        """更新 DNS 记录"""
        print(f"更新 DNS 记录: {ip}")
        # 实现 DNS 更新逻辑
    
    def setup_monitoring(self, endpoint: str) -> None:
        """设置监控"""
        print(f"设置监控端点: {endpoint}")
        # 实现监控设置逻辑


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="基础设施部署自动化")
    parser.add_argument("action", choices=["plan", "apply", "destroy"], help="要执行的操作")
    parser.add_argument("--environment", "-e", default="staging", help="环境名称")
    parser.add_argument("--terraform-dir", "-t", default="terraform", help="Terraform 目录")
    
    args = parser.parse_args()
    
    deployer = InfrastructureDeployer(
        environment=args.environment,
        terraform_dir=args.terraform_dir
    )
    
    try:
        deployer.initialize()
        deployer.validate()
        
        if args.action == "plan":
            plan = deployer.plan()
            print(plan)
        
        elif args.action == "apply":
            deployer.plan()
            outputs = deployer.apply()
            
            # 等待服务可用
            if "load_balancer_url" in outputs:
                deployer.wait_for_service(outputs["load_balancer_url"]["value"])
            
            # 后部署配置
            deployer.post_deploy_config(outputs)
            
            print("✅ 部署完成!")
            print(f"输出: {json.dumps(outputs, indent=2)}")
        
        elif args.action == "destroy":
            confirm = input(f"确认销毁 {args.environment} 环境? (yes/no): ")
            if confirm.lower() == "yes":
                deployer.destroy()
                print("✅ 基础设施已销毁")
    
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## 监控和可观测性

自动化监控和告警设置。

### .github/workflows/monitoring.yml

```yaml
name: Monitoring Setup

on:
  push:
    branches: [main]
    paths: ['monitoring/**']
  workflow_dispatch:

jobs:
  deploy-monitoring:
    name: Deploy Monitoring Stack
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 设置 kubectl
        uses: azure/setup-kubectl@v3
      
      - name: 配置 kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
      
      - name: 部署 Prometheus
        run: |
          kubectl apply -f monitoring/prometheus/
          kubectl wait --for=condition=available --timeout=300s \
            deployment/prometheus-server -n monitoring
      
      - name: 部署 Grafana
        run: |
          kubectl apply -f monitoring/grafana/
          kubectl wait --for=condition=available --timeout=300s \
            deployment/grafana -n monitoring
      
      - name: 配置 Grafana 数据源
        run: |
          kubectl apply -f monitoring/grafana/datasources/
      
      - name: 导入 Grafana 仪表板
        run: |
          kubectl apply -f monitoring/grafana/dashboards/
      
      - name: 部署 Alertmanager
        run: |
          kubectl apply -f monitoring/alertmanager/
      
      - name: 部署 Node Exporter
        run: |
          kubectl apply -f monitoring/node-exporter/
      
      - name: 验证监控堆栈
        run: |
          kubectl get pods -n monitoring
          kubectl get services -n monitoring
```

### monitoring/dashboards/application-dashboard.json

```json
{
  "dashboard": {
    "title": "应用程序监控",
    "panels": [
      {
        "title": "请求率",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "错误率",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx 错误"
          }
        ]
      },
      {
        "title": "延迟",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P95 延迟"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "P99 延迟"
          }
        ]
      },
      {
        "title": "CPU 使用率",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total[5m])",
            "legendFormat": "{{instance}}"
          }
        ]
      },
      {
        "title": "内存使用率",
        "type": "graph",
        "targets": [
          {
            "expr": "process_resident_memory_bytes",
            "legendFormat": "{{instance}}"
          }
        ]
      }
    ]
  }
}
```

## 文档生成

自动化文档生成和更新。

### .github/workflows/docs.yml

```yaml
name: Documentation

on:
  push:
    branches: [main]
    paths: ['**.md', 'docs/**']
  workflow_dispatch:

jobs:
  generate-docs:
    name: Generate Documentation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: 安装依赖
        run: |
          pip install mkdocs mkdocs-material mkdocs-gen-files
      
      - name: 生成 API 文档
        run: |
          mkdocs gen-files
          mkdocs build
      
      - name: 部署到 GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## 安全扫描

自动化安全扫描和合规检查。

### .github/workflows/security.yml

```yaml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 6 * * 1'  # 每周一早上 6 点运行
  workflow_dispatch:

jobs:
  # 依赖扫描
  dependency-scan:
    name: Dependency Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
      
      - name: 运行 npm audit
        run: npm audit --audit-level=high
        continue-on-error: true

  # 静态分析
  static-analysis:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript, python
      
      - name: 执行 CodeQL 分析
        uses: github/codeql-action/analyze@v3

  # 容器扫描
  container-scan:
    name: Container Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 构建测试镜像
        run: docker build -t test-image .
      
      - name: 运行 Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: test-image
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  # 密钥扫描
  secret-scan:
    name: Secret Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 运行 Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # 许可证合规
  license-compliance:
    name: License Compliance
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
      
      - name: 运行 FOSSA
        uses: fossas/fossa-action@v1
        with:
          api-key: ${{ secrets.FOSSA_API_KEY }}
```

## 依赖更新

自动化依赖更新和管理。

### .github/workflows/dependencies.yml

```yaml
name: Dependency Updates

on:
  schedule:
    - cron: '0 6 * * 1'  # 每周一早上 6 点运行
  workflow_dispatch:

jobs:
  update-dependencies:
    name: Update Dependencies
    runs-on: ubuntu-latest
    steps:
      - name: Checkout代码
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 设置 Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: 运行 Renovate
        uses: renovatebot/github-action@v40.0.6
        with:
          configurationFile: .github/renovate.json
          token: ${{ secrets.RENOVATE_TOKEN }}
```

### .github/renovate.json

```json
{
  "extends": [
    "config:base",
    ":dependencyDashboard",
    ":semanticCommits",
    ":automergeDigest",
    ":automergePatch",
    ":automergeBranchPush",
    ":rebaseStalePrs",
    ":prHourlyLimitNone",
    ":prConcurrentLimitNone"
  ],
  "labels": ["dependencies", "renovate"],
  "assignees": ["@maintainer-team"],
  "reviewers": ["@reviewer-team"],
  "timezone": "Asia/Shanghai",
  "schedule": ["every weekday"],
  "commitMessagePrefix": "chore(deps): ",
  "commitMessageAction": "更新",
  "commitMessageTopic": "{{depName}}",
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "assignees": []
  },
  "packageRules": [
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^eslint", "^prettier"],
      "automerge": true
    },
    {
      "matchDepTypes": ["devDependencies"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false
    }
  ],
  "lockFileMaintenance": {
    "enabled": true,
    "schedule": ["before 3am on Monday"]
  }
}
```

## 工作流编排

使用 TypeScript 编排复杂工作流。

### scripts/workflow-orchestrator.ts

```typescript
/**
 * 工作流编排器
 * 
 * 编排和自动化复杂的多步骤工作流
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);


interface WorkflowStep {
  name: string;
  command: string;
  args?: string[];
  cwd?: string;
  env?: Record<string, string>;
  continueOnError?: boolean;
  timeout?: number;
}


interface WorkflowConfig {
  name: string;
  description: string;
  steps: WorkflowStep[];
  onFailure?: WorkflowStep[];
  onSuccess?: WorkflowStep[];
}


interface WorkflowResult {
  success: boolean;
  steps: Map<string, boolean>;
  duration: number;
  error?: Error;
}


class WorkflowOrchestrator {
  private workflows: Map<string, WorkflowConfig> = new Map();

  /**
   * 注册工作流
   */
  registerWorkflow(config: WorkflowConfig): void {
    this.workflows.set(config.name, config);
  }

  /**
   * 从文件加载工作流
   */
  async loadWorkflow(filePath: string): Promise<void> {
    const content = await fs.readFile(filePath, 'utf-8');
    const config: WorkflowConfig = JSON.parse(content);
    this.registerWorkflow(config);
  }

  /**
   * 加载目录中的所有工作流
   */
  async loadWorkflowsFromDir(dir: string): Promise<void> {
    const files = await fs.readdir(dir);
    const jsonFiles = files.filter(f => f.endsWith('.json'));

    for (const file of jsonFiles) {
      await this.loadWorkflow(path.join(dir, file));
    }
  }

  /**
   * 执行工作流
   */
  async executeWorkflow(name: string, context?: Record<string, string>): Promise<WorkflowResult> {
    const workflow = this.workflows.get(name);
    if (!workflow) {
      throw new Error(`工作流 ${name} 未找到`);
    }

    const startTime = Date.now();
    const steps = new Map<string, boolean>();
    let lastError: Error | undefined;

    console.log(`🚀 开始工作流: ${workflow.name}`);
    console.log(`📝 ${workflow.description}`);

    try {
      // 执行主要步骤
      for (const step of workflow.steps) {
        const success = await this.executeStep(step, context);
        steps.set(step.name, success);

        if (!success && !step.continueOnError) {
          throw new Error(`步骤 ${step.name} 失败`);
        }
      }

      // 执行成功回调
      if (workflow.onSuccess) {
        console.log('✅ 执行成功回调...');
        for (const step of workflow.onSuccess) {
          await this.executeStep(step, context);
        }
      }

      const duration = Date.now() - startTime;
      console.log(`✅ 工作流 ${name} 完成 (${duration}ms)`);

      return {
        success: true,
        steps,
        duration
      };

    } catch (error) {
      lastError = error as Error;
      console.error(`❌ 工作流 ${name} 失败:`, error);

      // 执行失败回调
      if (workflow.onFailure) {
        console.log('🔧 执行失败回调...');
        for (const step of workflow.onFailure) {
          await this.executeStep(step, context);
        }
      }

      const duration = Date.now() - startTime;
      return {
        success: false,
        steps,
        duration,
        error: lastError
      };
    }
  }

  /**
   * 执行单个步骤
   */
  private async executeStep(step: WorkflowStep, context?: Record<string, string>): Promise<boolean> {
    console.log(`▶️  执行步骤: ${step.name}`);

    try {
      const startTime = Date.now();
      
      // 替换上下文变量
      const command = this.interpolateContext(step.command, context);
      const args = step.args?.map(arg => this.interpolateContext(arg, context)) || [];

      const cwd = step.cwd || process.cwd();
      const env = { ...process.env, ...step.env, ...context };

      const execOptions = {
        cwd,
        env: env as NodeJS.ProcessEnv,
        timeout: step.timeout || 300000
      };

      const fullCommand = args.length > 0 ? `${command} ${args.join(' ')}` : command;
      const { stdout, stderr } = await execAsync(fullCommand, execOptions);

      const duration = Date.now() - startTime;
      console.log(`✅ 步骤 ${step.name} 完成 (${duration}ms)`);
      
      if (stdout) console.log(`输出: ${stdout}`);
      if (stderr) console.error(`错误: ${stderr}`);

      return true;

    } catch (error) {
      console.error(`❌ 步骤 ${step.name} 失败:`, error);
      return false;
    }
  }

  /**
   * 替换上下文变量
   */
  private interpolateContext(text: string, context?: Record<string, string>): string {
    if (!context) return text;

    return text.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return context[key] || match;
    });
  }

  /**
   * 列出所有工作流
   */
  listWorkflows(): string[] {
    return Array.from(this.workflows.keys());
  }

  /**
   * 获取工作流配置
   */
  getWorkflow(name: string): WorkflowConfig | undefined {
    return this.workflows.get(name);
  }
}


// 示例工作流配置
const deploymentWorkflow: WorkflowConfig = {
  name: 'deploy-application',
  description: '部署应用程序到生产环境',
  steps: [
    {
      name: '运行测试',
      command: 'npm',
      args: ['test'],
      continueOnError: false
    },
    {
      name: '构建应用',
      command: 'npm',
      args: ['run', 'build'],
      continueOnError: false
    },
    {
      name: '构建 Docker 镜像',
      command: 'docker',
      args: ['build', '-t', 'app:latest', '.'],
      continueOnError: false
    },
    {
      name: '推送镜像',
      command: 'docker',
      args: ['push', 'app:latest'],
      continueOnError: false,
      env: {
        DOCKER_REGISTRY: process.env.DOCKER_REGISTRY || ''
      }
    },
    {
      name: '部署到 Kubernetes',
      command: 'kubectl',
      args: ['apply', '-f', 'k8s/'],
      continueOnError: false
    },
    {
      name: '验证部署',
      command: 'kubectl',
      args: ['rollout', 'status', 'deployment/app'],
      continueOnError: false,
      timeout: 600000
    }
  ],
  onSuccess: [
    {
      name: '运行健康检查',
      command: 'npm',
      args: ['run', 'health-check']
    },
    {
      name: '发送成功通知',
      command: 'node',
      args: ['scripts/notify.js', 'success']
    }
  ],
  onFailure: [
    {
      name: '回滚部署',
      command: 'kubectl',
      args: ['rollback', 'deployment/app']
    },
    {
      name: '发送失败通知',
      command: 'node',
      args: ['scripts/notify.js', 'failure']
    }
  ]
};


// 使用示例
async function main() {
  const orchestrator = new WorkflowOrchestrator();

  // 注册工作流
  orchestrator.registerWorkflow(deploymentWorkflow);

  // 从文件加载工作流
  await orchestrator.loadWorkflowsFromDir('./workflows');

  // 执行工作流
  const context = {
    BRANCH: 'main',
    VERSION: '1.0.0',
    ENVIRONMENT: 'production'
  };

  const result = await orchestrator.executeWorkflow('deploy-application', context);

  if (result.success) {
    console.log('✅ 工作流执行成功');
    console.log(`步骤: ${Array.from(result.steps.entries()).map(([k, v]) => `${k}: ${v}`).join(', ')}`);
    console.log(`总耗时: ${result.duration}ms`);
  } else {
    console.error('❌ 工作流执行失败');
    console.error(`错误: ${result.error?.message}`);
    process.exit(1);
  }
}


if (require.main === module) {
  main().catch(console.error);
}

export { WorkflowOrchestrator, WorkflowConfig, WorkflowStep, WorkflowResult };
```

## 最佳实践

1. **工作流设计**
   - 保持工作流简单和模块化
   - 使用可重用的 action 和模板
   - 优化缓存策略以减少构建时间
   - 实现适当的错误处理和重试逻辑

2. **安全性**
   - 使用 GitHub Secrets 存储敏感信息
   - 实施最小权限原则
   - 定期扫描依赖项和容器镜像
   - 使用签名的提交和标签

3. **监控和告警**
   - 为关键工作流配置通知
   - 跟踪工作流执行时间
   - 设置 SLA 和 SLO
   - 实现自动回滚机制

4. **维护**
   - 定期更新依赖项
   - 定期审查和优化工作流
   - 保持文档更新
   - 使用语义化版本控制

## 相关技能

- [cloud-architect](../agents/cloud-architect.md) - 云架构设计
- [devops-troubleshooter](../agents/devops-troubleshooter.md) - DevOps 故障排查
- [kubernetes-architect](../agents/kubernetes-architect.md) - Kubernetes 架构
- [terraform-specialist](../agents/terraform-specialist.md) - Terraform 专才
