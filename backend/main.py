from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_core.messages import HumanMessage

# 에이전트 생성 함수 임포트
from backend.agent.agent import create_agent

app = FastAPI()

# Pydantic 모델 정의
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    messages: List[ChatMessage]

# LangGraph 에이전트 초기화
agent_executor = create_agent()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    사용자의 메시지를 받아 LangGraph 에이전트를 실행하고,
    전체 대화 내용을 반환합니다.
    """
    # Pydantic 모델을 LangChain의 HumanMessage 객체 리스트로 변환합니다.
    # 현재는 마지막 메시지만 사용하지만, 전체 대화 기록을 사용하도록 확장할 수 있습니다.
    messages = [HumanMessage(content=msg.content) for msg in request.messages if msg.role == 'human']

    # LangGraph 에이전트 실행 (동기)
    output = agent_executor.invoke({
        "messages": messages
    })
    
    # 에이전트의 최종 응답을 ChatResponse 형식으로 변환
    response_messages = [
        ChatMessage(role=msg.type, content=msg.content) 
        for msg in output['messages']
    ]
    
    return ChatResponse(messages=response_messages)