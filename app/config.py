import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))
    BASE_URL: str = os.environ.get("BASE_URL", "/")
    
    TARGET_URL: str | None = os.environ.get("TARGET_URL")
    
    if not TARGET_URL:
        raise ValueError("TARGET_URL environment variable is not set")

    # 設定靜態資源路徑
    RESOURCE_PATH = os.environ.get("RESOURCE_PATH", "static")

    # 設定 SSL 憑證路徑
    ssl_keyfile = os.path.join("certs", "key.pem")
    ssl_certfile = os.path.join("certs", "cert.pem")
