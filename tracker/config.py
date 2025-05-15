"""
트래커 설정 모듈
"""

from pathlib import Path
from typing import Set

class TrackerConfig:
    def __init__(self):
        # 기본 디렉토리 설정
        self.WATCH_DIR = Path(r"C:\Users\jeahyuk\github")  # 감시할 디렉토리
        self.BACKUP_DIR = Path(r"C:\Users\jeahyuk\github_backup")  # 백업 디렉토리
        self.BACKUP_EXCLUDE_DIR = Path(r"C:\Users\jeahyuk\github_backup_exclude")  # 백업 제외 디렉토리

        # 파일 필터링 설정
        self.FILE_EXTENSIONS: Set[str] = {'.py', '.md'}  # 추적할 파일 확장자
        self.EXCLUDE_DIRS: Set[str] = {'.git', '__pycache__', 'venv', 'node_modules'}  # 제외할 디렉토리
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 최대 파일 크기 (10MB)

        # 저장소 설정
        self.STORAGE_DIR = Path(r"C:\Users\jeahyuk\storage")  # 저장소 디렉토리

        # 기타 설정
        self.BASELINE_ONLY_ON_FIRST_SEEN = True  # 첫 감지 시에만 기준선 저장

tracker_config = TrackerConfig() 