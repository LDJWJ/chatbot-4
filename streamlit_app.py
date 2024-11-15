import streamlit as st
from openai import OpenAI

# 앱 제목 및 설명
st.title("🩺 건강 상담 챗봇")
st.write(
    "이 챗봇은 OpenAI의 GPT-4o-mini 모델을 사용하여 건강 관련 질문에 답변합니다. "
    "OpenAI API 키를 입력하고 시작하세요. "
    "API 키는 [여기](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다."
)

# 사용자에게 OpenAI API 키를 입력받음
openai_api_key = st.text_input("OpenAI API 키", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 채팅 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "당신은 친절한 건강 상담 전문가입니다. 사용자 질문에 한글로 답변하세요."}]

    # 기존 채팅 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 필드 생성
    if user_input := st.chat_input("건강 관련 질문을 입력하세요..."):
        # 사용자 메시지를 세션 상태에 저장
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # GPT-4o-mini 모델을 사용하여 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변을 생성 중입니다..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                )
                assistant_message = response.choices[0].message.content

            # 응답 표시
            st.markdown(assistant_message)

        # 응답 메시지를 세션 상태에 저장
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
