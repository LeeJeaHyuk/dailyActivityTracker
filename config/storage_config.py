from .base_config import ROOT_DIR

# 저장 디렉토리
STORAGE_DIR = ROOT_DIR / 'storage' / 'activities'
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# 백업 설정
BACKUP_ENABLED = True
BACKUP_INTERVAL = 24 * 60 * 60  # 24시간 (초 단위)
MAX_BACKUPS = 7  # 최대 백업 개수 