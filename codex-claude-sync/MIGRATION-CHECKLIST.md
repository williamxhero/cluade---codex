# ✅ Codex → Claude Code 迁移检查清单

## 立即执行：重启 Claude Code

**重要**：所有配置文件已迁移完成，但 Claude Code 需要重启才能加载新配置。

### 重启步骤
1. 完全退出 Claude Code（不是最小化，是退出）
2. 重新启动 Claude Code
3. 打开任意会话
4. 输入 `/` 查看可用的 Skills

---

## 迁移完成情况

### ✅ 已完成（100%）

| 项目 | 数量 | 状态 | 位置 |
|------|------|------|------|
| 全局指令 (AGENTS.md) | 1 | ✅ | `C:\Users\will\.claude\CLAUDE.md` |
| Skills | 15 | ✅ | `C:\Users\will\.claude\skills\` |
| Commands | 14 | ✅ | `C:\Users\will\.claude\commands\` |
| MCP 服务器 | 3 | ✅ | `C:\Users\will\.claude\mcp.json` |
| Hooks | 4 | ✅ | `C:\Users\will\.claude\hooks\` |
| 核心设置 | 1 | ✅ | `C:\Users\will\.claude\settings.json` |

### ⚠️ 需要手动处理

| 项目 | 原因 | 操作 |
|------|------|------|
| Codex 插件 (~20个) | 插件系统不兼容 | 在 Claude Code 插件市场重新安装 |

---

## 快速验证命令

重启 Claude Code 后，在终端运行以下命令验证：

```bash
# 1. 查看 Skills（应显示 15 个目录）
ls C:/Users/will/.claude/skills/

# 2. 查看 Commands（应显示 14 个 .md 文件）
ls C:/Users/will/.claude/commands/

# 3. 查看 MCP 配置
cat C:/Users/will/.claude/mcp.json

# 4. 查看全局设置
cat C:/Users/will/.claude/settings.json

# 5. 查看 Hooks
ls C:/Users/will/.claude/hooks/
```

---

## 已迁移的 15 个 Skills

在 Claude Code 中输入 `/` 应该能看到：

1. `/apex-strategy-report` - A股行业分析与策略报告
2. `/asr` - 语音识别服务
3. `/crawler` - 爬虫任务管理
4. `/cross-project-delegation` - 跨项目委托协作
5. `/develop-web-game` - Web游戏开发
6. `/frontend-skill` - 前端开发技能
7. `/imagegen` - AI图像生成
8. `/iterate-quant-strategy` - 量化策略迭代优化
9. `/project-memory-sync` - 项目记忆同步
10. `/quote-mux-server-backfill` - 行情服务器数据回填
11. `/repair-image-thread` - 修复图片线程
12. `/sleep-after-task` - 任务完成后休眠
13. `/stock-api-docs` - 股票API文档
14. `/supermind-crawler` - SuperMind爬虫
15. `/yosef-server` - Yosef服务器管理

---

## 已迁移的 14 个 Commands

快捷命令（直接输入即可）：

- `/pua` - PUA模式
- `/mama` - Mama模式
- `/flavor` - Flavor设置
- `/kpi` - KPI查看
- `/survey` - Survey调查
- `/on` / `/off` - 开关控制
- `/pro` - Pro模式
- `/p7` / `/p9` / `/p10` - 优先级设置
- `/pua-loop` / `/cancel-pua-loop` - PUA循环控制
- `/yes` - 确认命令

---

## 已配置的 3 个 MCP 服务器

- **codegraph** - 代码结构分析（tree-sitter）
- **mempalace** - 记忆宫殿（知识管理）
- **node_repl** - Node.js REPL环境

---

## 问题排查

### 问题：看到的 Skills 数量不对

**可能原因：**
1. Claude Code 未重启 ⭐ **最可能**
2. 缓存未刷新
3. 技能文件格式问题

**解决方案：**
```bash
# 步骤1: 完全退出 Claude Code
# 步骤2: 验证文件存在
ls -R C:/Users/will/.claude/skills/

# 步骤3: 检查一个技能文件
cat C:/Users/will/.claude/skills/apex-strategy-report/SKILL.md

# 步骤4: 重新启动 Claude Code
# 步骤5: 输入 / 查看技能列表
```

### 问题：Commands 不显示

Claude Code 的 commands 机制可能与 Codex 不同，需要查看官方文档确认支持情况。

### 问题：MCP 工具无法使用

```bash
# 检查 codegraph 是否安装
codegraph --version

# 检查 MCP 配置
cat C:/Users/will/.claude/mcp.json

# 查看 Claude Code 日志（如果有）
```

---

## 迁移工具使用

如果未来需要再次同步配置：

```bash
# 预览模式（不实际修改文件）
python D:/WILL/AGENT/agent/codex-to-claude-migrator.py --dry-run

# 正式迁移
python D:/WILL/AGENT/agent/codex-to-claude-migrator.py

# 查看报告
cat C:/Users/will/.claude/migration-report.txt
```

---

## 相关文档

- 📋 [完整迁移报告](./FULL-MIGRATION-REPORT.md)
- 🔧 [迁移工具说明](./README-MIGRATOR.md)
- 📊 [迁移摘要](./MIGRATION-SUMMARY.md)

---

## 当前状态

🎉 **迁移已完成！**

所有可自动迁移的配置均已成功转移到 Claude Code。

**下一步：重启 Claude Code 以加载新配置。**

---

**迁移日期**: 2026-08-23  
**迁移工具版本**: v1.0  
**迁移状态**: ✅ 成功
