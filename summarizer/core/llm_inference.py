"""LLM 추론 관련 모듈"""

import subprocess
from pathlib import Path

def call_llm_for_summary(prompt: str, system_prompt: str) -> str:
    """로컬 LLM을 호출하여 요약을 생성합니다."""
    inference_script = Path(__file__).parent.parent / "model" / "deepkseek" / "inference.py"
    command = [
        "python", str(inference_script),
        "--system-prompt", system_prompt,
        "--user-prompt", prompt,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 로컬 모델 호출 실패: {e.stderr}")
        return "요약 생성 실패" 