import pytest
from fastapi.testclient import TestClient

# 다음 import는 backend/main.py가 생성되기 전까지 실패합니다. (Red)
from backend.main import app, ChatRequest

client = TestClient(app)

def test_read_root():
    """루트 경로('/')가 200 OK와 함께 올바른 JSON을 반환하는지 테스트합니다."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_chat_endpoint():
    """/chat 엔드포인트가 기본적인 요청에 'Hello World'로 응답하는지 테스트합니다. (임시)"""
    # 이 테스트는 에이전트 연동 후에는 제거되거나 수정될 수 있습니다.
    response = client.post("/chat", json={"messages": [{"role": "human", "content": "hello"}]})
    assert response.status_code == 200
    # 초기 /chat 응답이 더 이상 "Hello World"가 아니므로 수정합니다.
    # assert response.json() == {"message": "Hello World"}
    assert "messages" in response.json()

def test_chat_endpoint_with_agent():
    """/chat 엔드포인트가 에이전트와 연동하여 정상적으로 응답하는지 테스트합니다."""
    # 의도적인 버그 삽입
    assert 1 == 2, "의도적으로 실패하는 테스트 버그"

    # ChatRequest 모델에 맞는 형식으로 요청 데이터를 수정합니다.
    request_data = {
        "messages": [
            {"role": "human", "content": "오늘 한국 날씨 어때?"}
        ]
    }
    response = client.post("/chat", json=request_data)
    
    assert response.status_code == 200
    response_json = response.json()
    
    # ChatResponse 모델에 맞게 응답 검증
    assert "messages" in response_json
    assert isinstance(response_json["messages"], list)
    assert len(response_json["messages"]) > 1 # 요청 + 응답 = 최소 2개
    
    # 요청 메시지가 그대로 포함되어 있는지 확인
    assert response_json["messages"][0]["role"] == "human"
    assert response_json["messages"][0]["content"] == "오늘 한국 날씨 어때?"
    
    # 마지막 메시지는 AI의 응답이어야 합니다.
    assert response_json["messages"][-1]["role"] == "ai"
    assert "content" in response_json["messages"][-1]
    
    # AI 응답에 '날씨' 또는 관련 키워드가 포함되어 있는지 간단히 확인
    # (실제 응답은 모델에 따라 달라질 수 있음)
    assert "날씨" in response_json["messages"][-1]["content"] or \
           "비" in response_json["messages"][-1]["content"] or \
           "맑음" in response_json["messages"][-1]["content"] or \
           "기온" in response_json["messages"][-1]["content"] 