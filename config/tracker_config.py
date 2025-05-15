from .base_config import ROOT_DIR
from pathlib import Path

# 디렉토리 설정
STORAGE_DIR = ROOT_DIR / 'storage'
WATCH_DIR = ROOT_DIR  # 감시할 디렉토리 (프로젝트 루트)
BACKUP_DIR = STORAGE_DIR / 'backups'

# 파일 필터 설정
FILE_EXTENSIONS = ['.py', '.md']
EXCLUDE_DIRS = ['__pycache__', '.git', 'venv', 'env', 'storage', 'logs', 'diffs']

# 파일 크기 제한
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Diff 저장 기본 설정
MIN_CHANGE_SIZE = 10  # 최소 변경 크기 (문자 수)
MIN_CHANGE_LINES = 5  # 최소 변경 줄 수
MIN_SAVE_INTERVAL = 5  # 최소 저장 간격 (초)
MAX_DIFFS_PER_FILE = 50  # 파일당 최대 diff 수

# Diff 저장 고급 설정
USE_SIMILARITY_CHECK = True  # 유사성 검사 활성화 여부
SIMILARITY_THRESHOLD = 0.95  # 유사성 임계값 (95%)
BASELINE_ONLY_ON_FIRST_SEEN = True  # True면 첫 감지 시에만 baseline 저장, False면 모든 변경에 대해 diff 생성 