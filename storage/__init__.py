"""
스토리지 관련 기능을 포함하는 패키지
- core: 핵심 스토리지 기능 (diff 저장, 활동 로깅)
- activities: 활동 데이터 저장 디렉토리
"""

from .core.diff_storage import DiffStorage
from .core.activity_logger import ActivityLogger

__all__ = ['DiffStorage', 'ActivityLogger'] 