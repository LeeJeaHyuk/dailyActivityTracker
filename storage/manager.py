"""
스토리지 관리자
- diff 저장 및 관리
- 활동 로깅
- 저장소 초기화 및 관리
"""

from pathlib import Path
from typing import Optional, Dict, Any
from .core import DiffStorage, ActivityLogger
from . import config as storage_config

class StorageManager:
    """
    스토리지 관련 모든 기능을 통합 관리하는 클래스
    """

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or storage_config.STORAGE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # 하위 모듈 초기화
        self.diff_storage = DiffStorage(base_dir=self.base_dir)
        self.activity_logger = ActivityLogger(base_dir=self.base_dir)

    def save_diff(self, file_path: Path, old_content: str, new_content: str) -> Optional[str]:
        """
        파일 변경사항을 저장하고 관련 활동을 로깅합니다.
        """
        # diff 저장
        saved_diff = self.diff_storage.save_diff(file_path, old_content, new_content)
        
        if saved_diff:
            # 활동 로깅
            self.activity_logger.log_activity('diff_saved', {
                'file_path': str(file_path),
                'diff_path': saved_diff
            })
            
        return saved_diff

    def get_diffs(self, date: str, file_path: Optional[Path] = None) -> list[Path]:
        """특정 날짜의 diff 파일들을 조회합니다."""
        return self.diff_storage.get_diffs(date, file_path)

    def get_activities(self, date: str, activity_type: Optional[str] = None) -> list[Dict[str, Any]]:
        """특정 날짜의 활동 기록을 조회합니다."""
        return self.activity_logger.get_activities(date, activity_type)

    def log_activity(self, activity_type: str, data: Dict[str, Any]):
        """활동을 로깅합니다."""
        self.activity_logger.log_activity(activity_type, data) 