"""파일 처리 관련 유틸리티"""

import sys
from pathlib import Path
import config

def validate_storage_dirs(target_date: str) -> Path:
    """저장 디렉토리의 유효성을 검사합니다."""
    if not config.STORAGE_DIR.exists():
        print(f"❌ 저장 디렉토리가 존재하지 않습니다: {config.STORAGE_DIR}")
        sys.exit(1)

    target_dir = config.STORAGE_DIR / target_date / 'diffs'
    if not target_dir.exists():
        print(f"⚠️ {target_date} 날짜에 대한 diff 디렉토리가 없습니다.")
        sys.exit(1)
    return target_dir 