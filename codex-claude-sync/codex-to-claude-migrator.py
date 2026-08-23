#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex to Claude Code Migration Tool
====================================
迁移 OpenAI Codex 配置到 Claude Code，包括：
- 全局指令 (AGENTS.md)
- Skills (技能)
- MCP 服务器配置
- Hooks (钩子)
- 插件配置
- 个性化设置
"""

import os
import sys
import json
import shutil
import toml
from pathlib import Path
from typing import Dict, List, Any
import argparse

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class CodexToClaudeMigrator:
    def __init__(self, codex_home: str = None, claude_home: str = None, dry_run: bool = False):
        """初始化迁移器"""
        self.dry_run = dry_run

        # 设置路径
        if codex_home:
            self.codex_home = Path(codex_home)
        else:
            self.codex_home = Path.home() / ".codex"

        if claude_home:
            self.claude_home = Path(claude_home)
        else:
            self.claude_home = Path.home() / ".claude"

        # 验证路径
        if not self.codex_home.exists():
            raise FileNotFoundError(f"Codex 配置目录不存在: {self.codex_home}")

        self.claude_home.mkdir(parents=True, exist_ok=True)

        # 迁移报告
        self.report = {
            "agents_md": False,
            "skills": {"total": 0, "migrated": 0, "skipped": []},
            "mcp_servers": {"total": 0, "migrated": 0},
            "hooks": {"total": 0, "migrated": 0},
            "plugins": {"total": 0, "analyzed": 0, "notes": []},
            "settings": {"migrated": [], "skipped": []},
            "errors": []
        }

    def scan_codex_config(self) -> Dict[str, Any]:
        """扫描 Codex 配置"""
        print("📊 扫描 Codex 配置...")

        config = {
            "agents_md": self.codex_home / "AGENTS.md",
            "config_toml": self.codex_home / "config.toml",
            "skills_dir": self.codex_home / "skills",
            "hooks_dir": self.codex_home / "hooks",
            "plugins_cache": self.codex_home / "plugins" / "cache",
            "mcp_servers": {},
            "skills": [],
            "hooks": [],
            "plugins": []
        }

        # 扫描 Skills
        if config["skills_dir"].exists():
            for skill_dir in config["skills_dir"].iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        config["skills"].append(skill_dir)

        # 扫描 Hooks
        if config["hooks_dir"].exists():
            for hook_file in config["hooks_dir"].iterdir():
                if hook_file.is_file():
                    config["hooks"].append(hook_file)

        # 扫描 MCP 服务器 (从 config.toml)
        if config["config_toml"].exists():
            try:
                codex_config = toml.load(config["config_toml"])
                if "mcp_servers" in codex_config:
                    config["mcp_servers"] = codex_config["mcp_servers"]
            except Exception as e:
                self.report["errors"].append(f"读取 config.toml 失败: {e}")

        # 扫描插件
        if config["plugins_cache"].exists():
            for plugin_dir in config["plugins_cache"].iterdir():
                if plugin_dir.is_dir():
                    config["plugins"].append(plugin_dir)

        print(f"  ✓ 找到 {len(config['skills'])} 个技能")
        print(f"  ✓ 找到 {len(config['hooks'])} 个钩子文件")
        print(f"  ✓ 找到 {len(config['mcp_servers'])} 个 MCP 服务器")
        print(f"  ✓ 找到 {len(config['plugins'])} 个插件")

        return config

    def migrate_agents_md(self, codex_config: Dict) -> bool:
        """迁移 AGENTS.md"""
        print("\n📝 迁移 AGENTS.md...")

        source = codex_config["agents_md"]
        if not source.exists():
            print("  ⊘ Codex 中不存在 AGENTS.md")
            return False

        target_claude_md = self.claude_home / "CLAUDE.md"

        try:
            # 读取源文件
            with open(source, 'r', encoding='utf-8') as f:
                agents_content = f.read()

            # 检查目标文件
            if target_claude_md.exists():
                with open(target_claude_md, 'r', encoding='utf-8') as f:
                    existing_content = f.read()

                # 如果已经包含工作原则，追加而不是覆盖
                if "## 工作原则" in existing_content or "## Working Principles" in existing_content:
                    print("  ⊙ CLAUDE.md 已包含工作原则，将追加 Codex AGENTS.md 内容")
                    merged_content = existing_content + "\n\n" + "## Codex AGENTS.md 内容\n\n" + agents_content
                else:
                    merged_content = agents_content + "\n\n" + existing_content
            else:
                merged_content = agents_content

            if not self.dry_run:
                with open(target_claude_md, 'w', encoding='utf-8') as f:
                    f.write(merged_content)
                print(f"  ✓ 已迁移到 {target_claude_md}")
            else:
                print(f"  [DRY RUN] 将迁移到 {target_claude_md}")

            self.report["agents_md"] = True
            return True

        except Exception as e:
            error_msg = f"迁移 AGENTS.md 失败: {e}"
            self.report["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
            return False

    def migrate_skills(self, codex_config: Dict) -> None:
        """迁移 Skills"""
        print("\n🎯 迁移 Skills...")

        skills = codex_config["skills"]
        self.report["skills"]["total"] = len(skills)

        if not skills:
            print("  ⊘ 没有找到需要迁移的技能")
            return

        target_skills_dir = self.claude_home / "skills"
        target_skills_dir.mkdir(exist_ok=True)

        for skill_dir in skills:
            skill_name = skill_dir.name
            target_dir = target_skills_dir / skill_name

            try:
                # 跳过系统技能
                if skill_name.startswith(".system"):
                    self.report["skills"]["skipped"].append(f"{skill_name} (系统技能)")
                    continue

                if not self.dry_run:
                    if target_dir.exists():
                        shutil.rmtree(target_dir)
                    shutil.copytree(skill_dir, target_dir)
                    print(f"  ✓ {skill_name}")
                else:
                    print(f"  [DRY RUN] {skill_name}")

                self.report["skills"]["migrated"] += 1

            except Exception as e:
                error_msg = f"迁移技能 {skill_name} 失败: {e}"
                self.report["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")

        print(f"  完成: {self.report['skills']['migrated']}/{self.report['skills']['total']}")

    def migrate_mcp_servers(self, codex_config: Dict) -> None:
        """迁移 MCP 服务器配置"""
        print("\n🔌 迁移 MCP 服务器配置...")

        mcp_servers = codex_config["mcp_servers"]
        self.report["mcp_servers"]["total"] = len(mcp_servers)

        if not mcp_servers:
            print("  ⊘ 没有找到 MCP 服务器配置")
            return

        target_mcp_file = self.claude_home / "mcp.json"

        try:
            # 读取现有配置
            existing_mcp = {}
            if target_mcp_file.exists():
                with open(target_mcp_file, 'r', encoding='utf-8') as f:
                    existing_mcp = json.load(f)

            # 合并配置
            if "mcpServers" not in existing_mcp:
                existing_mcp["mcpServers"] = {}

            for server_name, server_config in mcp_servers.items():
                existing_mcp["mcpServers"][server_name] = server_config
                self.report["mcp_servers"]["migrated"] += 1
                print(f"  ✓ {server_name}")

            if not self.dry_run:
                with open(target_mcp_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_mcp, f, indent=2, ensure_ascii=False)
                print(f"  已保存到 {target_mcp_file}")
            else:
                print(f"  [DRY RUN] 将保存到 {target_mcp_file}")

        except Exception as e:
            error_msg = f"迁移 MCP 配置失败: {e}"
            self.report["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")

    def migrate_hooks(self, codex_config: Dict) -> None:
        """迁移 Hooks"""
        print("\n🪝 迁移 Hooks...")

        hooks = codex_config["hooks"]
        self.report["hooks"]["total"] = len(hooks)

        if not hooks:
            print("  ⊘ 没有找到 Hook 文件")
            return

        target_hooks_dir = self.claude_home / "hooks"
        target_hooks_dir.mkdir(exist_ok=True)

        for hook_file in hooks:
            try:
                target_file = target_hooks_dir / hook_file.name

                if not self.dry_run:
                    shutil.copy2(hook_file, target_file)
                    print(f"  ✓ {hook_file.name}")
                else:
                    print(f"  [DRY RUN] {hook_file.name}")

                self.report["hooks"]["migrated"] += 1

            except Exception as e:
                error_msg = f"迁移 Hook {hook_file.name} 失败: {e}"
                self.report["errors"].append(error_msg)
                print(f"  ✗ {error_msg}")

        print(f"  完成: {self.report['hooks']['migrated']}/{self.report['hooks']['total']}")

    def analyze_plugins(self, codex_config: Dict) -> None:
        """分析插件（插件系统不兼容，只分析不迁移）"""
        print("\n🔍 分析插件...")

        plugins = codex_config["plugins"]
        self.report["plugins"]["total"] = len(plugins)

        if not plugins:
            print("  ⊘ 没有找到插件")
            return

        print("  ⚠ 注意: Codex 和 Claude Code 的插件系统不兼容")
        print("  以下插件需要在 Claude Code 中重新安装:")

        for plugin_dir in plugins:
            marketplace = plugin_dir.parent.name
            plugin_name = plugin_dir.name

            # 尝试读取插件信息
            plugin_json = plugin_dir / ".codex-plugin" / "plugin.json"
            if plugin_json.exists():
                try:
                    with open(plugin_json, 'r', encoding='utf-8') as f:
                        plugin_info = json.load(f)
                        name = plugin_info.get("name", plugin_name)
                        desc = plugin_info.get("description", "")
                        print(f"    • {name} ({marketplace})")
                        if desc:
                            print(f"      {desc}")
                        self.report["plugins"]["notes"].append(f"{name}@{marketplace}")
                except:
                    print(f"    • {plugin_name} ({marketplace})")
            else:
                print(f"    • {plugin_name} ({marketplace})")

            self.report["plugins"]["analyzed"] += 1

    def migrate_settings(self, codex_config: Dict) -> None:
        """迁移个性化设置"""
        print("\n⚙️  迁移个性化设置...")

        source_config = codex_config["config_toml"]
        if not source_config.exists():
            print("  ⊘ 没有找到 config.toml")
            return

        try:
            codex_toml = toml.load(source_config)
            target_settings = self.claude_home / "settings.json"

            # 读取现有 Claude Code 设置
            claude_settings = {}
            if target_settings.exists():
                with open(target_settings, 'r', encoding='utf-8') as f:
                    claude_settings = json.load(f)

            # 映射配置项
            mappings = {
                "model": "model",
                "model_reasoning_effort": "effortLevel",
                "approval_policy": lambda v: {"never": "bypassPermissions"}.get(v),
            }

            for codex_key, claude_key in mappings.items():
                if codex_key in codex_toml:
                    value = codex_toml[codex_key]
                    if callable(claude_key):
                        mapped_value = claude_key(value)
                        if mapped_value and "permissions" in claude_settings:
                            claude_settings["permissions"]["defaultMode"] = mapped_value
                            self.report["settings"]["migrated"].append(f"{codex_key} -> permissions.defaultMode")
                    else:
                        # effortLevel 映射
                        if codex_key == "model_reasoning_effort":
                            value = value.lower()
                        claude_settings[claude_key] = value
                        self.report["settings"]["migrated"].append(f"{codex_key} -> {claude_key}")
                        print(f"  ✓ {codex_key} -> {claude_key}")

            if not self.dry_run:
                with open(target_settings, 'w', encoding='utf-8') as f:
                    json.dump(claude_settings, f, indent=2, ensure_ascii=False)

        except Exception as e:
            error_msg = f"迁移设置失败: {e}"
            self.report["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")

    def generate_report(self) -> str:
        """生成迁移报告"""
        report_lines = [
            "=" * 60,
            "Codex → Claude Code 迁移报告",
            "=" * 60,
            "",
            f"Codex 目录: {self.codex_home}",
            f"Claude Code 目录: {self.claude_home}",
            f"模式: {'DRY RUN (预览)' if self.dry_run else '正式迁移'}",
            "",
            "📊 迁移统计",
            "-" * 60,
            f"✓ AGENTS.md: {'已迁移' if self.report['agents_md'] else '未迁移'}",
            f"✓ Skills: {self.report['skills']['migrated']}/{self.report['skills']['total']}",
            f"✓ MCP 服务器: {self.report['mcp_servers']['migrated']}/{self.report['mcp_servers']['total']}",
            f"✓ Hooks: {self.report['hooks']['migrated']}/{self.report['hooks']['total']}",
            f"ℹ 插件分析: {self.report['plugins']['analyzed']}/{self.report['plugins']['total']}",
            f"✓ 设置项: {len(self.report['settings']['migrated'])}",
            "",
        ]

        if self.report['skills']['skipped']:
            report_lines.extend([
                "⊘ 跳过的技能:",
                *[f"  - {s}" for s in self.report['skills']['skipped']],
                ""
            ])

        if self.report['plugins']['notes']:
            report_lines.extend([
                "⚠ 需要在 Claude Code 中重新安装的插件:",
                *[f"  - {p}" for p in self.report['plugins']['notes']],
                ""
            ])

        if self.report['errors']:
            report_lines.extend([
                "❌ 错误:",
                *[f"  - {e}" for e in self.report['errors']],
                ""
            ])

        report_lines.extend([
            "=" * 60,
            "迁移完成！",
            "",
            "下一步:",
            "1. 重启 Claude Code 以加载新配置",
            "2. 根据上述插件列表，在 Claude Code 中重新安装插件",
            "3. 验证 MCP 服务器、Skills 和 Hooks 是否正常工作",
            "=" * 60
        ])

        return "\n".join(report_lines)

    def run(self) -> None:
        """执行迁移"""
        print("🚀 开始 Codex → Claude Code 迁移...")
        print()

        # 扫描
        codex_config = self.scan_codex_config()

        # 迁移
        self.migrate_agents_md(codex_config)
        self.migrate_skills(codex_config)
        self.migrate_mcp_servers(codex_config)
        self.migrate_hooks(codex_config)
        self.migrate_settings(codex_config)
        self.analyze_plugins(codex_config)

        # 生成报告
        print()
        report = self.generate_report()
        print(report)

        # 保存报告
        if not self.dry_run:
            report_file = self.claude_home / "migration-report.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 报告已保存到: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Codex to Claude Code Migration Tool - 迁移 Codex 配置到 Claude Code"
    )
    parser.add_argument(
        "--codex-home",
        help="Codex 配置目录路径 (默认: ~/.codex)"
    )
    parser.add_argument(
        "--claude-home",
        help="Claude Code 配置目录路径 (默认: ~/.claude)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际修改文件"
    )

    args = parser.parse_args()

    try:
        migrator = CodexToClaudeMigrator(
            codex_home=args.codex_home,
            claude_home=args.claude_home,
            dry_run=args.dry_run
        )
        migrator.run()
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
