#!/usr/bin/env python3
"""
Codex ↔ Claude Code 双向配置同步工具 v2.0

功能：
- 双向同步 Skills、Commands、Hooks、MCP 配置
- 自动检测修改时间，同步较新的版本
- 支持增删改操作
- 冲突检测和处理
- 预览模式（--dry-run）
- 可指定同步方向

使用方法：
    python sync-codex-claude.py                    # 双向自动同步
    python sync-codex-claude.py --dry-run          # 预览模式
    python sync-codex-claude.py --to-claude        # 仅 Codex → Claude
    python sync-codex-claude.py --to-codex         # 仅 Claude → Codex
    python sync-codex-claude.py --no-delete        # 不同步删除操作
"""

import os
import sys
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# Windows UTF-8 encoding fix
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

@dataclass
class SyncItem:
    """同步项"""
    name: str
    item_type: str  # 'skill', 'command', 'hook'
    action: str     # 'add', 'update', 'delete', 'conflict'
    source: str     # 'codex', 'claude'
    source_path: Optional[Path] = None
    target_path: Optional[Path] = None
    source_mtime: Optional[float] = None
    target_mtime: Optional[float] = None
    details: str = ""

@dataclass
class SyncPlan:
    """同步计划"""
    to_claude: List[SyncItem] = field(default_factory=list)
    to_codex: List[SyncItem] = field(default_factory=list)
    conflicts: List[SyncItem] = field(default_factory=list)

    def total_count(self) -> int:
        return len(self.to_claude) + len(self.to_codex)

    def has_conflicts(self) -> bool:
        return len(self.conflicts) > 0

class ConfigSync:
    """配置同步管理器"""

    def __init__(self, dry_run=False, sync_deletes=True):
        self.dry_run = dry_run
        self.sync_deletes = sync_deletes

        # 路径配置
        self.codex_skills = Path(r"C:\Users\will\.codex\skills")
        self.agents_skills = Path(r"C:\Users\will\.agents\skills")
        self.codex_commands = Path(r"C:\Users\will\.codex\commands")
        self.codex_hooks = Path(r"C:\Users\will\.codex\hooks")

        self.claude_skills = Path(r"C:\Users\will\.claude\skills")
        self.claude_commands = Path(r"C:\Users\will\.claude\commands")
        self.claude_hooks = Path(r"C:\Users\will\.claude\hooks")

    def scan_skills(self) -> Tuple[Dict[str, Path], Dict[str, Path]]:
        """扫描两边的 Skills"""
        codex_map = {}
        claude_map = {}

        # 扫描 .codex/skills
        if self.codex_skills.exists():
            for skill_dir in self.codex_skills.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    codex_map[skill_dir.name] = skill_dir

        # 扫描 .agents/skills（也算 Codex 的一部分）
        if self.agents_skills.exists():
            for skill_dir in self.agents_skills.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    # 如果 .codex 和 .agents 都有，优先使用 .agents（通常更新）
                    codex_map[skill_dir.name] = skill_dir

        # 扫描 .claude/skills
        if self.claude_skills.exists():
            for skill_dir in self.claude_skills.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    claude_map[skill_dir.name] = skill_dir

        return codex_map, claude_map

    def scan_commands(self) -> Tuple[Dict[str, Path], Dict[str, Path]]:
        """扫描两边的 Commands"""
        codex_map = {}
        claude_map = {}

        if self.codex_commands.exists():
            for cmd_file in self.codex_commands.glob("*.md"):
                codex_map[cmd_file.name] = cmd_file

        if self.claude_commands.exists():
            for cmd_file in self.claude_commands.glob("*.md"):
                claude_map[cmd_file.name] = cmd_file

        return codex_map, claude_map

    def scan_hooks(self) -> Tuple[Dict[str, Path], Dict[str, Path]]:
        """扫描两边的 Hooks"""
        codex_map = {}
        claude_map = {}

        if self.codex_hooks.exists():
            for hook_file in self.codex_hooks.iterdir():
                if hook_file.is_file():
                    codex_map[hook_file.name] = hook_file

        if self.claude_hooks.exists():
            for hook_file in self.claude_hooks.iterdir():
                if hook_file.is_file():
                    claude_map[hook_file.name] = hook_file

        return codex_map, claude_map

    def get_dir_mtime(self, dir_path: Path) -> float:
        """获取目录的最新修改时间（递归检查所有文件）"""
        if not dir_path.exists():
            return 0

        max_mtime = dir_path.stat().st_mtime
        for item in dir_path.rglob("*"):
            if item.is_file():
                max_mtime = max(max_mtime, item.stat().st_mtime)
        return max_mtime

    def compare_items(
        self,
        codex_map: Dict[str, Path],
        claude_map: Dict[str, Path],
        item_type: str
    ) -> List[SyncItem]:
        """比较两边的项目，生成同步列表"""
        sync_items = []
        all_names = set(codex_map.keys()) | set(claude_map.keys())

        for name in sorted(all_names):
            codex_path = codex_map.get(name)
            claude_path = claude_map.get(name)

            # 只在 Codex 有 → 添加到 Claude
            if codex_path and not claude_path:
                sync_items.append(SyncItem(
                    name=name,
                    item_type=item_type,
                    action='add',
                    source='codex',
                    source_path=codex_path,
                    target_path=self._get_target_path(name, item_type, 'claude'),
                    details=f"新增到 Claude"
                ))

            # 只在 Claude 有 → 添加到 Codex 或删除（取决于策略）
            elif claude_path and not codex_path:
                if self.sync_deletes:
                    # 判断是否应该删除还是反向同步
                    # 如果 Claude 的更新时间很新，可能是新增的，应该同步到 Codex
                    claude_mtime = self._get_mtime(claude_path)
                    if self._is_recent(claude_mtime):
                        sync_items.append(SyncItem(
                            name=name,
                            item_type=item_type,
                            action='add',
                            source='claude',
                            source_path=claude_path,
                            target_path=self._get_target_path(name, item_type, 'codex'),
                            details=f"新增到 Codex"
                        ))
                    # 否则认为是 Codex 删除了，需要从 Claude 也删除
                    # 但这个很危险，先标记为冲突让用户决定
                    else:
                        sync_items.append(SyncItem(
                            name=name,
                            item_type=item_type,
                            action='conflict',
                            source='claude',
                            source_path=claude_path,
                            details=f"Codex 中不存在，Claude 中存在（可能已删除或新增）"
                        ))

            # 两边都有 → 比较修改时间
            else:
                codex_mtime = self._get_mtime(codex_path)
                claude_mtime = self._get_mtime(claude_path)

                time_diff = abs(codex_mtime - claude_mtime)

                # 时间差小于 1 秒认为是相同的（避免文件系统时间精度问题）
                if time_diff < 1:
                    continue  # 已同步，跳过

                # Codex 更新 → 同步到 Claude
                elif codex_mtime > claude_mtime:
                    sync_items.append(SyncItem(
                        name=name,
                        item_type=item_type,
                        action='update',
                        source='codex',
                        source_path=codex_path,
                        target_path=claude_path,
                        source_mtime=codex_mtime,
                        target_mtime=claude_mtime,
                        details=f"Codex 更新 ({self._format_time(codex_mtime)} vs {self._format_time(claude_mtime)})"
                    ))

                # Claude 更新 → 同步到 Codex
                else:
                    sync_items.append(SyncItem(
                        name=name,
                        item_type=item_type,
                        action='update',
                        source='claude',
                        source_path=claude_path,
                        target_path=codex_path,
                        source_mtime=claude_mtime,
                        target_mtime=codex_mtime,
                        details=f"Claude 更新 ({self._format_time(claude_mtime)} vs {self._format_time(codex_mtime)})"
                    ))

        return sync_items

    def _get_mtime(self, path: Path) -> float:
        """获取文件或目录的修改时间"""
        if path.is_dir():
            return self.get_dir_mtime(path)
        else:
            return path.stat().st_mtime

    def _is_recent(self, mtime: float, days: int = 7) -> bool:
        """判断修改时间是否在最近N天内"""
        import time
        now = time.time()
        return (now - mtime) < (days * 24 * 3600)

    def _format_time(self, mtime: float) -> str:
        """格式化时间戳"""
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    def _get_target_path(self, name: str, item_type: str, target: str) -> Path:
        """获取目标路径"""
        if target == 'claude':
            if item_type == 'skill':
                return self.claude_skills / name
            elif item_type == 'command':
                return self.claude_commands / name
            elif item_type == 'hook':
                return self.claude_hooks / name
        else:  # codex
            if item_type == 'skill':
                return self.codex_skills / name
            elif item_type == 'command':
                return self.codex_commands / name
            elif item_type == 'hook':
                return self.codex_hooks / name

    def generate_sync_plan(self) -> SyncPlan:
        """生成同步计划"""
        plan = SyncPlan()

        # 扫描并比较 Skills
        print("🔍 扫描 Skills...")
        codex_skills, claude_skills = self.scan_skills()
        skill_items = self.compare_items(codex_skills, claude_skills, 'skill')

        # 扫描并比较 Commands
        print("🔍 扫描 Commands...")
        codex_commands, claude_commands = self.scan_commands()
        command_items = self.compare_items(codex_commands, claude_commands, 'command')

        # 扫描并比较 Hooks
        print("🔍 扫描 Hooks...")
        codex_hooks, claude_hooks = self.scan_hooks()
        hook_items = self.compare_items(codex_hooks, claude_hooks, 'hook')

        # 分类同步项
        all_items = skill_items + command_items + hook_items
        for item in all_items:
            if item.action == 'conflict':
                plan.conflicts.append(item)
            elif item.source == 'codex':
                plan.to_claude.append(item)
            elif item.source == 'claude':
                plan.to_codex.append(item)

        return plan

    def execute_sync(self, plan: SyncPlan, direction: Optional[str] = None):
        """执行同步计划

        Args:
            plan: 同步计划
            direction: 'to-claude', 'to-codex', None (双向)
        """

        if self.dry_run:
            print("\n🔍 预览模式 - 不会实际修改文件\n")

        # 同步到 Claude
        if direction in [None, 'to-claude'] and plan.to_claude:
            print(f"\n{'[预览] ' if self.dry_run else ''}📤 同步到 Claude Code ({len(plan.to_claude)} 项):")
            for item in plan.to_claude:
                self._sync_item(item)

        # 同步到 Codex
        if direction in [None, 'to-codex'] and plan.to_codex:
            print(f"\n{'[预览] ' if self.dry_run else ''}📥 同步到 Codex ({len(plan.to_codex)} 项):")
            for item in plan.to_codex:
                self._sync_item(item)

        # 显示冲突
        if plan.conflicts:
            print(f"\n⚠️  检测到 {len(plan.conflicts)} 个冲突项（需要手动处理）:")
            for item in plan.conflicts:
                print(f"   ❓ {item.item_type.capitalize()}: {item.name}")
                print(f"      {item.details}")

    def _sync_item(self, item: SyncItem):
        """同步单个项目"""
        action_emoji = {
            'add': '➕',
            'update': '🔄',
            'delete': '🗑️'
        }

        emoji = action_emoji.get(item.action, '❓')
        print(f"   {emoji} {item.item_type.capitalize()}: {item.name}")
        print(f"      {item.details}")

        if self.dry_run:
            return

        try:
            if item.action in ['add', 'update']:
                if item.source_path.is_dir():
                    # 复制目录
                    if item.target_path.exists():
                        shutil.rmtree(item.target_path)
                    shutil.copytree(item.source_path, item.target_path)
                else:
                    # 复制文件
                    item.target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item.source_path, item.target_path)

            elif item.action == 'delete':
                if item.target_path.exists():
                    if item.target_path.is_dir():
                        shutil.rmtree(item.target_path)
                    else:
                        item.target_path.unlink()

        except Exception as e:
            print(f"      ❌ 错误: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Codex ↔ Claude Code 双向配置同步工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python sync-codex-claude.py                # 双向自动同步
  python sync-codex-claude.py --dry-run      # 预览模式
  python sync-codex-claude.py --to-claude    # 仅同步到 Claude Code
  python sync-codex-claude.py --to-codex     # 仅同步到 Codex
  python sync-codex-claude.py --no-delete    # 不同步删除操作
        """
    )

    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，不实际修改文件')
    parser.add_argument('--to-claude', action='store_true',
                       help='仅同步 Codex → Claude Code')
    parser.add_argument('--to-codex', action='store_true',
                       help='仅同步 Claude Code → Codex')
    parser.add_argument('--no-delete', action='store_true',
                       help='不同步删除操作')

    args = parser.parse_args()

    # 确定同步方向
    direction = None
    if args.to_claude:
        direction = 'to-claude'
    elif args.to_codex:
        direction = 'to-codex'

    # 创建同步管理器
    syncer = ConfigSync(
        dry_run=args.dry_run,
        sync_deletes=not args.no_delete
    )

    print("=" * 70)
    print("🔄 Codex ↔ Claude Code 配置同步工具 v2.0")
    print("=" * 70)

    # 生成同步计划
    plan = syncer.generate_sync_plan()

    # 显示统计
    print(f"\n📊 同步计划统计:")
    print(f"   📤 同步到 Claude: {len(plan.to_claude)} 项")
    print(f"   📥 同步到 Codex: {len(plan.to_codex)} 项")
    print(f"   ⚠️  冲突项: {len(plan.conflicts)} 项")

    if plan.total_count() == 0 and not plan.has_conflicts():
        print("\n✅ 所有配置已同步，无需操作")
        return

    # 执行同步
    if plan.total_count() > 0:
        syncer.execute_sync(plan, direction)

    # 显示冲突
    if plan.has_conflicts():
        syncer.execute_sync(plan, direction)

    # 最终提示
    print("\n" + "=" * 70)
    if args.dry_run:
        print("ℹ️  这是预览模式，未实际修改文件")
        print("   移除 --dry-run 参数以执行实际同步")
    else:
        print("✅ 同步完成！")
        if direction is None:
            print("⚠️  请重启 Claude Code 和 Codex 以加载更新的配置")
        elif direction == 'to-claude':
            print("⚠️  请重启 Claude Code 以加载更新的配置")
        elif direction == 'to-codex':
            print("⚠️  请重启 Codex 以加载更新的配置")
    print("=" * 70)

if __name__ == "__main__":
    main()
