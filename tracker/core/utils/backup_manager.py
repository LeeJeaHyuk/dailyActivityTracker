"""
백업 관리자 구현
- 파일 백업 생성 및 관리
- 백업 파일 로드
- 오래된 백업 정리
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import shutil
import json
from interfaces.backup.manager import BackupManagerInterface
from interfaces.file.filter import FileFilterInterface

class BackupManager(BackupManagerInterface):
    """파일 백업 관리자"""
    
    def __init__(self, watch_dir: Path, backup_dir: Path, file_filter: FileFilterInterface):
        self.watch_dir = watch_dir
        self.backup_dir = backup_dir
        self.file_filter = file_filter
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backup_info = self._load_backup_info()
    
    def _load_backup_info(self) -> Dict[str, Any]:
        """백업 정보를 로드합니다."""
        info_path = self.backup_dir / "backup_info.json"
        if info_path.exists():
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 백업 정보 로드 실패: {e}")
        return {}
    
    def _save_backup_info(self):
        """백업 정보를 저장합니다."""
        info_path = self.backup_dir / "backup_info.json"
        try:
            with open(info_path, 'w', encoding='utf-8') as f:
                json.dump(self.backup_info, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 백업 정보 저장 실패: {e}")
    
    def update_backup(self, file_path: Path, content: str) -> Optional[str]:
        """
        파일의 백업을 생성하거나 업데이트합니다.
        
        Args:
            file_path: 백업할 파일 경로
            content: 파일 내용
            
        Returns:
            Optional[str]: 백업 파일 경로 (실패 시 None)
        """
        try:
            # 백업 파일 경로 생성
            backup_path = self.backup_dir / f"{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            
            # 백업 파일 저장
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 백업 정보 업데이트
            self.backup_info[str(file_path)] = {
                'last_backup': datetime.now().isoformat(),
                'backup_path': str(backup_path)
            }
            self._save_backup_info()
            
            return str(backup_path)
            
        except Exception as e:
            print(f"⚠️ 백업 생성 실패: {file_path} ({e})")
            return None
    
    def load_backup_content(self, file_path: Path) -> Optional[str]:
        """
        파일의 백업 내용을 로드합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Optional[str]: 백업 내용 (없는 경우 None)
        """
        try:
            backup_info = self.backup_info.get(str(file_path))
            if not backup_info:
                return None
            
            backup_path = Path(backup_info['backup_path'])
            if not backup_path.exists():
                return None
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            print(f"⚠️ 백업 로드 실패: {file_path} ({e})")
            return None
    
    def has_backup(self, file_path: Path) -> bool:
        """
        파일의 백업 존재 여부를 확인합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            bool: 백업 존재 여부
        """
        return str(file_path) in self.backup_info
    
    def cleanup_old_backups(self, days: int):
        """
        오래된 백업을 정리합니다.
        
        Args:
            days: 보관할 일수
        """
        try:
            now = datetime.now()
            to_remove = []
            
            # 삭제할 백업 파일 찾기
            for file_path, info in self.backup_info.items():
                backup_time = datetime.fromisoformat(info['last_backup'])
                if (now - backup_time).days > days:
                    backup_path = Path(info['backup_path'])
                    if backup_path.exists():
                        backup_path.unlink()
                    to_remove.append(file_path)
            
            # 백업 정보에서 제거
            for file_path in to_remove:
                del self.backup_info[file_path]
            
            self._save_backup_info()
            
        except Exception as e:
            print(f"⚠️ 백업 정리 실패: {e}")
    
    def get_backup_path(self, file_path: Path) -> Optional[Path]:
        """
        파일의 백업 경로를 반환합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Optional[Path]: 백업 파일 경로 (없는 경우 None)
        """
        backup_info = self.backup_info.get(str(file_path))
        if not backup_info:
            return None
            
        backup_path = Path(backup_info['backup_path'])
        return backup_path if backup_path.exists() else None 