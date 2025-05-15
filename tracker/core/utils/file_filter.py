"""
파일 필터링 모듈
- 파일 추적 여부 결정
- 제외 디렉토리 관리
- 파일 확장자 관리
"""

from pathlib import Path
from typing import List, Set
import shutil
from interfaces.file.filter import FileFilterInterface

class FileFilter(FileFilterInterface):
    """파일 필터링 클래스"""
    
    def __init__(self,
                 exclude_dirs: List[str],
                 file_extensions: Set[str],
                 max_file_size: int,
                 backup_exclude_dir: Path):
        self.exclude_dirs = exclude_dirs
        self.file_extensions = file_extensions
        self.max_file_size = max_file_size
        self.backup_exclude_dir = backup_exclude_dir
    
    def should_track(self, file_path: Path) -> bool:
        """
        해당 파일을 추적해야 하는지 결정합니다.
        
        Args:
            file_path: 확인할 파일 경로
            
        Returns:
            bool: 추적 여부
        """
        # 제외 디렉토리 검사
        if any(part in self.exclude_dirs for part in file_path.parts):
            return False
        
        # 확장자 검사
        if file_path.suffix not in self.file_extensions:
            return False
        
        # 파일 크기 검사
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except Exception:
            return False
        
        return True
    
    def get_exclude_dirs(self) -> List[str]:
        """
        제외할 디렉토리 목록을 반환합니다.
        
        Returns:
            List[str]: 제외할 디렉토리 목록
        """
        return self.exclude_dirs
    
    def get_file_extensions(self) -> Set[str]:
        """
        추적할 파일 확장자 목록을 반환합니다.
        
        Returns:
            Set[str]: 추적할 파일 확장자 집합
        """
        return self.file_extensions
    
    def cleanup_backup_files(self, backup_dir: Path):
        """
        백업 파일을 정리합니다.
        
        Args:
            backup_dir: 백업 디렉토리 경로
        """
        # 제외 디렉토리가 없으면 생성
        self.backup_exclude_dir.mkdir(parents=True, exist_ok=True)
        
        # 각 제외 디렉토리에 대해 처리
        for exclude_dir in self.exclude_dirs:
            exclude_path = backup_dir / exclude_dir
            
            # 제외 디렉토리가 존재하는 경우에만 처리
            if exclude_path.exists():
                # 제외 디렉토리의 모든 파일을 backup_exclude_dir로 이동
                for file_path in exclude_path.rglob('*'):
                    if file_path.is_file():
                        # 상대 경로 계산
                        rel_path = file_path.relative_to(backup_dir)
                        # 대상 경로 생성
                        target_path = self.backup_exclude_dir / rel_path
                        # 부모 디렉토리 생성
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        # 파일 이동
                        shutil.move(str(file_path), str(target_path))
                
                # 빈 디렉토리 삭제
                shutil.rmtree(exclude_path)

if __name__ == "__main__":
    file_filter = FileFilter()
    file_filter.print_settings()
