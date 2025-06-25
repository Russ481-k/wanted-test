import streamlit as st
import requests
import os

# 백엔드 서버 주소
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")

def get_response_from_backend(history: list):
    """
    백엔드에 전체 대화 기록을 보내고 업데이트된 기록을 받아옵니다.
    """
    try:
        response = requests.post(BACKEND_URL, json={"messages": history})
        response.raise_for_status()  # 오류가 발생하면 예외를 발생시킵니다.
        return response.json()["messages"]
    except requests.exceptions.RequestException as e:
        st.error(f"백엔드와 통신 중 오류가 발생했습니다: {e}")
        return None

# --- Streamlit UI ---

st.set_page_config(page_title="VIBE-CHATTING", page_icon="💬")
st.title("W2-1: AI 기반 상품 최저가 검색 챗봇")

# 테스트용 주석 추가
# PR 테스트를 위한 주석입니다.

# 세션 상태에 메시지 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "안녕하세요! 어떤 도움이 필요하신가요?"}
    ]

# 이전 대화 내용 표시
for message in st.session_state.messages:
    # LangChain의 역할(human, ai)을 Streamlit의 역할(user, assistant)에 맞게 변환
    role = message["role"]
    if role == "human":
        role = "user"
    elif role == "ai":
        role = "assistant"
    
    with st.chat_message(role):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요."):
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "human", "content": prompt})
    
    # 화면에 사용자 메시지 즉시 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 백엔드에 전체 대화 기록을 보내고 응답으로 세션 상태 업데이트
    with st.spinner("생각 중..."):
        backend_messages = get_response_from_backend(st.session_state.messages)
        if backend_messages:
            st.session_state.messages = backend_messages
            st.rerun() 