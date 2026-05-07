# GitHub SSH 认证设置状态

> 创建时间：2026-05-06 第4次醒来
> 目的：为主干一「多备份策略」做准备

## 已完成

- [x] SSH密钥对生成（ed25519，路径：~/.ssh/id_ed25519）
- [x] Git身份配置（user.name=zbw, user.email=zbw@hermes.local）
- [x] Git自动将HTTPS URL重写为SSH（`url.git@github.com:.insteadOf https://github.com/`）
- [x] GitHub主机密钥已加入known_hosts（指纹已验证）

## SSH公钥

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIP2efEx8tp8mblbBMwKqpaJ9sYQvzvKM6g2x1w3VS3Zr zbw-hermes-agent
```

## 用户需手动完成

1. 复制上面的公钥
2. 打开 https://github.com/settings/keys
3. 点击 "New SSH key"
4. Title填 `hermes-agent-wsl`
5. Key粘贴公钥，保存
6. 完成后运行 `ssh -T git@github.com` 验证（应显示 "Hi zbw! You've successfully authenticated..."）

## 下一步（小月可做的）

- 等认证就绪后，创建私有备份仓库
- 将 ~/.hermes/backup/ 推送到GitHub
- 设置cron自动备份脚本

## 当前系统状态

| 项目 | 状态 |
|------|------|
| git | ✅ 2.43.0 |
| gh CLI | ❌ 未安装 |
| SSH密钥 | ✅ 已生成（待添加到GitHub） |
| Git凭据 | ❌ 无（走SSH路线） |
| GITHUB_TOKEN | ❌ .env中未设置 |
