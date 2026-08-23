#!/bin/bash
# Codex ↔ Claude Code 配置同步工具
# 快速启动脚本 (Linux/Mac)

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          Codex ↔ Claude Code 配置同步工具                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

case "$1" in
    "")
        echo "🔄 执行双向自动同步..."
        echo ""
        python3 sync-codex-claude.py
        ;;
    "preview")
        echo "🔍 预览模式..."
        echo ""
        python3 sync-codex-claude.py --dry-run
        ;;
    "to-claude")
        echo "📤 同步到 Claude Code..."
        echo ""
        python3 sync-codex-claude.py --to-claude
        ;;
    "to-codex")
        echo "📥 同步到 Codex..."
        echo ""
        python3 sync-codex-claude.py --to-codex
        ;;
    "help")
        python3 sync-codex-claude.py --help
        ;;
    *)
        echo "❌ 未知选项: $1"
        echo ""
        echo "用法:"
        echo "  ./sync.sh              - 双向自动同步"
        echo "  ./sync.sh preview      - 预览模式"
        echo "  ./sync.sh to-claude    - 仅同步到 Claude"
        echo "  ./sync.sh to-codex     - 仅同步到 Codex"
        echo "  ./sync.sh help         - 显示帮助"
        exit 1
        ;;
esac

echo ""
