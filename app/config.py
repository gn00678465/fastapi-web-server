""" 應用程式設定 """
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """應用程式設定類別"""
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))
    BASE_URL: str = os.environ.get("BASE_URL", "/")
    
    TARGET_URL: str | None = os.environ.get("TARGET_URL")
    
    if not TARGET_URL:
        raise ValueError("TARGET_URL environment variable is not set")

    # 設定靜態資源路徑
    RESOURCE_DIR = os.environ.get("RESOURCE_DIR", "static")
    RESOURCE_SUB_DIRS: list[str] = os.environ.get("RESOURCE_SUB_DIRS", [])

    # 設定 SSL 憑證路徑 - 轉換為絕對路徑
    _ssl_keyfile_env = os.environ.get("SSL_KEYFILE")
    _ssl_certfile_env = os.environ.get("SSL_CERTFILE")
    
    # 如果是相對路徑，則相對於專案根目錄
    SSL_KEYFILE: Path | None = None
    SSL_CERTFILE: Path | None = None
    
    if _ssl_keyfile_env:
        if os.path.isabs(_ssl_keyfile_env):
            SSL_KEYFILE = Path(_ssl_keyfile_env)
        else:
            # 相對路徑，相對於專案根目錄
            project_root = Path(__file__).parent.parent
            SSL_KEYFILE = project_root / _ssl_keyfile_env
    
    if _ssl_certfile_env:
        if os.path.isabs(_ssl_certfile_env):
            SSL_CERTFILE = Path(_ssl_certfile_env)
        else:
            # 相對路徑，相對於專案根目錄
            project_root = Path(__file__).parent.parent
            SSL_CERTFILE = project_root / _ssl_certfile_env

    # 檢查 SSL 檔案是否存在
    HAS_SSL: bool = bool(
        SSL_KEYFILE and SSL_CERTFILE and 
        SSL_KEYFILE.is_file() and SSL_CERTFILE.is_file()
    )
