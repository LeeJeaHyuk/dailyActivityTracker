import os
import platform
import subprocess
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import sys

class ModelInferenceError(Exception):
    """모델 추론 중 발생하는 에러를 처리하기 위한 커스텀 예외"""
    pass

def validate_paths(base_dir: str) -> Dict[str, str]:
    """필요한 파일 경로들을 검증하고 반환합니다."""
    paths = {
        'main': os.path.join(base_dir, "..", "bin", "llama-cli.exe" if platform.system() == "Windows" else "llama-cli"),
        'model': os.path.join(base_dir, "..", "models", "BitNet-b1.58-2B-4T", "ggml-model-i2_s.gguf")
    }
    
    for name, path in paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name} 파일이 존재하지 않습니다: {path}")
    
    return paths

def get_model_config() -> Dict[str, Any]:
    """모델 실행에 필요한 설정값을 반환합니다."""
    return {
        'max_tokens': 128,
        'threads': 2,
        'context_size': 2048,
        'temperature': 0.8,
        'timeout': 30  # 초 단위
    }

def chat_with_model(system_prompt: str, prompts: List[str], config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    모델과 대화를 수행합니다.
    
    Args:
        system_prompt (str): 시스템 프롬프트
        prompts (List[str]): 사용자 프롬프트 리스트
        config (Optional[Dict[str, Any]]): 모델 설정값
        
    Returns:
        List[str]: 모델의 응답 리스트
        
    Raises:
        ModelInferenceError: 모델 추론 중 에러 발생 시
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = config or get_model_config()
    
    try:
        paths = validate_paths(base_dir)
    except FileNotFoundError as e:
        raise ModelInferenceError(str(e))

    # 모델 실행 명령어 구성
    cmd = [
        paths['main'],
        "-m", paths['model'],
        "-p", system_prompt,
        "-n", str(config['max_tokens']),
        "-t", str(config['threads']),
        "-c", str(config['context_size']),
        "--temp", str(config['temperature']),
        "-cnv"
    ]

    responses = []
    process = None

    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # 초기 system prompt에 대한 반응 읽기
        start_time = time.time()
        while time.time() - start_time < config['timeout']:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output and ">" in output:
                break
            if output:
                print(output.strip())

        # 각 프롬프트에 대한 응답 처리
        for prompt in prompts:
            print(f"\nSending prompt: {prompt}")
            process.stdin.write(prompt + "\n")
            process.stdin.flush()

            response = []
            start_time = time.time()
            while time.time() - start_time < config['timeout']:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    response.append(output.strip())
                if ">" in output:
                    break

            responses.append("\n".join(response))

    except subprocess.TimeoutExpired:
        raise ModelInferenceError("모델 응답 시간 초과")
    except Exception as e:
        raise ModelInferenceError(f"모델 추론 중 에러 발생: {str(e)}")
    finally:
        if process:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"프로세스 종료 중 에러 발생: {str(e)}")

    return responses

if __name__ == "__main__":
    try:
        system_prompt = "You are a helpful assistant."
        prompts = [
            "Hello, how are you?",
            "Can you tell me a joke?",
            "What's the weather like today?"
        ]
        
        responses = chat_with_model(system_prompt, prompts)
        print("\n모델 응답:")
        for i, response in enumerate(responses, 1):
            print(f"\n응답 {i}:")
            print(response)
            
    except ModelInferenceError as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)
