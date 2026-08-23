#!/usr/bin/env python3
"""
Codex ↔ Claude Code 自动同步守护进程

功能：
- 监控 Codex 和 Claude Code 配置目录的文件变化
- 自动检测修改、新增、删除操作
- 实时双向同步
- 后台运行，系统托盘图标
- 可配置同步间隔和规则

使用方法：
    python auto-sync-daemon.py                  # 启动守护进程
    python auto-sync-daemon.py --interval 30    # 每30秒检查一次
    python auto-sync-daemon.py --stop           # 停止守护进程
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Optional
import argparse
import threading
import logging

# Windows UTF-8 encoding fix
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('auto-sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FileWatcher:
    """文件监控器"""

    def __init__(self, path: Path):
        self.path = path
        self.snapshot = {}
        self.update_snapshot()

    def update_snapshot(self):
        """更新文件快照"""
        new_snapshot = {}

        if not self.path.exists():
            self.snapshot = new_snapshot
            return

        for item in self.path.rglob('*'):
            if item.is_file():
                try:
                    stat = item.stat()
                    rel_path = item.relative_to(self.path)
                    new_snapshot[str(rel_path)] = {
                        'mtime': stat.st_mtime,
                        'size': stat.st_size
                    }
                except Exception as e:
                    logger.debug(f"Error reading {item}: {e}")

        self.snapshot = new_snapshot

    def get_changes(self) -> Dict[str, Set[str]]:
        """检测变化（返回新增、修改、删除的文件）"""
        old_snapshot = self.snapshot.copy()
        self.update_snapshot()
        new_snapshot = self.snapshot

        old_files = set(old_snapshot.keys())
        new_files = set(new_snapshot.keys())

        added = new_files - old_files
        deleted = old_files - new_files

        modified = set()
        for file in old_files & new_files:
            if (old_snapshot[file]['mtime'] != new_snapshot[file]['mtime'] or
                old_snapshot[file]['size'] != new_snapshot[file]['size']):
                modified.add(file)

        return {
            'added': added,
            'modified': modified,
            'deleted': deleted
        }


class AutoSyncDaemon:
    """自动同步守护进程"""

    def __init__(self, interval: int = 60, enable_delete: bool = True):
        self.interval = interval
        self.enable_delete = enable_delete
        self.running = False
        self.sync_count = 0
        self.last_sync_time = None

        # 路径配置
        self.codex_skills = Path(r"C:\Users\will\.codex\skills")
        self.agents_skills = Path(r"C:\Users\will\.agents\skills")
        self.codex_commands = Path(r"C:\Users\will\.codex\commands")
        self.codex_hooks = Path(r"C:\Users\will\.codex\hooks")

        self.claude_skills = Path(r"C:\Users\will\.claude\skills")
        self.claude_commands = Path(r"C:\Users\will\.claude\commands")
        self.claude_hooks = Path(r"C:\Users\will\.claude\hooks")

        # 创建监控器
        self.watchers = {
            'codex_skills': FileWatcher(self.codex_skills),
            'agents_skills': FileWatcher(self.agents_skills),
            'codex_commands': FileWatcher(self.codex_commands),
            'codex_hooks': FileWatcher(self.codex_hooks),
            'claude_skills': FileWatcher(self.claude_skills),
            'claude_commands': FileWatcher(self.claude_commands),
            'claude_hooks': FileWatcher(self.claude_hooks),
        }

        # 状态文件
        self.state_file = Path.home() / '.claude' / 'auto-sync-state.json'
        self.load_state()

    def load_state(self):
        """加载状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.sync_count = state.get('sync_count', 0)
                    self.last_sync_time = state.get('last_sync_time')
                    logger.info(f"加载状态: {self.sync_count} 次同步")
            except Exception as e:
                logger.error(f"加载状态失败: {e}")

    def save_state(self):
        """保存状态"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            state = {
                'sync_count': self.sync_count,
                'last_sync_time': self.last_sync_time
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存状态失败: {e}")

    def check_and_sync(self):
        """检查并同步"""
        has_changes = False

        # 检查各个目录的变化
        for name, watcher in self.watchers.items():
            changes = watcher.get_changes()

            if changes['added'] or changes['modified'] or changes['deleted']:
                logger.info(f"检测到 {name} 的变化:")
                if changes['added']:
                    logger.info(f"  新增: {len(changes['added'])} 个文件")
                if changes['modified']:
                    logger.info(f"  修改: {len(changes['modified'])} 个文件")
                if changes['deleted']:
                    logger.info(f"  删除: {len(changes['deleted'])} 个文件")
                has_changes = True

        if has_changes:
            self.run_sync()

    def run_sync(self):
        """运行同步"""
        try:
            logger.info("开始同步...")

            # 导入同步工具
            sync_script = Path(__file__).parent / 'sync-codex-claude.py'
            if not sync_script.exists():
                logger.error("找不到 sync-codex-claude.py")
                return

            # 运行同步命令
            import subprocess
            cmd = [sys.executable, str(sync_script)]
            if not self.enable_delete:
                cmd.append('--no-delete')

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                self.sync_count += 1
                self.last_sync_time = datetime.now().isoformat()
                self.save_state()
                logger.info(f"同步完成 (第 {self.sync_count} 次)")
            else:
                logger.error(f"同步失败: {result.stderr}")

        except Exception as e:
            logger.error(f"同步出错: {e}")

    def start(self):
        """启动守护进程"""
        self.running = True
        logger.info(f"自动同步守护进程已启动 (间隔: {self.interval}秒)")
        logger.info(f"监控目录:")
        logger.info(f"  Codex Skills: {self.codex_skills}")
        logger.info(f"  Agents Skills: {self.agents_skills}")
        logger.info(f"  Claude Skills: {self.claude_skills}")
        logger.info(f"  Commands & Hooks")

        try:
            while self.running:
                self.check_and_sync()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("收到停止信号")
        finally:
            self.stop()

    def stop(self):
        """停止守护进程"""
        self.running = False
        self.save_state()
        logger.info("自动同步守护进程已停止")
        logger.info(f"总共同步: {self.sync_count} 次")


def main():
    parser = argparse.ArgumentParser(
        description='Codex ↔ Claude Code 自动同步守护进程',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python auto-sync-daemon.py                 # 启动，默认60秒间隔
  python auto-sync-daemon.py --interval 30   # 30秒间隔
  python auto-sync-daemon.py --no-delete     # 不同步删除操作
        """
    )

    parser.add_argument('--interval', type=int, default=60,
                       help='检查间隔（秒），默认60')
    parser.add_argument('--no-delete', action='store_true',
                       help='不同步删除操作')
    parser.add_argument('--stop', action='store_true',
                       help='停止守护进程')

    args = parser.parse_args()

    if args.stop:
        # TODO: 实现停止逻辑（需要 PID 文件）
        print("停止功能待实现")
        return

    # 启动守护进程
    daemon = AutoSyncDaemon(
        interval=args.interval,
        enable_delete=not args.no_delete
    )

    print("=" * 70)
    print("🔄 Codex ↔ Claude Code 自动同步守护进程")
    print("=" * 70)
    print(f"检查间隔: {args.interval} 秒")
    print(f"删除同步: {'禁用' if args.no_delete else '启用'}")
    print(f"日志文件: auto-sync.log")
    print()
    print("按 Ctrl+C 停止")
    print("=" * 70)
    print()

    daemon.start()


if __name__ == "__main__":
    main()
