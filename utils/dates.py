from datetime import datetime, timedelta

_PT_DAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def get_lookback_range() -> tuple[str, str, str, str]:
    today = datetime.now()
    weekday = today.weekday()
    days_from = 3 if weekday == 0 else (2 if weekday == 6 else 1)
    date_from = (today - timedelta(days=days_from)).strftime("%Y-%m-%d")
    date_to = today.strftime("%Y-%m-%d")
    since = date_from + "T00:00:00.000+0000"
    until = date_to + "T23:59:59.999+0000"
    return date_from, date_to, since, until


def shift_date(date_str: str, days: int) -> str:
    return (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")


def date_in_range(date: str, since: str, until: str) -> bool:
    return since <= date <= until


def day_label(at: str) -> str:
    d = datetime.strptime(at[:10], "%Y-%m-%d").date()
    delta = (datetime.now().date() - d).days
    if delta == 0:
        return "Hoje"
    if delta == 1:
        return "Ontem"
    return _PT_DAYS[d.weekday()]
