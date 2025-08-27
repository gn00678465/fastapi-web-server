FROM ghcr.io/astral-sh/uv:python3.13-trixie

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 以允許 Docker 快取層
COPY . .

# 安裝相依套件
RUN uv sync

# 建立 static 和 certs 目錄以供掛載使用
RUN mkdir -p /app/static /app/certs

# 定義 static 和 certs 目錄為 volume
VOLUME /app/static /app/certs

# 設定環境變數
ENV BASE_URL="/"
ENV TARGET_URL=""
ENV HOST="0.0.0.0"
ENV PORT="3000"
ENV RESOURCE_DIR="static"
ENV RESOURCE_SUB_DIRS='["_nuxt", "_fonts"]'
ENV SSL_KEYFILE=""
ENV SSL_CERTFILE=""

# 開放埠號 (使用環境變數)
EXPOSE $PORT

# 啟動應用程式
CMD ["sh", "-c", "uv run python -m app.main"]