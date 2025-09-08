# Review Regeneration API Backend

## 概要

このプロジェクトは、LangChainを利用して投稿されたレビューをより良い表現に書き換えるためのバックエンドAPIです。FastAPIとDockerを使用して構築されています。

## アーキテクチャ

- **Webフレームワーク**: [FastAPI](https://fastapi.tiangolo.com/) を使用しており、非同期処理による高いパフォーマンスと、自動生成されるAPIドキュメントが特徴です。
- **WSGIサーバー**: [Gunicorn](https://gunicorn.org/) をプロセスマネージャーとして利用し、Uvicornワーカーを管理することで、本番環境でのパフォーマンスと安定性を高めています。
- **コンテナ技術**: [Docker](https://www.docker.com/) と Docker Compose を使用して、開発環境と本番環境の差異をなくし、ポータビリティを確保しています。
- **LLM連携**: [LangChain](https://www.langchain.com/) ライブラリを介して大規模言語モデル (LLM) と連携し、レビューの書き換え処理を行います。

## ディレクトリ構成

```
/
├── compose.yml         # Docker Compose設定ファイル
├── Dockerfile          # Backendサービス用のDockerfile
├── requirements.txt    # Pythonの依存ライブラリ
├── .env                # (Git管理外) 環境変数を定義するファイル
├── .env.example        # .envファイルのテンプレート
├── app/                # FastAPIアプリケーションのソースコード
│   ├── main.py         # FastAPIアプリケーションのエントリポイント
│   ├── core/           # 設定ファイルなどコアなロジック
│   ├── routers/        # APIのルーティング定義
│   ├── schemas/        # リクエスト/レスポンスのデータモデル定義
│   └── services/       # ビジネスロジック（LangChainの処理など）
└── tests/              # テストコード
```

## 開発手順

### 1. 前提条件

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (Docker Desktopには同梱されています)

### 2. 環境設定

1.  プロジェクトのルートディレクトリに `.env` ファイルを作成します。`.env.example` を参考に、必要な環境変数を設定してください。

    ```bash
    cp .env.example .env
    ```

2.  `.env` ファイルを編集して、ご自身のAPIキーなどを設定します。`compose.yml` の `environment` キーで指定された変数が、コンテナに渡されます。

    ```dotenv
    # .env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

### 3. アプリケーションの起動

以下のコマンドを実行して、Dockerコンテナをビルドし、バックグラウンドで起動します。

```bash
docker compose up -d --build
```

`docker compose` はカレントディレクトリの `.env` ファイルを自動で読み込み、`compose.yml` 内の `${OPENAI_API_KEY}` をその値で置き換えてコンテナを起動します。

アプリケーションはホットリロードに対応しているため、`app/` ディレクトリ内のソースコードを変更すると、Gunicornワーカーが自動的に再起動します。

### 4. 動作確認

- **APIドキュメント (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ヘルスチェック**: [http://localhost:8000/health](http://localhost:8000/health)

### 5. アプリケーションの停止

```bash
docker compose down
```

## テストの実行

以下のコマンドで、実行中のコンテナ内で `pytest` を実行できます。

```bash
docker compose exec backend pytest
```

## 本番環境へのデプロイ (AWS ECS)

このアプリケーションをECSで公開する際の考慮点です。

1.  **Dockerイメージ**: ECR (Elastic Container Registry) にビルドしたDockerイメージをプッシュします。
2.  **環境変数**: ECSのタスク定義で、環境変数を設定します。APIキーなどの秘密情報は、**AWS Secrets Manager** や **SSM Parameter Store** を利用し、「ValueFrom」で安全にコンテナに渡すことを強く推奨します。
3.  **ヘルスチェック**: ロードバランサーのターゲットグループ設定で、ヘルスチェックパスを `/health` に指定します。これにより、コンテナが正常に動作しているかを外部から監視できます。
4.  **パフォーマンス**: `gunicorn` を導入済みのため、CPUリソースに応じたワーカー数をタスク定義で調整することで、パフォーマンスを最適化できます。
