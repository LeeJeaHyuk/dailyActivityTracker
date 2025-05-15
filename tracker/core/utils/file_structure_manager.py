"""
파일 구조 관리 모듈
- 백업 파일 구조 정의
- 파일 경로 생성 규칙
- 파일명 변환 규칙
"""

from pathlib import Path
from typing import Optional, Tuple, List
import json
from datetime import datetime
import hashlib
import re

class FileStructureManager:
    """
    파일 구조 관리를 위한 클래스
    - 백업 파일의 구조 정의
    - 파일 경로 생성 규칙 관리
    - 파일명 변환 규칙 관리
    """

    # 파일 확장자 정의
    CURRENT_VERSION_EXT = '.json'
    HISTORY_EXT = '.history.json'
    
    # 백업 데이터 구조 정의
    BACKUP_DATA_KEYS = {
        'content': '파일 내용',
        'timestamp': '백업 시간',
        'file_path': '원본 파일 경로',
        'file_size': '파일 크기',
        'checksum': '파일 체크섬'
    }

    def __init__(self, watch_dir: Path, backup_dir: Path):
        self.watch_dir = watch_dir
        self.backup_dir = backup_dir

    def _get_date_folder(self, timestamp: Optional[datetime] = None) -> Path:
        """
        날짜별 폴더 경로를 반환
        
        Args:
            timestamp: 기준 시간 (기본값: 현재 시간)
            
        Returns:
            Path: 날짜 폴더 경로
        """
        if timestamp is None:
            timestamp = datetime.now()
        return self.backup_dir / timestamp.strftime('%Y-%m-%d')

    def _get_file_hash(self, file_path: Path) -> str:
        """
        파일 경로의 해시값을 생성
        
        Args:
            file_path: 파일 경로
            
        Returns:
            str: 해시값
        """
        # 파일 경로를 문자열로 변환하고 해시 생성
        path_str = str(file_path.relative_to(self.watch_dir))
        return hashlib.md5(path_str.encode()).hexdigest()[:8]

    def _sanitize_filename(self, filename: str) -> str:
        """
        파일명에서 사용할 수 없는 문자를 제거하고 안전한 파일명으로 변환
        
        Args:
            filename: 원본 파일명
            
        Returns:
            str: 안전한 파일명
        """
        # 파일명에서 사용할 수 없는 문자 제거
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 공백을 언더스코어로 변환
        safe_name = safe_name.replace(' ', '_')
        # 연속된 언더스코어를 하나로 변환
        safe_name = re.sub(r'_+', '_', safe_name)
        return safe_name

    def _get_backup_filename(self, file_path: Path) -> str:
        """
        백업 파일명 생성
        
        Args:
            file_path: 원본 파일 경로
            
        Returns:
            str: 백업 파일명
        """
        file_hash = self._get_file_hash(file_path)
        original_name = self._sanitize_filename(file_path.name)
        return f"{file_hash}_{original_name}"

    def get_backup_paths(self, file_path: Path) -> Tuple[Optional[Path], Optional[Path]]:
        """
        파일의 백업 경로와 이력 경로를 반환
        
        Returns:
            Tuple[Optional[Path], Optional[Path]]: (백업 경로, 이력 경로)
        """
        try:
            # 백업 파일명 생성
            backup_filename = self._get_backup_filename(file_path)
            
            # 오늘 날짜 폴더
            date_folder = self._get_date_folder()
            
            # 백업 파일 경로
            current_version_path = date_folder / f"{backup_filename}{self.CURRENT_VERSION_EXT}"
            # 이력 파일 경로
            history_path = date_folder / f"{backup_filename}{self.HISTORY_EXT}"
            
            return current_version_path, history_path
        except ValueError:
            return None, None

    def find_latest_backup(self, file_path: Path) -> Optional[Path]:
        """
        파일의 가장 최근 백업 경로를 찾음
        
        Args:
            file_path: 원본 파일 경로
            
        Returns:
            Optional[Path]: 최근 백업 파일 경로
        """
        try:
            backup_filename = self._get_backup_filename(file_path)
            
            # 모든 날짜 폴더 검색
            date_folders = sorted(
                [d for d in self.backup_dir.iterdir() if d.is_dir()],
                key=lambda x: x.name,
                reverse=True
            )
            
            # 가장 최근 백업 파일 찾기
            for date_folder in date_folders:
                backup_path = date_folder / f"{backup_filename}{self.CURRENT_VERSION_EXT}"
                if backup_path.exists():
                    return backup_path
                    
            return None
        except Exception as e:
            print(f"⚠️ 최근 백업 파일 검색 실패: {file_path} ({e})")
            return None

    def find_all_backups(self, file_path: Path) -> List[Path]:
        """
        파일의 모든 백업 경로를 찾음
        
        Args:
            file_path: 원본 파일 경로
            
        Returns:
            List[Path]: 모든 백업 파일 경로 목록
        """
        try:
            backup_filename = self._get_backup_filename(file_path)
            backup_paths = []
            
            # 모든 날짜 폴더 검색
            for date_folder in self.backup_dir.iterdir():
                if not date_folder.is_dir():
                    continue
                    
                backup_path = date_folder / f"{backup_filename}{self.CURRENT_VERSION_EXT}"
                if backup_path.exists():
                    backup_paths.append(backup_path)
                    
            return sorted(backup_paths, key=lambda x: x.parent.name, reverse=True)
        except Exception as e:
            print(f"⚠️ 백업 파일 검색 실패: {file_path} ({e})")
            return []

    def create_backup_data(self, 
                          content: str, 
                          file_path: Path,
                          file_size: Optional[int] = None,
                          checksum: Optional[str] = None) -> dict:
        """
        백업 데이터 구조 생성
        
        Args:
            content: 파일 내용
            file_path: 원본 파일 경로
            file_size: 파일 크기 (선택)
            checksum: 파일 체크섬 (선택)
            
        Returns:
            dict: 백업 데이터
        """
        return {
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'file_path': str(file_path),
            'file_size': file_size,
            'checksum': checksum,
            'original_filename': file_path.name,
            'backup_filename': self._get_backup_filename(file_path)
        }

    def save_backup_data(self, 
                        data: dict, 
                        backup_path: Path,
                        ensure_ascii: bool = False,
                        indent: int = 2) -> bool:
        """
        백업 데이터를 파일로 저장
        
        Args:
            data: 저장할 데이터
            backup_path: 저장할 파일 경로
            ensure_ascii: ASCII 문자만 사용할지 여부
            indent: JSON 들여쓰기 크기
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
            return True
        except Exception as e:
            print(f"⚠️ 백업 데이터 저장 실패: {backup_path} ({e})")
            return False

    def load_backup_data(self, backup_path: Path) -> Optional[dict]:
        """
        백업 데이터를 파일에서 로드
        
        Args:
            backup_path: 로드할 파일 경로
            
        Returns:
            Optional[dict]: 로드된 데이터 또는 None
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 백업 데이터 로드 실패: {backup_path} ({e})")
            return None

    def get_backup_file_info(self, backup_path: Path) -> dict:
        """
        백업 파일의 정보를 반환
        
        Args:
            backup_path: 백업 파일 경로
            
        Returns:
            dict: 파일 정보
        """
        try:
            stat = backup_path.stat()
            return {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'date_folder': backup_path.parent.name
            }
        except Exception as e:
            print(f"⚠️ 백업 파일 정보 조회 실패: {backup_path} ({e})")
            return {} 