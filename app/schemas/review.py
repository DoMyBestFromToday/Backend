from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# --- 共通モデル ---

class Taste1Enum(str, Enum):
    sweet = "甘口"
    dry = "辛口"
    bitter = "苦み"

class UserProfile(BaseModel):
    taste1: Taste1Enum = Field(..., description='ユーザーの味の好み（甘口、辛口、苦みから一つ）')
    taste2: List[str] = Field(..., description='ユーザーの味の好み（酸っぱい、渋いなど、複数選択可）')
    aroma_preference: List[str] = Field(..., description='ユーザーの香りの好みのリスト (例: ["柑橘系", "フルーティー"])')
    alcohol_type_preference: List[str] = Field(..., description='ユーザーがよく飲んでいるお酒の種類のリスト (例: ["純米酒", "赤ワイン", "IPAビール"])')


# --- レビュー再生成API (/regenerate-review) 用 ---

class RegenerateReviewRequest(BaseModel):
    original_review: str
    product_info: str
    category: str = Field(..., description='お酒のカテゴリ (例: "日本酒", "ワイン", "ビール")')
    user_profile: Optional[UserProfile] = None

class RegenerateReviewResponse(BaseModel):
    regenerated_review: str

class RegenerateReviewResult(BaseModel):
    product_info: str
    regenerated_review: str

# --- ユーザープロフィール取得API (/user-profile) 用 ---

class UserProfileRequest(BaseModel):
    review_history: List[str]
    product_info_history: List[str]
