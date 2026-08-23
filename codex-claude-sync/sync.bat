@echo off
chcp 65001 >nul
REM Codex ↔ Claude Code 配置同步工具
REM 快速启动脚本

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          Codex ↔ Claude Code 配置同步工具                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d D:\WILL\AGENT\agent

if "%1"=="" (
    echo 🔄 执行双向自动同步...
    echo.
    python sync-codex-claude.py
) else if "%1"=="preview" (
    echo 🔍 预览模式...
    echo.
    python sync-codex-claude.py --dry-run
) else if "%1"=="to-claude" (
    echo 📤 同步到 Claude Code...
    echo.
    python sync-codex-claude.py --to-claude
) else if "%1"=="to-codex" (
    echo 📥 同步到 Codex...
    echo.
    python sync-codex-claude.py --to-codex
) else if "%1"=="help" (
    python sync-codex-claude.py --help
) else (
    echo ❌ 未知选项: %1
    echo.
    echo 用法:
    echo   sync              - 双向自动同步
    echo   sync preview      - 预览模式
    echo   sync to-claude    - 仅同步到 Claude
    echo   sync to-codex     - 仅同步到 Codex
    echo   sync help         - 显示帮助
)

echo.
pause
