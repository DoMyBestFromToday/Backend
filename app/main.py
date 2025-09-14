from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import review

app = FastAPI(
    title="Review Regeneration API",
    description="LangChainを使ってレビューをいい感じに書き換えるAPI",
    version="1.0.0",
)

# --- CORS設定 ---
# ❗️ このブロックを、app.include_routerよりも【前】に記述することが重要
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- CORS設定ここまで ---

app.include_router(review.router, prefix="/api", tags=["Review"])

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
