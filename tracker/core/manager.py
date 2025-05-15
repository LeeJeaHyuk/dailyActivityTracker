"""
트래커 관리자
- 파일 변경 감시
- 백업 관리
- diff 추적
"""

from pathlib import Path
from typing import Optional, Callable, List, Set
from .utils.backup_manager import BackupManager
from .utils.file_filter import FileFilter
from .utils.diff_generator import TextDiffGenerator
from .file_watcher import FileWatcher
from config import tracker_config
from .storage import TrackerStorage
from interfaces.diff.generator import DiffGeneratorInterface

class TrackerManager:
    """
    파일 변경 추적 관련 모든 기능을 통합 관리하는 클래스
    """

    def __init__(self, 
                 watch_dir: Path,
                 backup_dir: Path,
                 file_extensions: Set[str],
                 exclude_dirs: List[str],
                 max_file_size: int,
                 on_file_modified: Optional[Callable] = None):
        self.watch_dir = watch_dir
        self.backup_dir = backup_dir
        
        # 하위 모듈 초기화
        self.file_filter = FileFilter(
            exclude_dirs=exclude_dirs,
            file_extensions=file_extensions,
            max_file_size=max_file_size,
            backup_exclude_dir=tracker_config.BACKUP_EXCLUDE_DIR
        )
        self.backup_manager = BackupManager(
            watch_dir=self.watch_dir,
            backup_dir=self.backup_dir,
            file_filter=self.file_filter
        )
        self.file_watcher = FileWatcher(
            watch_dir=self.watch_dir,
            file_filter=self.file_filter,
            on_modified=self._on_file_modified
        )
        self.storage = TrackerStorage(base_dir=tracker_config.STORAGE_DIR)
        self.diff_generator = TextDiffGenerator(supported_extensions=file_extensions)

    def _on_file_modified(self, event):
        """파일이 수정되었을 때 호출되는 콜백"""
        file_path = Path(event.src_path)
        
        # 파일이 존재하는지 확인
        if not file_path.exists():
            print(f"⚠️ 파일이 존재하지 않음 (삭제된 파일일 수 있음): {file_path}")
            return

        # (1) EXCLUDE_DIRS 검사
        if any(part in tracker_config.EXCLUDE_DIRS for part in file_path.parts):
            return

        # (2) 확장자 검사
        if file_path.suffix not in tracker_config.FILE_EXTENSIONS:
            return

        # (3) 파일 사이즈 검사
        try:
            if file_path.stat().st_size > tracker_config.MAX_FILE_SIZE:
                return
        except Exception as e:
            print(f"⚠️ 파일 크기 확인 실패 (삭제된 파일일 수 있음): {file_path} ({e})")
            return

        try:
            # 새 내용 읽기
            new_content = file_path.read_text(encoding='utf-8')
            
            # 이전 백업 내용 로드
            old_content = self.load_backup_content(file_path)
            
            # 내용이 변경된 경우에만 처리
            if old_content != new_content:
                # BASELINE_ONLY_ON_FIRST_SEEN이 True이고 백업이 없는 경우에는 diff를 생성하지 않음
                if tracker_config.BASELINE_ONLY_ON_FIRST_SEEN and not self.has_backup(file_path):
                    print(f"📝 첫 감지된 파일, diff 생성 생략: {file_path}")
                    self.update_backup(file_path, new_content)
                    return

                # diff 생성
                diff_data = self.diff_generator.generate_diff(old_content, new_content)
                formatted_diff = self.diff_generator.format_diff(diff_data)
                
                # diff 저장
                saved_diff = self.storage.save_diff(file_path, old_content, new_content)
                if saved_diff:
                    print(f"✅ 변경사항 저장 완료: {saved_diff}")
                    print(formatted_diff)  # diff 내용 출력
                    self.storage.log_activity('file_modified', {
                        'file_path': str(file_path),
                        'diff_path': saved_diff,
                        'diff_summary': diff_data['summary']
                    })
                else:
                    print(f"⚠️ 변경사항 저장 실패: {file_path}")
                
                # 백업 업데이트
                self.update_backup(file_path, new_content)
            else:
                print(f"ℹ️ 변경 없음: {file_path}")
                
        except Exception as e:
            print(f"⚠️ 파일 처리 중 오류 발생: {file_path} ({e})")

    def _backup_existing_files(self):
        """현재 존재하는 파일들의 초기 백업을 수행합니다."""
        print("📦 기존 파일들의 초기 백업을 시작합니다...")
        
        for ext in self.file_filter.get_file_extensions():
            for file_path in self.watch_dir.rglob(f"*{ext}"):
                # 제외 디렉토리 검사
                if not self.file_filter.should_track(file_path):
                    continue
                
                # 파일 내용 읽기 및 백업
                try:
                    content = file_path.read_text(encoding='utf-8')
                    self.backup_manager.update_backup(file_path, content)
                except Exception as e:
                    print(f"⚠️ 파일 백업 실패: {file_path} ({e})")
        
        print("📦 초기 백업이 완료되었습니다.")

    def start(self):
        """파일 변경 감시를 시작합니다."""
        # 백업 파일 정리
        print("🧹 백업 파일 정리를 시작합니다...")
        self.file_filter.cleanup_backup_files(self.backup_dir)
        print("✅ 백업 파일 정리가 완료되었습니다.")
        
        # 초기 백업 수행
        self._backup_existing_files()
        
        # 파일 감시 시작
        self.file_watcher.start()

    def stop(self):
        """파일 변경 감시를 중지합니다."""
        self.file_watcher.stop()

    def load_backup_content(self, file_path: Path) -> str:
        """파일의 백업 내용을 로드합니다."""
        return self.backup_manager.load_backup_content(file_path)

    def update_backup(self, file_path: Path, new_content: str):
        """파일의 백업을 업데이트합니다."""
        self.backup_manager.update_backup(file_path, new_content)

    def has_backup(self, file_path: Path) -> bool:
        """파일의 백업이 존재하는지 확인합니다."""
        return self.backup_manager.has_backup(file_path) 