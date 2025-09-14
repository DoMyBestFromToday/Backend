from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.schemas.review import UserProfile, RegenerateReviewResult
from typing import List, Optional

# LLMの初期化
llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-5-mini")

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
        ("system", '''あなたは優秀なデータアナリストです。
            提供されたお酒に関するレビュー履歴から、ユーザーのプロファイルを分析し、指定された構造で出力してください。

            ### 重要事項 ###
            - **レビューが書かれているという事実だけで、その商品の特徴をユーザーの好みだと結論付けないでください。** レビューが肯定的か否定的かを注意深く判断し、ユーザーが明確に「好き」「美味しい」と言及している場合や、明らかにポジティブな文脈の場合にのみ、その特徴を「好み」として抽出してください。
            - 逆に、「甘すぎる」「好みではない」といった否定的なレビューの場合、その商品の特徴はユーザーの好みでは**ない**と判断してください。
            - 情報が不足しており分析が困難な項目については、「データ不足のため分析できません」と回答してください。

            ### 判断例 ###
            1.  **入力**:
                製品: フルーティーで甘口の純米酒
                レビュー: 私には少し甘すぎた。もっとキリッとした辛口が好きです。
                **正しい判断**: このユーザーは「辛口」を好む。「フルーティー」や「甘口」は好みではない。

            2.  **入力**:
                製品: 芳醇な香りの純米大吟醸
                レビュー: 香りがとても良く、特別な日にまた飲みたいです。
                **正しい判断**: このユーザーは「芳醇な香り」を好む。
            ''',
        ),
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
    system_message = '''
        あなたはレビュー文のバイアスを除去する職人です。
        ユーザーの元なレビュー文から、ユーザーの好みなどによるバイアスを除去したレビュー文に書き換えてください。
        もしユーザープロフィールが与えられている場合は、それを参考にしてバイアスを除去することを心掛けてください。
        ここで重要なことはプロダクト情報はユーザープロフィールと比較するための情報に過ぎないということです。
        つまり、製品情報は結果に含めず、元なレビュー文に記載のないことは生成しないようにお願いします。
        元レビューに情報を追記することは絶対に避けるようにしてください。
        例えば、元なレビュー文に「甘い」と記載されており、ユーザープロフィールに好みの甘さが「甘い」だとしたら、そのレビュー文はバイアスがかかっている可能性が高いです。
        そのため、「甘いお酒が好きな私にはちょうどいい」と書いたり、逆にユーザープロフィールが「辛口」だとしたら
        「辛口が好きな私には甘すぎるので、もう少し甘さが抑えられたものがおすすめ」と書き換える。
        このような例を参考にしながら、元レビュー文のバイアス除去を行ってください。
        出力は指定したデータ構造で行なってください。
    '''
    
    profile_context = ""
    if user_profile:
        profile_context += "\n\n以下はユーザーのプロファイルです。これを強く参考にして、ユーザーの好みやよく利用される表現を一般化し、バイアスを除去することを心掛けてください.\n"
        profile_context += f"- 味の好み: {', '.join(user_profile.taste_preference)}\n"
        profile_context += f"- 香りの好み: {', '.join(user_profile.aroma_preference)}\n"
        profile_context += f"- 甘さの好み: {user_profile.sweetness_level}\n"
        profile_context += f"- 表現の癖: {user_profile.expression_habit}"

    structured_llm = llm.with_structured_output(RegenerateReviewResult)

    review_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "製品情報: {product_info}\n元のレビュー: {original_review}{profile_context}")
    ])
    
    review_chain = review_prompt | structured_llm
    response = review_chain.invoke({
        "product_info": product_info,
        "original_review": original_review,
        "profile_context": profile_context
    })
    
    return response.regenerated_review
