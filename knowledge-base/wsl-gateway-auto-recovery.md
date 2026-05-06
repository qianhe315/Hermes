# WSL Gateway 自动恢复方案

> 创建日期：2026-05-06 12:01 CST
> 对应路线图：主干一「WSL重启后gateway自动恢复」

## 现状检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| systemd=true (wsl.conf) | ✅ | WSL2启用systemd |
| gateway systemd服务 | ✅ 已安装+已启用 | `~/.config/systemd/user/hermes-gateway.service` |
| lingering | ✅ yes | 用户服务随系统启动，无需登录 |
| WSL空闲超时 | ✅ vmIdleTimeout=-1 | 2026.05.06新配置，WSL不会自动关闭 |
| cron gateway依赖 | ✅ | gateway运行中，cron正常 |

## 自动恢复链路

```
Windows启动 → WSL自动启动(如果配置) → systemd启动
  → user@1000.service启动(lingering=yes)
    → hermes-gateway.service自动启动(enabled)
      → cron jobs开始触发
```

## 已完成的配置

### 1. systemd用户服务（已有）
```bash
hermes gateway install   # 安装服务
systemctl --user enable hermes-gateway.service  # 开机自启
loginctl enable-linger zbw  # 无登录也启动用户服务
```

### 2. WSL空闲防护（本次新增）
文件：`C:\Users\郑博文\.wslconfig`
```ini
[wsl2]
vmIdleTimeout=-1
```
**生效方式**：需要在 PowerShell（管理员）中执行 `wsl --shutdown` 然后重新打开WSL。

## 剩余风险：Windows主机重启

WSL随Windows启动需要外部触发。两种方案：

### 方案A：Windows任务计划程序（推荐）
创建基本任务：
- 触发器：系统启动时
- 操作：启动程序 `wsl.exe`，参数 `-d Ubuntu`
- 勾选"使用最高权限运行"

### 方案B：启动文件夹快捷方式
创建 `shell:startup` 快捷方式指向 `wsl.exe -d Ubuntu`

**注意**：以上需要用户在Windows侧操作，小月无法从WSL内部配置。

## 验证方法

```bash
# 检查gateway状态
hermes cron status

# 检查systemd服务
systemctl --user status hermes-gateway.service

# 检查linger
loginctl show-user zbw | grep Linger

# 模拟WSL重启后的恢复（不实际重启）
systemctl --user restart hermes-gateway.service
hermes cron status  # 确认cron检测到gateway
```
