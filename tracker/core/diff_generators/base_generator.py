"""
Diff 생성기 기본 클래스
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseDiffGenerator(ABC):
    """모든 diff 생성기의 기본이 되는 추상 클래스"""
    
    @abstractmethod
    def generate_diff(self, old_content: Any, new_content: Any) -> Dict[str, Any]:
        """
        두 버전의 내용을 비교하여 diff를 생성합니다.
        
        Args:
            old_content: 이전 버전의 내용
            new_content: 새로운 버전의 내용
            
        Returns:
            Dict[str, Any]: 생성된 diff 정보
        """
        pass
    
    @abstractmethod
    def can_handle(self, file_extension: str) -> bool:
        """
        해당 파일 확장자를 처리할 수 있는지 확인합니다.
        
        Args:
            file_extension: 파일 확장자 (예: '.txt', '.py')
            
        Returns:
            bool: 처리 가능 여부
        """
        pass
    
    def get_file_type(self) -> str:
        """
        이 생성기가 처리하는 파일 타입을 반환합니다.
        
        Returns:
            str: 파일 타입 설명
        """
        return self.__class__.__name__.replace('DiffGenerator', '').lower() 