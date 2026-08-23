@echo off
chcp 65001 >nul
REM 自动同步守护进程启动脚本

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║       Codex ↔ Claude Code 自动同步守护进程                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d %~dp0

if "%1"=="" (
    echo 🤖 启动自动同步守护进程（60秒间隔）...
    echo.
    python auto-sync-daemon.py
) else if "%1"=="fast" (
    echo 🤖 启动自动同步守护进程（30秒间隔）...
    echo.
    python auto-sync-daemon.py --interval 30
) else if "%1"=="slow" (
    echo 🤖 启动自动同步守护进程（120秒间隔）...
    echo.
    python auto-sync-daemon.py --interval 120
) else if "%1"=="background" (
    echo 🤖 在后台启动自动同步守护进程...
    start /B pythonw auto-sync-daemon.py
    echo 守护进程已在后台启动
    echo 查看日志: auto-sync.log
) else if "%1"=="stop" (
    echo ⏹️  停止守护进程...
    taskkill /IM python.exe /FI "WINDOWTITLE eq auto-sync-daemon*"
) else (
    echo ❌ 未知选项: %1
    echo.
    echo 用法:
    echo   auto-sync              - 启动（60秒间隔）
    echo   auto-sync fast         - 快速模式（30秒）
    echo   auto-sync slow         - 慢速模式（120秒）
    echo   auto-sync background   - 后台运行
    echo   auto-sync stop         - 停止
)

echo.
