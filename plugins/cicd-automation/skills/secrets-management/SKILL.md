---
name: secrets-management
description: 使用 Vault、AWS Secrets Manager 或原生平台解决方案为 CI/CD 流水线实施安全的密钥管理。用于处理敏感凭证、轮换密钥或保护 CI/CD 环境。
---

# 密钥管理

使用 Vault、AWS Secrets Manager 和其他工具为 CI/CD 流水线实施安全密钥管理实践。

## 目的

在 CI/CD 流水线中实施安全的密钥管理,而无需硬编码敏感信息。

## 何时使用

- 存储 API 密钥和凭证
- 管理数据库密码
- 处理 TLS 证书
- 自动轮换密钥
- 实施最小权限访问

## 密钥管理工具

### HashiCorp Vault

- 集中式密钥管理
- 动态密钥生成
- 密钥轮换
- 审计日志
- 细粒度访问控制

### AWS Secrets Manager

- AWS 原生解决方案
- 自动轮换
- 与 RDS 集成
- CloudFormation 支持

### Azure Key Vault

- Azure 原生解决方案
- HSM 支持的密钥
- 证书管理
- RBAC 集成

### Google Secret Manager

- GCP 原生解决方案
- 版本控制
- IAM 集成

## HashiCorp Vault 集成

### 设置 Vault

```bash
# 启动 Vault 开发服务器
vault server -dev

# 设置环境变量
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# 启用密钥引擎
vault secrets enable -path=secret kv-v2

# 存储密钥
vault kv put secret/database/config username=admin password=secret
```

### GitHub Actions 与 Vault 集成

```yaml
name: 使用 Vault 密钥部署

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 从 Vault 导入密钥
        uses: hashicorp/vault-action@v2
        with:
          url: https://vault.example.com:8200
          token: ${{ secrets.VAULT_TOKEN }}
          secrets: |
            secret/data/database username | DB_USERNAME ;
            secret/data/database password | DB_PASSWORD ;
            secret/data/api key | API_KEY

      - name: 使用密钥
        run: |
          echo "以 $DB_USERNAME 身份连接数据库"
          # 使用 $DB_PASSWORD, $API_KEY
```

### GitLab CI 与 Vault 集成

```yaml
deploy:
  image: vault:latest
  before_script:
    - export VAULT_ADDR=https://vault.example.com:8200
    - export VAULT_TOKEN=$VAULT_TOKEN
    - apk add curl jq
  script:
    - |
      DB_PASSWORD=$(vault kv get -field=password secret/database/config)
      API_KEY=$(vault kv get -field=key secret/api/credentials)
      echo "正在使用密钥部署..."
      # 使用 $DB_PASSWORD, $API_KEY
```

**参考:** 参见 `references/vault-setup.md`

## AWS Secrets Manager

### 存储密钥

```bash
aws secretsmanager create-secret \
  --name production/database/password \
  --secret-string "super-secret-password"
```

### 在 GitHub Actions 中检索

```yaml
- name: 配置 AWS 凭证
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-west-2

- name: 从 AWS 获取密钥
  run: |
    SECRET=$(aws secretsmanager get-secret-value \
      --secret-id production/database/password \
      --query SecretString \
      --output text)
    echo "::add-mask::$SECRET"
    echo "DB_PASSWORD=$SECRET" >> $GITHUB_ENV

- name: 使用密钥
  run: |
    # 使用 $DB_PASSWORD
    ./deploy.sh
```

### Terraform 与 AWS Secrets Manager

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/database/password"
}

resource "aws_db_instance" "main" {
  allocated_storage    = 100
  engine              = "postgres"
  instance_class      = "db.t3.large"
  username            = "admin"
  password            = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

## GitHub 密钥

### 组织/仓库密钥

```yaml
- name: 使用 GitHub 密钥
  run: |
    echo "API 密钥: ${{ secrets.API_KEY }}"
    echo "数据库 URL: ${{ secrets.DATABASE_URL }}"
```

### 环境密钥

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: production
  steps:
    - name: 部署
      run: |
        echo "使用 ${{ secrets.PROD_API_KEY }} 部署"
```

**参考:** 参见 `references/github-secrets.md`

## GitLab CI/CD 变量

### 项目变量

```yaml
deploy:
  script:
    - echo "使用 $API_KEY 部署"
    - echo "数据库: $DATABASE_URL"
```

### 受保护和掩码变量

- 受保护: 仅在受保护分支中可用
- 掩码: 在任务日志中隐藏
- 文件类型: 存储为文件

## 最佳实践

1. **绝不将密钥提交到 Git**
2. **每个环境使用不同的密钥**
3. **定期轮换密钥**
4. **实施最小权限访问**
5. **启用审计日志**
6. **使用密钥扫描** (GitGuardian, TruffleHog)
7. **在日志中掩码密钥**
8. **静态加密密钥**
9. **尽可能使用短期令牌**
10. **记录密钥要求**

## 密钥轮换

### 使用 AWS 自动轮换

```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')

    # 获取当前密钥
    response = client.get_secret_value(SecretId='my-secret')
    current_secret = json.loads(response['SecretString'])

    # 生成新密码
    new_password = generate_strong_password()

    # 更新数据库密码
    update_database_password(new_password)

    # 更新密钥
    client.put_secret_value(
        SecretId='my-secret',
        SecretString=json.dumps({
            'username': current_secret['username'],
            'password': new_password
        })
    )

    return {'statusCode': 200}
```

### 手动轮换流程

1. 生成新密钥
2. 更新密钥存储中的密钥
3. 更新应用程序以使用新密钥
4. 验证功能
5. 撤销旧密钥

## External Secrets Operator

### Kubernetes 集成

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: database/config
        property: username
    - secretKey: password
      remoteRef:
        key: database/config
        property: password
```

## 密钥扫描

### Pre-commit 钩子

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 使用 TruffleHog 检查密钥
docker run --rm -v "$(pwd):/repo" \
  trufflesecurity/trufflehog:latest \
  filesystem --directory=/repo

if [ $? -ne 0 ]; then
  echo "❌ 检测到密钥! 提交被阻止。"
  exit 1
fi
```

### CI/CD 密钥扫描

```yaml
secret-scan:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem .
  allow_failure: false
```

## 参考文件

- `references/vault-setup.md` - HashiCorp Vault 配置
- `references/github-secrets.md` - GitHub Secrets 最佳实践

## 相关技能

- `github-actions-templates` - GitHub Actions 集成
- `gitlab-ci-patterns` - GitLab CI 集成
- `deployment-pipeline-design` - 流水线架构
