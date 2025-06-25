import os
from dotenv import load_dotenv
from pathlib import Path

def test_env_file_and_variables_load():
    """
    .env 파일이 존재하고, 환경 변수를 성공적으로 로드하는지 검사합니다.
    """
    env_file = Path(".env")
    assert env_file.exists() and env_file.is_file(), ".env 파일이 존재하지 않습니다."
    
    loaded = load_dotenv()
    assert loaded, ".env 파일의 환경 변수를 불러오지 못했습니다."
    
    # 주요 환경 변수들이 로드되었는지 확인
    assert "LANGSMITH_API_KEY" in os.environ, "LANGSMITH_API_KEY가 .env 파일에 설정되지 않았습니다." 

def test_google_api_key_is_set():
    """ .env 파일에 GOOGLE_API_KEY가 설정되어 있는지 확인합니다."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    assert api_key is not None and api_key != "", "GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다."