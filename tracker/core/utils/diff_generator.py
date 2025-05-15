"""
Diff 생성기 구현
- 텍스트 파일 변경사항 생성
- diff 포맷팅
- 파일 타입별 처리
"""

from pathlib import Path
from typing import Set, Dict, Any, List
from datetime import datetime
import difflib
from interfaces.diff.generator import DiffGeneratorInterface

class TextDiffGenerator(DiffGeneratorInterface):
    """텍스트 파일용 Diff 생성기"""
    
    def __init__(self, supported_extensions: Set[str] = None):
        self.supported_extensions = supported_extensions or {'.txt', '.py', '.md', '.json', '.yaml', '.yml'}
    
    def generate_diff(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        파일의 변경사항을 생성합니다.
        
        Args:
            old_content: 이전 파일 내용
            new_content: 새로운 파일 내용
            
        Returns:
            Dict[str, Any]: 생성된 diff 데이터
            {
                'changes': List[Dict],  # 변경사항 목록
                'summary': Dict,        # 변경 요약
                'metadata': Dict        # 메타데이터
            }
        """
        # diff 생성
        diff = list(difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm=''
        ))
        
        # 변경사항 분석
        changes = []
        summary = {
            'added_lines': 0,
            'removed_lines': 0,
            'modified_files': 1 if diff else 0
        }
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                summary['added_lines'] += 1
                changes.append({'type': 'add', 'content': line[1:]})
            elif line.startswith('-') and not line.startswith('---'):
                summary['removed_lines'] += 1
                changes.append({'type': 'remove', 'content': line[1:]})
        
        return {
            'changes': changes,
            'summary': summary,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'diff_type': 'unified'
            }
        }
    
    def get_supported_extensions(self) -> Set[str]:
        """
        지원하는 파일 확장자 목록을 반환합니다.
        
        Returns:
            Set[str]: 지원하는 파일 확장자 집합
        """
        return self.supported_extensions
    
    def format_diff(self, diff_data: Dict[str, Any]) -> str:
        """
        diff 데이터를 포맷팅합니다.
        
        Args:
            diff_data: generate_diff()에서 생성된 diff 데이터
            
        Returns:
            str: 포맷팅된 diff 문자열
        """
        result = []
        
        # 요약 정보 추가
        summary = diff_data['summary']
        result.append(f"=== 변경 요약 ===")
        result.append(f"추가된 라인: {summary['added_lines']}")
        result.append(f"삭제된 라인: {summary['removed_lines']}")
        result.append(f"수정된 파일: {summary['modified_files']}")
        result.append("")
        
        # 변경사항 추가
        result.append("=== 변경사항 ===")
        for change in diff_data['changes']:
            prefix = '+' if change['type'] == 'add' else '-'
            result.append(f"{prefix} {change['content']}")
        
        return '\n'.join(result)
    
    def is_supported(self, file_path: Path) -> bool:
        """
        해당 파일이 지원되는지 확인합니다.
        
        Args:
            file_path: 확인할 파일 경로
            
        Returns:
            bool: 지원 여부
        """
        return file_path.suffix in self.supported_extensions
    
    def get_diff_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        파일의 diff 메타데이터를 반환합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Dict[str, Any]: 메타데이터
            {
                'file_type': str,       # 파일 타입
                'encoding': str,        # 인코딩
                'line_count': int,      # 라인 수
                'last_modified': str    # 마지막 수정 시간
            }
        """
        try:
            stat = file_path.stat()
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                line_count = len(content.splitlines())
            
            return {
                'file_type': file_path.suffix,
                'encoding': 'utf-8',
                'line_count': line_count,
                'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        except Exception as e:
            return {
                'file_type': file_path.suffix,
                'encoding': 'unknown',
                'line_count': 0,
                'last_modified': None,
                'error': str(e)
            } 