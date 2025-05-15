"""
파일 감시 인터페이스
- 파일 변경 감시
- 감시 시작/중지
- 감시 상태 관리
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Callable, List

class FileWatcherInterface(ABC):
    """파일 감시 인터페이스"""
    
    @abstractmethod
    def start(self):
        """
        파일 감시를 시작합니다.
        """
        pass
    
    @abstractmethod
    def stop(self):
        """
        파일 감시를 중지합니다.
        """
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """
        파일 감시가 활성화되어 있는지 확인합니다.
        
        Returns:
            bool: 활성화 여부
        """
        pass
    
    @abstractmethod
    def get_watch_paths(self) -> List[Path]:
        """
        현재 감시 중인 경로 목록을 반환합니다.
        
        Returns:
            List[Path]: 감시 중인 경로 목록
        """
        pass
    
    @abstractmethod
    def add_watch_path(self, path: Path):
        """
        감시할 경로를 추가합니다.
        
        Args:
            path: 감시할 경로
        """
        pass
    
    @abstractmethod
    def remove_watch_path(self, path: Path):
        """
        감시 중인 경로를 제거합니다.
        
        Args:
            path: 제거할 경로
        """
        pass 