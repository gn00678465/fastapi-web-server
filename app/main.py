""" 主應用程式入口 """
import os
from pathlib import Path
import httpx

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, RedirectResponse
from dotenv import load_dotenv

from app.config import Config
from app.utils.static_dirs import setup_static_dirs

# 載入環境變數
load_dotenv()

app = FastAPI(
    title="Web server"
)

# 設定 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，生產環境應設定為特定來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有標頭
)

# 根路徑重定向到 devicemanage
@app.get("/")
async def redirect_to_base_url():
    """根路徑重定向到環境變數的 BASE_URL"""
    if Config.BASE_URL != '/':
        return RedirectResponse(Config.BASE_URL)

@app.api_route(f"{Config.BASE_URL}/api/{{path:path}}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def api_proxy(path: str, request: Request):
    """API 代理路由處理器"""
    print(f"API proxy called: {request.method} {request.url.path}")
    target_url = f"{Config.TARGET_URL}{request.url.path}"
    
    # 處理查詢參數
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"
    
    print(f"Forwarding request to: {target_url}")
    
    try:
        # 取得請求內容
        content = await request.body()
        
        # 改進標頭處理 - 只過濾必要標頭，保留更多原始標頭
        headers = dict(request.headers.items())
        
        # 僅移除絕對必要的標頭
        if 'host' in headers:
            del headers['host']
        if 'content-length' in headers:
            del headers['content-length']
            
        # 輸出轉發的標頭，協助除錯
        # print(f"Forwarding headers: {headers}")
        
        # 建立非同步客戶端並轉發請求
        async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=content,
                timeout=30.0,  # 設定較長的逾時時間
                cookies=request.cookies,  # 轉發 cookies
            )
        # # 輸出回應資訊
        # print(f"API 回應: 狀態碼={response.status_code}, 內容類型={response.headers.get('content-type')}")
        # print(f"回應標頭: {response.headers}")

        # 構建回應並返回
        resp = Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

        # 確保回應不會被快取
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp

    except Exception as e:
        print(f"API proxy error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"API proxy error: {str(e)}")

@app.get(f"{Config.BASE_URL}")
async def read_index():
    """
    處理首頁
    """
    index_path = Path(Config.RESOURCE_DIR) / "index.html"
    if index_path.is_file():
        return FileResponse(index_path)

        # 若 index.html 不存在，建立一個簡單的預設頁面
    return Response(
        content="""
        <html>
        <head><title>Web Server</title></head>
        <body>
            <h1>Welcome to Web Server</h1>
            <p>Static resources are available at <a href="/static/">/static/</a></p>
            <p>Available static files structure:</p>
        </body>
        </html>
        """,
        media_type="text/html"
    )

# 處理其他前端路由
@app.get(f"{Config.BASE_URL}/{{path:path}}")
async def catch_all(path: str, request: Request):
    """
    處理所有其他路由
    """
    # 明確排除 API 路徑
    if path.startswith("api/"):
        print(f"Warning: API request fell into catch_all: {request.url.path}")
        raise HTTPException(status_code=404, detail="API endpoint does not exist")

    # 檢查是否為靜態檔案
    file_path = Path(Config.RESOURCE_DIR) / path
    if file_path.is_file():
        return FileResponse(file_path)

    # 返回 index.html 以支援前端路由
    index_path = Path(Config.RESOURCE_DIR) / "index.html"
    if index_path.is_file():
        return FileResponse(index_path)

    # 若 index.html 不存在，顯示錯誤訊息
    return Response(
        content=f"<html><body><h1>Page not found</h1><p>Requested path: {path}</p></body></html>",
        media_type="text/html",
        status_code=404
    )


# API 路由群組
@app.get("/api/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "message": "API 運作正常"}

# 掛載靜態資源（注意路徑配置）
if os.path.exists(Config.RESOURCE_DIR):
    setup_static_dirs(
        app,
        Config.BASE_URL,
        Config.RESOURCE_DIR,
        Config.RESOURCE_SUB_DIRS
    )

def run_server():
    """ 啟動 Uvicorn 伺服器"""
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        ssl_keyfile=str(Config.SSL_KEYFILE) if Config.HAS_SSL else None,
        ssl_certfile=str(Config.SSL_CERTFILE) if Config.HAS_SSL else None
    )

if __name__ == "__main__":
    run_server()