# Review Regeneration API Backend

## 概要

このプロジェクトは、LangChainを利用して投稿されたレビューをより良い表現に書き換えるためのバックエンドAPIです。FastAPIを使用して構築されています。

## 主な技術スタック

- **Webフレームワーク**: [FastAPI](https://fastapi.tiangolo.com/) を使用しており、非同期処理による高いパフォーマンスと、自動生成されるAPIドキュメントが特徴です。
- **LLM連携**: [LangChain](https://www.langchain.com/) ライブラリを介して大規模言語モデル (LLM) と連携し、レビューの書き換え処理を行います。
- **コンテナ技術**: [Docker](https://www.docker.com/) と Docker Compose を使用して、開発環境と本番環境の差異をなくし、ポータビリティを確保しています。
- **本番サーバー**: [Gunicorn](https://gunicorn.org/) をプロセスマネージャーとして利用し、Uvicornワーカーを管理することで、本番環境でのパフォーマンスと安定性を高めています。

## ディレクトリ構成

```
/
├── compose.yml         # Docker Compose設定ファイル
├── Dockerfile          # Backendサービス用のDockerfile
├── requirements.txt    # Pythonの依存ライブラリ
├── requirements-dev.txt # Pythonの依存ライブラリ (開発・テスト用)
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

---

## 開発環境のセットアップ

開発方法は、Dockerを利用する方法と、ローカルのPython環境を直接利用する方法の2通りがあります。

### 1. Dockerを利用した開発 (推奨)

コンテナ技術を利用して、環境差異を気にせずに開発を進める方法です。

#### 前提条件
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### 手順
1.  **.envファイルの準備**
    `.env.example`をコピーして`.env`ファイルを作成し、お使いのOpenAI APIキーを設定します。
    ```bash
    cp .env.example .env
    ```
    ```dotenv
    # .env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

2.  **コンテナの起動**
    以下のコマンドでコンテナをビルドし、バックグラウンドで起動します。
    ```bash
    docker compose up -d --build
    ```
    ホットリロードが有効なため、`app/`ディレクトリ内のソースコードを更新すると、サーバーが自動で再起動します。

3.  **動作確認**
    - **APIドキュメント (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ヘルスチェック**: [http://localhost:8000/health](http://localhost:8000/health)

4.  **コンテナの停止**
    ```bash
    docker compose down
    ```

### 2. ローカルPython環境での開発

Dockerを使わず、お使いのPCのPython環境で直接開発やテストを行う方法です。

#### 前提条件
- Python 3.10 以降

#### 手順
1.  **仮想環境の構築 (推奨)**
    プロジェクトルートで以下のコマンドを実行し、仮想環境を作成・有効化します。
    ```bash
    # 仮想環境を作成
    python3 -m venv venv
    # 仮想環境を有効化 (macOS/Linux)
    source venv/bin/activate
    # (Windowsの場合は `venv\Scripts\activate` を実行)
    ```

2.  **依存ライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

3.  **.envファイルの準備**
    Dockerの場合と同様に、`.env.example`をコピーしてAPIキーを設定します。
    ```bash
    cp .env.example .env
    ```

4.  **開発サーバーの起動**
    以下のコマンドで、Uvicornサーバーを起動します。
    ```bash
    uvicorn app.main:app --reload
    ```

---

## テストの実行

### Dockerコンテナ内での実行
```bash
docker compose exec backend pytest
```

### ローカル環境での実行
```bash
python3 -m pytest
```
特定のテストのみを実行したい場合は、ファイルや関数を指定します。
```bash
python3 -m pytest tests/test_review.py::test_health_check
```

---

## 本番環境へのデプロイ (AWS ECS)

このアプリケーションをECSで公開する際の考慮点です。

1.  **Dockerイメージ**: ECR (Elastic Container Registry) にビルドしたDockerイメージをプッシュします。
2.  **環境変数**: ECSのタスク定義で、環境変数を設定します。APIキーなどの秘密情報は、**AWS Secrets Manager** や **SSM Parameter Store** を利用し、「ValueFrom」で安全にコンテナに渡すことを強く推奨します。
3.  **ヘルスチェック**: ロードバランサーのターゲットグループ設定で、ヘルスチェックパスを `/health` に指定します。
4.  **パフォーマンス**: `gunicorn` を導入済みのため、CPUリソースに応じたワーカー数をタスク定義で調整することで、パフォーマンスを最適化できます。