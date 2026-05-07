# Spark Bounty 审计发现 — 2026-05-07

## 已审计合约

| 合约 | 文件 | 关键点 |
|------|------|--------|
| ALMProxy | spark-alm/ALMProxy.sol | 简单代理，仅CONTROLLER可调用 |
| RateLimits | spark-alm/RateLimits.sol | 速率限制，标准实现 |
| ForeignController | spark-alm/ForeignController.sol | 跨链控制器，LayerZero+CCTP |
| PSM3 | spark-psm/PSM3.sol | 3资产Peg Stability Module |
| LayerZeroLib | spark-alm/libraries/LayerZeroLib.sol | LayerZero跨链桥接 |

## 发现

### F6: PSM3 ERC4626通胀攻击（中等）
- 位置: PSM3.sol deposit() L160-173
- 问题: shares在资产转入前计算，totalAssets为0时存在1:1铸造漏洞。USDS/sUSDS可直接捐赠
- 攻击: 首笔小额存款→捐赠→稀释后续存户
- 影响: 需要大资金（~$100K），收益约33%
- 缓解: 协议部署时注入初始流动性即可消除

### F7: ForeignController.transferTokenLayerZero部署未测试（关键）
- 位置: ForeignController.sol L294-315
- 注释明确写: "deployed without integration testing"
- "KEEP RATE LIMIT AT ZERO until LayerZero dependencies are live"
- 风险: 如果速率限制被误设为非零，RELAYER角色可通过LayerZero桥接资产
- LayerZeroLib中minAmountLD先设0后quote更新——报价与执行之间可能有滑点

### F8: ForeignController速率限制时序不一致
- withdrawPSM (L237): 速率限制在提款后检查
- withdrawAave (L434): 同样
- redeemERC4626 (L374): 同样
- 缓解: 事务原子性——revert会回滚，实际安全但模式异常

## Spark In-Scope资产总览
Spark是Aave v3 fork + 跨链SSR预言机 + ALM + PSM3
- 核心代码库: sparklend, aave-v3-core, aave-v3-periphery
- 跨链: xchain-ssr-oracle, spark-alm-controller
- 新组件(2026.03): ALM_CONTROLLER_v1.11.0, SPARKLEND_CAP_AUTOMATOR_v1.1.0, SPARK_SAVINGS_INTENTS
- 最新(2026.03.18): Spark Savings Intents

## 下一步优先级
1. 检查Spark Savings Intents (2026.03.18 — 最新部署)
2. 审计MainnetController
3. 验证PSM3通胀攻击在部署环境中的可利用性
