"""
트래커 메인 모듈
- 파일 변경 감시 시작/중지
- 백업 관리
- diff 추적
"""

import sys
from pathlib import Path
from core.manager import TrackerManager
from config import tracker_config

def setup_directories():
    """필요한 디렉토리들을 생성합니다."""
    print("📁 필요한 디렉토리 생성 중...")
    
    # 감시 디렉토리 생성
    tracker_config.WATCH_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   - 감시 디렉토리 생성됨: {tracker_config.WATCH_DIR}")
    
    # 백업 디렉토리 생성
    tracker_config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   - 백업 디렉토리 생성됨: {tracker_config.BACKUP_DIR}")
    
    # 저장소 디렉토리 생성
    tracker_config.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   - 저장소 디렉토리 생성됨: {tracker_config.STORAGE_DIR}")

def main():
    """메인 함수"""
    print("\n" + "="*40)
    
    # 필요한 디렉토리 설정
    setup_directories()
    
    print("\n🛰️ 파일 변경 감시 시작...")
    
    # 트래커 매니저 초기화
    tracker = TrackerManager(
        watch_dir=tracker_config.WATCH_DIR,
        backup_dir=tracker_config.BACKUP_DIR,
        file_extensions=tracker_config.FILE_EXTENSIONS,
        exclude_dirs=tracker_config.EXCLUDE_DIRS,
        max_file_size=tracker_config.MAX_FILE_SIZE
    )
    
    try:
        # 파일 변경 감시 시작
        tracker.start()
        print("✅ 파일 변경 감시가 시작되었습니다.")
        print("   종료하려면 Ctrl+C를 누르세요.")
        
        # 무한 대기
        while True:
            pass
            
    except KeyboardInterrupt:
        print("\n⚠️ 파일 변경 감시를 중지합니다...")
        tracker.stop()
        print("✅ 파일 변경 감시가 중지되었습니다.")
        sys.exit(0)

if __name__ == "__main__":
    main() 