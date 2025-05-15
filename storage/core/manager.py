"""
저장소 관리자
- 데이터 검증, 정리, 전처리 기능 통합 관리
"""

from pathlib import Path
from typing import List, Dict, Optional
from ..utils.file_utils import FileUtils
from ..utils.backup_utils import BackupUtils
from .validator import StorageValidator
from .cleaner import StorageCleaner

class StorageManager:
    """
    저장소 관리를 담당하는 클래스
    - 데이터 검증
    - 데이터 정리
    - 데이터 전처리
    """

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.validator = StorageValidator(storage_dir)
        self.cleaner = StorageCleaner(storage_dir)
        self.file_utils = FileUtils()
        self.backup_utils = BackupUtils()

    def validate_storage(self) -> Dict[str, List[str]]:
        """
        저장소 데이터 검증
        Returns:
            Dict[str, List[str]]: 검증 결과 (문제 유형별 파일 목록)
        """
        return self.validator.validate_all()

    def clean_storage(self, 
                     max_age_days: int = 30,
                     remove_duplicates: bool = True) -> Dict[str, int]:
        """
        저장소 데이터 정리
        Args:
            max_age_days: 보관할 최대 일수
            remove_duplicates: 중복 파일 제거 여부
        Returns:
            Dict[str, int]: 정리 결과 통계
        """
        return self.cleaner.clean_all(max_age_days, remove_duplicates)

    def preprocess_data(self, 
                       convert_formats: bool = True,
                       clean_metadata: bool = True) -> Dict[str, int]:
        """
        데이터 전처리
        Args:
            convert_formats: 파일 형식 변환 여부
            clean_metadata: 메타데이터 정리 여부
        Returns:
            Dict[str, int]: 전처리 결과 통계
        """
        stats = {
            'converted': 0,
            'cleaned': 0,
            'backed_up': 0
        }

        if convert_formats:
            stats['converted'] = self.file_utils.convert_formats(self.storage_dir)
        
        if clean_metadata:
            stats['cleaned'] = self.file_utils.clean_metadata(self.storage_dir)
        
        # 백업 생성
        stats['backed_up'] = self.backup_utils.create_backup(self.storage_dir)

        return stats

    def get_storage_stats(self) -> Dict[str, int]:
        """
        저장소 통계 정보 조회
        Returns:
            Dict[str, int]: 저장소 통계
        """
        return {
            'total_files': self.file_utils.count_files(self.storage_dir),
            'total_size': self.file_utils.get_total_size(self.storage_dir),
            'old_files': self.cleaner.count_old_files(self.storage_dir),
            'duplicate_files': self.validator.count_duplicates(self.storage_dir)
        } 