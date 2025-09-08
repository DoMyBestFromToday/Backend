# 1. ベースイメージとして公式のPythonイメージを使用
FROM python:3.11-slim

# 2. 環境変数を設定
# PYTHONUNBUFFERED: Pythonの出力がバッファリングされず、直接ターミナルに表示されるようにする
# これにより、DockerのログでPythonのprint出力などをリアルタイムで確認できる
ENV PYTHONUNBUFFERED 1

# 3. 作業ディレクトリを作成・設定
WORKDIR /app

# 4. 依存関係ファイルをコピーし、インストール
# まずrequirements.txtだけをコピーすることで、Dockerのレイヤーキャッシュを有効活用する
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 5. アプリケーションコードをコピー
COPY ./app /app/app

# 6. gunicornを起動するコマンドを設定
# -w: ワーカープロセスの数（CPUコア数に応じて調整）
# -k: Uvicornワーカークラスを指定
# --bind: 0.0.0.0:8000 でコンテナの外部からアクセス可能にする
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
