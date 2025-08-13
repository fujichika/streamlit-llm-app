import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit アプリ設定
st.set_page_config(page_title="LLM Webアプリ", page_icon="🤖")

# アプリ概要表示
st.title("💬 LLM Webアプリ")
st.write("""
このアプリは、あなたの質問にLLMが回答します。
下記の手順で使ってください：
1. 専門家の種類をラジオボタンから選択
2. テキストを入力
3. 「送信」を押すと、選択した専門家になりきったLLMが回答します
""")

# 専門家の種類を選択
expert_type = st.radio(
    "専門家の種類を選んでください",
    ("旅行プランナー", "歴史研究者")
)

# ユーザー入力
user_input = st.text_area("質問を入力してください")

# LLM呼び出し関数
def get_llm_response(expert, text):
    if expert == "旅行プランナー":
        system_prompt = "あなたは旅行プランの専門家です。旅行者の希望に合わせた最適な旅行プランを提案してください。"
    elif expert == "歴史研究者":
        system_prompt = "あなたは歴史の専門家です。質問に対して歴史的事実と背景を詳しく説明してください。"
    else:
        system_prompt = "あなたは有能なアシスタントです。"

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]

    response = llm(messages)
    return response.content

# 実行ボタン
if st.button("送信"):
    if user_input.strip():
        answer = get_llm_response(expert_type, user_input)
        st.subheader("回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")


