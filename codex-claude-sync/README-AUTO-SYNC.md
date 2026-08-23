# 自动同步守护进程

自动监控 Codex 和 Claude Code 配置目录的文件变化，实时双向同步。

## 🎯 功能特性

- ✅ 实时监控文件变化
- ✅ 自动检测增删改操作
- ✅ 后台运行，无需手动触发
- ✅ 可配置检查间隔
- ✅ 详细日志记录
- ✅ 轻量级，低资源占用

## 🚀 快速开始

### Windows

```cmd
# 启动守护进程（60秒间隔）
auto-sync

# 快速模式（30秒间隔）
auto-sync fast

# 后台运行
auto-sync background

# 停止
auto-sync stop
```

### Linux/Mac

```bash
# 启动守护进程（60秒间隔）
./auto-sync.sh

# 快速模式（30秒间隔）
./auto-sync.sh fast

# 后台运行
./auto-sync.sh background

# 停止
./auto-sync.sh stop
```

## ⚙️ 配置选项

### 检查间隔

```bash
# 默认 60 秒
python auto-sync-daemon.py

# 自定义间隔（秒）
python auto-sync-daemon.py --interval 30

# 快速模式（30秒）
auto-sync fast

# 慢速模式（120秒）
auto-sync slow
```

### 同步选项

```bash
# 禁用删除同步
python auto-sync-daemon.py --no-delete
```

## 📊 监控范围

守护进程监控以下目录：

**Codex 配置**:
- `C:\Users\will\.codex\skills\`
- `C:\Users\will\.agents\skills\`
- `C:\Users\will\.codex\commands\`
- `C:\Users\will\.codex\hooks\`

**Claude Code 配置**:
- `C:\Users\will\.claude\skills\`
- `C:\Users\will\.claude\commands\`
- `C:\Users\will\.claude\hooks\`

## 🔍 工作原理

1. **快照比较**: 定期扫描目录，创建文件快照
2. **变化检测**: 比较快照差异，识别增删改
3. **自动同步**: 检测到变化后自动运行同步工具
4. **状态保存**: 记录同步次数和时间

## 📝 日志

守护进程会记录详细日志到 `auto-sync.log`：

```bash
# 查看日志
tail -f auto-sync.log        # Linux/Mac
Get-Content auto-sync.log -Tail 20 -Wait  # Windows PowerShell
```

日志内容包括：
- 启动/停止时间
- 检测到的文件变化
- 同步操作结果
- 错误信息

## 🎮 使用场景

### 场景 1: 开发时自动同步

```bash
# 早上启动电脑后
auto-sync background

# 一天工作中，任何修改都会自动同步
# 晚上关机前自动保存状态
```

### 场景 2: 快速测试

```bash
# 测试时使用快速模式
auto-sync fast

# 测试完成后停止
auto-sync stop
```

### 场景 3: 后台持续运行

```bash
# 后台运行，开机自启动（需要配置）
auto-sync background
```

## 🔧 进阶配置

### Windows 开机自启动

1. 创建快捷方式指向 `auto-sync.bat background`
2. 将快捷方式放到：`C:\Users\你的用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

### Linux/Mac 开机自启动

**systemd服务** (Linux):

```bash
# 创建服务文件
sudo nano /etc/systemd/system/codex-claude-sync.service

# 内容：
[Unit]
Description=Codex Claude Code Auto Sync
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/codex-claude-sync
ExecStart=/usr/bin/python3 auto-sync-daemon.py
Restart=always

[Install]
WantedBy=multi-user.target

# 启用服务
sudo systemctl enable codex-claude-sync
sudo systemctl start codex-claude-sync
```

**launchd** (Mac):

```bash
# 创建 plist 文件
~/Library/LaunchAgents/com.codex-claude-sync.plist

# 内容：
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.codex-claude-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/auto-sync-daemon.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>

# 加载服务
launchctl load ~/Library/LaunchAgents/com.codex-claude-sync.plist
```

## 🛡️ 安全性

- **只读监控**: 监控过程不修改文件
- **双重确认**: 检测到变化后才调用同步工具
- **日志审计**: 所有操作都有详细日志
- **状态保存**: 记录同步历史，可追溯

## ⚡ 性能优化

### 资源占用

- **CPU**: 空闲时几乎为 0
- **内存**: ~10-20 MB
- **磁盘**: 仅扫描元数据，不读取文件内容

### 推荐间隔

- **开发时**: 30-60 秒（快速响应）
- **日常使用**: 60-120 秒（平衡性能）
- **低资源**: 300 秒以上（降低开销）

## 🔍 故障排查

### 问题1: 守护进程无法启动

```bash
# 检查 Python 版本
python --version  # 需要 3.6+

# 检查依赖
python auto-sync-daemon.py --help
```

### 问题2: 同步不工作

```bash
# 查看日志
cat auto-sync.log

# 手动测试同步
python sync-codex-claude.py --dry-run
```

### 问题3: 后台进程找不到

```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep auto-sync
```

### 问题4: 占用资源过高

```bash
# 增加检查间隔
python auto-sync-daemon.py --interval 300  # 5分钟
```

## 📊 状态查看

守护进程状态保存在：`~/.claude/auto-sync-state.json`

```json
{
  "sync_count": 42,
  "last_sync_time": "2026-08-23T15:30:00"
}
```

## 🆚 对比手动同步

| 特性 | 手动同步 | 自动守护进程 |
|------|---------|-------------|
| 触发方式 | 手动运行 | 自动检测 |
| 响应速度 | 需要记得运行 | 实时（按间隔） |
| 使用场景 | 偶尔同步 | 持续开发 |
| 资源占用 | 0（不运行时） | 很低（后台） |
| 适合人群 | 轻度用户 | 重度用户 |

## 💡 使用建议

1. **开发时启用**: 开发期间启动守护进程
2. **合理间隔**: 根据修改频率选择间隔
3. **定期查看日志**: 确保同步正常
4. **配合手动同步**: 重要修改后手动同步一次确认

## 🔗 相关命令

```bash
# 查看守护进程状态
cat ~/.claude/auto-sync-state.json

# 查看实时日志
tail -f auto-sync.log

# 停止守护进程
auto-sync stop

# 重启守护进程
auto-sync stop && auto-sync background
```

## ⚠️ 注意事项

1. **网络环境**: 守护进程在本地运行，无需网络
2. **文件冲突**: 如果两边同时修改，后修改的会覆盖
3. **删除操作**: 使用 `--no-delete` 可以禁用删除同步
4. **重启工具**: 同步后仍需重启 Codex/Claude Code 加载配置

---

**推荐**: 开发期间启用自动同步，配合偶尔的手动同步验证
