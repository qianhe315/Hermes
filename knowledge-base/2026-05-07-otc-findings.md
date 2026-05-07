# MainnetController OTC 发现 — 2026-05-07

## OTC (Over-The-Counter) Swap 系统

MainnetController.sol L1094-1167

### 机制
1. `otcSend`: RELAYER发送资产到exchange的OTC buffer
2. `otcClaim`: RELAYER从OTC buffer取回资产
3. `isOtcSwapReady`: 检查是否足够资产已取回

### Recharge机制 (L1153-1159)
```solidity
getOtcClaimWithRecharge = claimed18 + time * rechargeRate18
```
线性时间充电——随等待时间增长"已取回"金额。

### F9: OTC Recharge可能导致连续资金发送给恶意交易所
- `isOtcSwapReady`检查: `getOtcClaimWithRecharge >= sent18 * maxSlippage`
- 如果`rechargeRate18 > 0`: 即使交易所偷走所有资产，仅靠等待就能让swap变"就绪"
- 下次`otcSend`会再次发送资产→重复被盗
- 缓解: `rechargeRate18`由admin设置，应设为0防范恶意交易所
- 严重性: 中（需admin配置错误+恶意交易所）

### F10: otcSend重置claimed18导致超额归还被丢弃
- `otcSend` (L1117): `otc.claimed18 = 0` 重置累计
- 如果交易所超额归还，多余部分在下次swap时丢失（仅18-decimal accounting，资产已取回）
- 严重性: 信息（实际资产不丢失）

## 整体审计进度汇总

| 平台 | 合约数 | 发现数 | 最高严重性 |
|------|--------|--------|-----------|
| Sky | 10 | 5 (F1-F5) | 中(CEI) |
| Spark | 9 | 3 (F6-F8) | 中(LayerZero未测试) |
| Spark MC | 1 | 2 (F9-F10) | 中(OTC recharge) |

总计: 19个合约, 10个发现, 无Critical级别
