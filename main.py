import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from storage.core.activity_logger import ActivityLogger
from storage.core.diff_storage import DiffStorage
from summarizer.core.summary_generator import main as generate_summary
from tracker.core.diff_tracker import main as track_diff
import config

def parse_args():
    parser = argparse.ArgumentParser(description='Daily Activity Tracker')
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # diff 추적 명령어
    track_parser = subparsers.add_parser('track', help='파일 변경사항 추적')
    track_parser.add_argument('--no-backup', action='store_true', help='백업 없이 diff 추적 시작')

    # 백업만 수행하는 명령어
    backup_parser = subparsers.add_parser('backup', help='백업만 수행')
    backup_parser.add_argument('--summary', action='store_true', help='백업 결과 요약 출력')

    # 요약 생성 명령어
    summarize_parser = subparsers.add_parser('summarize', help='변경사항 요약 생성')
    summarize_parser.add_argument('--date', help='요약할 날짜 (YYYY-MM-DD)')
    summarize_parser.add_argument('--today', action='store_true', help='오늘 날짜를 요약')
    summarize_parser.add_argument('--system-prompt', help='LLM에 사용할 시스템 프롬프트')

    # 활동 조회 명령어
    view_parser = subparsers.add_parser('view', help='활동 기록 조회')
    view_parser.add_argument('--date', help='조회할 날짜 (YYYY-MM-DD)')

    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.command == 'summarize':
        date = args.date
        if args.today:
            date = datetime.now().strftime('%Y-%m-%d')
        generate_summary(date, args.system_prompt)
    elif args.command == 'track':
        track_diff()
    # 다른 명령어들에 대한 처리 추가 예정

if __name__ == "__main__":
    main()
