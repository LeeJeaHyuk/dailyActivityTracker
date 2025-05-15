# Storage Module

데이터 저장소 관리 모듈

## 구조

```
storage/
├── core/            # 핵심 기능
│   ├── manager.py   # 저장소 관리자
│   ├── validator.py # 데이터 검증
│   └── cleaner.py   # 데이터 정리
├── utils/           # 유틸리티
│   ├── file_utils.py # 파일 처리
│   └── backup_utils.py # 백업 처리
└── main.py          # 저장소 관리 실행
```

## 기능

- 데이터 검증
  - 저장 구조 검증
  - 파일 형식 검증
  - 메타데이터 검증
  - 중복 데이터 검사

- 데이터 정리
  - 오래된 데이터 정리
  - 중복 데이터 제거
  - 불필요한 파일 정리
  - 저장 공간 최적화

- 데이터 전처리
  - 파일 형식 변환
  - 메타데이터 정리
  - 데이터 구조화
  - 백업 생성

## 사용 방법

1. 설정:
   - `config/storage_config.py`에서 설정 확인
   - 저장소 경로 설정
   - 정리 정책 설정
   - 백업 설정

2. 실행:
```bash
# 데이터 검증
python main.py validate

# 데이터 정리
python main.py clean

# 데이터 전처리
python main.py preprocess
```

## 의존성

- `pathlib`: 경로 처리
- `config`: 설정 관리
- `watchdog`: 파일 시스템 이벤트 감시 