import streamlit as st
from google import genai

# -------------------------------------------------------
# Streamlit + Google Gemini Chat UI (with Loading Spinner)
# -------------------------------------------------------

def main():
    st.set_page_config(page_title="호갱제로 시세 예측 앱", page_icon="💬", layout="centered")
    st.title(" 호갱제로 시세 예측 앱")

    # Gemini 클라이언트 초기화
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    # 세션 상태 초기화 (대화 기록)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요 👋 Gemini 챗봇입니다. 무엇이든 물어보세요!"}
        ]

    # 기존 대화 표시
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    if user_input := st.chat_input("질문을 입력하세요..."):
        # 사용자 입력 메시지 표시 및 저장
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 로딩 스피너 표시
        with st.chat_message("assistant"):
            with st.spinner("⏳ 답변 생성 중... 잠시만 기다려주세요."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents= "어르신들 대상의 서비스니까, 친절하고 살갑게 대답해줘.그리고 대답은 알기 쉬운 용어를 써서 말해줘.유저질문이 ,노인복지 관련 내용이 아니면, 복지내용만 말하게 해줘."
                    )
                    bot_reply = response.text
                except Exception as e:
                    bot_reply = f"⚠️ 오류 발생: {str(e)}"

            st.markdown(bot_reply)

        # 대화 저장
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})


if __name__ == "__main__":
    main()
