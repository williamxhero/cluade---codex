# Codex → Claude Code 迁移工具

完整的配置迁移工具，支持从 OpenAI Codex 迁移到 Claude Code。

## 功能特性

✅ **全量迁移支持**
- AGENTS.md → CLAUDE.md
- Skills (56+ 技能)
- MCP 服务器配置
- Hooks (钩子系统)
- 个性化设置
- 插件分析（插件系统不兼容，提供安装指南）

✅ **安全可靠**
- Dry-run 预览模式
- 智能合并已有配置
- 完整迁移报告
- 错误追踪

## 使用方法

### 1. 预览模式（推荐先运行）

```bash
python codex-to-claude-migrator.py --dry-run
```

这会显示将要迁移的内容，但不实际修改文件。

### 2. 正式迁移

```bash
python codex-to-claude-migrator.py
```

### 3. 自定义路径

```bash
python codex-to-claude-migrator.py \
  --codex-home C:/Users/will/.codex \
  --claude-home C:/Users/will/.claude
```

## 迁移内容详解

### ✅ 自动迁移

1. **AGENTS.md**
   - 合并到 CLAUDE.md
   - 保留现有内容
   - 添加 Codex 工作原则

2. **Skills (56+ 个)**
   - 完整复制技能目录
   - 保留技能结构
   - 跳过系统技能

3. **MCP 服务器**
   - 合并到 mcp.json
   - 保留现有配置
   - 支持多服务器

4. **Hooks**
   - 复制所有钩子文件
   - 包括语音提示脚本
   - 保留可执行权限

5. **设置项**
   - 模型配置
   - Reasoning effort
   - 权限模式

### ⚠️ 需要手动处理

**插件 (14 应用 + 6 MCP + 3 技能)**

Codex 和 Claude Code 的插件系统不兼容。工具会：
- 分析所有已安装插件
- 生成插件清单
- 提供重新安装指南

迁移后需要在 Claude Code 中手动安装这些插件。

## 输出

迁移完成后会生成：

1. **控制台报告** - 实时显示迁移进度
2. **migration-report.txt** - 完整迁移报告，包含：
   - 迁移统计
   - 成功/失败项目
   - 插件清单
   - 下一步指南

## 示例输出

```
🚀 开始 Codex → Claude Code 迁移...

📊 扫描 Codex 配置...
  ✓ 找到 56 个技能
  ✓ 找到 4 个钩子文件
  ✓ 找到 3 个 MCP 服务器
  ✓ 找到 14 个插件

📝 迁移 AGENTS.md...
  ✓ 已迁移到 C:\Users\will\.claude\CLAUDE.md

🎯 迁移 Skills...
  ✓ apex-strategy-report
  ✓ asr
  ✓ crawler
  ...
  完成: 54/56

🔌 迁移 MCP 服务器配置...
  ✓ codegraph
  ✓ mempalace
  ✓ node_repl

🪝 迁移 Hooks...
  ✓ turn-complete-voice.ps1
  ✓ generate-thread-title-audio.py
  ...

🔍 分析插件...
  ⚠ 以下插件需要在 Claude Code 中重新安装:
    • chrome@openai-bundled
    • documents@openai-primary-runtime
    ...

============================================================
Codex → Claude Code 迁移报告
============================================================

📊 迁移统计
------------------------------------------------------------
✓ AGENTS.md: 已迁移
✓ Skills: 54/56
✓ MCP 服务器: 3/3
✓ Hooks: 4/4
ℹ 插件分析: 14/14
✓ 设置项: 3

下一步:
1. 重启 Claude Code 以加载新配置
2. 根据上述插件列表，在 Claude Code 中重新安装插件
3. 验证 MCP 服务器、Skills 和 Hooks 是否正常工作
============================================================
```

## 依赖

```bash
pip install toml
```

## 注意事项

1. **备份**：迁移前建议备份 Claude Code 配置目录
2. **权限**：确保有读写权限
3. **插件**：插件需要手动重新安装
4. **验证**：迁移后务必测试关键功能

## 故障排除

### 找不到 Codex 配置
```bash
python codex-to-claude-migrator.py --codex-home /path/to/codex
```

### 权限错误
确保有读写权限，或使用管理员权限运行。

### 迁移失败
查看错误日志，使用 `--dry-run` 预览模式排查问题。

## 高级用法

### 只迁移特定部分

编辑脚本，注释掉不需要的迁移函数：

```python
# self.migrate_skills(codex_config)  # 跳过技能迁移
self.migrate_mcp_servers(codex_config)  # 只迁移 MCP
```

### 自定义映射规则

修改 `migrate_settings()` 中的 `mappings` 字典。

## 反向迁移

目前不支持 Claude Code → Codex 的反向迁移。

如需双向同步，请参考：
- [ai-config-sync-manager](https://github.com/slash9494/ai-config-sync-manager)
- [claude-code-codex-bridge](https://github.com/vladolaru/claude-code-codex-bridge)

## 许可证

MIT License
