"""
Diff 생성기 인터페이스
- 파일 변경사항 생성
- diff 포맷팅
- 지원 파일 타입 관리
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Set, Dict, Optional, Any

class DiffGeneratorInterface(ABC):
    """Diff 생성기 인터페이스"""
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> Set[str]:
        """
        지원하는 파일 확장자 목록을 반환합니다.
        
        Returns:
            Set[str]: 지원하는 파일 확장자 집합 (예: {'.py', '.md', '.txt'})
        """
        pass
    
    @abstractmethod
    def format_diff(self, diff_data: Dict[str, Any]) -> str:
        """
        diff 데이터를 포맷팅합니다.
        
        Args:
            diff_data: generate_diff()에서 생성된 diff 데이터
            
        Returns:
            str: 포맷팅된 diff 문자열
        """
        pass
    
    @abstractmethod
    def is_supported(self, file_path: Path) -> bool:
        """
        해당 파일이 지원되는지 확인합니다.
        
        Args:
            file_path: 확인할 파일 경로
            
        Returns:
            bool: 지원 여부
        """
        pass
    
    @abstractmethod
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
        pass 