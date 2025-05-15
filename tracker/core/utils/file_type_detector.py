"""
파일 타입 감지 유틸리티
"""

from typing import List, Optional
from ..diff_generators.base_generator import BaseDiffGenerator

class FileTypeDetector:
    """파일 타입에 따른 적절한 diff 생성기를 선택하는 클래스"""
    
    def __init__(self):
        self.generators: List[BaseDiffGenerator] = []
    
    def register_generator(self, generator: BaseDiffGenerator) -> None:
        """
        새로운 diff 생성기를 등록합니다.
        
        Args:
            generator: 등록할 diff 생성기
        """
        if not isinstance(generator, BaseDiffGenerator):
            raise TypeError("generator는 BaseDiffGenerator의 인스턴스여야 합니다.")
        self.generators.append(generator)
    
    def get_generator(self, file_extension: str) -> Optional[BaseDiffGenerator]:
        """
        파일 확장자에 맞는 diff 생성기를 반환합니다.
        
        Args:
            file_extension: 파일 확장자 (예: '.txt', '.py')
            
        Returns:
            Optional[BaseDiffGenerator]: 적절한 diff 생성기 또는 None
        """
        for generator in self.generators:
            if generator.can_handle(file_extension):
                return generator
        return None
    
    def get_supported_extensions(self) -> List[str]:
        """
        등록된 모든 생성기가 지원하는 파일 확장자 목록을 반환합니다.
        
        Returns:
            List[str]: 지원하는 파일 확장자 목록
        """
        extensions = set()
        for generator in self.generators:
            if hasattr(generator, 'supported_extensions'):
                extensions.update(generator.supported_extensions)
        return sorted(list(extensions)) 