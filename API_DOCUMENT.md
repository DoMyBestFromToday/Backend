# APIドキュメント

このドキュメントは、利用可能なAPIエンドポイント、その機能、および期待されるリクエストとレスポンスの形式を概説します。

## エンドポイント

### 1. ユーザープロフィール生成

- **エンドポイント:** `POST /user-profile`
- **説明:** ユーザーのレビュー履歴に基づいて、そのユーザーのお酒の好みに関するプロフィールを生成します。

#### リクエストボディ

リクエストボディは、次の構造を持つJSONオブジェクトである必要があります。

```json
{
  "review_history": [
    "string"
  ],
  "product_info_history": [
    "string"
  ]
}
```

- `review_history`: ユーザーが書いたレビューの文字列のリスト。
- `product_info_history`: `review_history`の同じインデックスにあるレビューに対応する製品情報の文字列のリスト。

#### レスポンスボディ

レスポンスボディは、ユーザーのプロフィールを表すJSONオブジェクトになります。

```json
{
  "taste1": "string",
  "taste2": [
    "string"
  ],
  "aroma_preference": [
    "string"
  ],
  "alcohol_type_preference": [
    "string"
  ]
}
```

- `taste1`: ユーザーの最も基本的な味の好み（`"甘口"`, `"辛口"`, `"苦み"`のいずれか）。
- `taste2`: その他の味の好みを示す文字列のリスト (例: `["酸っぱい", "渋い", "フルーティー"]`)。
- `aroma_preference`: ユーザーの香りの好みを示す文字列のリスト (例: `["柑橘系", "芳醇"]`)。
- `alcohol_type_preference`: ユーザーがよく飲むお酒の種類を示す文字列のリスト (例: `["純米酒", "赤ワイン", "IPAビール"]`)。

プロフィールの生成に失敗した場合（レビュー履歴が不十分な場合など）、エンドポイントは `404 Not Found` エラーと次のボディを返します。
```json
{
    "detail": "ユーザープロファイルの作成に失敗しました。レビュー履歴が不足している可能性があります。"
}
```

### 2. レビュー再生成

- **エンドポイント:** `POST /regenerate-review`
- **説明:** 元のレビュー、製品情報、お酒のカテゴリ、およびオプションのユーザープロフィールに基づいて、レビューから個人的なバイアスを除去し、より客観的な内容に書き換えます。

#### リクエストボディ

リクエストボディは、次の構造を持つJSONオブジェクトである必要があります。

```json
{
  "original_review": "string",
  "product_info": "string",
  "category": "string",
  "user_profile": {
    "taste1": "string",
    "taste2": [
      "string"
    ],
    "aroma_preference": [
      "string"
    ],
    "alcohol_type_preference": [
      "string"
    ]
  }
}
```

- `original_review`: ユーザーが書いた元のレビューテキスト。
- `product_info`: レビュー対象の製品に関する情報。
- `category`: レビュー対象のお酒のカテゴリ (例: `"日本酒"`, `"ワイン"`, `"ビール"`)。
- `user_profile`: (オプション) ユーザープロフィールオブジェクト。提供された場合、ユーザーの好みに合わせてバイアス除去の精度を高めるために使用されます。

#### レスポンスボディ

レスポンスボディは、再生成されたレビューを含むJSONオブジェクトになります。

```json
{
  "regenerated_review": "string"
}
```

- `regenerated_review`: 再生成された、より客観的なレビューテキスト。
