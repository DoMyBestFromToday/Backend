from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.schemas.review import UserProfile
from typing import List, Optional

# LLMの初期化
llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-3.5-turbo")

def create_user_profile(
    review_history: List[str],
    product_info_history: List[str]
) -> Optional[UserProfile]:
    """
    レビュー履歴からユーザープロファイルを生成します。
    """
    if not review_history:
        return None

    history_text = ""
    for i, review in enumerate(review_history):
        info = product_info_history[i] if i < len(product_info_history) else "N/A"
        history_text += f"製品: {info}\nレビュー: {review}\n---\n"

    structured_llm = llm.with_structured_output(UserProfile)

    profile_prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは優秀なデータアナリストです。提供されたお酒に関するレビュー履歴から、ユーザーのプロファイルを分析し、指定された構造で出力してください。"),
        ("user", "レビュー履歴:\n{history}")
    ])
    
    profile_chain = profile_prompt | structured_llm
    
    try:
        user_profile_data = profile_chain.invoke({"history": history_text})
        return user_profile_data
    except Exception as e:
        print(f"ユーザープロファイルの作成に失敗しました: {e}")
        return None

def regenerate_review_text(
    original_review: str,
    product_info: str,
    user_profile: Optional[UserProfile] = None
) -> str:
    """
    受け取った情報（ユーザープロファイルを含む）を基にレビューを再生成します。
    """
    system_message = "あなたは優秀なレビュー編集者です。ユーザーが入力した情報と、提供されたユーザープロファイルを参考に、レビューをより魅力的で具体的な文章に書き換えてください。"
    
    profile_context = ""
    if user_profile:
        profile_context += "\n\n以下はユーザーのプロファイルです。これを強く参考にして、ユーザーが好みそうな表現や内容でレビューを生成してください。\n"
        profile_context += f"- 味の好み: {', '.join(user_profile.taste_preference)}\n"
        profile_context += f"- 香りの好み: {', '.join(user_profile.aroma_preference)}\n"
        profile_context += f"- 甘さの好み: {user_profile.sweetness_level}\n"
        profile_context += f"- 表現の癖: {user_profile.expression_habit}"

    review_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "製品情報: {product_info}\n元のレビュー: {original_review}{profile_context}")
    ])
    
    review_chain = review_prompt | llm
    response = review_chain.invoke({
        "product_info": product_info,
        "original_review": original_review,
        "profile_context": profile_context
    })
    
    return response.content