# Summarizer Module

변경 사항을 요약하는 모듈

## 구조

```
summarizer/
├── core/            # 핵심 기능
│   └── summary_generator.py # 요약 생성
├── utils/           # 유틸리티
├── prompts/         # LLM 프롬프트
└── main.py          # 요약 실행
```

## 기능

- LLM 기반 요약
  - 변경 사항 분석
  - 자연어 요약 생성
  - 요약 보고서 생성

- 변경 사항 분석
  - diff 분석
  - 코드 변경 분석
  - 문서 변경 분석

- 요약 보고서 생성
  - 일일 활동 요약
  - 변경 사항 통계
  - 중요 변경 사항 하이라이트

## 사용 방법

1. 설정:
   - `config/summarizer_config.py`에서 설정 확인
   - LLM 모델 설정
   - 프롬프트 설정
   - 요약 설정

2. 실행:
```bash
python main.py
```

## 의존성

- `transformers`: LLM 모델 사용
- `config`: 설정 관리
- `prompts`: 프롬프트 관리 