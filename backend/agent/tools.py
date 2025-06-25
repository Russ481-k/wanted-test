import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def scrape_website(url: str) -> str:
    """
    주어진 URL의 웹페이지 내용을 텍스트로 추출합니다.
    URL이 유효하지 않거나 페이지를 가져오는 데 실패하면 에러 메시지를 반환합니다.
    """
    if not url.startswith("http"):
        return "Invalid URL: URL은 'http://' 또는 'https://'로 시작해야 합니다."
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 200 OK가 아니면 예외 발생
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 스크립트와 스타일 태그 제거
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # 텍스트 추출 및 공백 정리
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        return text
        
    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve the webpage. Error: {e}" 