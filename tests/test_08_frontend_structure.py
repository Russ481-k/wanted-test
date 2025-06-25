from pathlib import Path

def test_frontend_app_file_exists():
    """frontend/app.py 파일이 존재하는지 검사합니다."""
    path = Path("frontend/app.py")
    assert path.exists() and path.is_file(), "frontend/app.py 파일이 존재하지 않습니다."
