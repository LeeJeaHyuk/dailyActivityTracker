import os
from pathlib import Path

# 기본 경로 설정
ROOT_DIR = Path(__file__).parent.parent.absolute()
WATCH_DIR = Path('C:/Users/jeahyuk/github')
BACKUP_DIR = Path('C:/Users/jeahyuk/github_backup')

# 로그 디렉토리
LOG_DIR = ROOT_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# LLM 기본 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
MODEL_NAME = 'gpt-3.5-turbo'
USE_LOCAL_LLM = True  # True면 BitNet, False면 OpenAI 사용

# 기본 시스템 프롬프트
DEFAULT_SYSTEM_PROMPT = (
    "Please summarize the following file changes focusing on the key updates. "
    "Limit the summary to no more than five sentences."
) 