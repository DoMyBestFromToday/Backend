from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings

# LLMの初期化 (OpenAIを使用)
llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo")

# プロンプトテンプレートの定義
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀なレビュー編集者です。ユーザーが入力したレビューを、より丁寧で魅力的な文章に書き換えてください。"),
    ("user", "元のレビュー: {review_text}")
])

# LangChainの組み立て
chain = prompt | llm

def regenerate_review_text(original_review: str) -> str:
    """
    LangChainを使用してレビューテキストを再生成します。
    """
    response = chain.invoke({"review_text": original_review})
    return response.content
