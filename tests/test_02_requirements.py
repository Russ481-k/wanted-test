def read_requirements(file_path):
    """requirements.txt 파일을 읽어 패키지 목록을 반환합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def test_backend_requirements_content():
    """backend/requirements.txt 파일에 필수 패키지가 포함되어 있는지 검사합니다."""
    required_packages = {'fastapi', 'uvicorn', 'python-dotenv'}
    installed_packages = set(read_requirements('backend/requirements.txt'))
    assert required_packages.issubset(installed_packages), \
        f"필수 패키지가 누락되었습니다: {required_packages - installed_packages}"

def test_frontend_requirements_content():
    """frontend/requirements.txt 파일에 필수 패키지가 포함되어 있는지 검사합니다."""
    required_packages = {'streamlit'}
    installed_packages = set(read_requirements('frontend/requirements.txt'))
    assert required_packages.issubset(installed_packages), \
        f"필수 패키지가 누락되었습니다: {required_packages - installed_packages}" 