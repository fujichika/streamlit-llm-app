# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage  # Lesson8の書き方に合わせています

# --- .env / Secrets の読み込み ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Streamlit ページ設定 ---
st.set_page_config(page_title="LLM Webアプリ", page_icon="🤖", layout="centered")
st.title("💬 LLM Webアプリ（LangChain × Streamlit）")
st.markdown("""
**使い方**  
1. 専門家の種類（A/B）を選択  
2. テキストを入力  
3. 「送信」を押すと、選択した専門家としてLLMが回答します  
""")

# --- 専門家プロファイル（A/B） ---
EXPERTS = {
    "A": {
        "label": "A：旅行プランナー",
        "system": "あなたは旅行プランの専門家です。旅行者の希望や制約に合わせ、現実的で安全な旅程を日本語で提案してください。必要に応じて費用感・移動手段・注意事項も補足してください。"
    },
    "B": {
        "label": "B：歴史研究者",
        "system": "あなたは歴史の専門家です。質問に対して史実に基づき、日本語でわかりやすく背景・因果・重要人物を整理して説明してください。推測は推測と明確に区別してください。"
    },
}

# --- LLM呼び出し関数（入力テキスト, ラジオ選択値 を引数に、回答文字列を返す） ---
def get_llm_response(input_text: str, expert_key: str) -> str:
    if expert_key not in EXPERTS:
        raise ValueError("expert_key は 'A' か 'B' を指定してください。")
    system_prompt = EXPERTS[expert_key]["system"]

    # OPENAI_API_KEY は .env / Secrets から自動で読まれるので引数は不要
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]
    result = llm(messages)  # AIMessage
    return result.content

# --- UI ---
# ラジオ：A/Bを内部キーで保持し、表示はlabelに
expert_key = st.radio(
    "専門家の種類を選んでください",
    options=list(EXPERTS.keys()),
    format_func=lambda k: EXPERTS[k]["label"],
    horizontal=True
)

user_input = st.text_area("質問・相談内容を入力してください", height=150)

# --- 送信ハンドラ ---
if st.button("送信"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY が未設定です。Streamlit Cloud の Secrets か .env に設定してください。", icon="❌")
    elif not user_input.strip():
        st.warning("テキストを入力してください。", icon="⚠️")
    else:
        with st.spinner("AIが回答を生成しています…"):
            try:
                answer = get_llm_response(user_input, expert_key)
                st.subheader("✅ 回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラー: {e}")


