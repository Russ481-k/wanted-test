import pytest
from backend.agent.agent import create_agent
from langchain_core.runnables.base import Runnable

def test_create_agent():
    """create_agent 함수가 실행 가능한 (Runnable) 에이전트를 생성하는지 검사합니다."""
    agent = create_agent()
    assert agent is not None, "에이전트가 생성되지 않았습니다."
    assert isinstance(agent, Runnable), "생성된 객체가 Runnable 타입이 아닙니다." 