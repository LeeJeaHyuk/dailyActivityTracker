from pathlib import Path
from .core import call_llm_for_summary

class LLMSummarizer:
    def __init__(self):
        # BitNet Inference 관련 경로 설정
        self.inference_script = Path(__file__).parent / "model" / "BitNetInference" / "scripts" / "run_inference.py"
        self.model_path = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"  # 상대경로 