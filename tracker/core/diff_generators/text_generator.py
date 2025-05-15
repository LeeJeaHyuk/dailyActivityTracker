"""
텍스트 파일용 diff 생성기
"""

from typing import Any, Dict, List
import difflib
from .base_generator import BaseDiffGenerator

class TextDiffGenerator(BaseDiffGenerator):
    """텍스트 파일용 diff 생성기"""
    
    def __init__(self):
        self.supported_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml'}
    
    def can_handle(self, file_extension: str) -> bool:
        return file_extension.lower() in self.supported_extensions
    
    def generate_diff(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """
        텍스트 파일의 diff를 생성합니다.
        
        Args:
            old_content: 이전 버전의 텍스트
            new_content: 새로운 버전의 텍스트
            
        Returns:
            Dict[str, Any]: 생성된 diff 정보
        """
        if not isinstance(old_content, str) or not isinstance(new_content, str):
            raise ValueError("텍스트 파일 diff 생성기는 문자열 타입만 처리할 수 있습니다.")
        
        # difflib을 사용하여 diff 생성
        diff = list(difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            lineterm=''
        ))
        
        return {
            'type': 'text',
            'diff': diff,
            'old_size': len(old_content),
            'new_size': len(new_content),
            'changes': len(diff)
        } 