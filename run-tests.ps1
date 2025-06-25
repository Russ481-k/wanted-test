# 이 스크립트는 프로젝트의 모든 pytest 테스트를 실행합니다.

# 프로젝트 루트를 PYTHONPATH에 추가하여 모듈을 올바르게 찾을 수 있도록 설정합니다.
$env:PYTHONPATH = "."

# pytest를 실행합니다.
# pytest는 자동으로 'tests' 폴더 아래의 'test_*.py' 패턴의 파일들을 찾아 실행합니다.
pytest

# 스크립트 실행이 끝나면 환경 변수 설정을 원래대로 되돌릴 수 있지만,
# 현재 스크립트 세션에만 적용되므로 필수는 아닙니다.
# Remove-Item Env:\PYTHONPATH 