# 📈 Daily Activity Tracker

일일 활동 추적 및 백업 시스템

## 프로젝트 구조

```
dailyActivityTracker/
├── config/                 # 전역 설정 파일
│   ├── base_config.py     # 기본 설정
│   ├── tracker_config.py  # 파일 추적 설정
│   ├── storage_config.py  # 저장소 설정
│   └── summarizer_config.py # 요약 설정
│
├── tracker/               # 파일 변경 추적 모듈
│   ├── core/             # 핵심 기능
│   │   ├── manager.py    # 트래커 관리자
│   │   ├── file_watcher.py # 파일 감시
│   │   └── diff_tracker.py # 변경 추적
│   ├── utils/            # 유틸리티
│   │   ├── file_filter.py # 파일 필터링
│   │   └── backup_manager.py # 백업 관리
│   └── main.py           # 트래커 실행
│
├── summarizer/           # 변경 사항 요약 모듈
│   ├── core/            # 핵심 기능
│   │   └── summary_generator.py # 요약 생성
│   ├── utils/           # 유틸리티
│   ├── prompts/         # LLM 프롬프트
│   └── main.py          # 요약 실행
│
├── storage/             # 저장소 관리 모듈
│   ├── core/           # 핵심 기능
│   │   ├── manager.py  # 저장소 관리자
│   │   ├── validator.py # 데이터 검증
│   │   └── cleaner.py  # 데이터 정리
│   ├── utils/          # 유틸리티
│   │   ├── file_utils.py # 파일 처리
│   │   └── backup_utils.py # 백업 처리
│   └── main.py         # 저장소 관리 실행
│
├── utils/              # 전역 유틸리티
├── logs/              # 로그 파일
└── main.py           # 메인 실행 파일
```

## 하위 프로젝트

### 1. Tracker
파일 변경 사항을 추적하고 백업하는 모듈
- 파일 변경 감시
- 변경 사항 백업
- 변경 이력 관리

### 2. Summarizer
변경 사항을 요약하는 모듈
- LLM 기반 요약
- 변경 사항 분석
- 요약 보고서 생성

### 3. Storage
데이터 저장소 관리 모듈
- 데이터 검증 및 정리
- 저장 구조 관리
- 백업 및 복구
- 저장 공간 최적화

## 표준 디렉토리 구조

각 하위 프로젝트는 다음 구조를 따릅니다:
```
project/
├── core/           # 핵심 기능
├── utils/          # 유틸리티
├── main.py         # 실행 파일
└── README.md       # 프로젝트 문서
```

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 설정:
- `config/base_config.py`에서 기본 설정 확인
- `config/tracker_config.py`에서 추적 설정 확인
- `config/summarizer_config.py`에서 요약 설정 확인

3. 실행:
```bash
# 전체 시스템 실행
python main.py

# 개별 모듈 실행
python tracker/main.py
python summarizer/main.py
```

## 설정

각 모듈의 설정은 `config` 디렉토리에서 관리됩니다:
- `base_config.py`: 기본 설정 (경로, 모델 등)
- `tracker_config.py`: 파일 추적 설정
- `storage_config.py`: 저장소 설정
- `summarizer_config.py`: 요약 설정

## 로그

로그 파일은 `logs` 디렉토리에 저장됩니다:
- `tracker.log`: 파일 추적 로그
- `summarizer.log`: 요약 로그
- `storage.log`: 저장소 로그

## ✨ 주요 기능

- 하루 동안 진행한 **코딩 및 문서 작업의 전체 이력**을 자동으로 기록
- 변경사항을 diff 형식으로 저장하여 **정확한 변경 내용 추적**
- LLM을 통한 **자동 요약 생성**으로 작업 내용 파악 용이
- 날짜별로 구조화된 저장으로 **활동 이력 관리 용이**
- 변경 크기와 시간 간격 제어로 **저장 공간 효율적 관리**

## 🚀 설치 및 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
# OpenAI API를 사용하는 경우
export OPENAI_API_KEY='your-api-key'
```

### 3. 실행 방법

#### Diff 추적 실행
```bash
# 메인 실행 파일 사용
python main.py track

# 또는 직접 실행
python tracker/diff_tracker.py
```

#### 요약 생성 실행
```bash
# 메인 실행 파일 사용
python main.py summarize

# 또는 직접 실행
python summarizer/summary_generator.py
```

#### 활동 기록 조회
```bash
# 특정 날짜의 활동 기록 조회
python main.py view --date 2024-04-26

# 특정 파일의 활동 기록 조회
python main.py view --date 2024-04-26 --file path/to/file.py
```

## 📁 프로젝트 구조

```
DailyActivityTracker/
├── tracker/
│   ├── file_watcher.py        # 파일 시스템 이벤트 감시
│   ├── content_tracker.py     # 파일 내용 변경 추적
│   └── diff_tracker.py        # diff 추적 실행 파일
├── summarizer/
│   ├── llm_summarizer.py      # LLM을 통한 일일 요약 생성
│   └── summary_generator.py   # 요약 생성 실행 파일
├── storage/
│   ├── diff_storage.py        # diff 저장 및 관리
│   └── activity_logger.py     # 활동 기록 관리
├── tools/
│   └── clean_diffs.py         # diff 파일 정리 도구
├── config.py                  # 환경 설정
├── main.py                    # 메인 실행 파일
└── README.md                  # 프로젝트 설명 문서
```

## 📦 저장 구조

```
storage/
└── activities/
    └── 2024-04-26/                    # 날짜별 디렉토리
        ├── diffs/                      # diff 저장
        │   ├── example.py.120000.diff  # 파일별 diff (시간 포함)
        │   └── README.md.123000.diff
        ├── metadata/                   # 메타데이터
        │   ├── example.py.json         # 파일별 메타데이터
        │   └── README.md.json
        └── summaries/                  # 요약
            └── daily_summary.md        # 일일 요약
```

## ⚙️ 환경 설정 (config.py)

```python
# 기본 설정
WATCH_DIR = Path('C:/Users/jeahyuk/github')  # 감시할 디렉토리
FILE_EXTENSIONS = ['.py', '.md']             # 감시할 파일 확장자
EXCLUDE_DIRS = ['__pycache__', '.git']       # 제외할 디렉토리
MAX_FILE_SIZE = 10 * 1024 * 1024            # 최대 파일 크기 (10MB)

# 저장 설정
STORAGE_DIR = ROOT_DIR / 'storage' / 'activities'  # 저장 디렉토리

# Diff 저장 설정
MIN_CHANGE_SIZE = 10     # 최소 변경 크기 (문자 수)
MIN_CHANGE_LINES = 5     # 최소 변경 줄 수
MIN_SAVE_INTERVAL = 5    # 최소 저장 간격 (초)
MAX_DIFFS_PER_FILE = 50  # 파일당 최대 diff 수

# LLM 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')       # OpenAI API 키
MODEL_NAME = 'gpt-3.5-turbo'                       # 모델 이름
```

## 🔧 Diff 저장 제어

### 1. 최소 변경 크기
- `MIN_CHANGE_SIZE = 10`: 10자 미만의 변경은 무시
- `MIN_CHANGE_LINES = 5`: 5줄 미만의 변경은 무시
- 너무 작은 변경사항은 diff로 저장하지 않음

### 2. 최소 저장 간격
- `MIN_SAVE_INTERVAL = 5`: 5초 이내의 연속된 변경은 하나로 통합
- 짧은 시간 내의 연속된 변경을 하나의 diff로 통합

### 3. 최대 diff 수
- `MAX_DIFFS_PER_FILE = 50`: 파일당 하루 최대 50개의 diff만 저장
- 이를 초과하면 더 이상의 diff는 저장하지 않음

## 🧹 파일 정리 도구 (clean_diffs.py)

잘못 생성되거나 중복된 파일들을 정리하는 도구입니다.

### 주요 기능
- 프로젝트별/날짜별 폴더 구조 검증
- 잘못된 형식의 파일 감지 및 정리
- 중복 파일 감지
- 메타데이터와 diff 파일 간의 일관성 검사

### 검증 항목
1. 파일 위치 검증
   - 올바른 폴더 구조: `프로젝트/날짜/diffs/*.diff`
   - 날짜 형식: `YYYY-MM-DD`

2. 파일명 검증
   - diff 파일: `파일명.HHMMSS.diff`
   - 중복된 확장자 검사 (예: `.json.json`, `.diff.diff`)

3. 중복 파일 검사
   - MD5 해시를 통한 파일 내용 비교
   - 동일한 내용의 파일 그룹화

### 사용법
```bash
python tools/clean_diffs.py
```

실행하면:
1. 잘못된 위치나 형식의 파일을 감지
2. 중복된 파일을 보고
3. 문제가 있는 파일을 백업 후 삭제
4. 메타데이터 파일 정리

### 백업
- 삭제된 파일은 `invalid_files_backup` 폴더에 원본 경로 구조를 유지하여 백업됨
- 실수로 삭제된 파일은 백업 폴더에서 복구 가능

## ⚠️ 주의사항

1. 백업 확인
   - 파일 정리 전에 중요한 데이터 백업
   - 정리 후 `invalid_files_backup` 폴더 확인

2. 수동 복구
   - 필요한 경우 백업 폴더에서 파일 복구 가능
