from fastapi import APIRouter
from app.schemas.review import ReviewRequest, ReviewResponse
from app.services import review_service

router = APIRouter()

@router.post("/regenerate-review", response_model=ReviewResponse)
def regenerate_review(request: ReviewRequest):
    """
    レビューテキストを受け取り、再生成したレビューを返すエンドポイント。
    """
    regenerated_text = review_service.regenerate_review_text(request.original_review)
    return ReviewResponse(regenerated_review=regenerated_text)
