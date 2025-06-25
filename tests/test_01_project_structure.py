from pathlib import Path

def test_backend_directory_exists():
    """backend 폴더가 존재하는지 검사합니다."""
    path = Path("backend")
    assert path.exists() and path.is_dir(), "backend 폴더가 존재하지 않습니다."

def test_frontend_directory_exists():
    """frontend 폴더가 존재하는지 검사합니다."""
    path = Path("frontend")
    assert path.exists() and path.is_dir(), "frontend 폴더가 존재하지 않습니다."

def test_backend_requirements_file_exists():
    """backend/requirements.txt 파일이 존재하는지 검사합니다."""
    path = Path("backend/requirements.txt")
    assert path.exists() and path.is_file(), "backend/requirements.txt 파일이 존재하지 않습니다."

def test_frontend_requirements_file_exists():
    """frontend/requirements.txt 파일이 존재하는지 검사합니다."""
    path = Path("frontend/requirements.txt")
    assert path.exists() and path.is_file(), "frontend/requirements.txt 파일이 존재하지 않습니다."

def test_env_file_exists():
    """루트 경로에 .env 파일이 존재하는지 검사합니다."""
    path = Path(".env")
    assert path.exists() and path.is_file(), ".env 파일이 존재하지 않습니다." 