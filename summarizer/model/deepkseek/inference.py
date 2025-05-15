import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse
import os
import glob

# ================================
# 모델 로딩 (초기화 1번만)
# ================================
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16
).cuda()

# ================================
# 함수: 텍스트 추론 (프롬프트 주입)
# ================================
def infer(prompt: str, max_new_tokens: int = 512) -> str:
    messages = [
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)

    outputs = model.generate(
        inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
    return result.strip()

# ================================
# 함수: 파일 읽고 타입별 요약 요청
# ================================
def summarize_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path).lower()

    if ext in [".py", ".diff"]:
        prompt = (
            "다음은 코드 파일 또는 코드 변경사항(diff)입니다. "
            "주요 변경사항이나 동작을 간단히 요약해 주세요.\n\n"
            f"```python\n{content}\n```"
        )
    elif ext in [".md", ".txt"] or "readme" in filename:
        prompt = (
            "다음은 문서 파일입니다. "
            "핵심 주제와 중요한 내용을 요약해 주세요.\n\n"
            f"{content}"
        )
    else:
        prompt = (
            "다음은 텍스트 파일입니다. "
            "주요 내용을 요약해 주세요.\n\n"
            f"{content}"
        )

    summary = infer(prompt)
    return summary

# ================================
# 함수: 요약 결과 파일로 저장
# ================================
def save_summary(file_path: str, summary: str) -> None:
    summary_path = file_path + ".summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

# ================================
# 함수: 디렉토리 배치 요약 처리
# ================================
def batch_summarize(directory: str) -> None:
    files = glob.glob(os.path.join(directory, "**"), recursive=True)
    target_files = [f for f in files if os.path.isfile(f) and os.path.splitext(f)[1].lower() in [".py", ".diff", ".md", ".txt"]]

    print(f"총 {len(target_files)}개 파일 요약 시작...")

    for file_path in target_files:
        print(f"요약 중: {file_path}")
        summary = summarize_file(file_path)
        save_summary(file_path, summary)
        print(f"완료: {file_path}.summary.txt 생성\n")

# ================================
# 메인 실행부
# ================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="요약할 파일 경로")
    parser.add_argument("--dir", type=str, help="요약할 디렉토리 경로 (batch mode)")
    args = parser.parse_args()

    if args.dir:
        batch_summarize(args.dir)
    elif args.file:
        summary = summarize_file(args.file)
        print("\n===== 요약 결과 =====\n")
        print(summary)
        print("\n======================\n")
        save_summary(args.file, summary)
        print(f"요약 결과가 {args.file}.summary.txt 파일로 저장되었습니다.")
    else:
        print("--file 또는 --dir 중 하나를 지정해야 합니다.")

# python inference.py --file "C:\Users\jeahyuk\github\dailyActivityTracker\storage\activities\2025-04-28\diffs\BitNet_run_inference_with_file.py.111951.diff"