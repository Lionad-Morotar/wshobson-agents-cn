---
name: paypal-integration
description: 集成 PayPal 支付处理，支持快速结账、订阅和退款管理。在实现 PayPal 支付、处理在线交易或构建电子商务结账流程时使用。
---

# PayPal 集成

掌握 PayPal 支付集成，包括快速结账、IPN 处理、定期计费和退款工作流。

## 何时使用此技能

- 集成 PayPal 作为支付选项
- 实现快速结账流程
- 使用 PayPal 设置定期计费
- 处理退款和支付争议
- 处理 PayPal webhook（IPN）
- 支持国际支付
- 实现 PayPal 订阅

## 核心概念

### 1. 支付产品

**PayPal Checkout（PayPal 结账）**

- 一次性支付
- 快速结账体验
- 访客和 PayPal 账户支付

**PayPal Subscriptions（PayPal 订阅）**

- 定期计费
- 订阅计划
- 自动续费

**PayPal Payouts（PayPal 付款）**

- 向多个收款人付款
- 市场和平台支付

### 2. 集成方法

**客户端（JavaScript SDK）**

- 智能支付按钮
- 托管支付流程
- 最少的后端代码

**服务端（REST API）**

- 完全控制支付流程
- 自定义结账 UI
- 高级功能

### 3. IPN（即时支付通知）

- 类似 webhook 的支付通知
- 异步支付更新
- 需要验证

## 快速开始

```javascript
// 前端 - PayPal 智能按钮
<div id="paypal-button-container"></div>

<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '25.00'
          }
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        // 支付成功
        console.log('Transaction completed by ' + details.payer.name.given_name);

        // 发送到后端进行验证
        fetch('/api/paypal/capture', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({orderID: data.orderID})
        });
      });
    }
  }).render('#paypal-button-container');
</script>
```

```python
# 后端 - 验证并捕获订单
from paypalrestsdk import Payment
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # 或 "live"
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

def capture_paypal_order(order_id):
    """捕获 PayPal 订单。"""
    payment = Payment.find(order_id)

    if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
        # 支付成功
        return {
            'status': 'success',
            'transaction_id': payment.id,
            'amount': payment.transactions[0].amount.total
        }
    else:
        # 支付失败
        return {
            'status': 'failed',
            'error': payment.error
        }
```

## 快速结账实现

### 服务端订单创建

```python
import requests
import json

class PayPalClient:
    def __init__(self, client_id, client_secret, mode='sandbox'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """获取 OAuth 访问令牌。"""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}

        response = requests.post(
            url,
            headers=headers,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret)
        )

        return response.json()['access_token']

    def create_order(self, amount, currency='USD'):
        """创建 PayPal 订单。"""
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                }
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def capture_order(self, order_id):
        """捕获订单的支付。"""
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(url, headers=headers)
        return response.json()

    def get_order_details(self, order_id):
        """获取订单详情。"""
        url = f"{self.base_url}/v2/checkout/orders/{order_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        return response.json()
```

## IPN（即时支付通知）处理

### IPN 验证和处理

```python
from flask import Flask, request
import requests
from urllib.parse import parse_qs

app = Flask(__name__)

@app.route('/ipn', methods=['POST'])
def handle_ipn():
    """处理 PayPal IPN 通知。"""
    # 获取 IPN 消息
    ipn_data = request.form.to_dict()

    # 与 PayPal 验证 IPN
    if not verify_ipn(ipn_data):
        return 'IPN verification failed', 400

    # 根据交易类型处理 IPN
    payment_status = ipn_data.get('payment_status')
    txn_type = ipn_data.get('txn_type')

    if payment_status == 'Completed':
        handle_payment_completed(ipn_data)
    elif payment_status == 'Refunded':
        handle_refund(ipn_data)
    elif payment_status == 'Reversed':
        handle_chargeback(ipn_data)

    return 'IPN processed', 200

def verify_ipn(ipn_data):
    """验证 IPN 消息的真实性。"""
    # 添加 'cmd' 参数
    verify_data = ipn_data.copy()
    verify_data['cmd'] = '_notify-validate'

    # 发送回 PayPal 进行验证
    paypal_url = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'  # 或生产环境 URL

    response = requests.post(paypal_url, data=verify_data)

    return response.text == 'VERIFIED'

def handle_payment_completed(ipn_data):
    """处理完成的支付。"""
    txn_id = ipn_data.get('txn_id')
    payer_email = ipn_data.get('payer_email')
    mc_gross = ipn_data.get('mc_gross')
    item_name = ipn_data.get('item_name')

    # 检查是否已处理（防止重复）
    if is_transaction_processed(txn_id):
        return

    # 更新数据库
    # 发送确认邮件
    # 履行订单
    print(f"Payment completed: {txn_id}, Amount: ${mc_gross}")

def handle_refund(ipn_data):
    """处理退款。"""
    parent_txn_id = ipn_data.get('parent_txn_id')
    mc_gross = ipn_data.get('mc_gross')

    # 在系统中处理退款
    print(f"Refund processed: {parent_txn_id}, Amount: ${mc_gross}")

def handle_chargeback(ipn_data):
    """处理支付撤销/拒付。"""
    txn_id = ipn_data.get('txn_id')
    reason_code = ipn_data.get('reason_code')

    # 处理拒付
    print(f"Chargeback: {txn_id}, Reason: {reason_code}")
```

## 订阅/定期计费

### 创建订阅计划

```python
def create_subscription_plan(name, amount, interval='MONTH'):
    """创建订阅计划。"""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v1/billing/plans"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {
        "product_id": "PRODUCT_ID",  # 首先创建产品
        "name": name,
        "billing_cycles": [{
            "frequency": {
                "interval_unit": interval,
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 1,
            "total_cycles": 0,  # 无限
            "pricing_scheme": {
                "fixed_price": {
                    "value": str(amount),
                    "currency_code": "USD"
                }
            }
        }],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def create_subscription(plan_id, subscriber_email):
    """为客户创建订阅。"""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v1/billing/subscriptions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {
        "plan_id": plan_id,
        "subscriber": {
            "email_address": subscriber_email
        },
        "application_context": {
            "return_url": "https://yourdomain.com/subscription/success",
            "cancel_url": "https://yourdomain.com/subscription/cancel"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    subscription = response.json()

    # 获取批准 URL
    for link in subscription.get('links', []):
        if link['rel'] == 'approve':
            return {
                'subscription_id': subscription['id'],
                'approval_url': link['href']
            }
```

## 退款工作流

```python
def create_refund(capture_id, amount=None, note=None):
    """为已捕获的支付创建退款。"""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v2/payments/captures/{capture_id}/refund"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.access_token}"
    }

    payload = {}
    if amount:
        payload["amount"] = {
            "value": str(amount),
            "currency_code": "USD"
        }

    if note:
        payload["note_to_payer"] = note

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def get_refund_details(refund_id):
    """获取退款详情。"""
    client = PayPalClient(CLIENT_ID, CLIENT_SECRET)

    url = f"{client.base_url}/v2/payments/refunds/{refund_id}"
    headers = {
        "Authorization": f"Bearer {client.access_token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

## 错误处理

```python
class PayPalError(Exception):
    """自定义 PayPal 错误。"""
    pass

def handle_paypal_api_call(api_function):
    """带有错误处理的 PayPal API 调用包装器。"""
    try:
        result = api_function()
        return result
    except requests.exceptions.RequestException as e:
        # 网络错误
        raise PayPalError(f"Network error: {str(e)}")
    except Exception as e:
        # 其他错误
        raise PayPalError(f"PayPal API error: {str(e)}")

# 使用
try:
    order = handle_paypal_api_call(lambda: client.create_order(25.00))
except PayPalError as e:
    # 适当处理错误
    log_error(e)
```

## 测试

```python
# 使用沙盒凭据
SANDBOX_CLIENT_ID = "..."
SANDBOX_SECRET = "..."

# 测试账户
# 在 developer.paypal.com 创建测试买家和卖家账户

def test_payment_flow():
    """测试完整的支付流程。"""
    client = PayPalClient(SANDBOX_CLIENT_ID, SANDBOX_SECRET, mode='sandbox')

    # 创建订单
    order = client.create_order(10.00)
    assert 'id' in order

    # 获取批准 URL
    approval_url = next((link['href'] for link in order['links'] if link['rel'] == 'approve'), None)
    assert approval_url is not None

    # 批准后（使用测试账户手动步骤）
    # 捕获订单
    # captured = client.capture_order(order['id'])
    # assert captured['status'] == 'COMPLETED'
```

## 资源

- **references/express-checkout.md**: 快速结账实现指南
- **references/ipn-handling.md**: IPN 验证和处理
- **references/refund-workflows.md**: 退款处理模式
- **references/billing-agreements.md**: 定期计费设置
- **assets/paypal-client.py**: 生产环境 PayPal 客户端
- **assets/ipn-processor.py**: IPN webhook 处理器
- **assets/recurring-billing.py**: 订阅管理

## 最佳实践

1. **始终验证 IPN**: 不要在没有验证的情况下信任 IPN
2. **幂等处理**: 处理重复的 IPN 通知
3. **错误处理**: 实现健壮的错误处理
4. **日志记录**: 记录所有交易和错误
5. **彻底测试**: 广泛使用沙盒
6. **Webhook 备份**: 不要仅依赖客户端回调
7. **货币处理**: 始终明确指定货币

## 常见陷阱

- **不验证 IPN**: 接受未经验证的 IPN
- **重复处理**: 不检查重复交易
- **错误环境**: 混合沙盒和生产环境 URL/凭据
- **缺少 Webhook**: 不处理所有支付状态
- **硬编码值**: 不针对不同环境进行配置
