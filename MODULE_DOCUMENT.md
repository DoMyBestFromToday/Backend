# 使用しているOSS・ライブラリ・API

このプロジェクトで使用しているOSS、ライブラリ、APIについてまとめます。

## ライブラリ

| ライブラリ名 | 公式URL | ライセンス | 利用理由 |
|---|---|---|---|
| fastapi | https://fastapi.tiangolo.com/ | MIT License | APIサーバーを構築するため。MITライセンスのため、商用利用も可能であり、問題ないと判断しました。 |
| uvicorn | https://www.uvicorn.org/ | BSD-3-Clause License | ASGIサーバーとしてFastAPIを動作させるため。BSDライセンスのため、問題ないと判断しました。 |
| pydantic | https://docs.pydantic.dev/ | MIT License | データバリデーションとスキーマ定義のため。FastAPIと連携して使用します。MITライセンスのため、問題ないと判断しました。 |
| langchain | https://www.langchain.com/ | MIT License | 大規模言語モデル（LLM）を利用したアプリケーションを構築するため。MITライセンスのため、問題ないと判断しました。 |
| langchain-openai | https://pypi.org/project/langchain-openai/ | MIT License | LangChainでOpenAIのモデルを利用するため。MITライセンスのため、問題ないと判断しました。 |
| python-dotenv | https://pypi.org/project/python-dotenv/ | BSD 3-Clause License | 環境変数を.envファイルから読み込むため。BSDライセンスのため、問題ないと判断しました。 |
| pydantic-settings | https://docs.pydantic.dev/latest/usage/pydantic_settings/ | MIT License | Pydanticモデルを使用して設定を管理するため。MITライセンスのため、問題ないと判断しました。 |
| gunicorn | https://gunicorn.org/ | MIT License | 本番環境でFastAPIアプリケーションを動作させるためのWSGIサーバーとして利用するため。MITライセンスのため、問題ないと判断しました。 |
| pytest | https://docs.pytest.org/ | MIT License | テストフレームワークとして利用するため。MITライセンスのため、問題ないと判断しました。 |
| pytest-mock | https://pypi.org/project/pytest-mock/ | MIT License | テストでモックオブジェクトを使用するため。MITライセンスのため、問題ないと判断しました。 |
| httpx | https://www.python-httpx.org/ | BSD-3-Clause License | テストで非同期HTTPリクエストを送信するため。BSDライセンスのため、問題ないと判断しました。 |

## API

| API名 | 公式URL | ライセンス | 利用理由 |
|---|---|---|---|
| OpenAI API | https://openai.com/api/ | - | レビューの感情分析や要約機能で利用するため。利用規約に基づき、適切に利用します。 |
