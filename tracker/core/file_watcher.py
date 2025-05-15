"""
파일 변경 감시 모듈
"""

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pathlib import Path
from typing import Callable, Optional, List
from .utils.file_filter import FileFilter
from interfaces.file.watcher import FileWatcherInterface

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, 
                 file_filter: FileFilter,
                 on_modified: Optional[Callable] = None):
        self.file_filter = file_filter
        self.on_modified = on_modified
        
    def on_created(self, event):
        if not event.is_directory and self.file_filter.should_track(Path(event.src_path)):
            print(f"파일 생성됨: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory and self.file_filter.should_track(Path(event.src_path)):
            print(f"파일 수정됨: {event.src_path}")
            if self.on_modified:
                self.on_modified(event)
            
    def on_deleted(self, event):
        if not event.is_directory and self.file_filter.should_track(Path(event.src_path)):
            print(f"파일 삭제됨: {event.src_path}")

class FileWatcher(FileWatcherInterface):
    """
    파일 변경을 감시하는 클래스
    - 지정된 디렉토리의 파일 변경 감시
    - 파일 변경 시 콜백 함수 호출
    """

    def __init__(
        self,
        watch_dir: Path,
        file_filter: FileFilter,
        on_modified: Optional[Callable] = None
    ):
        self.watch_dir = watch_dir
        self.file_filter = file_filter
        self.on_modified = on_modified
        self.observer = Observer()
        self._is_active = False
        self.event_handler = FileChangeHandler(
            file_filter=file_filter,
            on_modified=on_modified
        )
        
    def start(self):
        """파일 감시를 시작합니다."""
        if not self._is_active:
            self.observer.schedule(
                self.event_handler,
                str(self.watch_dir),
                recursive=True
            )
            self.observer.start()
            self._is_active = True
            print(f"파일 감시 시작: {self.watch_dir}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("파일 감시 중지")
            
        self.observer.join()
        
    def stop(self):
        """파일 감시를 중지합니다."""
        if self._is_active:
            self.observer.stop()
            self.observer.join()
            self._is_active = False

    def is_active(self) -> bool:
        """파일 감시가 활성화되어 있는지 확인합니다."""
        return self._is_active
    
    def get_watch_paths(self) -> List[Path]:
        """현재 감시 중인 경로 목록을 반환합니다."""
        return [self.watch_dir]
    
    def add_watch_path(self, path: Path):
        """감시할 경로를 추가합니다."""
        if not self._is_active:
            return
        self.observer.schedule(
            self.event_handler,
            str(path),
            recursive=True
        )
    
    def remove_watch_path(self, path: Path):
        """감시 중인 경로를 제거합니다."""
        if not self._is_active:
            return
        for watch in self.observer.watches.copy():
            if watch.path == str(path):
                self.observer.unschedule(watch)

if __name__ == "__main__":
    file_filter = FileFilter()
    watcher = FileWatcher(
        watch_dir=Path(WATCH_DIR),
        file_filter=file_filter,
        on_modified=None
    )
    watcher.start()
