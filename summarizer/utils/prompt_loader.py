"""프롬프트 파일 로딩 관련 유틸리티"""

import sys
from pathlib import Path

def load_prompt(prompt_type: str) -> str:
    """프롬프트 파일을 로드합니다."""
    prompt_file = Path(__file__).parent.parent / "prompts" / f"{prompt_type}.txt"
    try:
        content = prompt_file.read_text(encoding='utf-8')
        if not content.strip():
            print(f"❌ 프롬프트 파일이 비어있습니다: {prompt_file}")
            sys.exit(1)
        return content
    except FileNotFoundError:
        print(f"❌ 프롬프트 파일을 찾을 수 없습니다: {prompt_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 프롬프트 파일 로드 실패 ({prompt_type}): {e}")
        sys.exit(1) 