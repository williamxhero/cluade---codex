# Codex ↔ Claude Code 配置同步工具

完整的 Codex 和 Claude Code 配置迁移与双向同步解决方案。

## 🎯 功能特性

- ✅ **完整迁移**: 一次性迁移所有配置（Skills、Commands、Hooks、MCP 等）
- ✅ **双向同步**: 智能的双向配置同步工具
- ✅ **自动同步**: 后台守护进程，实时监控并自动同步 ⭐ **新功能**
- ✅ **增量更新**: 支持增删改操作
- ✅ **安全保护**: 预览模式、冲突检测、新文件保护
- ✅ **简单易用**: 一键启动脚本

## 🚀 快速开始

### 1. 首次迁移（如果还没迁移）

```bash
cd codex-claude-sync
python codex-to-claude-migrator-v1.1.py
```

### 2. 手动同步

```bash
# Windows
sync preview           # 预览
sync                   # 同步

# Linux/Mac
./sync.sh preview
./sync.sh
```

### 3. 自动同步 ⭐ **推荐**

```bash
# Windows
auto-sync              # 启动自动同步（60秒间隔）
auto-sync fast         # 快速模式（30秒）
auto-sync background   # 后台运行

# Linux/Mac
./auto-sync.sh
./auto-sync.sh fast
./auto-sync.sh background
```

## 📖 使用方式

### 方式一：手动同步（按需）

适合：偶尔修改配置的用户

```bash
# 修改配置后手动运行
sync
```

### 方式二：自动同步（推荐）⭐

适合：频繁修改配置的开发者

```bash
# 启动后自动监控和同步
auto-sync background

# 查看日志
tail -f auto-sync.log
```

## 🛠️ 工具说明

### 核心工具

| 文件 | 说明 | 使用场景 |
|------|------|---------|
| `sync-codex-claude.py` | 双向同步工具 | 手动同步 |
| `auto-sync-daemon.py` | 自动同步守护进程 ⭐ | 持续开发 |
| `sync.bat / sync.sh` | 手动同步快捷脚本 | 快速同步 |
| `auto-sync.bat / auto-sync.sh` | 自动同步快捷脚本 ⭐ | 后台运行 |
| `codex-to-claude-migrator-v1.1.py` | 迁移工具 | 首次迁移 |

### 命令对比

**手动同步**:
```bash
sync                   # 双向同步
sync preview          # 预览模式
sync to-claude        # 单向：Codex → Claude
sync to-codex         # 单向：Claude → Codex
```

**自动同步** ⭐:
```bash
auto-sync             # 启动（60秒间隔）
auto-sync fast        # 快速（30秒间隔）
auto-sync background  # 后台运行
auto-sync stop        # 停止
```

## 📝 使用场景

### 场景 1: 开发期间（推荐自动同步）

```bash
# 早上开始工作
auto-sync background

# 一天的工作中，任何修改都会自动同步
# 无需手动操作

# 晚上停止（可选，关机会自动停止）
auto-sync stop
```

### 场景 2: 偶尔修改（手动同步）

```bash
# 修改后运行一次
sync
```

### 场景 3: 测试新功能（快速自动同步）

```bash
# 快速响应模式
auto-sync fast

# 测试完成后停止
auto-sync stop
```

## 📚 文档

- [README-SYNC-TOOL.md](./README-SYNC-TOOL.md) - 手动同步完整文档
- [README-AUTO-SYNC.md](./README-AUTO-SYNC.md) - 自动同步完整文档 ⭐
- [快速使用-一键同步.md](./快速使用-一键同步.md) - 快速上手指南
- [项目总结-Codex-Claude-同步.md](./项目总结-Codex-Claude-同步.md) - 项目总结
- [TEST-SYNC-TOOL.md](./TEST-SYNC-TOOL.md) - 测试指南

## 🔧 安装

### 克隆仓库

```bash
git clone https://github.com/williamxhero/cluade---codex.git
cd cluade---codex/codex-claude-sync
```

### 依赖

Python 3.6+ （无需额外依赖）

## ⚙️ 配置

工具默认使用以下路径：

- **Codex 配置**:
  - `C:\Users\will\.codex\`
  - `C:\Users\will\.agents\`
  
- **Claude Code 配置**:
  - `C:\Users\will\.claude\`

如需修改路径，编辑相应的 `.py` 文件中的路径配置。

## 🆚 手动 vs 自动

| 特性 | 手动同步 | 自动同步 ⭐ |
|------|---------|------------|
| 触发方式 | 手动运行 | 自动检测 |
| 响应速度 | 即时 | 按间隔（30-120秒） |
| 资源占用 | 运行时占用 | 后台低占用（~10MB） |
| 适合场景 | 偶尔修改 | 持续开发 |
| 使用难度 | 需要记得运行 | 一次启动，持续工作 |

**建议**: 开发期间使用自动同步，偶尔使用手动同步验证

## ⚠️ 重要提示

1. **同步后需要重启**
   - 修改了 Codex 配置 → 重启 Codex
   - 修改了 Claude Code 配置 → 重启 Claude Code
   - 自动同步会同步文件，但工具仍需手动重启

2. **自动同步日志**
   ```bash
   # 查看自动同步日志
   tail -f auto-sync.log        # Linux/Mac
   Get-Content auto-sync.log -Tail 20 -Wait  # Windows
   ```

3. **安全建议**
   - 首次使用建议先用手动同步的预览模式
   - 自动同步默认启用删除同步，使用 `--no-delete` 可以禁用
   - 查看日志确保同步正常

## 📊 同步内容

当前版本支持：
- ✅ Skills（56 个）
- ✅ Commands（14 个）
- ✅ Hooks（5 个）

未来计划：
- ⏳ MCP 服务器配置同步
- ⏳ 全局配置文件同步
- ⏳ 核心设置同步

## 🎯 工作原理

### 手动同步
1. 扫描两边目录
2. 比较修改时间
3. 同步较新版本

### 自动同步 ⭐
1. 后台监控文件变化
2. 检测到修改后自动调用手动同步
3. 记录日志和状态
4. 低资源占用，持续运行

## 🧪 测试

```bash
# 测试手动同步
python sync-codex-claude.py --dry-run

# 测试自动同步
python auto-sync-daemon.py --interval 10  # 10秒间隔测试
```

## 📈 版本历史

### v2.1 (2026-08-23) - 自动同步
- ✨ 新增自动同步守护进程
- ✨ 实时文件监控
- ✨ 后台运行支持
- ✨ 详细日志记录

### v2.0 (2026-08-23) - 双向同步
- ✨ 双向同步支持
- ✨ 智能修改时间比较
- ✨ 冲突检测

### v1.1 (2026-08-23) - 完整迁移
- ✨ 支持 `.agents/skills` 目录
- ✨ 迁移所有 56 个技能

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可

MIT License

---

**项目主页**: https://github.com/williamxhero/cluade---codex  
**问题反馈**: https://github.com/williamxhero/cluade---codex/issues

**推荐使用**: 自动同步守护进程 - 一次启动，持续工作！⭐
