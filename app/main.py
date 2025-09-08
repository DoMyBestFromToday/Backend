from fastapi import FastAPI
from app.routers import review

app = FastAPI(
    title="Review Regeneration API",
    description="LangChainを使ってレビューをいい感じに書き換えるAPI",
    version="1.0.0",
)

app.include_router(review.router, prefix="/api", tags=["Review"])

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
