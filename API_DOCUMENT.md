# APIドキュメント

このドキュメントは、利用可能なAPIエンドポイント、その機能、および期待されるリクエストとレスポンスの形式を概説します。

## エンドポイント

### 1. ユーザープロフィール生成

- **エンドポイント:** `POST /user-profile`
- **説明:** ユーザーのレビュー履歴に基づいてユーザープロフィールを生成します。

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
  "taste_preference": [
    "string"
  ],
  "aroma_preference": [
    "string"
  ],
  "sweetness_level": "string",
  "expression_habit": "string"
}
```

- `taste_preference`: ユーザーの味の好みを示す文字列のリスト (例: `["フルーティー", "軽快"]`)。
- `aroma_preference`: ユーザーの香りの好みを示す文字列のリスト (例: `["柑橘系"]`)。
- `sweetness_level`: ユーザーの甘さの好みを示す文字列 (例: `"やや甘口"`)。
- `expression_habit`: ユーザーの典型的なレビュー表現を説明する文字列 (例: `"「甘い」という表現を多用する傾向"`)。

プロフィールの生成に失敗した場合（レビュー履歴が不十分な場合など）、エンドポイントは `404 Not Found` エラーと次のボディを返します。
```json
{
    "detail": "ユーザープロファイルの作成に失敗しました。レビュー履歴が不足している可能性があります。"
}
```

### 2. レビュー再生成

- **エンドポイント:** `POST /regenerate-review`
- **説明:** 元のレビュー、製品情報、およびオプションのユーザープロフィールに基づいて、レビューをより魅力的で具体的なものに再生成します。

#### リクエストボディ

リクエストボディは、次の構造を持つJSONオブジェクトである必要があります。

```json
{
  "original_review": "string",
  "product_info": "string",
  "user_profile": {
    "taste_preference": [
      "string"
    ],
    "aroma_preference": [
      "string"
    ],
    "sweetness_level": "string",
    "expression_habit": "string"
  }
}
```

- `original_review`: ユーザーが書いた元のレビューテキスト。
- `product_info`: レビュー対象の製品に関する情報。
- `user_profile`: (オプション) ユーザープロフィールオブジェクト。提供された場合、ユーザーの好みに合わせて再生成されたレビューを調整するために使用されます。

#### レスポンスボディ

レスポンスボディは、再生成されたレビューを含むJSONオブジェクトになります。

```json
{
  "regenerated_review": "string"
}
```

- `regenerated_review`: 再生成された、より魅力的なレビューテキスト。