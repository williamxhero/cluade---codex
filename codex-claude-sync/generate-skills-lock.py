#!/usr/bin/env python3
"""
生成包含所有技能的 skills-lock.json
"""

import json
from pathlib import Path

claude_skills = Path(r"C:\Users\will\.claude\skills")
project_root = Path(r"D:\WILL\AGENT\agent")

# 扫描所有技能
skills_dict = {}

for skill_dir in sorted(claude_skills.iterdir()):
    if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            skills_dict[skill_dir.name] = "USER_SKILL"

# 生成 skills-lock.json
skills_lock = {
    "version": 1,
    "skills": skills_dict
}

# 写入项目目录
output_file = project_root / "skills-lock.json"
output_file.write_text(json.dumps(skills_lock, indent=2, ensure_ascii=False), encoding='utf-8')

print(f"✅ 已生成 skills-lock.json")
print(f"   位置: {output_file}")
print(f"   包含技能数: {len(skills_dict)}")
print()
print("前 10 个技能:")
for i, name in enumerate(list(skills_dict.keys())[:10], 1):
    print(f"  {i}. {name}")

if len(skills_dict) > 10:
    print(f"  ... 还有 {len(skills_dict) - 10} 个")

print()
print("下一步:")
print("1. 重启 Claude Code")
print("2. 打开此项目")
print("3. 检查 Settings → Skills")
