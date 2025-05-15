"""
인터페이스 패키지
- 파일 관련 인터페이스 (file/)
- 저장소 관련 인터페이스 (storage/)
- diff 관련 인터페이스 (diff/)
- 백업 관련 인터페이스 (backup/)
"""

from .file.watcher import FileWatcherInterface
from .file.filter import FileFilterInterface
from .storage.storage import StorageInterface
from .diff.generator import DiffGeneratorInterface
from .backup.manager import BackupManagerInterface

__all__ = [
    'FileWatcherInterface',
    'FileFilterInterface',
    'StorageInterface',
    'DiffGeneratorInterface',
    'BackupManagerInterface'
] 