"""요약 생성 모듈"""

import sys
from pathlib import Path
from summarizer.core.diff_merger import DiffMerger
from summarizer.utils.prompt_loader import load_prompt
from summarizer.utils.date_utils import resolve_date
from summarizer.utils.file_utils import validate_storage_dirs
from summarizer.llm.inference import call_llm_for_summary
from config import STORAGE_DIR, DEFAULT_SYSTEM_PROMPT

def merge_diffs_for_date(target_dir: Path):
    """해당 날짜의 diff 파일들을 병합합니다."""
    print(f"🔍 diff 디렉토리: {target_dir}")
    merger = DiffMerger(diff_dir=str(target_dir))
    merger.run()
    final_diffs = list(target_dir.glob("*_final.diff"))
    if not final_diffs:
        print("⚠️ 통합된 diff 파일이 없습니다.")
        sys.exit(0)
    print(f"🔍 발견된 통합 diff 파일 수: {len(final_diffs)}")
    return final_diffs

def summarize_each_diff(final_diffs, system_prompt, target_date):
    """각 diff 파일을 요약합니다."""
    summaries = []
    system_prompt = system_prompt or load_prompt("system_summary")
    
    for final_diff in final_diffs:
        print(f"📝 처리 중인 파일: {final_diff.name}")
        with open(final_diff, 'r', encoding='utf-8') as f:
            diff_content = f.read()
        summary = call_llm_for_summary(diff_content, system_prompt)

        summary_filename = final_diff.stem.replace('_final', '')
        summary_path = STORAGE_DIR / target_date / 'summaries' / f'{summary_filename}.md'
        summary_path.parent.mkdir(parents=True, exist_ok=True)

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"# Summary - {summary_filename}\n\n")
            f.write(summary)

        summaries.append((summary_filename, summary))
        print(f"✅ 요약이 저장되었습니다: {summary_path}")
    return summaries

def generate_overall_summary(summaries, target_date, system_prompt):
    """전체 요약을 생성합니다."""
    combined = ""
    for name, content in summaries:
        combined += f"\n\n## {name}\n\n{content}"

    total_prompt = load_prompt("total_summary")
    total_prompt += f"\n\n{combined}"  # 프롬프트 내용 뒤에 combined 추가
    
    return call_llm_for_summary(total_prompt, system_prompt)

def save_total_summary(total_summary: str, target_date: str):
    """전체 요약을 저장합니다."""
    summary_path = STORAGE_DIR / target_date / 'summaries' / 'total_summary.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# Total Summary - {target_date}\n\n")
        f.write(total_summary)
    print(f"✅ 전체 총평이 저장되었습니다: {summary_path}")

def main(date=None, system_prompt=None):
    """메인 함수"""
    print("\n" + "="*40)
    target_date = resolve_date(date)
    print(f"📄 {target_date}의 변경사항 요약 생성 중...")

    target_dir = validate_storage_dirs(target_date)
    final_diffs = merge_diffs_for_date(target_dir)
    summaries = summarize_each_diff(final_diffs, system_prompt, target_date)

    print("\n📊 전체 총평 생성 중...")
    total_summary = generate_overall_summary(summaries, target_date, system_prompt)
    save_total_summary(total_summary, target_date)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
