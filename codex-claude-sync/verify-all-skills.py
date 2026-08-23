#!/usr/bin/env python3
"""
验证所有 Claude Code Skills 的格式正确性

检查项：
- SKILL.md 文件存在
- YAML frontmatter 格式正确
- 必需字段（name, description）存在
- 文件编码正确
"""

import sys
from pathlib import Path
import re

def check_skill_format(skill_dir: Path) -> tuple[bool, str]:
    """检查单个技能的格式"""
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md 文件不存在"

    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"读取文件失败: {e}"

    # 检查 YAML frontmatter
    if not content.startswith('---'):
        return False, "缺少 YAML frontmatter 起始标记"

    # 提取 frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "YAML frontmatter 格式不完整"

    frontmatter = parts[1]

    # 检查必需字段
    if not re.search(r'^name:\s*\S+', frontmatter, re.MULTILINE):
        return False, "缺少 name 字段"

    if not re.search(r'^description:\s*.+', frontmatter, re.MULTILINE):
        return False, "缺少 description 字段"

    return True, "格式正确"


def main():
    claude_skills = Path(r"C:\Users\will\.claude\skills")

    if not claude_skills.exists():
        print(f"❌ Claude Code skills 目录不存在: {claude_skills}")
        return 1

    print("=" * 70)
    print("验证 Claude Code Skills 格式")
    print("=" * 70)
    print()

    valid_count = 0
    invalid_count = 0
    invalid_skills = []

    skill_dirs = sorted([d for d in claude_skills.iterdir() if d.is_dir() and not d.name.startswith('.')])

    for skill_dir in skill_dirs:
        is_valid, message = check_skill_format(skill_dir)

        if is_valid:
            print(f"✅ {skill_dir.name:<30} {message}")
            valid_count += 1
        else:
            print(f"❌ {skill_dir.name:<30} {message}")
            invalid_count += 1
            invalid_skills.append((skill_dir.name, message))

    print()
    print("=" * 70)
    print(f"总计: {len(skill_dirs)} 个技能")
    print(f"✅ 有效: {valid_count}")
    print(f"❌ 无效: {invalid_count}")

    if invalid_skills:
        print()
        print("需要修复的技能:")
        for name, error in invalid_skills:
            print(f"  • {name}: {error}")
        return 1
    else:
        print()
        print("🎉 所有技能格式正确！")
        print()
        print("如果 Claude Code 仍然只显示 1 个技能，请：")
        print("1. 完全退出 Claude Code")
        print("2. 确保进程已关闭（任务管理器）")
        print("3. 重新启动 Claude Code")
        print("4. 输入 / 查看技能列表")
        return 0


if __name__ == "__main__":
    sys.exit(main())
