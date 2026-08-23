# Codex ↔ Claude Code 配置同步工具

双向同步 Codex 和 Claude Code 之间的配置，支持增删改操作。

## 功能特性

- ✅ 双向自动同步（基于修改时间）
- ✅ 支持 Skills、Commands、Hooks 同步
- ✅ 自动检测新增、修改、删除
- ✅ 冲突检测和提示
- ✅ 预览模式（--dry-run）
- ✅ 可指定单向同步
- ✅ 安全的删除策略

## 快速开始

### 基本用法

```bash
# 双向自动同步
python sync-codex-claude.py

# 预览模式（不实际修改文件）
python sync-codex-claude.py --dry-run

# 仅同步到 Claude Code
python sync-codex-claude.py --to-claude

# 仅同步到 Codex
python sync-codex-claude.py --to-codex

# 不同步删除操作
python sync-codex-claude.py --no-delete
```

### 典型场景

**场景 1: 在 Codex 中新增了一个 Skill**
```bash
# 同步到 Claude Code
python sync-codex-claude.py --to-claude
```

**场景 2: 在 Claude Code 中修改了一个 Command**
```bash
# 同步回 Codex
python sync-codex-claude.py --to-codex
```

**场景 3: 不确定哪边有更新**
```bash
# 先预览
python sync-codex-claude.py --dry-run

# 确认后执行
python sync-codex-claude.py
```

## 同步策略

### 修改时间比较

工具通过比较文件/目录的修改时间来判断哪边更新：
- 如果 Codex 的文件更新 → 同步到 Claude Code
- 如果 Claude Code 的文件更新 → 同步到 Codex
- 如果时间差小于 1 秒 → 认为已同步，跳过

### 新增检测

- 一边有，另一边没有 → 自动添加到另一边
- 新增的文件会完整复制（包括子目录和所有文件）

### 删除处理

默认情况下：
- 如果一边删除了某项，另一边也会删除
- 但如果另一边的文件很新（7天内修改），会标记为冲突而不是直接删除

使用 `--no-delete` 可以禁用删除同步，只进行新增和修改。

### 冲突处理

以下情况会被标记为冲突，需要手动处理：
- 一边删除，另一边是最近新增/修改的
- 两边都修改了同一文件（目前未实现内容比较）

## 支持的配置项

### Skills
- **Codex 路径**:
  - `C:\Users\will\.codex\skills\`
  - `C:\Users\will\.agents\skills\`（共享技能库）
- **Claude Code 路径**: `C:\Users\will\.claude\skills\`

### Commands
- **Codex 路径**: `C:\Users\will\.codex\commands\`
- **Claude Code 路径**: `C:\Users\will\.claude\commands\`

### Hooks
- **Codex 路径**: `C:\Users\will\.codex\hooks\`
- **Claude Code 路径**: `C:\Users\will\.claude\hooks\`

### 未来支持

- MCP 服务器配置同步（需要格式转换）
- 全局配置同步（AGENTS.md ↔ CLAUDE.md）
- 核心设置同步（config.toml ↔ settings.json）

## 命令行选项

```
usage: sync-codex-claude.py [-h] [--dry-run] [--to-claude] [--to-codex] [--no-delete]

options:
  -h, --help    显示帮助信息
  --dry-run     预览模式，不实际修改文件
  --to-claude   仅同步 Codex → Claude Code
  --to-codex    仅同步 Claude Code → Codex
  --no-delete   不同步删除操作
```

## 输出示例

```
======================================================================
🔄 Codex ↔ Claude Code 配置同步工具 v2.0
======================================================================
🔍 扫描 Skills...
🔍 扫描 Commands...
🔍 扫描 Hooks...

📊 同步计划统计:
   📤 同步到 Claude: 2 项
   📥 同步到 Codex: 1 项
   ⚠️  冲突项: 0 项

📤 同步到 Claude Code (2 项):
   ➕ Skill: new-skill
      新增到 Claude
   🔄 Command: updated-command.md
      Codex 更新 (2026-08-23 15:30:00 vs 2026-08-20 10:00:00)

📥 同步到 Codex (1 项):
   🔄 Skill: modified-skill
      Claude 更新 (2026-08-23 14:00:00 vs 2026-08-22 09:00:00)

======================================================================
✅ 同步完成！
⚠️  请重启 Claude Code 和 Codex 以加载更新的配置
======================================================================
```

## 安全性

- ✅ 所有操作前都会检查文件/目录是否存在
- ✅ 删除操作有额外的时间检查，避免误删新文件
- ✅ 支持 `--dry-run` 预览，不会实际修改
- ✅ 错误处理：操作失败时会显示错误信息并继续

## 注意事项

1. **首次使用建议先预览**
   ```bash
   python sync-codex-claude.py --dry-run
   ```

2. **同步后需要重启**
   - Claude Code 和 Codex 都需要重启才能加载新配置

3. **备份重要配置**
   - 虽然工具很安全，但首次使用前建议备份配置目录

4. **冲突处理**
   - 遇到冲突时，工具不会自动处理
   - 手动检查冲突文件，决定保留哪个版本

5. **.agents 目录**
   - `.agents/skills/` 被视为 Codex 的一部分
   - 优先级：`.agents` > `.codex`（当同名技能存在于两个目录时）

## 工作流程建议

### 日常开发流程

1. 在任意一边（Codex 或 Claude Code）修改配置
2. 运行同步工具：`python sync-codex-claude.py`
3. 重启相应的工具以加载更新

### 定期同步

可以设置定时任务（如每天运行一次）：

**Windows 任务计划程序**:
```bash
schtasks /create /tn "Sync Codex Claude" /tr "python D:\WILL\AGENT\agent\sync-codex-claude.py" /sc daily /st 09:00
```

**Linux/Mac Cron**:
```bash
0 9 * * * cd /path/to/agent && python sync-codex-claude.py
```

## 故障排查

### 问题1: 权限错误
**解决**: 以管理员身份运行

### 问题2: 编码错误（Windows）
**解决**: 工具已内置 UTF-8 编码修复

### 问题3: 同步后看不到新技能
**解决**: 完全重启 Claude Code/Codex（不是最小化）

### 问题4: 提示路径不存在
**解决**: 确保配置目录存在：
```bash
mkdir -p C:/Users/will/.claude/skills
mkdir -p C:/Users/will/.claude/commands
mkdir -p C:/Users/will/.claude/hooks
```

## 相关文档

- [完整迁移报告](./FULL-MIGRATION-REPORT.md)
- [迁移工具 v1.1](./codex-to-claude-migrator-v1.1.py) - 单向迁移工具

## 版本历史

### v2.0 (2026-08-23)
- ✨ 新功能：双向同步支持
- ✨ 新功能：基于修改时间的智能同步
- ✨ 新功能：冲突检测
- ✨ 新功能：预览模式
- ✨ 新功能：可选同步方向
- ✨ 新功能：可选删除同步

### v1.1 (2026-08-23)
- ✨ 支持 `.agents/skills/` 目录
- 🐛 修复了 Windows 编码问题

### v1.0 (2026-08-23)
- 🎉 初始版本：单向迁移工具

## 贡献

欢迎提交问题和改进建议！

## 许可

MIT License
