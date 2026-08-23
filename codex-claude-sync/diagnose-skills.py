#!/usr/bin/env python3
"""
诊断 Claude Code Skills 识别问题
"""

import sys
import json
from pathlib import Path
import yaml
import re

def check_skill_yaml(skill_md_path):
    """检查 SKILL.md 的 YAML 格式"""
    try:
        content = skill_md_path.read_text(encoding='utf-8')

        if not content.startswith('---'):
            return False, "缺少 YAML frontmatter"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "YAML frontmatter 不完整"

        frontmatter = parts[1].strip()

        # 尝试解析 YAML
        try:
            import yaml
            data = yaml.safe_load(frontmatter)
            if not isinstance(data, dict):
                return False, "YAML 格式不是字典"
            if 'name' not in data:
                return False, "缺少 name 字段"
            if 'description' not in data:
                return False, "缺少 description 字段"
            return True, f"✓ name={data.get('name')}"
        except Exception as e:
            # YAML 解析失败，尝试简单的正则匹配
            if not re.search(r'^name:\s*\S', frontmatter, re.MULTILINE):
                return False, "name 字段格式错误"
            if not re.search(r'^description:', frontmatter, re.MULTILINE):
                return False, "description 字段格式错误"
            return True, "✓ (简单验证通过)"

    except Exception as e:
        return False, f"读取错误: {e}"

def main():
    claude_skills = Path(r"C:\Users\will\.claude\skills")

    print("=" * 70)
    print("诊断 Claude Code Skills 识别问题")
    print("=" * 70)
    print()

    if not claude_skills.exists():
        print(f"❌ 错误：skills 目录不存在")
        print(f"   路径: {claude_skills}")
        return 1

    print(f"✓ Skills 目录存在: {claude_skills}")
    print()

    # 统计
    all_dirs = [d for d in claude_skills.iterdir() if d.is_dir() and not d.name.startswith('.')]
    valid_skills = []
    invalid_skills = []

    print(f"发现 {len(all_dirs)} 个子目录")
    print()

    # 检查每个技能
    for skill_dir in sorted(all_dirs):
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            invalid_skills.append((skill_dir.name, "缺少 SKILL.md"))
            print(f"❌ {skill_dir.name:<30} 缺少 SKILL.md")
            continue

        is_valid, message = check_skill_yaml(skill_md)

        if is_valid:
            valid_skills.append(skill_dir.name)
            print(f"✅ {skill_dir.name:<30} {message}")
        else:
            invalid_skills.append((skill_dir.name, message))
            print(f"❌ {skill_dir.name:<30} {message}")

    print()
    print("=" * 70)
    print(f"总结:")
    print(f"  总目录数: {len(all_dirs)}")
    print(f"  ✅ 有效技能: {len(valid_skills)}")
    print(f"  ❌ 无效技能: {len(invalid_skills)}")
    print()

    if invalid_skills:
        print("无效技能列表:")
        for name, reason in invalid_skills:
            print(f"  • {name}: {reason}")
        print()

    # 检查 settings.json
    settings_file = Path(r"C:\Users\will\.claude\settings.json")
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text(encoding='utf-8'))
            print("✓ settings.json 存在并可读")
            if 'skills' in settings:
                print(f"  包含 skills 配置: {settings['skills']}")
            else:
                print("  ⚠️ 没有 skills 配置（可能是正常的，使用默认扫描）")
        except Exception as e:
            print(f"❌ settings.json 读取错误: {e}")
    else:
        print("⚠️ settings.json 不存在")

    print()
    print("=" * 70)
    print("可能的问题:")
    print()

    if invalid_skills:
        print("1. ❌ 有无效的技能文件需要修复")
    else:
        print("1. ✅ 所有技能文件格式正确")

    print()
    print("2. 可能的原因（如果文件都正确）：")
    print("   • Claude Code 缓存问题")
    print("   • Claude Code 版本问题")
    print("   • 技能加载机制不同")
    print("   • 需要在 UI 中手动刷新")
    print()
    print("建议操作:")
    print("  1. 完全重启 Claude Code（已尝试）")
    print("  2. 清除缓存: 删除 C:\\Users\\will\\.claude\\cache\\")
    print("  3. 检查 Claude Code 版本是否最新")
    print("  4. 查看 Claude Code 日志（如果有）")
    print("  5. 在 Settings → Skills 页面尝试刷新")

    return 0 if not invalid_skills else 1

if __name__ == "__main__":
    # 添加 UTF-8 支持
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    sys.exit(main())
