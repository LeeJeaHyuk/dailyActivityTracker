# Daily Activity Tracker

파일 변경을 감시하고 백업을 관리하는 파일 트래킹 시스템입니다.

## 프로젝트 구조

```
tracker/
├── core/
│   ├── file_watcher.py    # 파일 변경 감시 모듈
│   ├── manager.py         # 트래커 관리자
│   ├── diff_tracker.py    # diff 추적 모듈
│   └── utils/            # 유틸리티 모듈
├── main.py               # 메인 실행 파일
└── README.md            # 프로젝트 문서
```

## 주요 모듈 설명

### main.py
메인 실행 파일로, 파일 변경 감시를 시작하고 중지하는 기능을 제공합니다.

- `main()`: 프로그램의 진입점으로, TrackerManager를 초기화하고 파일 변경 감시를 시작합니다.

### core/manager.py
파일 변경 추적 관련 모든 기능을 통합 관리하는 클래스를 포함합니다.

#### TrackerManager 클래스
- `__init__(watch_dir, backup_dir, on_file_modified)`: 트래커 매니저를 초기화합니다.
- `start()`: 파일 변경 감시를 시작합니다.
- `stop()`: 파일 변경 감시를 중지합니다.
- `load_backup_content(file_path)`: 파일의 백업 내용을 로드합니다.
- `update_backup(file_path, new_content)`: 파일의 백업을 업데이트합니다.
- `has_backup(file_path)`: 파일의 백업이 존재하는지 확인합니다.

### core/file_watcher.py
파일 변경을 감시하는 모듈입니다.

#### FileWatcher 클래스
- `__init__(watch_dir, file_filter, on_modified)`: 파일 감시기를 초기화합니다.
- `start()`: 파일 감시를 시작합니다.
- `stop()`: 파일 감시를 중지합니다.

#### FileChangeHandler 클래스
- `on_created(event)`: 파일 생성 이벤트를 처리합니다.
- `on_modified(event)`: 파일 수정 이벤트를 처리합니다.
- `on_deleted(event)`: 파일 삭제 이벤트를 처리합니다.

## 사용 방법

1. 프로그램 실행:
```bash
python main.py
```

2. 파일 변경 감시 시작:
- 프로그램이 실행되면 자동으로 지정된 디렉토리의 파일 변경을 감시합니다.
- 파일이 수정되면 자동으로 백업이 생성됩니다.

3. 프로그램 종료:
- Ctrl+C를 눌러 프로그램을 종료할 수 있습니다.

## 주요 기능

- 실시간 파일 변경 감시
- 자동 백업 생성 및 관리
- 파일 변경 이력 추적
- 지정된 파일 확장자만 감시
- 제외 디렉토리 설정
- 최대 파일 크기 제한 