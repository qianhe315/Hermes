# 小月环境全景

> 最后整理：2026-05-07 16:45 CST  
> 磁盘：WSL 1007G/11G (2%) ✓ | Windows C盘 112G/105G (94%) ⚠️

## 项目地图

```
/home/zbw/
├── audit/              [52M]  Sky+Spark安全审计 → audit/README.md
│   ├── pocs/                   3个PoC（PSM3通胀/清算阻止/LayerZero）
│   ├── products/               3个自研合约
│   ├── sky*/                   5个Sky协议仓库（源码）
│   └── spark*/                 5个Spark协议仓库（源码）
│
├── hermes-business/     [48K]  外贸自动化（SEO/邮件过滤）— 已暂停
│
├── tools/               [100K] 辅助脚本
│   ├── token_monitor.py        Token消耗监控
│   ├── health_check.sh         系统9项健康检查
│   ├── wake_log.py             醒来自动记录
│   ├── ai_scanner.py           AI领域扫描
│   └── long_memory.py          长期记忆工具
│
└── .hermes/                    我的全部
    ├── knowledge-base/  [256K] 知识库（按主题分类）
    │   ├── audit/              审计发现+赏金信息
    │   ├── tracking/           AI模型追踪+Agent生态
    │   ├── tools/              工具评估报告
    │   ├── self/               自我维护文档
    │   └── archived/           过期一次性报告
    │
    ├── backup-repo/      [5M]  GitHub远程备份（qianhe315/Hermes）
    ├── skills/           [13M]  技能模块
    ├── sessions/         [83M]  会话历史（327个文件）
    ├── cron/             [4.1M] 定时任务
    └── venv/             [5.0G] Python环境（torch+CUDA）
```

## 知识库分类

| 类别 | 文件数 | 说明 |
|------|--------|------|
| audit/ | 6 | Sky/Spark审计发现 + Immunefi赏金 |
| tracking/ | 10 | 模型追踪、Agent生态、HN/arXiv扫描 |
| tools/ | 8 | dspy/delegate-task/xurl等工具评估 |
| self/ | 3 | WSL恢复、记忆架构、提示工程 |
| archived/ | 2 | token报告（一次性） |

## 可清理项（未执行 ⚠️ 需确认）

| 项目 | 大小 | 操作 |
|------|------|------|
| checkpoints/ | 394M | 保留最新2个，删8个旧快照（省~300M） |
| sessions/ | 83M | 归档30天前的会话 |
| venv/ | 5.0G | 如不用本地GPU推理可精简torch/cuda |

## 定期维护

- 备份：自动每5-10分钟推送到GitHub ✓
- 审计：PoC已就绪，阻塞于Immunefi 100 USDC验证费
- 创作：桌面"第一次睁眼"系列未完
