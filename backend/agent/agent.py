import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

# 새로 만든 스크래핑 도구 임포트
from .tools import scrape_website

# .env 파일에서 환경 변수 로드
load_dotenv()

# --- Agent State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | ToolMessage], operator.add]

# --- Agent Nodes ---
def should_continue(state: AgentState) -> str:
    """결정 노드: 도구를 호출할지, 아니면 종료할지 결정합니다."""
    last_message = state['messages'][-1]
    # 도구 호출이 없으면 종료
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    # 도구 호출이 있으면 도구 노드로 이동
    return "tools"

def call_model(state: AgentState, llm, system_prompt):
    """모델 호출 노드: LLM을 호출하여 응답을 생성합니다."""
    messages = [SystemMessage(content=system_prompt)] + state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# --- Agent 생성 함수 ---
def create_agent():
    """
    DuckDuckGo 검색 도구, 웹 스크레이퍼와 Google Gemini 모델을 사용하여
    LangGraph ReAct 에이전트를 생성합니다.
    """
    # 1. 도구 정의
    tools = [DuckDuckGoSearchRun(), scrape_website]
    tool_node = ToolNode(tools)

    # 2. 모델 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        convert_system_message_to_human=True
    )
    
    # 3. 시스템 프롬프트 정의
    system_prompt = """당신은 상품 최저가 검색 전문 어시스턴트 입니다.
사용자가 요청한 상품에 대해 웹 검색을 통해 판매 사이트가 나오도록 정보를 찾아 제공하고,
한국어로 유용하고 정확한 상품 최저가 정보를 제공해주세요."""

    # 4. Graph 정의
    graph = StateGraph(AgentState)
    
    # 노드와 엣지(흐름) 정의
    graph.add_node("llm", lambda state: call_model(state, llm, system_prompt))
    graph.add_node("tools", tool_node)
    
    graph.set_entry_point("llm")
    
    graph.add_conditional_edges(
        "llm",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )
    graph.add_edge("tools", "llm")
    
    # 5. Graph 컴파일
    agent_executor = graph.compile()
    
    return agent_executor 