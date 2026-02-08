---
name: stripe-integration
description: 实现 Stripe 支付处理，提供稳健且符合 PCI 标准的支付流程，包括结账、订阅和 Webhook。适用于集成 Stripe 支付、构建订阅系统或实现安全结账流程。
---

# Stripe 集成

精通 Stripe 支付处理集成，提供稳健且符合 PCI 标准的支付流程，包括结账、订阅、Webhook 和退款。

## 何时使用此技能

- 在 Web/移动应用中实现支付处理
- 设置订阅计费系统
- 处理一次性付款和定期扣款
- 处理退款和争议
- 管理客户支付方式
- 为欧洲支付实现 SCA（强客户认证）
- 使用 Stripe Connect 构建市场支付流程

## 核心概念

### 1. 支付流程

**结账会话（托管）**

- Stripe 托管的支付页面
- 最小的 PCI 合规负担
- 最快的实现方式
- 支持一次性付款和定期付款

**支付意图（自定义 UI）**

- 完全控制支付 UI
- 需要使用 Stripe.js 以符合 PCI 要求
- 实现较为复杂
- 更好的自定义选项

**设置意图（保存支付方式）**

- 在不扣款的情况下收集支付方式
- 用于订阅和未来的支付
- 需要客户确认

### 2. Webhook

**关键事件：**

- `payment_intent.succeeded`: 支付完成
- `payment_intent.payment_failed`: 支付失败
- `customer.subscription.updated`: 订阅变更
- `customer.subscription.deleted`: 订阅取消
- `charge.refunded`: 退款处理完成
- `invoice.payment_succeeded`: 订阅支付成功

### 3. 订阅

**组件：**

- **产品（Product）**: 你销售的内容
- **价格（Price）**: 金额和计费周期
- **订阅（Subscription）**: 客户的定期付款
- **发票（Invoice）**: 每个计费周期生成

### 4. 客户管理

- 创建和管理客户记录
- 存储多种支付方式
- 跟踪客户元数据
- 管理账单详情

## 快速开始

```python
import stripe

stripe.api_key = "sk_test_..."

# 创建结账会话
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # $20.00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel',
)

# 将用户重定向到 session.url
print(session.url)
```

## 支付实现模式

### 模式 1：一次性付款（托管结账）

```python
def create_checkout_session(amount, currency='usd'):
    """创建一次性付款的结账会话。"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Purchase',
                        'images': ['https://example.com/product.jpg'],
                    },
                    'unit_amount': amount,  # 金额（单位：分）
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={
                'order_id': 'order_123',
                'user_id': 'user_456'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # 处理错误
        print(f"Stripe error: {e.user_message}")
        raise
```

### 模式 2：自定义支付意图流程

```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """创建用于自定义结账 UI 的支付意图。"""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # 发送到前端

# 前端（JavaScript）
"""
const stripe = Stripe('pk_test_...');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

const {error, paymentIntent} = await stripe.confirmCardPayment(
    clientSecret,
    {
        payment_method: {
            card: cardElement,
            billing_details: {
                name: 'Customer Name'
            }
        }
    }
);

if (error) {
    // 处理错误
} else if (paymentIntent.status === 'succeeded') {
    // 支付成功
}
"""
```

### 模式 3：订阅创建

```python
def create_subscription(customer_id, price_id):
    """为客户创建订阅。"""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### 模式 4：客户门户

```python
def create_customer_portal_session(customer_id):
    """创建门户会话，供客户管理订阅。"""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='https://yourdomain.com/account',
    )
    return session.url  # 将客户重定向到此 URL
```

## Webhook 处理

### 安全的 Webhook 端点

```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = 'whsec_...'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # 无效的负载
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # 无效的签名
        return 'Invalid signature', 400

    # 处理事件
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200

def handle_successful_payment(payment_intent):
    """处理成功的支付。"""
    customer_id = payment_intent.get('customer')
    amount = payment_intent['amount']
    metadata = payment_intent.get('metadata', {})

    # 更新数据库
    # 发送确认邮件
    # 履行订单
    print(f"Payment succeeded: {payment_intent['id']}")

def handle_failed_payment(payment_intent):
    """处理失败的支付。"""
    error = payment_intent.get('last_payment_error', {})
    print(f"Payment failed: {error.get('message')}")
    # 通知客户
    # 更新订单状态

def handle_subscription_canceled(subscription):
    """处理订阅取消。"""
    customer_id = subscription['customer']
    # 更新用户访问权限
    # 发送取消邮件
    print(f"Subscription canceled: {subscription['id']}")
```

### Webhook 最佳实践

```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """手动验证 webhook 签名。"""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """确保 webhook 仅处理一次。"""
    # 检查事件是否已处理
    if is_event_processed(event_id):
        return

    # 处理事件
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe 将重试失败的 webhook
        raise
```

## 客户管理

```python
def create_customer(email, name, payment_method_id=None):
    """创建 Stripe 客户。"""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        } if payment_method_id else None,
        metadata={
            'user_id': '12345'
        }
    )
    return customer

def attach_payment_method(customer_id, payment_method_id):
    """将支付方式关联到客户。"""
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # 设置为默认
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def list_customer_payment_methods(customer_id):
    """列出客户的所有支付方式。"""
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    return payment_methods.data
```

## 退款处理

```python
def create_refund(payment_intent_id, amount=None, reason=None):
    """创建退款。"""
    refund_params = {
        'payment_intent': payment_intent_id
    }

    if amount:
        refund_params['amount'] = amount  # 部分退款

    if reason:
        refund_params['reason'] = reason  # 'duplicate', 'fraudulent', 'requested_by_customer'

    refund = stripe.Refund.create(**refund_params)
    return refund

def handle_dispute(charge_id, evidence):
    """使用证据更新争议。"""
    stripe.Dispute.modify(
        charge_id,
        evidence={
            'customer_name': evidence.get('customer_name'),
            'customer_email_address': evidence.get('customer_email'),
            'shipping_documentation': evidence.get('shipping_proof'),
            'customer_communication': evidence.get('communication'),
        }
    )
```

## 测试

```python
# 使用测试模式密钥
stripe.api_key = "sk_test_..."

# 测试卡号
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995'
}

def test_payment_flow():
    """测试完整的支付流程。"""
    # 创建测试客户
    customer = stripe.Customer.create(
        email="test@example.com"
    )

    # 创建支付意图
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        customer=customer.id,
        payment_method_types=['card']
    )

    # 使用测试卡确认
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'  # 测试支付方式
    )

    assert confirmed.status == 'succeeded'
```

## 资源

- **references/checkout-flows.md**: 详细的结账实现
- **references/webhook-handling.md**: Webhook 安全和处理
- **references/subscription-management.md**: 订阅生命周期
- **references/customer-management.md**: 客户和支付方式处理
- **references/invoice-generation.md**: 开票和计费
- **assets/stripe-client.py**: 生产就绪的 Stripe 客户端封装
- **assets/webhook-handler.py**: 完整的 webhook 处理器
- **assets/checkout-config.json**: 结账配置模板

## 最佳实践

1. **始终使用 Webhook**: 不要仅依赖客户端确认
2. **幂等性**: 以幂等方式处理 webhook 事件
3. **错误处理**: 优雅地处理所有 Stripe 错误
4. **测试模式**: 在生产前使用测试密钥进行充分测试
5. **元数据**: 使用元数据将 Stripe 对象关联到你的数据库
6. **监控**: 跟踪支付成功率和错误
7. **PCI 合规**: 永远不要在服务器上处理原始卡数据
8. **SCA 就绪**: 为欧洲支付实现 3D Secure

## 常见陷阱

- **未验证 Webhook**: 始终验证 webhook 签名
- **遗漏 Webhook 事件**: 处理所有相关的 webhook 事件
- **硬编码金额**: 使用分/最小货币单位
- **无重试逻辑**: 为 API 调用实现重试
- **忽略测试模式**: 使用测试卡测试所有边缘情况
