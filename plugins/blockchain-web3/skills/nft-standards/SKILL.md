---
name: nft-standards
description: 实现具有适当元数据处理、铸造策略和市场集成的 NFT 标准（ERC-721、ERC-1155）。在创建 NFT 合约、构建 NFT 市场或实现数字资产系统时使用。
---

# NFT 标准

掌握 ERC-721 和 ERC-1155 NFT 标准、元数据最佳实践和高级 NFT 功能。

## 何时使用此技能

- 创建 NFT 集合（艺术、游戏、收藏品）
- 实现市场功能
- 构建链上或链下元数据
- 创建灵魂绑定代币（不可转让）
- 实现版税和收入共享
- 开发动态/演进式 NFT

## ERC-721（非同质化代币标准）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage, ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.08 ether;
    uint256 public constant MAX_PER_MINT = 20;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mint(uint256 quantity) external payable {
        require(quantity > 0 && quantity <= MAX_PER_MINT, "Invalid quantity");
        require(_tokenIds.current() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIds.increment();
            uint256 newTokenId = _tokenIds.current();
            _safeMint(msg.sender, newTokenId);
            _setTokenURI(newTokenId, generateTokenURI(newTokenId));
        }
    }

    function generateTokenURI(uint256 tokenId) internal pure returns (string memory) {
        // 返回 IPFS URI 或链上元数据
        return string(abi.encodePacked("ipfs://QmHash/", Strings.toString(tokenId), ".json"));
    }

    // 必需的覆盖函数
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

## ERC-1155（多代币标准）

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant SWORD = 1;
    uint256 public constant SHIELD = 2;
    uint256 public constant POTION = 3;

    mapping(uint256 => uint256) public tokenSupply;
    mapping(uint256 => uint256) public maxSupply;

    constructor() ERC1155("ipfs://QmBaseHash/{id}.json") {
        maxSupply[SWORD] = 1000;
        maxSupply[SHIELD] = 500;
        maxSupply[POTION] = 10000;
    }

    function mint(
        address to,
        uint256 id,
        uint256 amount
    ) external onlyOwner {
        require(tokenSupply[id] + amount <= maxSupply[id], "Exceeds max supply");

        _mint(to, id, amount, "");
        tokenSupply[id] += amount;
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts
    ) external onlyOwner {
        for (uint256 i = 0; i < ids.length; i++) {
            require(tokenSupply[ids[i]] + amounts[i] <= maxSupply[ids[i]], "Exceeds max supply");
            tokenSupply[ids[i]] += amounts[i];
        }

        _mintBatch(to, ids, amounts, "");
    }

    function burn(
        address from,
        uint256 id,
        uint256 amount
    ) external {
        require(from == msg.sender || isApprovedForAll(from, msg.sender), "Not authorized");
        _burn(from, id, amount);
        tokenSupply[id] -= amount;
    }
}
```

## 元数据标准

### 链下元数据（IPFS）

```json
{
  "name": "NFT #1",
  "description": "Description of the NFT",
  "image": "ipfs://QmImageHash",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    },
    {
      "trait_type": "Power",
      "value": 95,
      "display_type": "number",
      "max_value": 100
    }
  ]
}
```

### 链上元数据

```solidity
contract OnChainNFT is ERC721 {
    struct Traits {
        uint8 background;
        uint8 body;
        uint8 head;
        uint8 rarity;
    }

    mapping(uint256 => Traits) public tokenTraits;

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        Traits memory traits = tokenTraits[tokenId];

        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "NFT #', Strings.toString(tokenId), '",',
                        '"description": "On-chain NFT",',
                        '"image": "data:image/svg+xml;base64,', generateSVG(traits), '",',
                        '"attributes": [',
                        '{"trait_type": "Background", "value": "', Strings.toString(traits.background), '"},',
                        '{"trait_type": "Rarity", "value": "', getRarityName(traits.rarity), '"}',
                        ']}'
                    )
                )
            )
        );

        return string(abi.encodePacked("data:application/json;base64,", json));
    }

    function generateSVG(Traits memory traits) internal pure returns (string memory) {
        // 基于特征生成 SVG
        return "...";
    }
}
```

## 版税（EIP-2981）

```solidity
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

contract NFTWithRoyalties is ERC721, IERC2981 {
    address public royaltyRecipient;
    uint96 public royaltyFee = 500; // 5%

    constructor() ERC721("Royalty NFT", "RNFT") {
        royaltyRecipient = msg.sender;
    }

    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        return (royaltyRecipient, (salePrice * royaltyFee) / 10000);
    }

    function setRoyalty(address recipient, uint96 fee) external onlyOwner {
        require(fee <= 1000, "Royalty fee too high"); // 最大 10%
        royaltyRecipient = recipient;
        royaltyFee = fee;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, IERC165)
        returns (bool)
    {
        return interfaceId == type(IERC2981).interfaceId ||
               super.supportsInterface(interfaceId);
    }
}
```

## 灵魂绑定代币（不可转让）

```solidity
contract SoulboundToken is ERC721 {
    constructor() ERC721("Soulbound", "SBT") {}

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal virtual override {
        require(from == address(0) || to == address(0), "Token is soulbound");
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function mint(address to) external {
        uint256 tokenId = totalSupply() + 1;
        _safeMint(to, tokenId);
    }

    // 允许销毁（用户可以销毁他们的 SBT）
    function burn(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        _burn(tokenId);
    }
}
```

## 动态 NFT

```solidity
contract DynamicNFT is ERC721 {
    struct TokenState {
        uint256 level;
        uint256 experience;
        uint256 lastUpdated;
    }

    mapping(uint256 => TokenState) public tokenStates;

    function gainExperience(uint256 tokenId, uint256 exp) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");

        TokenState storage state = tokenStates[tokenId];
        state.experience += exp;

        // 升级逻辑
        if (state.experience >= state.level * 100) {
            state.level++;
        }

        state.lastUpdated = block.timestamp;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        TokenState memory state = tokenStates[tokenId];

        // 基于当前状态生成元数据
        return generateMetadata(tokenId, state);
    }

    function generateMetadata(uint256 tokenId, TokenState memory state)
        internal
        pure
        returns (string memory)
    {
        // 动态元数据生成
        return "";
    }
}
```

## Gas 优化的铸造（ERC721A）

```solidity
import "erc721a/contracts/ERC721A.sol";

contract OptimizedNFT is ERC721A {
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.05 ether;

    constructor() ERC721A("Optimized NFT", "ONFT") {}

    function mint(uint256 quantity) external payable {
        require(_totalMinted() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        _mint(msg.sender, quantity);
    }

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://QmBaseHash/";
    }
}
```

## 资源

- **references/erc721.md**：ERC-721 规范详情
- **references/erc1155.md**：ERC-1155 多代币标准
- **references/metadata-standards.md**：元数据最佳实践
- **references/enumeration.md**：代币枚举模式
- **assets/erc721-contract.sol**：生产级 ERC-721 模板
- **assets/erc1155-contract.sol**：生产级 ERC-1155 模板
- **assets/metadata-schema.json**：标准元数据格式
- **assets/metadata-uploader.py**：IPFS 上传工具

## 最佳实践

1. **使用 OpenZeppelin**：经过实战测试的实现
2. **固定元数据**：使用带有固定服务的 IPFS
3. **实现版税**：EIP-2981 用于市场兼容性
4. **Gas 优化**：批量铸造使用 ERC721A
5. **揭示机制**：占位符 → 揭示模式
6. **枚举**：支持 walletOfOwner 用于市场
7. **白名单**：使用默克尔树实现高效白名单

## 市场集成

- OpenSea：ERC-721/1155、元数据标准
- LooksRare：版税执行
- Rarible：协议费用、懒惰铸造
- Blur：Gas 优化的交易
