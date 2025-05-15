"""
파일 처리 유틸리티
- 파일 형식 변환
- 메타데이터 정리
- 파일 크기 계산
- 파일 수 계산
"""

from pathlib import Path
from typing import Dict, List, Optional
import json
import shutil
import logging
from datetime import datetime

class FileUtils:
    """
    파일 처리를 담당하는 유틸리티 클래스
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = {
            '.txt': self._convert_to_txt,
            '.md': self._convert_to_md,
            '.json': self._convert_to_json
        }

    def convert_formats(self, directory: Path) -> int:
        """
        파일 형식 변환
        Args:
            directory: 변환할 디렉토리
        Returns:
            int: 변환된 파일 수
        """
        converted_count = 0

        for date_dir in directory.iterdir():
            if not date_dir.is_dir():
                continue

            for file_path in date_dir.rglob('*'):
                if file_path.is_file():
                    # 지원하는 형식으로 변환
                    for target_format, converter in self.supported_formats.items():
                        if file_path.suffix != target_format:
                            try:
                                if converter(file_path):
                                    converted_count += 1
                                    self.logger.info(f"Converted file: {file_path}")
                            except Exception as e:
                                self.logger.error(f"Error converting file {file_path}: {e}")

        return converted_count

    def clean_metadata(self, directory: Path) -> int:
        """
        메타데이터 정리
        Args:
            directory: 정리할 디렉토리
        Returns:
            int: 정리된 파일 수
        """
        cleaned_count = 0

        for date_dir in directory.iterdir():
            if not date_dir.is_dir():
                continue

            metadata_dir = date_dir / 'metadata'
            if not metadata_dir.exists():
                continue

            for metadata_file in metadata_dir.glob('*.json'):
                try:
                    if self._clean_metadata_file(metadata_file):
                        cleaned_count += 1
                        self.logger.info(f"Cleaned metadata: {metadata_file}")
                except Exception as e:
                    self.logger.error(f"Error cleaning metadata {metadata_file}: {e}")

        return cleaned_count

    def count_files(self, directory: Path) -> int:
        """
        파일 수 계산
        Args:
            directory: 계산할 디렉토리
        Returns:
            int: 파일 수
        """
        count = 0
        for _ in directory.rglob('*'):
            if _.is_file():
                count += 1
        return count

    def get_total_size(self, directory: Path) -> int:
        """
        디렉토리 전체 크기 계산
        Args:
            directory: 계산할 디렉토리
        Returns:
            int: 전체 크기 (바이트)
        """
        total_size = 0
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size

    def _convert_to_txt(self, file_path: Path) -> bool:
        """
        텍스트 파일로 변환
        Args:
            file_path: 변환할 파일
        Returns:
            bool: 변환 성공 여부
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_path = file_path.with_suffix('.txt')
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_path.unlink()
            return True
        except Exception:
            return False

    def _convert_to_md(self, file_path: Path) -> bool:
        """
        마크다운 파일로 변환
        Args:
            file_path: 변환할 파일
        Returns:
            bool: 변환 성공 여부
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_path = file_path.with_suffix('.md')
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(f"# {file_path.stem}\n\n")
                f.write(content)
            
            file_path.unlink()
            return True
        except Exception:
            return False

    def _convert_to_json(self, file_path: Path) -> bool:
        """
        JSON 파일로 변환
        Args:
            file_path: 변환할 파일
        Returns:
            bool: 변환 성공 여부
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_path = file_path.with_suffix('.json')
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'content': content,
                    'original_format': file_path.suffix,
                    'converted_at': datetime.now().isoformat()
                }, f, indent=2)
            
            file_path.unlink()
            return True
        except Exception:
            return False

    def _clean_metadata_file(self, metadata_file: Path) -> bool:
        """
        메타데이터 파일 정리
        Args:
            metadata_file: 정리할 메타데이터 파일
        Returns:
            bool: 정리 성공 여부
        """
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # 필수 필드 확인
            required_fields = {'filename', 'timestamp', 'size', 'type'}
            if not all(field in metadata for field in required_fields):
                return False

            # 불필요한 필드 제거
            cleaned_metadata = {
                'filename': metadata['filename'],
                'timestamp': metadata['timestamp'],
                'size': metadata['size'],
                'type': metadata['type']
            }

            # 정리된 메타데이터 저장
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_metadata, f, indent=2)

            return True
        except Exception:
            return False 