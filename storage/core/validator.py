"""
저장소 데이터 검증
- 저장 구조 검증
- 파일 형식 검증
- 메타데이터 검증
- 중복 데이터 검사
"""

from pathlib import Path
from typing import List, Dict, Set
import hashlib
import json
from datetime import datetime

class StorageValidator:
    """
    저장소 데이터 검증을 담당하는 클래스
    """

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.valid_extensions = {'.diff', '.json', '.md'}
        self.required_dirs = {'diffs', 'metadata', 'summaries'}

    def validate_all(self) -> Dict[str, List[str]]:
        """
        모든 검증 수행
        Returns:
            Dict[str, List[str]]: 검증 결과 (문제 유형별 파일 목록)
        """
        results = {
            'invalid_structure': self.validate_structure(),
            'invalid_formats': self.validate_formats(),
            'invalid_metadata': self.validate_metadata(),
            'duplicates': self.find_duplicates()
        }
        return results

    def validate_structure(self) -> List[str]:
        """
        저장 구조 검증
        Returns:
            List[str]: 문제가 있는 경로 목록
        """
        invalid_paths = []
        
        # 필수 디렉토리 검사
        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue
                
            # 날짜 형식 검사
            try:
                datetime.strptime(date_dir.name, '%Y-%m-%d')
            except ValueError:
                invalid_paths.append(str(date_dir))
                continue

            # 필수 하위 디렉토리 검사
            for required_dir in self.required_dirs:
                if not (date_dir / required_dir).exists():
                    invalid_paths.append(str(date_dir / required_dir))

        return invalid_paths

    def validate_formats(self) -> List[str]:
        """
        파일 형식 검증
        Returns:
            List[str]: 문제가 있는 파일 목록
        """
        invalid_files = []
        
        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue

            for file_path in date_dir.rglob('*'):
                if file_path.is_file():
                    # 확장자 검사
                    if file_path.suffix not in self.valid_extensions:
                        invalid_files.append(str(file_path))
                        continue

                    # diff 파일 형식 검사
                    if file_path.suffix == '.diff':
                        if not self._validate_diff_format(file_path):
                            invalid_files.append(str(file_path))

                    # JSON 파일 형식 검사
                    elif file_path.suffix == '.json':
                        if not self._validate_json_format(file_path):
                            invalid_files.append(str(file_path))

        return invalid_files

    def validate_metadata(self) -> List[str]:
        """
        메타데이터 검증
        Returns:
            List[str]: 문제가 있는 메타데이터 파일 목록
        """
        invalid_metadata = []
        
        for date_dir in self.storage_dir.iterdir():
            if not date_dir.is_dir():
                continue

            metadata_dir = date_dir / 'metadata'
            if not metadata_dir.exists():
                continue

            for metadata_file in metadata_dir.glob('*.json'):
                if not self._validate_metadata_content(metadata_file):
                    invalid_metadata.append(str(metadata_file))

        return invalid_metadata

    def find_duplicates(self) -> List[str]:
        """
        중복 파일 검사
        Returns:
            List[str]: 중복된 파일 목록
        """
        duplicates = []
        file_hashes: Dict[str, Set[Path]] = {}

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

        # 중복 파일 그룹화
        for hash_value, file_paths in file_hashes.items():
            if len(file_paths) > 1:
                duplicates.extend([str(path) for path in file_paths])

        return duplicates

    def count_duplicates(self, directory: Path) -> int:
        """
        중복 파일 수 계산
        Args:
            directory: 검사할 디렉토리
        Returns:
            int: 중복 파일 수
        """
        return len(self.find_duplicates())

    def _validate_diff_format(self, file_path: Path) -> bool:
        """
        diff 파일 형식 검증
        Args:
            file_path: diff 파일 경로
        Returns:
            bool: 형식이 올바른지 여부
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content.startswith('---') and '+++' in content
        except Exception:
            return False

    def _validate_json_format(self, file_path: Path) -> bool:
        """
        JSON 파일 형식 검증
        Args:
            file_path: JSON 파일 경로
        Returns:
            bool: 형식이 올바른지 여부
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
                return True
        except Exception:
            return False

    def _validate_metadata_content(self, metadata_file: Path) -> bool:
        """
        메타데이터 내용 검증
        Args:
            metadata_file: 메타데이터 파일 경로
        Returns:
            bool: 내용이 올바른지 여부
        """
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                required_fields = {'filename', 'timestamp', 'size', 'type'}
                return all(field in metadata for field in required_fields)
        except Exception:
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        파일 해시 계산
        Args:
            file_path: 파일 경로
        Returns:
            str: 파일 해시값
        """
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest() 