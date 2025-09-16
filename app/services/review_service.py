from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.schemas.review import UserProfile, RegenerateReviewResult, Taste1Enum
from typing import List, Optional

# LLMの初期化
llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-4-turbo")

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
            提供されたレビュー履歴から、ユーザーの**お酒に関する好み**のプロファイルを分析し、指定された構造で出力してください。

            ### 分析項目
            - **taste1**: ユーザーの最も基本的な味の好み。「甘口」「辛口」「苦み」のいずれか一つを必ず選択してください。レビュー内容から最も当てはまるものを判断します。
            - **taste2**: `taste1`以外の味の好み。レビュー内で言及されている味の表現（例: 「酸っぱい」「渋い」「フルーティー」「軽快」）をリストとして抽出します。
            - **aroma_preference**: 香りの好み。レビュー内で言及されている香りの表現（例: 「柑橘系」「芳醇」）をリストとして抽出します。
            - **alcohol_type_preference**: 好んで飲んでいるお酒の種類。レビュー内で言及されているポジティブな評価のお酒の種類（例: 「純米酒」「赤ワイン」「IPAビール」）をリストとして抽出します。

            ### 重要事項
            - **思考プロセスを重視**: 判断例で示す「思考プロセス」のように、レビューからどのように結論を導き出したかの論理的なステップを内部で組み立ててから、最終的な構造で出力してください。
            - **お酒のレビューを最優先**: 分析の主目的は**お酒の好み**を特定することです。日本酒、ワイン、ビールなど、お酒に関するレビューを最優先で分析してください。
            - **お酒以外のレビューの扱い**: これらは基本的にお酒の好みとは無関係なため、無視してください。ただし、そのレビューがお酒の好みを推測する上で明らかに役立つ情報（例: 「甘いものが好きなので、このジュースもとても美味しい」）を含んでいる場合に限り、補助的な情報として考慮しても構いません。
            - **肯定的レビューを重視**: ユーザーが明確に「好き」「美味しい」と評価している場合や、明らかにポジティブな文脈で言及している特徴を「好み」として抽出してください。
            - **否定的レビューの扱い**: 「甘すぎる」「好みではない」といった否定的なレビューの場合、その特徴はユーザーの好みでは**ない**と判断し、抽出しないでください。
            - **taste1の判断**: レビュー全体を総合的に判断し、最もユーザーの嗜好を代表すると思われるものを「甘口」「辛口」「苦み」から一つだけ選んでください。例えば、「甘口が好きだけど、これは甘すぎた」というレビューからは「甘口」が好みであると判断します。
            - **情報不足の場合**: 分析が困難な項目については、リストの場合は空のリスト `[]` を返し、`taste1`がどうしても判断できない場合はデフォルトで「甘口」としてください。

            ### 判断例
            1.  **入力**:
                製品: フルーティーで甘口の純米酒
                レビュー: 私には少し甘すぎた。もっとキリッとした辛口が好きです。
                **思考プロセス**:
                1. レビュー内の「少し甘すぎた」は、製品の「甘口」という特徴に対するネガティブな反応である。
                2. 「もっとキリッとした辛口が好き」という記述は、「辛口」と「キリッとした」味への明確な選好を示している。
                3. したがって、`taste1`は"辛口"、`taste2`には"キリッとした"を含める。`alcohol_type_preference`に関する言及はない。
                **正しい判断**:
                - `taste1`: "辛口"
                - `taste2`: ["キリッとした"]
                - `aroma_preference`: []
                - `alcohol_type_preference`: []

            2.  **入力**:
                製品: 芳醇な香りの赤ワイン
                レビュー: 香りがとても良く、特別な日にまた飲みたいです。やっぱり赤ワインは美味しい。酸味も穏やかで良い。
                **思考プロセス**:
                1. 「香りがとても良い」は「芳醇」という特徴へのポジティブな反応。`aroma_preference`に「芳醇」を追加。
                2. 「やっぱり赤ワインは美味しい」は「赤ワイン」への明確な選好を示している。`alcohol_type_preference`に「赤ワイン」を追加。
                3. 「酸味も穏やかで良い」は「酸味が穏やか」という特徴へのポジティブな反応。`taste2`に「酸味が穏やか」を追加。
                4. 全体的にポジティブなレビューで、特に辛口や苦みに関する言及がないため、`taste1`はデフォルト寄りの「甘口」と判断するのが妥当。
                **正しい判断**:
                - `taste1`: "甘口"
                - `taste2`: ["酸味が穏やか"]
                - `aroma_preference`: ["芳醇"]
                - `alcohol_type_preference`: ["赤ワイン"]

            3. **入力**:
                製品: オレンジジュース
                レビュー: このジュースは酸味が強くて美味しい。
                **思考プロセス**:
                1. レビュー対象は「オレンジジュース」であり、お酒ではない。
                2. 基本ルールに基づき、このレビューは無視する。ただし、「酸味」が好みである可能性は補助情報として記憶しておく。
                3. このレビュー単体ではプロファイルに何も反映しない。
                **正しい判断**:
                - `taste1`: "甘口" (デフォルト)
                - `taste2`: []
                - `aroma_preference`: []
                - `alcohol_type_preference`: []
            '''
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
    category: str,
    user_profile: Optional[UserProfile] = None
) -> str:
    """
    受け取った情報（ユーザープロファイルを含む）を基にレビューを再生成します。
    """
    system_message = '''
        あなたは、ECサイトに投稿されたお酒のレビューを、より多くの人の参考になるように客観的な表現に書き換えるプロの編集者です。

        ### あなたのタスク
        元のレビューに含まれる、投稿者の個人的な好みや嗜好に起因する「バイアス」を特定し、それを除去・緩和してください。
        最終的なレビューは、元のレビューの構成や事実情報を維持しつつ、より客観的で、幅広いユーザーにとって有益な内容にする必要があります。

        ### バイアス除去の基本方針
        1.  **構造は変えない**: 元のレビューの文章の流れや段落構成は変更しないでください。
        2.  **事実は維持する**: 元のレビューが伝えている製品に関する具体的な事実（例：「リンゴのような香りがした」「後味がすっきりしている」）は、消さずに必ず残してください。
        3.  **新しい情報は加えない**: 元のレビューに書かれていない製品の特徴や感想を、勝手に追加しないでください。
        4.  **表現を一般化する**: ユーザーの好み（ユーザープロフィール）と製品情報（客観的な事実）を比較し、個人的な嗜好が強く反映された表現を、より一般的で客観的な表現に修正します。

        ### 具体的な書き換えの指示
        - **過剰な表現の緩和**: 「最高に美味しい！」「二度と買わない」のような極端な感情表現を、「多くの人に好まれそうな味わいです」「私の好みとは少し異なりました」のように、より穏やかで客観的なトーンに修正してください。
        - **主観的な断定を客観的な描写へ**:
            - NG例: 「甘すぎて飲めない。」
            - OK例: 「しっかりとした甘みが感じられる味わいです。」
        - **好みと事実の切り分け**: ユーザープロフィールから判断できる「好み」がレビューに強く影響している部分を特定し、その影響を弱めます。

        ### 参考情報の使い方
        - **元のレビュー**: あなたが編集する対象の文章です。
        - **製品情報**: その製品が持つ客観的な特徴（例: 甘口、辛口、フルーティーなど）です。
        - **お酒のカテゴリ**: レビュー対象のお酒のカテゴリ（例: 日本酒, ワイン, ビール）です。
        - **ユーザープロフィール**: レビュー投稿者の好み（基本的な味、その他の味、香り、よく飲むお酒の種類など）です。元のレビューのどの部分が、このユーザーの個人的な好みに基づく「バイアス」なのかを判断するための最も重要な情報です。

        ### 書き換え例
        **例1**
        - **元のレビュー**: "フルーティーでめちゃくちゃ美味しい！甘くて飲みやすいから、お酒が苦手な人にも絶対おすすめ！リピ確定です。"
        - **お酒のカテゴリ**: "日本酒"
        - **製品情報**: "種類: 純米吟醸, 味わい: フルーティー, 甘口"
        - **ユーザープロフィール**: "taste1: 甘口, taste2: [フルーティー], aroma_preference: [], alcohol_type_preference: [純米吟醸]"
        - **思考プロセス**:
            1. レビュアーは「甘口」で「フルーティー」な「純米吟醸」を好む（プロフィールと一致）。
            2. 製品も「甘口」「フルーティー」「純米吟醸」である（製品情報、お酒のカテゴリと一致）。
            3. 「めちゃくちゃ美味しい」「絶対おすすめ」「リピ確定」は、このユーザーの好みに強く影響されたポジティブなバイアスであると判断。
        - **生成されるレビュー**: "フルーティーな香りが特徴で、甘口で飲みやすい味わいの純米吟醸です。お酒を飲み慣れていない方にも試しやすいかもしれません。"

        **例2**
        - **元のレビュー**: "うーん、ちょっと渋すぎるかな。もっと軽やかな赤ワインが好きな私には合いませんでした。"
        - **お酒のカテゴリ**: "ワイン"
        - **製品情報**: "種類: フルボディ赤ワイン, 特徴: 強い渋み"
        - **ユーザープロフィール**: "taste1: 甘口, taste2: [軽やか], aroma_preference: [], alcohol_type_preference: [白ワイン]"
        - **思考プロセス**:
            1. レビュアーは「軽やか」な味を好み、「赤ワイン」よりは「白ワイン」を好む傾向がある。
            2. 製品は「強い渋み」を持つ「フルボディ赤ワイン」である。
            3. 「渋すぎる」「合いませんでした」は、このユーザーの好みと製品の特徴のミスマッチから生じたネガティブなバイアスであると判断。
        - **生成されるレビュー**: "しっかりとした渋みが特徴のフルボディ赤ワインです。軽やかな味わいを好む方には、少し渋みが強く感じられるかもしれません。"

        出力は指定されたデータ構造（RegenerateReviewResult）に従ってください。
    '''
    
    profile_context = ""
    if user_profile:
        profile_context += "\n\n以下はユーザーのプロファイルです。これを強く参考にして、ユーザーの好みやよく利用される表現を一般化し、バイアスを除去することを心掛けてください.\n"
        profile_context += f"- 基本的な味の好み: {user_profile.taste1.value}\n"
        if user_profile.taste2:
            profile_context += f"- その他の味の好み: {', '.join(user_profile.taste2)}\n"
        if user_profile.aroma_preference:
            profile_context += f"- 香りの好み: {', '.join(user_profile.aroma_preference)}\n"
        if user_profile.alcohol_type_preference:
            profile_context += f"- よく飲むお酒の種類: {', '.join(user_profile.alcohol_type_preference)}\n"

    structured_llm = llm.with_structured_output(RegenerateReviewResult)

    review_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "お酒の種類: {category}\n製品情報: {product_info}\n元のレビュー: {original_review}{profile_context}")
    ])
    
    review_chain = review_prompt | structured_llm
    response = review_chain.invoke({
        "category": category,
        "product_info": product_info,
        "original_review": original_review,
        "profile_context": profile_context
    })
    
    return response.regenerated_review
