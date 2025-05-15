"""날짜 처리 관련 유틸리티"""

from datetime import datetime, timedelta

def resolve_date(date: str = None) -> str:
    """날짜 문자열을 해석합니다. 날짜가 주어지지 않으면 어제 날짜를 반환합니다."""
    return date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') 