"""
요약 생성 메인 모듈
- diff 파일 병합
- 개별 요약 생성
- 전체 요약 생성
"""

import sys
from pathlib import Path
from core.summary_generator import main as generate_summary

def main():
    """메인 함수"""
    print("\n" + "="*40)
    print("📝 요약 생성 시작...")
    
    # 명령행 인자 처리
    date = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # 요약 생성
        generate_summary(date)
        print("✅ 요약이 완료되었습니다.")
        
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 