"""
백업 처리 유틸리티
- 백업 생성
- 백업 복원
- 백업 검증
- 백업 정리
"""

from pathlib import Path
from typing import Dict, List, Optional
import shutil
import json
import logging
from datetime import datetime
import hashlib
import tarfile
import gzip

class BackupUtils:
    """
    백업 처리를 담당하는 유틸리티 클래스
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_backup(self, directory: Path) -> int:
        """
        백업 생성
        Args:
            directory: 백업할 디렉토리
        Returns:
            int: 백업된 파일 수
        """
        backup_count = 0
        backup_dir = directory / 'backups'
        backup_dir.mkdir(exist_ok=True)

        # 백업 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}.tar.gz"
        backup_path = backup_dir / backup_name

        try:
            # tar.gz 파일 생성
            with tarfile.open(backup_path, 'w:gz') as tar:
                for file_path in directory.rglob('*'):
                    if file_path.is_file() and 'backups' not in file_path.parts:
                        tar.add(file_path, arcname=file_path.relative_to(directory))
                        backup_count += 1

            # 백업 메타데이터 생성
            self._create_backup_metadata(backup_path, directory)
            
            self.logger.info(f"Created backup: {backup_path}")
            return backup_count
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            if backup_path.exists():
                backup_path.unlink()
            return 0

    def restore_backup(self, backup_path: Path, target_dir: Path) -> bool:
        """
        백업 복원
        Args:
            backup_path: 백업 파일 경로
            target_dir: 복원할 디렉토리
        Returns:
            bool: 복원 성공 여부
        """
        try:
            # 백업 검증
            if not self._verify_backup(backup_path):
                return False

            # 기존 파일 백업
            temp_backup = self._backup_existing_files(target_dir)
            
            # 백업 파일 압축 해제
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.extractall(target_dir)

            # 백업 메타데이터 검증
            if not self._verify_restored_files(target_dir, backup_path):
                # 복원 실패 시 원래 상태로 복구
                self._restore_from_temp_backup(temp_backup, target_dir)
                return False

            self.logger.info(f"Restored backup: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return False

    def verify_backup(self, backup_path: Path) -> bool:
        """
        백업 검증
        Args:
            backup_path: 백업 파일 경로
        Returns:
            bool: 검증 성공 여부
        """
        return self._verify_backup(backup_path)

    def clean_old_backups(self, directory: Path, max_age_days: int = 30) -> int:
        """
        오래된 백업 정리
        Args:
            directory: 백업 디렉토리
            max_age_days: 보관할 최대 일수
        Returns:
            int: 삭제된 백업 수
        """
        removed_count = 0
        backup_dir = directory / 'backups'
        if not backup_dir.exists():
            return 0

        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        for backup_file in backup_dir.glob('backup_*.tar.gz'):
            try:
                # 파일명에서 타임스탬프 추출
                timestamp_str = backup_file.stem.split('_')[1]
                backup_date = datetime.strptime(timestamp_str, '%Y%m%d')

                if backup_date < cutoff_date:
                    backup_file.unlink()
                    removed_count += 1
                    self.logger.info(f"Removed old backup: {backup_file}")
            except Exception as e:
                self.logger.error(f"Error removing old backup {backup_file}: {e}")

        return removed_count

    def _create_backup_metadata(self, backup_path: Path, source_dir: Path) -> None:
        """
        백업 메타데이터 생성
        Args:
            backup_path: 백업 파일 경로
            source_dir: 원본 디렉토리
        """
        metadata = {
            'backup_time': datetime.now().isoformat(),
            'source_dir': str(source_dir),
            'file_count': 0,
            'total_size': 0,
            'file_hashes': {}
        }

        # 파일 정보 수집
        with tarfile.open(backup_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile():
                    metadata['file_count'] += 1
                    metadata['total_size'] += member.size
                    
                    # 파일 해시 계산
                    f = tar.extractfile(member)
                    if f:
                        content = f.read()
                        file_hash = hashlib.md5(content).hexdigest()
                        metadata['file_hashes'][member.name] = file_hash

        # 메타데이터 저장
        metadata_path = backup_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

    def _verify_backup(self, backup_path: Path) -> bool:
        """
        백업 파일 검증
        Args:
            backup_path: 백업 파일 경로
        Returns:
            bool: 검증 성공 여부
        """
        try:
            # 파일 존재 확인
            if not backup_path.exists():
                return False

            # tar.gz 파일 검증
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.getmembers()

            # 메타데이터 검증
            metadata_path = backup_path.with_suffix('.json')
            if not metadata_path.exists():
                return False

            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # 필수 필드 확인
            required_fields = {'backup_time', 'source_dir', 'file_count', 'total_size', 'file_hashes'}
            if not all(field in metadata for field in required_fields):
                return False

            return True
        except Exception:
            return False

    def _verify_restored_files(self, target_dir: Path, backup_path: Path) -> bool:
        """
        복원된 파일 검증
        Args:
            target_dir: 복원된 디렉토리
            backup_path: 백업 파일 경로
        Returns:
            bool: 검증 성공 여부
        """
        try:
            metadata_path = backup_path.with_suffix('.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # 파일 수 확인
            restored_count = sum(1 for _ in target_dir.rglob('*') if _.is_file())
            if restored_count != metadata['file_count']:
                return False

            # 파일 해시 확인
            for file_path in target_dir.rglob('*'):
                if file_path.is_file():
                    rel_path = str(file_path.relative_to(target_dir))
                    if rel_path in metadata['file_hashes']:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                            if file_hash != metadata['file_hashes'][rel_path]:
                                return False

            return True
        except Exception:
            return False

    def _backup_existing_files(self, target_dir: Path) -> Optional[Path]:
        """
        기존 파일 백업
        Args:
            target_dir: 대상 디렉토리
        Returns:
            Optional[Path]: 임시 백업 파일 경로
        """
        if not target_dir.exists():
            return None

        temp_backup = target_dir.parent / f"temp_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        try:
            with tarfile.open(temp_backup, 'w:gz') as tar:
                for file_path in target_dir.rglob('*'):
                    if file_path.is_file():
                        tar.add(file_path, arcname=file_path.relative_to(target_dir))
            return temp_backup
        except Exception:
            if temp_backup.exists():
                temp_backup.unlink()
            return None

    def _restore_from_temp_backup(self, temp_backup: Optional[Path], target_dir: Path) -> None:
        """
        임시 백업에서 복원
        Args:
            temp_backup: 임시 백업 파일 경로
            target_dir: 대상 디렉토리
        """
        if temp_backup and temp_backup.exists():
            try:
                # 기존 파일 삭제
                shutil.rmtree(target_dir)
                target_dir.mkdir()

                # 임시 백업에서 복원
                with tarfile.open(temp_backup, 'r:gz') as tar:
                    tar.extractall(target_dir)

                # 임시 백업 삭제
                temp_backup.unlink()
            except Exception as e:
                self.logger.error(f"Error restoring from temp backup: {e}") 