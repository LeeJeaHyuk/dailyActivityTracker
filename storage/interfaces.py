"""
저장소 인터페이스 정의
- 모든 저장소 구현체가 따라야 하는 기본 인터페이스
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any

class StorageInterface(ABC):
    """저장소 기본 인터페이스"""
    
    @abstractmethod
    def save_diff(self, file_path: Path, old_content: str, new_content: str) -> Optional[str]:
        """파일 변경사항을 저장합니다."""
        pass
    
    @abstractmethod
    def get_diffs(self, date: str, file_path: Optional[Path] = None) -> list[Path]:
        """특정 날짜의 diff 파일들을 조회합니다."""
        pass
    
    @abstractmethod
    def log_activity(self, activity_type: str, data: Dict[str, Any]):
        """활동을 로깅합니다."""
        pass
    
    @abstractmethod
    def get_activities(self, date: str, activity_type: Optional[str] = None) -> list[Dict[str, Any]]:
        """특정 날짜의 활동 기록을 조회합니다."""
        pass 