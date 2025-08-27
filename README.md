# Fastapi web Server

一個基於 FastAPI 的 Web 伺服器專案，主要功能包括 API 代理、靜態檔案服務和前端路由支援。

## 專案概述

本專案是一個全功能的 Web 伺服器，具備以下核心功能：

- **API 代理服務**：將前端 API 請求代理轉發至後端目標伺服器
- **靜態檔案服務**：提供前端資源（HTML、CSS、JS、字體檔案等）的服務
- **SPA 路由支援**：支援單頁應用程式（SPA）的前端路由
- **SSL/HTTPS 支援**：可配置 SSL 憑證以提供安全連線
- **CORS 中介軟體**：處理跨域資源共享

## 技術堆疊

- **Python 3.13+**
- **uv**: 套件管理
- **FastAPI**：現代、快速的 Web 框架
- **Uvicorn**：ASGI 伺服器
- **httpx**：異步 HTTP 客戶端
- **Playwright**：端到端測試工具

## 專案結構

```
web-server/
├── .venv/                  # 虛擬環境（uv 自動建立）
├── app/                    # 應用程式核心
│   ├── main.py            # FastAPI 應用程式主檔案
│   ├── config.py          # 配置管理
│   ├── services/          # 服務層
│   └── utils/             # 工具函數
│       └── static_dirs.py # 靜態檔案掛載邏輯
├── static/                # 靜態資源
│   ├── index.html         # 主頁面
│   ├── _nuxt/            # Nuxt.js 建置檔案
│   └── _fonts/           # 字體檔案
├── certs/                 # SSL 憑證
│   ├── cert.pem
│   └── key.pem
├── .env                   # 環境變數設定檔案
├── pyproject.toml         # 專案配置與依賴
└── uv.lock               # 依賴版本鎖定檔案
```

## 環境變數配置

建立 `.env` 檔案並設定以下變數：

```env
# 伺服器配置
HOST=0.0.0.0
PORT=8000
BASE_URL=/

# API 代理目標
TARGET_URL=http://your-backend-server:port

# 靜態資源路徑
RESOURCE_DIR=static
# 靜態資源目錄內的子目錄（可選）
RESOURCE_SUB_DIRS=["dir_a", "dir_b"]

# SSL 憑證（可選）
SSL_KEYFILE=certs/key.pem
SSL_CERTFILE=certs/cert.pem
```

## 快速開始

### 環境準備

1. **確保已安裝 uv**：
   ```bash
   # 安裝 uv（如果尚未安裝）
   pip install uv
   ```

2. **建立並啟用虛擬環境**：
   ```bash
   # uv 會自動建立虛擬環境並同步依賴
   uv sync
   ```

   如需手動啟用虛擬環境：
   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   
   # Windows CMD
   .venv\Scripts\activate.bat
   
   # Linux/macOS
   source .venv/bin/activate
   ```

### 啟動應用程式

1. **設定環境變數**：
   複製並修改 `.env.example` 為 `.env`

2. **啟動開發伺服器**：
   ```bash
   # 使用 uv run（推薦，自動使用正確的虛擬環境）
   uv run fastapi dev app/main.py
   
   # 或者在已啟用的虛擬環境中執行
   fastapi dev app/main.py
   ```

4. **存取應用程式**：
   - 主頁面：`http://localhost:8000`
   - API 健康檢查：`http://localhost:8000/api/health`

## HTTPS 配置

本專案支援 HTTPS 安全連線，提供加密的通訊協定。

### SSL 憑證設定

1. **準備 SSL 憑證**：
   - 將憑證檔案放置於 `certs/` 目錄
   - 確保檔案名稱為 `cert.pem`（憑證）和 `key.pem`（私鑰）

2. **自簽憑證生成**（開發環境）：
   ```bash
   # 建立 certs 目錄
   mkdir certs

   # 生成自簽憑證（有效期 365 天）
   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
   ```

3. **環境變數設定**：
   ```env
   # SSL 憑證路徑
   SSL_KEYFILE=certs/key.pem
   SSL_CERTFILE=certs/cert.pem
   ```

### HTTPS 啟動

當正確設定 SSL 憑證後，伺服器將自動啟用 HTTPS：

```bash
# 啟動 HTTPS 伺服器
uv run python -m app.main
```

**存取 HTTPS 服務**：
- 安全主頁面：`https://localhost:8000`
- 安全 API：`https://localhost:8000/api/health`

### 憑證驗證邏輯

專案會自動檢查 SSL 憑證：
- 如果 `SSL_KEYFILE` 和 `SSL_CERTFILE` 都存在且有效，自動啟用 HTTPS
- 如果憑證檔案不存在或無效，回退到 HTTP 模式
- 支援相對路徑和絕對路徑的憑證配置

### 生產環境建議

1. **使用正式 CA 憑證**：
   - 從 Let's Encrypt、DigiCert 等 CA 機構取得憑證
   - 避免在生產環境使用自簽憑證

2. **憑證安全管理**：
   - 定期更新憑證
   - 保護私鑰檔案的存取權限
   - 使用環境變數管理憑證路徑

3. **反向代理配置**：
   - 考慮使用 Nginx 或 Apache 作為反向代理處理 SSL
   - 可提供更好的效能和安全性

## 主要功能

### API 代理
- 自動將 `/api/*` 路徑的請求代理至 `TARGET_URL`
- 保留原始請求標頭、查詢參數和 Cookies
- 支援所有 HTTP 方法（GET、POST、PUT、DELETE 等）

### 靜態檔案服務
- 自動掛載 `static/` 目錄下的所有檔案
- 支援 Nuxt.js 等現代前端框架的建置輸出
- 包含字體檔案、圖片、樣式表等靜態資源

### 前端路由支援
- 對於非 API 路徑，返回 `index.html` 以支援 SPA 前端路由
- 自動處理 404 錯誤頁面

## 開發說明

### 環境管理

- **虛擬環境**：專案使用 `uv` 管理虛擬環境，位於 `.venv/` 目錄
- **依賴管理**：
  - `uv add <package>` - 新增依賴套件
  - `uv remove <package>` - 移除依賴套件
  - `uv sync` - 同步依賴至虛擬環境
  - `uv lock` - 更新依賴鎖定檔案

### 開發工具

- 使用 FastAPI 的自動 API 文檔：`http://localhost:8000/docs`
- 支援熱重載開發模式
- 包含完整的 CORS 配置，適合前後端分離開發

## 版本資訊

- 版本：0.1.0
- Python 需求：>=3.13
- 主要依賴：FastAPI, Playwright, httpx