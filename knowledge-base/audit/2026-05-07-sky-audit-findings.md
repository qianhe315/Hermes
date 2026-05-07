# Sky Bug Bounty 审计发现 — 2026-05-07

## 已审计合约

| 合约 | 文件 | 行数 | Solidity | 复杂度 |
|------|------|------|----------|--------|
| Vat | dss/src/vat.sol | 246 | 0.6.12 | 核心账本 |
| Spotter | dss/src/spot.sol | 108 | 0.6.12 | 预言机 |
| Dog | dss/src/dog.sol | 249 | 0.6.12 | 清算 |
| End | dss/src/end.sol | 449 | 0.6.12 | 全局结算 |
| Sky | sky/src/Sky.sol | 253 | 0.8.21 | 治理代币 |
| MkrSky | sky/src/MkrSky.sol | 110 | 0.8.21 | 代币转换 |
| LockstakeEngine | lockstake/src/LockstakeEngine.sol | 426 | 0.8.21 | 锁仓引擎 |
| LockstakeClipper | lockstake/src/LockstakeClipper.sol | 516 | 0.8.21 | 拍卖 |
| LockstakeUrn | lockstake/src/LockstakeUrn.sol | 80 | 0.8.21 | Urn代理 |
| SDAO | endgame-toolkit/src/SDAO.sol | 418 | 0.8.16 | 子DAO代币 |

## 发现

### F1: LockstakeEngine — CEI违反（中等风险）
- 位置: _selectVoteDelegate (L255-266), _selectFarm (L279-289)
- 问题: 外部调用(VoteDelegate.free/lock, LockstakeUrn.withdraw/stake)在状态更新(urnVoteDelegates, urnFarms)之前
- 当前可利用性: 低——VoteDelegate和Farm由信任方创建
- 潜在影响: 如果未来引入恶意委托/农场合约，可导致重入
- 修复: 将状态更新移至外部调用之前

### F2: LockstakeEngine — 恶意委托/农场可阻止清算
- 位置: onKick (L391-400) 调用 _selectVoteDelegate 和 _selectFarm
- 问题: 如果urn的VoteDelegate.free()或Farm.withdraw() revert，清算将失败
- 攻击场景: 用户创建恶意委托/农场，设置到urn，借款后等待清算→清算失败→坏账累积
- 缓解: 治理可通过selectVoteDelegate/selectFarm移除恶意委托/农场
- 注意: Sky bounty明确提到"reserveHatch功能"用于解决此问题——可能已知

### F3: _divup vs 取整不一致
- 位置: draw (L350) 使用 _divup 取上整，wipe (L362) 使用除法取下整
- 影响: 每轮draw/wipe有微小取整差异，但gas成本远超收益
- 严重性: 信息性

### F4: _free函数外部调用在前
- 位置: _free (L325-343)
- 问题: LockstakeUrn.withdraw 和 VoteDelegate.free 在 vat.frob/slip 之前
- 缓解: Vat和lssky无回调功能

### F5: LockstakeClipper.take — SKY在DAI支付前转移
- 位置: take (L406-407: engine.onTake, L420: clipperCall, L424: vat.move)
- 问题: SKY代币在DAI收款前已转给买家
- 可利用性: 原子交易——DAI转账失败则全部回滚

## 攻击面映射（待深入）

1. **LockstakeEngine + Dog + Clipper交互**: 清算边缘情况
2. **End.sol 全局结算**: 与LockstakeEngine的交互（snip/skip函数）
3. **预言机更新时序**: spot vs jug.drip 竞态
4. **Cure合约**: 新引入的坏账处理组件（未在clone中，需验证）
5. **LockstakeMigrator**: 迁移过程中状态一致性

## 下一步
1. 审计LockstakeMigrator.sol
2. 检查Cure合约
3. 运行Slither静态分析（需安装到venv）
4. 研究已有审计报告中的已知问题
5. 关注新部署合约的升级变动
