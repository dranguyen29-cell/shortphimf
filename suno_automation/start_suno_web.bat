@echo off
chcp 65001 >nul
echo ==========================================================================
echo 🎹 KHOI DONG SUNO DIRECT STUDIO WEB SERVER (PORT 8088)
echo ==========================================================================
cd /d "%~dp0"
start "" "http://localhost:8088"
python web_server.py
pause

