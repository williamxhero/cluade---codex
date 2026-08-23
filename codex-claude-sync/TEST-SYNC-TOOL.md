# 测试同步工具

## 测试步骤

### 1. 基本功能测试
```bash
# 测试帮助信息
python sync-codex-claude.py --help

# 测试预览模式
python sync-codex-claude.py --dry-run

# 测试单向同步预览
python sync-codex-claude.py --to-claude --dry-run
python sync-codex-claude.py --to-codex --dry-run
```

### 2. 实际同步测试

**场景 A: 创建新技能并同步**
```bash
# 1. 在 Codex 中创建测试技能
mkdir "C:\Users\will\.codex\skills\test-skill"
echo "---
name: test-skill
description: Test skill for sync
---
# Test Skill" > "C:\Users\will\.codex\skills\test-skill\SKILL.md"

# 2. 预览同步
python sync-codex-claude.py --dry-run

# 3. 执行同步
python sync-codex-claude.py --to-claude

# 4. 验证
ls "C:\Users\will\.claude\skills\test-skill"

# 5. 清理
rm -rf "C:\Users\will\.codex\skills\test-skill"
rm -rf "C:\Users\will\.claude\skills\test-skill"
```

**场景 B: 修改现有技能并同步**
```bash
# 1. 修改 Claude Code 中的某个技能
touch "C:\Users\will\.claude\skills\grill-me\SKILL.md"

# 2. 预览同步（应该显示需要同步到 Codex）
python sync-codex-claude.py --dry-run

# 3. 执行同步
python sync-codex-claude.py --to-codex

# 4. 验证修改时间
stat "C:\Users\will\.agents\skills\grill-me\SKILL.md"
```

**场景 C: 双向同步测试**
```bash
# 1. 在两边分别修改不同的文件
touch "C:\Users\will\.codex\skills\apex-strategy-report\SKILL.md"
touch "C:\Users\will\.claude\skills\crawler\SKILL.md"

# 2. 预览双向同步
python sync-codex-claude.py --dry-run

# 3. 执行双向同步
python sync-codex-claude.py
```

### 3. 冲突测试

```bash
# 1. 在两边修改同一个文件（制造冲突）
echo "# Modified in Codex" >> "C:\Users\will\.codex\skills\test-skill\SKILL.md"
sleep 2
echo "# Modified in Claude" >> "C:\Users\will\.claude\skills\test-skill\SKILL.md"

# 2. 运行同步（应该检测到冲突）
python sync-codex-claude.py --dry-run
```

### 4. 删除同步测试

```bash
# 1. 删除 Codex 中的某个技能
rm -rf "C:\Users\will\.codex\skills\test-skill"

# 2. 预览（应该显示要从 Claude 也删除）
python sync-codex-claude.py --dry-run

# 3. 使用 --no-delete 预览（应该不显示删除操作）
python sync-codex-claude.py --no-delete --dry-run
```

## 预期结果

### ✅ 正常输出
- 显示同步统计
- 列出需要同步的项目
- 显示操作类型（新增/修改/删除）
- 显示修改时间对比

### ✅ 预览模式
- 不实际修改文件
- 显示 "[预览]" 标记
- 提示移除 --dry-run 执行实际同步

### ✅ 冲突检测
- 检测到同时修改的文件
- 标记为冲突项
- 提示手动处理

### ✅ 错误处理
- 路径不存在时给出清晰提示
- 操作失败时显示错误信息
- 不会因为单个错误而中断整个同步

## 性能测试

```bash
# 测试大量文件的同步性能
time python sync-codex-claude.py --dry-run
```

预期：
- 56 个 Skills 扫描应该在 1 秒内完成
- 完整同步应该在 5 秒内完成

## 安全检查

- ✅ 不会覆盖更新的文件
- ✅ 删除前会检查时间
- ✅ 新文件（7天内）不会被误删
- ✅ 支持 --no-delete 禁用删除
- ✅ 预览模式不修改文件

## 已知限制

1. **不支持内容比较**
   - 只比较修改时间，不比较文件内容
   - 如果两边同时修改，只能根据时间判断

2. **目录结构假设**
   - 假设配置目录固定在 C:\Users\will\.codex 和 .claude
   - 未来可以考虑支持自定义路径

3. **MCP/配置文件未同步**
   - 当前只同步 Skills/Commands/Hooks
   - MCP 配置需要格式转换，未实现

## 改进建议

1. **添加配置文件**
   - 支持自定义路径
   - 支持忽略列表
   - 支持同步规则

2. **增强冲突处理**
   - 内容对比
   - 交互式选择
   - 三方合并

3. **支持更多配置项**
   - MCP 服务器配置
   - 全局配置文件
   - 核心设置

4. **自动化**
   - 监听文件变化
   - 后台自动同步
   - 定时同步任务
