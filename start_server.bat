@echo off
cd /d %~dp0
uv run python -m uvicorn main:app --reload --port 7979
pause
