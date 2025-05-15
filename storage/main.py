"""
저장소 관리 실행
- 데이터 검증
- 데이터 정리
- 데이터 전처리
"""

import argparse
import logging
from pathlib import Path
from core.manager import StorageManager

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_command(args):
    """데이터 검증 명령어 처리"""
    manager = StorageManager(Path(args.directory))
    results = manager.validate_storage()
    
    # 검증 결과 출력
    print("\n=== 검증 결과 ===")
    for category, files in results.items():
        print(f"\n{category}:")
        if files:
            for file in files:
                print(f"  - {file}")
        else:
            print("  문제 없음")

def clean_command(args):
    """데이터 정리 명령어 처리"""
    manager = StorageManager(Path(args.directory))
    stats = manager.clean_storage(
        max_age_days=args.max_age,
        remove_duplicates=args.remove_duplicates
    )
    
    # 정리 결과 출력
    print("\n=== 정리 결과 ===")
    print(f"제거된 오래된 파일: {stats['removed_old']}개")
    print(f"제거된 중복 파일: {stats['removed_duplicates']}개")
    print(f"제거된 불필요 파일: {stats['removed_unnecessary']}개")
    print(f"해제된 공간: {stats['freed_space'] / 1024 / 1024:.2f}MB")

def preprocess_command(args):
    """데이터 전처리 명령어 처리"""
    manager = StorageManager(Path(args.directory))
    stats = manager.preprocess_data(
        convert_formats=args.convert_formats,
        clean_metadata=args.clean_metadata
    )
    
    # 전처리 결과 출력
    print("\n=== 전처리 결과 ===")
    print(f"변환된 파일: {stats['converted']}개")
    print(f"정리된 메타데이터: {stats['cleaned']}개")
    print(f"생성된 백업: {stats['backed_up']}개")

def stats_command(args):
    """통계 정보 조회 명령어 처리"""
    manager = StorageManager(Path(args.directory))
    stats = manager.get_storage_stats()
    
    # 통계 정보 출력
    print("\n=== 저장소 통계 ===")
    print(f"전체 파일 수: {stats['total_files']}개")
    print(f"전체 크기: {stats['total_size'] / 1024 / 1024:.2f}MB")
    print(f"오래된 파일 수: {stats['old_files']}개")
    print(f"중복 파일 수: {stats['duplicate_files']}개")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='저장소 관리 도구')
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # 공통 인자
    for subparser in [subparsers.add_parser('validate'),
                     subparsers.add_parser('clean'),
                     subparsers.add_parser('preprocess'),
                     subparsers.add_parser('stats')]:
        subparser.add_argument('directory', help='저장소 디렉토리 경로')

    # clean 명령어 인자
    clean_parser = subparsers.choices['clean']
    clean_parser.add_argument('--max-age', type=int, default=30,
                            help='보관할 최대 일수 (기본값: 30)')
    clean_parser.add_argument('--remove-duplicates', action='store_true',
                            help='중복 파일 제거')

    # preprocess 명령어 인자
    preprocess_parser = subparsers.choices['preprocess']
    preprocess_parser.add_argument('--convert-formats', action='store_true',
                                 help='파일 형식 변환')
    preprocess_parser.add_argument('--clean-metadata', action='store_true',
                                 help='메타데이터 정리')

    args = parser.parse_args()

    # 로깅 설정
    setup_logging()

    # 명령어 처리
    if args.command == 'validate':
        validate_command(args)
    elif args.command == 'clean':
        clean_command(args)
    elif args.command == 'preprocess':
        preprocess_command(args)
    elif args.command == 'stats':
        stats_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 