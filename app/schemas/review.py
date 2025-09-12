from pydantic import BaseModel, Field
from typing import List, Optional

# --- 共通モデル ---

class UserProfile(BaseModel):
    taste_preference: List[str] = Field(..., description='ユーザーの味の好みのリスト (例: ["フルーティー", "軽快"])')
    aroma_preference: List[str] = Field(..., description='ユーザーの香りの好みのリスト (例: ["柑橘系"])')
    sweetness_level: str = Field(..., description='ユーザーの甘さの好みの度合い (例: "やや甘口")')
    expression_habit: str = Field(..., description='ユーザーのレビュー表現の癖 (例: "「甘い」という表現を多用する傾向")')

# --- レビュー再生成API (/regenerate-review) 用 ---

class RegenerateReviewRequest(BaseModel):
    original_review: str
    product_info: str
    user_profile: Optional[UserProfile] = None

class RegenerateReviewResponse(BaseModel):
    regenerated_review: str

# --- ユーザープロフィール取得API (/user-profile) 用 ---

class UserProfileRequest(BaseModel):
    review_history: List[str]
    product_info_history: List[str]