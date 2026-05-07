# Sky Bug Bounty Scope — 2026-05-07

## 基本信息
- 平台：Immunefi
- 最高赏金：$10,000,000
- KYC：不需要 ✅
- PoC：必须（所有级别）
- 付款：DAI或USDS（由Sky团队决定）
- 规则：Primacy of Rules（严格按条款）

## 已Clone仓库
- `/home/zbw/audit/sky/` — SKY token + MkrSky converter

## 核心合约（已审计）
| 合约 | 文件 | 功能 |
|------|------|------|
| Sky.sol | src/Sky.sol | SKY治理代币，ERC20+permit+EIP-1271 |
| MkrSky.sol | src/MkrSky.sol | MKR→SKY单向转换器 |

## 代码质量评估
- Sky.sol：标准ERC20实现，无明显漏洞
- MkrSky.sol：简单转换器逻辑，fee上限WAD，整数运算使用unchecked+先check

## 已有审计
- Certora形式化验证（仓库内certora/目录）
- ChainSecurity多次审计
- Cantina审计
- Sherlock审计

## In-Scope Assets（从Immunefi页面）
- chainlog.makerdao.com 注册的所有已部署合约
- 多个GitHub仓库（sky-ecosystem/*)
- Smart Contracts & Web/App

## Out of Scope
- dai.js repo
- 旧版本合约（chainlog上的是最新）
- 预言机极端波动（设计决策）
- 治理ward被假定为可信
- 需要第三方协议配合的攻击（除非满足三个条件）

## 攻击路径思路
1. 新合约/模块交互边界
2. 升级引入的回归
3. 多合约组合攻击
4. EIP-1271签名验证边界情况
5. MKR/SKY转换器+其他模块的经济攻击

## 下一步
1. Clone更多核心模块（dss, endgame-toolkit, lockstake等）
2. 系统化审计框架
3. 设置cron监控bounty变化
