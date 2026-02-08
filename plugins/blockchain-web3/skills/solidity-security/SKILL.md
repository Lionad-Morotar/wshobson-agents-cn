---
name: solidity-security
description: 掌握智能合约安全最佳实践，防止常见漏洞并实现安全的 Solidity 模式。在编写智能合约、审计现有合约或为区块链应用实现安全措施时使用。
---

# Solidity 安全

掌握智能合约安全最佳实践、漏洞预防和安全的 Solidity 开发模式。

## 何时使用此技能

- 编写安全的智能合约
- 审计现有合约的漏洞
- 实现安全的 DeFi 协议
- 防止重入、溢出和访问控制问题
- 在保持安全性的同时优化 Gas 使用
- 为专业审计准备合约
- 理解常见攻击向量

## 关键漏洞

### 1. 重入攻击

攻击者在状态更新前回调合约。

**易受攻击的代码：**

```solidity
// 易受重入攻击
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];

        // 危险：外部调用在状态更新之前
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);

        balances[msg.sender] = 0;  // 太晚了！
    }
}
```

**安全模式（检查-效果-交互）：**

```solidity
contract SecureBank {
    mapping(address => uint256) public balances;

    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        // 效果：在外部调用之前更新状态
        balances[msg.sender] = 0;

        // 交互：外部调用放在最后
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

**替代方案：ReentrancyGuard**

```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 2. 整数溢出/下溢

**易受攻击的代码（Solidity < 0.8.0）：**

```solidity
// 易受攻击
contract VulnerableToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // 无溢出检查 - 可能回绕
        balances[msg.sender] -= amount;  // 可能下溢！
        balances[to] += amount;          // 可能溢出！
    }
}
```

**安全模式（Solidity >= 0.8.0）：**

```solidity
// Solidity 0.8+ 具有内置的溢出/下溢检查
contract SecureToken {
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        // 在溢出/下溢时自动回滚
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

**对于 Solidity < 0.8.0，使用 SafeMath：**

```solidity
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SecureToken {
    using SafeMath for uint256;
    mapping(address => uint256) public balances;

    function transfer(address to, uint256 amount) public {
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[to] = balances[to].add(amount);
    }
}
```

### 3. 访问控制

**易受攻击的代码：**

```solidity
// 易受攻击：任何人都可以调用关键函数
contract VulnerableContract {
    address public owner;

    function withdraw(uint256 amount) public {
        // 无访问控制！
        payable(msg.sender).transfer(amount);
    }
}
```

**安全模式：**

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is Ownable {
    function withdraw(uint256 amount) public onlyOwner {
        payable(owner()).transfer(amount);
    }
}

// 或实现自定义基于角色的访问
contract RoleBasedContract {
    mapping(address => bool) public admins;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Not an admin");
        _;
    }

    function criticalFunction() public onlyAdmin {
        // 受保护的函数
    }
}
```

### 4. 抢跑攻击

**易受攻击：**

```solidity
// 易受抢跑攻击
contract VulnerableDEX {
    function swap(uint256 amount, uint256 minOutput) public {
        // 攻击者在内存池中看到此交易并抢跑
        uint256 output = calculateOutput(amount);
        require(output >= minOutput, "Slippage too high");
        // 执行交换
    }
}
```

**缓解措施：**

```solidity
contract SecureDEX {
    mapping(bytes32 => bool) public usedCommitments;

    // 步骤 1：提交交易
    function commitTrade(bytes32 commitment) public {
        usedCommitments[commitment] = true;
    }

    // 步骤 2：揭示交易（下一个区块）
    function revealTrade(
        uint256 amount,
        uint256 minOutput,
        bytes32 secret
    ) public {
        bytes32 commitment = keccak256(abi.encodePacked(
            msg.sender, amount, minOutput, secret
        ));
        require(usedCommitments[commitment], "Invalid commitment");
        // 执行交换
    }
}
```

## 安全最佳实践

### 检查-效果-交互模式

```solidity
contract SecurePattern {
    mapping(address => uint256) public balances;

    function withdraw(uint256 amount) public {
        // 1. 检查：验证条件
        require(amount <= balances[msg.sender], "Insufficient balance");
        require(amount > 0, "Amount must be positive");

        // 2. 效果：更新状态
        balances[msg.sender] -= amount;

        // 3. 交互：外部调用放在最后
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 拉取优于推送模式

```solidity
// 首选此方式（拉取）
contract SecurePayment {
    mapping(address => uint256) public pendingWithdrawals;

    function recordPayment(address recipient, uint256 amount) internal {
        pendingWithdrawals[recipient] += amount;
    }

    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to withdraw");

        pendingWithdrawals[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}

// 而非此方式（推送）
contract RiskyPayment {
    function distributePayments(address[] memory recipients, uint256[] memory amounts) public {
        for (uint i = 0; i < recipients.length; i++) {
            // 如果任何转账失败，整批失败
            payable(recipients[i]).transfer(amounts[i]);
        }
    }
}
```

### 输入验证

```solidity
contract SecureContract {
    function transfer(address to, uint256 amount) public {
        // 验证输入
        require(to != address(0), "Invalid recipient");
        require(to != address(this), "Cannot send to contract");
        require(amount > 0, "Amount must be positive");
        require(amount <= balances[msg.sender], "Insufficient balance");

        // 继续转账
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

### 紧急停止（熔断器）

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyStop is Pausable, Ownable {
    function criticalFunction() public whenNotPaused {
        // 函数逻辑
    }

    function emergencyStop() public onlyOwner {
        _pause();
    }

    function resume() public onlyOwner {
        _unpause();
    }
}
```

## Gas 优化

### 使用 `uint256` 而非较小类型

```solidity
// 更 Gas 高效
contract GasEfficient {
    uint256 public value;  // 最佳

    function set(uint256 _value) public {
        value = _value;
    }
}

// 较低效
contract GasInefficient {
    uint8 public value;  // 仍使用 256 位槽

    function set(uint8 _value) public {
        value = _value;  // 类型转换需要额外 Gas
    }
}
```

### 打包存储变量

```solidity
// Gas 高效（3 个变量在 1 个槽中）
contract PackedStorage {
    uint128 public a;  // 槽 0
    uint64 public b;   // 槽 0
    uint64 public c;   // 槽 0
    uint256 public d;  // 槽 1
}

// Gas 低效（每个变量在单独的槽中）
contract UnpackedStorage {
    uint256 public a;  // 槽 0
    uint256 public b;  // 槽 1
    uint256 public c;  // 槽 2
    uint256 public d;  // 槽 3
}
```

### 对函数参数使用 `calldata` 而非 `memory`

```solidity
contract GasOptimized {
    // 更 Gas 高效
    function processData(uint256[] calldata data) public pure returns (uint256) {
        return data[0];
    }

    // 较低效
    function processDataMemory(uint256[] memory data) public pure returns (uint256) {
        return data[0];
    }
}
```

### 适当时使用事件进行数据存储

```solidity
contract EventStorage {
    // 发出事件比存储更便宜
    event DataStored(address indexed user, uint256 indexed id, bytes data);

    function storeData(uint256 id, bytes calldata data) public {
        emit DataStored(msg.sender, id, data);
        // 除非需要，否则不要存储在合约存储中
    }
}
```

## 常见漏洞清单

```solidity
// 安全检查清单合约
contract SecurityChecklist {
    /**
     * [ ] 重入保护（ReentrancyGuard 或 CEI 模式）
     * [ ] 整数溢出/下溢（Solidity 0.8+ 或 SafeMath）
     * [ ] 访问控制（Ownable、角色、修饰器）
     * [ ] 输入验证（require 语句）
     * [ ] 抢跑缓解（如适用则使用提交-揭示）
     * [ ] Gas 优化（打包存储、calldata）
     * [ ] 紧急停止机制（Pausable）
     * [ ] 支付的拉取优于推送模式
     * [ ] 不对不受信任的合约进行 delegatecall
     * [ ] 不使用 tx.origin 进行身份验证（使用 msg.sender）
     * [ ] 适当的事件发出
     * [ ] 外部调用在函数末尾
     * [ ] 检查外部调用的返回值
     * [ ] 无硬编码地址
     * [ ] 升级机制（如果是代理模式）
     */
}
```

## 安全测试

```javascript
// Hardhat 测试示例
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function () {
  it("Should prevent reentrancy attack", async function () {
    const [attacker] = await ethers.getSigners();

    const VictimBank = await ethers.getContractFactory("SecureBank");
    const bank = await VictimBank.deploy();

    const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
    const attackerContract = await Attacker.deploy(bank.address);

    // 存入资金
    await bank.deposit({ value: ethers.utils.parseEther("10") });

    // 尝试重入攻击
    await expect(
      attackerContract.attack({ value: ethers.utils.parseEther("1") }),
    ).to.be.revertedWith("ReentrancyGuard: reentrant call");
  });

  it("Should prevent integer overflow", async function () {
    const Token = await ethers.getContractFactory("SecureToken");
    const token = await Token.deploy();

    // 尝试溢出
    await expect(token.transfer(attacker.address, ethers.constants.MaxUint256))
      .to.be.reverted;
  });

  it("Should enforce access control", async function () {
    const [owner, attacker] = await ethers.getSigners();

    const Contract = await ethers.getContractFactory("SecureContract");
    const contract = await Contract.deploy();

    // 尝试未授权提取
    await expect(contract.connect(attacker).withdraw(100)).to.be.revertedWith(
      "Ownable: caller is not the owner",
    );
  });
});
```

## 审计准备

```solidity
contract WellDocumentedContract {
    /**
     * @title 文档完善的合约
     * @dev 审计的正确文档示例
     * @notice 此合约处理用户存款和取款
     */

    /// @notice 用户余额映射
    mapping(address => uint256) public balances;

    /**
     * @dev 将 ETH 存入合约
     * @notice 任何人都可以存入资金
     */
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    /**
     * @dev 提取用户余额
     * @notice 遵循 CEI 模式以防止重入
     * @param amount 要提取的金额（以 wei 为单位）
     */
    function withdraw(uint256 amount) public {
        // 检查
        require(amount <= balances[msg.sender], "Insufficient balance");

        // 效果
        balances[msg.sender] -= amount;

        // 交互
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## 资源

- **references/reentrancy.md**：全面的重入预防
- **references/access-control.md**：基于角色的访问模式
- **references/overflow-underflow.md**：SafeMath 和整数安全
- **references/gas-optimization.md**：Gas 节省技术
- **references/vulnerability-patterns.md**：常见漏洞目录
- **assets/solidity-contracts-templates.sol**：安全合约模板
- **assets/security-checklist.md**：审计前清单
- **scripts/analyze-contract.sh**：静态分析工具

## 安全分析工具

- **Slither**：静态分析工具
- **Mythril**：安全分析工具
- **Echidna**：模糊测试工具
- **Manticore**：符号执行
- **Securify**：自动安全扫描器

## 常见陷阱

1. **使用 `tx.origin` 进行身份验证**：改用 `msg.sender`
2. **未检查的外部调用**：始终检查返回值
3. **对不受信任的合约进行 Delegatecall**：可能劫持您的合约
4. **浮动Pragma**：固定到特定的 Solidity 版本
5. **缺少事件**：为状态变更发出事件
6. **循环中过多的 Gas**：可能达到区块 Gas 限制
7. **无升级路径**：如果需要升级，考虑代理模式
