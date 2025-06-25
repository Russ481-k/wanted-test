import pytest
from unittest.mock import patch, MagicMock
import requests
from backend.agent.tools import scrape_website

@patch('requests.get')
def test_scrape_website_success(mock_get):
    """
    scrape_website 함수가 정상적인 URL에 대해 성공적으로 텍스트를 반환하는지 테스트합니다.
    """
    # 가짜 HTML 응답 설정
    fake_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Welcome!</h1>
            <p>This is a test paragraph.</p>
            <a href="/about">About us</a>
        </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = fake_html
    mock_get.return_value = mock_response

    # 함수 실행
    url = "https://www.google.com"  # 실제 요청을 보내지 않도록 모의(mock) 처리됨
    result = scrape_website(url)

    # 결과 검증
    mock_get.assert_called_once_with(url, timeout=5)
    assert "Welcome!" in result
    assert "This is a test paragraph." in result
    assert "About us" in result
    assert "<html" not in result  # HTML 태그는 제거되어야 함

def test_scrape_website_invalid_url():
    """
    scrape_website 함수가 유효하지 않은 URL에 대해 에러 메시지를 반환하는지 테스트합니다.
    """
    url = "not a valid url"
    result = scrape_website(url)
    assert "Invalid URL" in result

@patch('requests.get')
def test_scrape_website_request_error(mock_get):
    """
    웹페이지 요청 중 에러가 발생했을 때, 에러 메시지를 반환하는지 테스트합니다.
    """
    url = "http://real-but-error-url.com"
    mock_get.side_effect = requests.exceptions.RequestException("Test error")

    result = scrape_website(url)
    assert "Failed to retrieve" in result
    assert "Test error" in result 