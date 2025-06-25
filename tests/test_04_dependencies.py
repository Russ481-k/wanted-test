import importlib.metadata

def get_installed_packages():
    """현재 환경에 설치된 패키지 이름의 집합을 반환합니다."""
    return {dist.metadata['Name'] for dist in importlib.metadata.distributions()}

def test_backend_dependencies_installed():
    """backend 의존성 패키지가 가상 환경에 설치되었는지 검사합니다."""
    # requirements.txt에 명시된 패키지 이름과 설치 후 실제 패키지 이름이 다를 수 있습니다.
    # 예를 들어 'python-dotenv'는 'dotenv'로 조회해야 할 수 있습니다.
    # 여기서는 requirements.txt에 명시된 이름을 기준으로 검사합니다.
    required_packages = {'fastapi', 'uvicorn', 'python-dotenv'}
    installed_packages = get_installed_packages()
    assert required_packages.issubset(installed_packages), \
        f"누락된 backend 패키지: {required_packages - installed_packages}"

def test_frontend_dependencies_installed():
    """frontend 의존성 패키지가 가상 환경에 설치되었는지 검사합니다."""
    required_packages = {'streamlit'}
    installed_packages = get_installed_packages()
    assert required_packages.issubset(installed_packages), \
        f"누락된 frontend 패키지: {required_packages - installed_packages}" 