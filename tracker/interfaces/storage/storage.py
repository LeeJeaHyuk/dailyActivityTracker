"""
저장소 인터페이스
- 파일 변경사항 저장
- 활동 로그 관리
- 저장소 정리
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

class StorageInterface(ABC):
    """저장소 인터페이스"""
    
    @abstractmethod
    def save_diff(self, file_path: Path, old_content: str, new_content: str) -> Optional[str]:
        """
        파일의 변경사항을 저장합니다.
        
        Args:
            file_path: 변경된 파일 경로
            old_content: 이전 파일 내용
            new_content: 새로운 파일 내용
            
        Returns:
            Optional[str]: 저장된 diff 파일 경로 (실패 시 None)
        """
        pass
    
    @abstractmethod
    def get_diffs(self, date: datetime) -> List[Path]:
        """
        특정 날짜의 diff 파일 목록을 반환합니다.
        
        Args:
            date: 날짜
            
        Returns:
            List[Path]: diff 파일 경로 목록
        """
        pass
    
    @abstractmethod
    def log_activity(self, activity_type: str, data: Dict[str, Any]):
        """
        활동을 로그에 기록합니다.
        
        Args:
            activity_type: 활동 유형
            data: 활동 데이터
        """
        pass
    
    @abstractmethod
    def get_activities(self, date: datetime) -> List[Dict[str, Any]]:
        """
        특정 날짜의 활동 로그를 반환합니다.
        
        Args:
            date: 날짜
            
        Returns:
            List[Dict[str, Any]]: 활동 로그 목록
        """
        pass
    
    @abstractmethod
    def cleanup_old_data(self, days: int):
        """
        오래된 데이터를 정리합니다.
        
        Args:
            days: 보관할 일수
        """
        pass 