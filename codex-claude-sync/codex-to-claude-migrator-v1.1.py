#!/usr/bin/env python3
"""
Codex to Claude Code Migration Tool - v1.1
完整版：支持 .codex 和 .agents 两个目录的迁移
"""

import os
import sys
import shutil
import json
from pathlib import Path

# Windows UTF-8 encoding fix
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def migrate_all_skills():
    """迁移所有技能：从 .codex 和 .agents 目录"""

    codex_skills = Path(r"C:\Users\will\.codex\skills")
    agents_skills = Path(r"C:\Users\will\.agents\skills")
    claude_skills = Path(r"C:\Users\will\.claude\skills")

    claude_skills.mkdir(parents=True, exist_ok=True)

    migrated_count = 0
    sources = []

    # 迁移 .codex/skills
    if codex_skills.exists():
        for skill_dir in codex_skills.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                target_dir = claude_skills / skill_dir.name
                if not target_dir.exists():
                    shutil.copytree(skill_dir, target_dir)
                    migrated_count += 1
                    sources.append(f"  ✅ {skill_dir.name} (from .codex)")

    # 迁移 .agents/skills
    if agents_skills.exists():
        for skill_dir in agents_skills.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                target_dir = claude_skills / skill_dir.name
                if not target_dir.exists():
                    shutil.copytree(skill_dir, target_dir)
                    migrated_count += 1
                    sources.append(f"  ✅ {skill_dir.name} (from .agents)")
                else:
                    sources.append(f"  ⏭️  {skill_dir.name} (已存在，跳过)")

    return migrated_count, sources

def main():
    print("🚀 Codex → Claude Code 完整迁移工具 v1.1\n")
    print("=" * 60)

    # 迁移 Skills
    print("\n📁 迁移 Skills...")
    count, sources = migrate_all_skills()
    print(f"   迁移了 {count} 个技能")
    for source in sources[:10]:  # 只显示前 10 个
        print(source)
    if len(sources) > 10:
        print(f"   ... 还有 {len(sources) - 10} 个")

    # 统计最终结果
    claude_skills = Path(r"C:\Users\will\.claude\skills")
    total_skills = len([d for d in claude_skills.iterdir() if d.is_dir() and not d.name.startswith('.')])

    print("\n" + "=" * 60)
    print(f"\n✅ 迁移完成！")
    print(f"   Claude Code 现在有 {total_skills} 个技能")
    print(f"\n⚠️  请重启 Claude Code 以加载新技能")
    print("=" * 60)

if __name__ == "__main__":
    main()
