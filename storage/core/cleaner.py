"""
저장소 데이터 정리
- 오래된 데이터 정리
- 중복 데이터 제거
- 불필요한 파일 정리
- 저장 공간 최적화
"""

from pathlib import Path
from typing import Dict, List, Set
import shutil
from datetime import datetime, timedelta
import json
import logging

class StorageCleaner:
    """
    저장소 데이터 정리를 담당하는 클래스
    """

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.logger = logging.getLogger(__name__)

    def clean_all(self, 
                 max_age_days: int = 30,
                 remove_duplicates: bool = True) -> Dict[str, int]:
        """
        모든 정리 작업 수행
        Args:
            max_age_days: 보관할 최대 일수
            remove_duplicates: 중복 파일 제거 여부
        Returns:
            Dict[str, int]: 정리 결과 통계
        """
        stats = {
            'removed_old': 0,
            'removed_duplicates': 0,
            'removed_unnecessary': 0,
            'freed_space': 0
        }

        # 오래된 데이터 정리
        if max_age_days > 0:
            removed_old, freed_space = self.clean_old_data(max_age_days)
            stats['removed_old'] = removed_old
            stats['freed_space'] += freed_space

        # 중복 데이터 제거
        if remove_duplicates:
            removed_duplicates, freed_space = self.remove_duplicates()
            stats['removed_duplicates'] = removed_duplicates
            stats['freed_space'] += freed_space

        # 불필요한 파일 정리
        removed_unnecessary, freed_space = self.clean_unnecessary_files()
        stats['removed_unnecessary'] = removed_unnecessary
        stats['freed_space'] += freed_space

        return stats

    def clean_old_data(self, max_age_days: int) -> tuple[int, int]:
        """
        오래된 데이터 정리
        Args:
            max_age_days: 보관할 최대 일수
        Returns:
            tuple[int, int]: (제거된 파일 수, 해제된 공간)
        """
        removed_count = 0
        freed_space = 0
        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue

            try:
                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                if dir_date < cutoff_date:
                    # 디렉토리 크기 계산
                    dir_size = self._get_dir_size(date_dir)
                    
                    # 디렉토리 삭제
                    shutil.rmtree(date_dir)
                    
                    removed_count += 1
                    freed_space += dir_size
                    self.logger.info(f"Removed old directory: {date_dir}")
            except ValueError:
                continue

        return removed_count, freed_space

    def remove_duplicates(self) -> tuple[int, int]:
        """
        중복 파일 제거
        Returns:
            tuple[int, int]: (제거된 파일 수, 해제된 공간)
        """
        removed_count = 0
        freed_space = 0
        file_hashes: Dict[str, Set[Path]] = {}

        # 해시값으로 파일 그룹화
        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue

            for file_path in date_dir.rglob('*'):
                if file_path.is_file():
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash in file_hashes:
                        file_hashes[file_hash].add(file_path)
                    else:
                        file_hashes[file_hash] = {file_path}

        # 각 그룹에서 가장 오래된 파일만 유지
        for hash_value, file_paths in file_hashes.items():
            if len(file_paths) > 1:
                # 파일 수정 시간 기준으로 정렬
                sorted_files = sorted(file_paths, key=lambda x: x.stat().st_mtime)
                
                # 가장 오래된 파일을 제외한 나머지 삭제
                for file_path in sorted_files[1:]:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    removed_count += 1
                    freed_space += file_size
                    self.logger.info(f"Removed duplicate file: {file_path}")

        return removed_count, freed_space

    def clean_unnecessary_files(self) -> tuple[int, int]:
        """
        불필요한 파일 정리
        Returns:
            tuple[int, int]: (제거된 파일 수, 해제된 공간)
        """
        removed_count = 0
        freed_space = 0
        unnecessary_patterns = {
            '*.tmp', '*.temp', '*.bak', '*.old',
            '*.log', '*.cache', '*.swp'
        }

        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue

            for pattern in unnecessary_patterns:
                for file_path in date_dir.rglob(pattern):
                    if file_path.is_file():
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        removed_count += 1
                        freed_space += file_size
                        self.logger.info(f"Removed unnecessary file: {file_path}")

        return removed_count, freed_space

    def count_old_files(self, directory: Path) -> int:
        """
        오래된 파일 수 계산
        Args:
            directory: 검사할 디렉토리
        Returns:
            int: 오래된 파일 수
        """
        count = 0
        cutoff_date = datetime.now() - timedelta(days=30)  # 기본값 30일

        for date_dir in directory.iterdir():
            if not date_dir.is_dir():
                continue

            try:
                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                if dir_date < cutoff_date:
                    count += 1
            except ValueError:
                continue

        return count

    def _get_dir_size(self, directory: Path) -> int:
        """
        디렉토리 크기 계산
        Args:
            directory: 디렉토리 경로
        Returns:
            int: 디렉토리 크기 (바이트)
        """
        total_size = 0
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size

    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        파일 해시 계산
        Args:
            file_path: 파일 경로
        Returns:
            str: 파일 해시값
        """
        import hashlib
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest() 