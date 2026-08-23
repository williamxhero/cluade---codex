#!/bin/bash
# 自动同步守护进程启动脚本

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       Codex ↔ Claude Code 自动同步守护进程                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

case "$1" in
    "")
        echo "🤖 启动自动同步守护进程（60秒间隔）..."
        echo ""
        python3 auto-sync-daemon.py
        ;;
    "fast")
        echo "🤖 启动自动同步守护进程（30秒间隔）..."
        echo ""
        python3 auto-sync-daemon.py --interval 30
        ;;
    "slow")
        echo "🤖 启动自动同步守护进程（120秒间隔）..."
        echo ""
        python3 auto-sync-daemon.py --interval 120
        ;;
    "background")
        echo "🤖 在后台启动自动同步守护进程..."
        nohup python3 auto-sync-daemon.py > auto-sync.log 2>&1 &
        echo "守护进程已在后台启动 (PID: $!)"
        echo "查看日志: auto-sync.log"
        echo "停止: kill $!"
        echo $! > auto-sync.pid
        ;;
    "stop")
        echo "⏹️  停止守护进程..."
        if [ -f auto-sync.pid ]; then
            kill $(cat auto-sync.pid) 2>/dev/null && echo "已停止" || echo "进程未运行"
            rm auto-sync.pid
        else
            pkill -f auto-sync-daemon.py && echo "已停止" || echo "进程未运行"
        fi
        ;;
    *)
        echo "❌ 未知选项: $1"
        echo ""
        echo "用法:"
        echo "  ./auto-sync.sh              - 启动（60秒间隔）"
        echo "  ./auto-sync.sh fast         - 快速模式（30秒）"
        echo "  ./auto-sync.sh slow         - 慢速模式（120秒）"
        echo "  ./auto-sync.sh background   - 后台运行"
        echo "  ./auto-sync.sh stop         - 停止"
        exit 1
        ;;
esac

echo ""
