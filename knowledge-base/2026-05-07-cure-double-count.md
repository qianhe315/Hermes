# 新发现: Cure合约 drop+lift+reload 双重计数

## Cure.sol (Debt Rectifier) — /home/zbw/audit/sky-dss/src/cure.sol

### 问题描述

`load(src)` 中的 `say` 累计公式:
```
say = say - oldAmt + newAmt
```

当源被 `drop()` 删除后，`amt[src]` 被清除但 `say` 不做相应扣除。
如果该源被 `lift()` 重新添加（在 cage 之前），再次 `load()` 时:
- `oldAmt_ = 0`（因为被 delete 了）
- `newAmt_ = SourceLike(src).cure()`
- `say = say + newAmt_` （旧贡献仍在 say 中 → 双重计数）

### 攻击场景

前提: 治理层在 cage 前恶意（或错误）操作 drop+lift

1. Cage 前: source A loaded → say=100
2. 治理 drop A (delete amt[A], say 不变 = 100, loaded[A] 保持 = 1)
3. 治理 lift A
4. Cage → 等待期
5. 再次 load A → oldAmt=0, newAmt=100, say=200（应为100）

### 影响

say 被高估 → End.thaw() 的 debt 被低估 → DAI 持有者在 cash() 中获得更多抵押品

### 缓解

- drop/lift 都是 auth（治理），且在 cage 前（live==1）
- 治理被假定为可信
- 当前严重性: 低（治理可信）→ 但如果治理操作失误，会导致全局结算资产分配错误

### 修复建议

在 `drop()` 中: `say = _sub(say, amt[src])` — 删除源时从 say 中扣除其贡献
