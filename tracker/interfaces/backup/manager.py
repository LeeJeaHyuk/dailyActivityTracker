"""
백업 관리자 인터페이스
- 파일 백업 관리
- 백업 내용 로드
- 백업 정리
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

class BackupManagerInterface(ABC):
    """백업 관리자 인터페이스"""
    
    @abstractmethod
    def update_backup(self, file_path: Path, content: str):
        """
        파일의 백업을 업데이트합니다.
        
        Args:
            file_path: 백업할 파일 경로
            content: 파일 내용
        """
        pass
    
    @abstractmethod
    def load_backup_content(self, file_path: Path) -> Optional[str]:
        """
        파일의 백업 내용을 로드합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Optional[str]: 백업 내용 (없는 경우 None)
        """
        pass
    
    @abstractmethod
    def has_backup(self, file_path: Path) -> bool:
        """
        파일의 백업이 존재하는지 확인합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            bool: 백업 존재 여부
        """
        pass
    
    @abstractmethod
    def cleanup_old_backups(self, days: int):
        """
        오래된 백업을 정리합니다.
        
        Args:
            days: 보관할 일수
        """
        pass
    
    @abstractmethod
    def get_backup_path(self, file_path: Path) -> Optional[Path]:
        """
        파일의 백업 경로를 반환합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Optional[Path]: 백업 파일 경로 (없는 경우 None)
        """
        pass 