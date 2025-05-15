"""
Summarizer 모듈의 저장소 구현
- 요약 데이터 저장
- 활동 로깅
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime
from storage.interfaces import StorageInterface

class SummarizerStorage(StorageInterface):
    """Summarizer 모듈의 저장소 구현"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def save_diff(self, file_path: Path, old_content: str, new_content: str) -> Optional[str]:
        """파일 변경사항을 저장합니다."""
        today = datetime.now().strftime('%Y-%m-%d')
        diff_dir = self.base_dir / today / 'diffs'
        diff_dir.mkdir(parents=True, exist_ok=True)
        
        # diff 파일명 생성
        timestamp = datetime.now().strftime('%H%M%S')
        diff_filename = f"{file_path.name}.{timestamp}.diff"
        diff_path = diff_dir / diff_filename
        
        # diff 내용 생성 및 저장
        diff_content = f"--- {file_path}\n+++ {file_path}\n"
        if old_content != new_content:
            diff_content += f"@@ -1 +1 @@\n-{old_content}\n+{new_content}\n"
        
        diff_path.write_text(diff_content, encoding='utf-8')
        return str(diff_path)
    
    def get_diffs(self, date: str, file_path: Optional[Path] = None) -> list[Path]:
        """특정 날짜의 diff 파일들을 조회합니다."""
        diff_dir = self.base_dir / date / 'diffs'
        if not diff_dir.exists():
            return []
            
        if file_path:
            return list(diff_dir.glob(f"{file_path.name}.*.diff"))
        return list(diff_dir.glob("*.diff"))
    
    def log_activity(self, activity_type: str, data: Dict[str, Any]):
        """활동을 로깅합니다."""
        today = datetime.now().strftime('%Y-%m-%d')
        activity_dir = self.base_dir / today / 'activities'
        activity_dir.mkdir(parents=True, exist_ok=True)
        
        # 활동 로그 파일명 생성
        timestamp = datetime.now().strftime('%H%M%S')
        log_filename = f"{activity_type}.{timestamp}.json"
        log_path = activity_dir / log_filename
        
        # 활동 데이터 저장
        activity_data = {
            'type': activity_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        log_path.write_text(json.dumps(activity_data, indent=2), encoding='utf-8')
    
    def get_activities(self, date: str, activity_type: Optional[str] = None) -> list[Dict[str, Any]]:
        """특정 날짜의 활동 기록을 조회합니다."""
        activity_dir = self.base_dir / date / 'activities'
        if not activity_dir.exists():
            return []
            
        activities = []
        pattern = f"{activity_type}.*.json" if activity_type else "*.json"
        
        for log_file in activity_dir.glob(pattern):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    activities.append(json.load(f))
            except Exception as e:
                print(f"활동 로그 읽기 실패: {log_file} ({e})")
                
        return activities
        
    def save_summary(self, date: str, summary: str, metadata: Dict[str, Any] = None):
        """요약 데이터를 저장합니다."""
        summary_dir = self.base_dir / date / 'summaries'
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        # 요약 파일명 생성
        timestamp = datetime.now().strftime('%H%M%S')
        summary_filename = f"summary.{timestamp}.md"
        summary_path = summary_dir / summary_filename
        
        # 요약 데이터 저장
        summary_data = {
            'content': summary,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # 마크다운 형식으로 저장
        markdown_content = f"# 요약 ({date})\n\n"
        markdown_content += f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown_content += f"## 메타데이터\n\n"
        for key, value in summary_data['metadata'].items():
            markdown_content += f"- {key}: {value}\n"
        markdown_content += f"\n## 요약 내용\n\n{summary_data['content']}"
        
        summary_path.write_text(markdown_content, encoding='utf-8')
        return str(summary_path) 