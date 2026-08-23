# Codex ↔ Claude Code 配置同步工具

完整的 Codex 和 Claude Code 配置迁移与双向同步解决方案。

## 🎯 功能特性

- ✅ **完整迁移**: 一次性迁移所有配置（Skills、Commands、Hooks、MCP 等）
- ✅ **双向同步**: 智能的双向配置同步工具
- ✅ **增量更新**: 支持增删改操作
- ✅ **安全保护**: 预览模式、冲突检测、新文件保护
- ✅ **简单易用**: 一键启动脚本

## 🚀 快速开始

### 1. 首次迁移（如果还没迁移）

```bash
cd codex-claude-sync
python codex-to-claude-migrator-v1.1.py
```

这会将所有 Codex 配置迁移到 Claude Code：
- 56 个 Skills（来自 `.codex/skills` 和 `.agents/skills`）
- 14 个 Commands
- 5 个 Hooks
- MCP 服务器配置
- 全局配置和设置

### 2. 日常同步

```bash
# Windows
sync preview           # 预览模式
sync                   # 双向自动同步

# Linux/Mac
./sync.sh preview
./sync.sh
```

## 📝 使用场景

### 场景 1: 在 Codex 中新增了技能
```bash
sync to-claude         # 同步到 Claude Code
# 然后重启 Claude Code
```

### 场景 2: 在 Claude Code 中修改了配置
```bash
sync to-codex          # 同步回 Codex
# 然后重启 Codex
```

### 场景 3: 不确定哪边有变化
```bash
sync                   # 自动判断并双向同步
```

## 🛠️ 工具说明

### 核心工具

| 文件 | 说明 |
|------|------|
| `sync-codex-claude.py` | 双向同步工具（主要工具） |
| `sync.bat` | Windows 快捷脚本 |
| `sync.sh` | Linux/Mac 快捷脚本 |
| `codex-to-claude-migrator-v1.1.py` | 单向迁移工具（首次使用） |

### 同步命令

```bash
sync                   # 双向自动同步（推荐）
sync preview          # 预览模式，不实际修改
sync to-claude        # 仅同步 Codex → Claude Code
sync to-codex         # 仅同步 Claude Code → Codex
sync help             # 显示帮助
```

## 📖 文档

- [README-SYNC-TOOL.md](./README-SYNC-TOOL.md) - 完整使用文档
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

如需修改路径，编辑 `sync-codex-claude.py` 中的路径配置。

## ⚠️ 重要提示

1. **首次使用建议预览**
   ```bash
   sync preview
   ```

2. **同步后需要重启**
   - 修改了 Codex 配置 → 重启 Codex
   - 修改了 Claude Code 配置 → 重启 Claude Code

3. **安全建议**
   - 首次使用前备份重要配置
   - 使用 `--no-delete` 可以禁用删除同步
   - 遇到冲突时会提示，不会自动处理

## 📊 同步内容

当前版本支持：
- ✅ Skills
- ✅ Commands
- ✅ Hooks

未来计划：
- ⏳ MCP 服务器配置同步
- ⏳ 全局配置文件同步
- ⏳ 核心设置同步

## 🎯 工作原理

### 智能同步策略

1. **修改时间比较**: 比较两边文件的修改时间
2. **自动判断方向**: 较新的版本同步到较旧的一边
3. **操作检测**:
   - 新增：一边有，另一边没有 → 复制过去
   - 修改：两边都有但时间不同 → 同步较新版本
   - 删除：可选是否同步删除操作

### 安全保护

- **预览模式**: `--dry-run` 不实际修改文件
- **冲突检测**: 两边同时修改会标记为冲突
- **新文件保护**: 7 天内的新文件不会被误删
- **可选删除**: `--no-delete` 禁用删除同步

## 🧪 测试

```bash
# 运行测试
python sync-codex-claude.py --dry-run

# 查看详细测试指南
cat TEST-SYNC-TOOL.md
```

## 📈 版本历史

### v2.0 (2026-08-23)
- ✨ 双向同步支持
- ✨ 智能修改时间比较
- ✨ 冲突检测
- ✨ 预览模式
- ✨ 单向同步选项

### v1.1 (2026-08-23)
- ✨ 支持 `.agents/skills` 目录
- ✨ 迁移所有 56 个技能

### v1.0 (2026-08-23)
- 🎉 初始版本

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可

MIT License

## 🙏 致谢

感谢 Codex 和 Claude Code 团队提供优秀的工具。

---

**项目主页**: https://github.com/williamxhero/cluade---codex  
**问题反馈**: https://github.com/williamxhero/cluade---codex/issues
