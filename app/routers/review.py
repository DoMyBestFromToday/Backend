from fastapi import APIRouter, HTTPException
from app.schemas.review import (
    RegenerateReviewRequest,
    RegenerateReviewResponse,
    UserProfileRequest,
    UserProfile,
)
from app.services import review_service

router = APIRouter()

@router.post("/regenerate-review", response_model=RegenerateReviewResponse)
def regenerate_review(request: RegenerateReviewRequest):
    """
    レビュー情報とオプションのユーザープロファイルを受け取り、
    再生成したレビューを返すエンドポイント。
    """
    regenerated_text = review_service.regenerate_review_text(
        original_review=request.original_review,
        product_info=request.product_info,
        user_profile=request.user_profile
    )
    return RegenerateReviewResponse(regenerated_review=regenerated_text)


@router.post("/user-profile", response_model=UserProfile)
def get_user_profile(request: UserProfileRequest):
    """
    レビュー履歴を受け取り、ユーザープロファイルを生成して返すエンドポイント。
    """

    print("--- フロントエンドから受信したデータ ---")
    print(f"レビュー履歴の件数: {len(request.review_history)}")
    print(f"レビュー履歴の内容: {request.review_history}")
    print("------------------------------------")
    
    user_profile = review_service.create_user_profile(
        review_history=request.review_history,
        product_info_history=request.product_info_history
    )
    if user_profile is None:
        raise HTTPException(status_code=404, detail="ユーザープロファイルの作成に失敗しました。レビュー履歴が不足している可能性があります。")
    
    return user_profile