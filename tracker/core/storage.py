"""
Tracker 모듈의 저장소 구현
- 파일 변경사항 저장
- 활동 로깅
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
import hashlib
import shutil
from interfaces.storage.storage import StorageInterface

class TrackerStorage(StorageInterface):
    """Tracker 모듈의 저장소 구현"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.diff_dir = base_dir / "diffs"
        self.activity_dir = base_dir / "activities"
        
        # 필요한 디렉토리 생성
        self.diff_dir.mkdir(parents=True, exist_ok=True)
        self.activity_dir.mkdir(parents=True, exist_ok=True)
        
    def save_diff(self, file_path: Path, old_content: str, new_content: str) -> Optional[str]:
        """
        파일의 변경사항을 저장합니다.
        
        Args:
            file_path: 변경된 파일 경로
            old_content: 이전 파일 내용
            new_content: 새로운 파일 내용
            
        Returns:
            Optional[str]: 저장된 diff 파일 경로 (실패 시 None)
        """
        try:
            # 날짜별 디렉토리 생성
            date_dir = self.diff_dir / datetime.now().strftime("%Y-%m-%d")
            date_dir.mkdir(parents=True, exist_ok=True)
            
            # 파일명 생성 (타임스탬프 포함)
            timestamp = datetime.now().strftime("%H-%M-%S")
            diff_filename = f"{file_path.stem}_{timestamp}.diff"
            diff_path = date_dir / diff_filename
            
            # diff 내용 저장
            diff_content = {
                'file_path': str(file_path),
                'old_content': old_content,
                'new_content': new_content,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(diff_path, 'w', encoding='utf-8') as f:
                json.dump(diff_content, f, ensure_ascii=False, indent=2)
            
            return str(diff_path)
            
        except Exception as e:
            print(f"⚠️ diff 저장 실패: {file_path} ({e})")
            return None
    
    def get_diffs(self, date: datetime) -> List[Path]:
        """
        특정 날짜의 diff 파일 목록을 반환합니다.
        
        Args:
            date: 날짜
            
        Returns:
            List[Path]: diff 파일 경로 목록
        """
        date_dir = self.diff_dir / date.strftime("%Y-%m-%d")
        if not date_dir.exists():
            return []
        
        return list(date_dir.glob("*.diff"))
    
    def log_activity(self, activity_type: str, data: Dict[str, Any]):
        """
        활동을 로그에 기록합니다.
        
        Args:
            activity_type: 활동 유형
            data: 활동 데이터
        """
        try:
            # 날짜별 디렉토리 생성
            date_dir = self.activity_dir / datetime.now().strftime("%Y-%m-%d")
            date_dir.mkdir(parents=True, exist_ok=True)
            
            # 로그 파일 경로
            log_path = date_dir / "activities.json"
            
            # 기존 로그 로드
            activities = []
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    activities = json.load(f)
            
            # 새 활동 추가
            activity = {
                'type': activity_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            activities.append(activity)
            
            # 로그 저장
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(activities, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"⚠️ 활동 로그 기록 실패: {activity_type} ({e})")
    
    def get_activities(self, date: datetime) -> List[Dict[str, Any]]:
        """
        특정 날짜의 활동 로그를 반환합니다.
        
        Args:
            date: 날짜
            
        Returns:
            List[Dict[str, Any]]: 활동 로그 목록
        """
        log_path = self.activity_dir / date.strftime("%Y-%m-%d") / "activities.json"
        if not log_path.exists():
            return []
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 활동 로그 로드 실패: {date} ({e})")
            return []
    
    def cleanup_old_data(self, days: int):
        """
        오래된 데이터를 정리합니다.
        
        Args:
            days: 보관할 일수
        """
        try:
            # 현재 날짜
            now = datetime.now()
            
            # diff 파일 정리
            for diff_date_dir in self.diff_dir.iterdir():
                if not diff_date_dir.is_dir():
                    continue
                
                # 날짜 파싱
                try:
                    date = datetime.strptime(diff_date_dir.name, "%Y-%m-%d")
                    if (now - date).days > days:
                        shutil.rmtree(diff_date_dir)
                except ValueError:
                    continue
            
            # 활동 로그 정리
            for activity_date_dir in self.activity_dir.iterdir():
                if not activity_date_dir.is_dir():
                    continue
                
                # 날짜 파싱
                try:
                    date = datetime.strptime(activity_date_dir.name, "%Y-%m-%d")
                    if (now - date).days > days:
                        shutil.rmtree(activity_date_dir)
                except ValueError:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 오래된 데이터 정리 실패: {e}") 