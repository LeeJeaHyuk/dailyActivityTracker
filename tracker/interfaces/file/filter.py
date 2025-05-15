"""
파일 필터링 인터페이스
- 파일 추적 여부 결정
- 제외 디렉토리 관리
- 파일 확장자 관리
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Set

class FileFilterInterface(ABC):
    """파일 필터링 인터페이스"""
    
    @abstractmethod
    def should_track(self, file_path: Path) -> bool:
        """
        해당 파일을 추적해야 하는지 결정합니다.
        
        Args:
            file_path: 확인할 파일 경로
            
        Returns:
            bool: 추적 여부
        """
        pass
    
    @abstractmethod
    def get_exclude_dirs(self) -> List[str]:
        """
        제외할 디렉토리 목록을 반환합니다.
        
        Returns:
            List[str]: 제외할 디렉토리 목록
        """
        pass
    
    @abstractmethod
    def get_file_extensions(self) -> Set[str]:
        """
        추적할 파일 확장자 목록을 반환합니다.
        
        Returns:
            Set[str]: 추적할 파일 확장자 집합
        """
        pass
    
    @abstractmethod
    def cleanup_backup_files(self, backup_dir: Path):
        """
        백업 파일을 정리합니다.
        
        Args:
            backup_dir: 백업 디렉토리 경로
        """
        pass 