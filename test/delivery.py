from datetime import datetime, timedelta

DELIVERY_DAYS = 2

def _is_holiday(day: datetime) -> bool:
    return day.weekday() >= 6  # 일요일만 휴일

def get_eta(purchase_date: datetime) -> datetime:
    current_date = purchase_date
    remaining_days = DELIVERY_DAYS

    while remaining_days > 0:
        current_date += timedelta(days=1)
        if not _is_holiday(current_date):
            remaining_days -= 1

    return current_date
