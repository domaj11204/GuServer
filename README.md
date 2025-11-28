# GuServer

這是一個輕量級的本地 API 伺服器，作為Gu系統的中轉站

## 技術堆疊

*   **語言**: Python 3.12+
*   **框架**: FastAPI
*   **資料庫**: SQLite (`chat_logs.db`)
*   **套件管理**: uv 

## 快速開始

本專案使用 `uv` 進行依賴管理與執行。

### 啟動伺服器
直接執行目錄下的 `start_server.bat` 即可。

或者手動執行：
```powershell
# uv 會自動建立虛擬環境並安裝所有依賴
uv run python -m uvicorn main:app --host 127.0.0.1 --port 7979 --reload
```

伺服器啟動後，API 文件位於：`http://127.0.0.1:7979/docs`

## 開發指南

*   **新增依賴**: `uv add <package_name>`
*   **更新依賴**: `uv lock --upgrade`
*   **同步環境**: `uv sync`

## 專案結構
*   `main.py`: 伺服器入口與 API 定義
*   `database.py`: 資料庫連線設定
*   `models.py`: 資料表模型定義
*   `pyproject.toml`: 專案設定與依賴清單
