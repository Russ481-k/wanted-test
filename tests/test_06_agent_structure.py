from pathlib import Path

def test_agent_directory_exists():
    """backend/agent 폴더가 존재하는지 검사합니다."""
    path = Path("backend/agent")
    assert path.exists() and path.is_dir(), "backend/agent 폴더가 존재하지 않습니다."

def test_agent_init_file_exists():
    """backend/agent/__init__.py 파일이 존재하는지 검사합니다."""
    path = Path("backend/agent/__init__.py")
    assert path.exists() and path.is_file(), "backend/agent/__init__.py 파일이 존재하지 않습니다."

def test_agent_py_file_exists():
    """backend/agent/agent.py 파일이 존재하는지 검사합니다."""
    path = Path("backend/agent/agent.py")
    assert path.exists() and path.is_file(), "backend/agent/agent.py 파일이 존재하지 않습니다." 