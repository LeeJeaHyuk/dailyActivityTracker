"""
핵심 비즈니스 로직을 포함하는 패키지
- summary_generator: 요약 생성 관련
- diff_merger: diff 병합 관련
- llm_inference: LLM 모델 호출 관련
"""

from .summary_generator import main as generate_summary
from .diff_merger import DiffMerger
from .llm_inference import call_llm_for_summary

__all__ = ['generate_summary', 'DiffMerger', 'call_llm_for_summary'] 