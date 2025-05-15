from .base_config import MODEL_NAME, USE_LOCAL_LLM, DEFAULT_SYSTEM_PROMPT

# 요약 템플릿
SUMMARY_TEMPLATE = """
다음은 하루 동안의 파일 변경사항입니다. 핵심 변경사항을 중심으로 5문장 이내로 요약해주세요:
{changes}
"""

# LLM 요약 설정
SUMMARY_MODEL_NAME = MODEL_NAME
USE_LOCAL_LLM_FOR_SUMMARY = USE_LOCAL_LLM
SUMMARY_SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT 