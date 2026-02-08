---
name: hybrid-cloud-networking
description: 使用 VPN 和专线连接配置本地基础设施与云平台之间的安全、高性能连接。在构建混合云架构、将数据中心连接到云或实现安全的跨场所网络时使用。
---

# 混合云网络

使用 VPN、Direct Connect 和 ExpressRoute 配置本地环境与云环境之间的安全、高性能连接。

## 目的

在本地数据中心与云提供商(AWS、Azure、GCP)之间建立安全、可靠的网络连接。

## 适用场景

混合云网络技能在以下情况下适用：

- **混合云架构**：将本地基础设施扩展到云端
- **数据中心迁移**：在迁移过程中连接本地和云端资源
- **灾难恢复**：使用云端作为本地工作负载的恢复站点
- **云爆发**：峰值期间将工作负载扩展到云端
- **多云策略**：跨多个云提供商分布资源

## 约束和指导原则

使用此技能时，遵循这些约束和指导原则：

- **加密**：所有连接必须使用强加密(IPsec、TLS)
- **冗余**：为连接部署冗余隧道和网关
- **监控**：为连接指标设置监控和警报
- **成本优化**：根据成本考虑选择 VPN 与专线
- **安全**：实现正确的防火墙规则和安全组
- **性能**：根据带宽需求选择连接类型

## 工作流程

### 混合云连接计划

规划混合云连接时：

1. **评估需求**：确定带宽、延迟和可用性要求
2. **选择连接类型**：在 VPN 与专线之间选择
3. **设计网络拓扑**：规划 IP 地址、路由和防火墙
4. **规划冗余**：设计冗余以实现高可用性
5. **估算成本**：估算数据传输和连接成本
6. **实施监控**：规划连接健康和性能的监控

### VPN 连接

建立 VPN 连接：

1. **创建虚拟网关**：
   ```hcl
   # AWS Site-to-Site VPN
   resource "aws_vpn_gateway" "main" {
     vpc_id = aws_vpc.main.id
     tags = {
       Name = "main-vpn-gateway"
     }
   }

   resource "aws_customer_gateway" "main" {
     bgp_asn    = 65000
     ip_address = "YOUR_ON_PREM_IP"
     type       = "ipsec.1"
   }
   ```

2. **创建 VPN 连接**：
   ```hcl
   resource "aws_vpn_connection" "main" {
     customer_gateway_id = aws_customer_gateway.main.id
     vpn_gateway_id      = aws_vpn_gateway.main.id
     type                = "ipsec.1"

     static_routes_only = false
   }
   ```

3. **配置路由**：
   ```hcl
   resource "aws_route_table" "vpn" {
     vpc_id = aws_vpc.main.id

     route {
       cidr_block                = "10.0.0.0/16"
       gateway_id                = aws_vpn_gateway.main.id
     }
   }
   ```

### AWS Direct Connect

使用 AWS Direct Connect 实现专用连接：

1. **创建连接**：
   ```hcl
   resource "aws_dx_connection" "main" {
     name            = "main-dx-connection"
     location        = "EqSE2-RK1ujJL"
     bandwidth       = "1Gbps"
     partner_name    = "Example Partner"
   }
   ```

2. **创建 LAG**：
   ```hcl
   resource "aws_dx_lag" "main" {
     name                  = "main-lag"
     connections_bandwidth = "1Gbps"
     location              = "EqSE2-RK1ujJL"
   }
   ```

3. **创建虚拟接口**：
   ```hcl
   resource "aws_dx_private_virtual_interface" "main" {
     connection_id = aws_dx_connection.main.id

     name           = "main-vif"
     vlan           = 4094
     address_family = "ipv4"
     bgp_asn        = 65000
     bgp_auth_key   = "12345678"

     amazon_address = "192.168.0.2/30"
     customer_address = "192.168.0.1/30"

     vpn_gateway_id = aws_vpn_gateway.main.id
   }
   ```

### Azure ExpressRoute

使用 Azure ExpressRoute 连接：

1. **创建 ExpressRoute 线路**：
   ```hcl
   resource "azurerm_express_route_circuit" "main" {
     name                   = "main-er-circuit"
     resource_group_name    = azurerm_resource_group.main.name
     location               = azurerm_resource_group.main.location
     service_provider_name  = "Equinix"
     peering_location       = "Silicon Valley"
     bandwidth_in_mbps      = 1000

     sku {
       tier   = "Premium"
       family = "MeteredData"
     }
   }
   ```

2. **配置对等互连**：
   ```hcl
   resource "azurerm_express_route_circuit_peering" "azure_private" {
     peering_type                  = "AzurePrivatePeering"
     express_route_circuit_name     = azurerm_express_route_circuit.main.name
     resource_group_name           = azurerm_resource_group.main.name
     peer_asn                      = 65000
     primary_peer_address_prefix   = "192.168.1.0/30"
     secondary_peer_address_prefix = "192.168.2.0/30"
     vlan_id                       = 100
   }
   ```

### GCP Cloud Interconnect

使用 GCP Cloud Interconnect：

1. **创建互连附件**：
   ```hcl
   resource "google_compute_interconnect_attachment" "main" {
     name               = "main-interconnect-attachment"
     edge_availability_domain = "availability-domain-1"
     type               = "PARTNER"
     router             = google_compute_router.main.name
     region             = "us-central1"
     bandwidth          = "BPS_10G"
   }
   ```

2. **配置 Cloud Router**：
   ```hcl
   resource "google_compute_router" "main" {
     name    = "main-router"
     region  = "us-central1"
     network = google_compute_network.main.id

     bgp {
       asn = 65000
     }
   }

   resource "google_compute_router_interface" "main" {
     name        = "main-interface"
     router      = google_compute_router.main.name
     region      = "us-central1"
     ip_range    = "169.254.1.0/30"
     interconnect_attachment = google_compute_interconnect_attachment.main.id
   }
   ```

### 网络配置

配置网络设置：

1. **VPC 和子网**：
   ```hcl
   resource "aws_vpc" "main" {
     cidr_block           = "10.0.0.0/16"
     enable_dns_hostnames = true
     enable_dns_support   = true

     tags = {
       Name = "main-vpc"
     }
   }

   resource "aws_subnet" "public" {
     vpc_id     = aws_vpc.main.id
     cidr_block = "10.0.1.0/24"

     tags = {
       Name = "public-subnet"
     }
   }
   ```

2. **安全组和防火墙**：
   ```hcl
   resource "aws_security_group" "vpn" {
     name   = "vpn-security-group"
     vpc_id = aws_vpc.main.id

     ingress {
       from_port   = 443
       to_port     = 443
       protocol    = "tcp"
       cidr_blocks = ["YOUR_ON_PREM_CIDR"]
     }
   }
   ```

### 高可用性配置

配置高可用性：

1. **冗余 VPN 隧道**：
   ```hcl
   resource "aws_vpn_connection" "main" {
     customer_gateway_id = aws_customer_gateway.main.id
     vpn_gateway_id      = aws_vpn_gateway.main.id
     type                = "ipsec.1"

     tunnel1_preshared_key = "tunnel1-key"
     tunnel2_preshared_key = "tunnel2-key"
   }
   ```

2. **冗余网关**：
   ```hcl
   resource "aws_vpn_gateway" "main" {
     vpc_id = aws_vpc.main.id
     tags = {
       Name = "main-vpn-gateway"
     }
   }

   resource "aws_vpn_gateway_route_propagation" "main" {
     vpn_gateway_id = aws_vpn_gateway.main.id
     route_table_id = aws_route_table.main.id
   }
   ```

### 监控和故障排除

监控连接性能：

1. **CloudWatch 指标**：
   ```hcl
   resource "aws_cloudwatch_metric_alarm" "tunnel_state" {
     alarm_name          = "vpn-tunnel-state"
     comparison_operator = "LessThanThreshold"
     evaluation_periods  = "1"
     metric_name         = "TunnelState"
     namespace           = "AWS/VPNConnection"
     period              = "300"
     statistic           = "Average"
     threshold           = "1"

     dimensions = {
       VpnId = aws_vpn_connection.main.id
     }
   }
   ```

2. **连接监控**：
   ```bash
   # 检查 VPN 状态
   aws ec2 describe-vpn-connections --vpn-connection-ids ${VPN_ID}

   # 测试连接
   ping -c 4 REMOTE_PRIVATE_IP

   # 检查路由
   traceroute REMOTE_PRIVATE_IP
   ```

### 安全配置

配置安全设置：

1. **加密设置**：
   ```hcl
   resource "aws_vpn_connection" "main" {
     customer_gateway_id = aws_customer_gateway.main.id
     vpn_gateway_id      = aws_vpn_gateway.main.id
     type                = "ipsec.1"

     tunnel1_phase1_lifetime     = 28800
     tunnel1_phase2_lifetime     = 3600
     tunnel1_preshared_key       = random_string.tunnel1_key.result

     tunnel2_phase1_lifetime     = 28800
     tunnel2_phase2_lifetime     = 3600
     tunnel2_preshared_key       = random_string.tunnel2_key.result
   }
   ```

2. **访问控制**：
   ```hcl
   resource "aws_security_group_rule" "vpn_ingress" {
     type              = "ingress"
     from_port         = 0
     to_port           = 65535
     protocol          = "-1"
     cidr_blocks       = [YOUR_ON_PREM_CIDR]
     security_group_id = aws_security_group.vpn.id
   }
   ```

### 成本优化

优化连接成本：

1. **选择正确的连接类型**：
   - 使用 VPN 代替 Direct Connect/ExpressRoute 处理低带宽需求
   - 对高带宽需求使用专线连接
   - 考虑使用带转接的合作伙伴连接

2. **监控使用情况**：
   ```bash
   # 检查数据传输成本
   aws ce get-cost-and-usage \
     --time-period Start=2024-01-01,End=2024-01-31 \
     --granularity MONTHLY \
     --metrics BlendedCost \
     --filter '{"Dimensions": {"Key": "USAGE_TYPE", "Values": ["DataTransfer"]}}'
   ```

## 约束和指导原则

### 网络设计

- **IP 地址规划**：规划 IP 地址以避免冲突
- **路由配置**：为资源配置正确的路由
- **DNS 配置**：设置本地和云端之间的 DNS 解析
- **MTU 设置**：配置路径 MTU 发现
- **防火墙规则**：实现最小权限原则

### 性能优化

- **带宽规划**：选择适当的连接带宽
- **延迟优化**：为低延迟要求选择最近的区域
- **冗余规划**：为关键工作负载实施冗余
- **负载均衡**：跨多个连接分布流量

### 安全最佳实践

- **加密**：所有连接使用强加密
- **身份认证**：使用强密钥和证书
- **网络隔离**：使用 VPC、子网和安全组
- **访问控制**：实施网络访问控制列表
- **监控**：记录和监控网络流量

## 何时使用此技能

使用此技能进行混合云网络时：

- **连接规划**：规划本地和云端之间的连接
- **连接实施**：实施 VPN 和专线连接
- **安全配置**：配置网络安全设置
- **性能优化**：优化网络性能
- **故障排除**：诊断连接问题
- **成本优化**：优化连接成本
- **高可用性**：实施冗余和故障切换
- **监控设置**：配置连接的监控和警报

不要将此技能用于：

- **纯云网络**：使用云网络技能替代
- **纯本地网络**：使用网络工程技能
- **SD-WAN 解决方案**：使用 SD-WAN 专用技能
- **负载均衡配置**：使用负载均衡技能
