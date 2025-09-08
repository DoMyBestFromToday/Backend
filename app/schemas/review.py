from pydantic import BaseModel

class ReviewRequest(BaseModel):
    original_review: str

class ReviewResponse(BaseModel):
    regenerated_review: str
