from __future__ import annotations

from datetime import date as date_cls, datetime


DATE_FMT = "%Y-%m-%d"
MONTH_FMT = "%Y-%m"


def parse_date(date_str: str) -> date_cls:
    try:
        return datetime.strptime(date_str, DATE_FMT).date()
    except ValueError as exc:
        raise ValueError("date must be YYYY-MM-DD") from exc


def parse_month(month_str: str) -> tuple[int, int]:
    try:
        parsed = datetime.strptime(month_str, MONTH_FMT)
    except ValueError as exc:
        raise ValueError("month must be YYYY-MM") from exc
    return parsed.year, parsed.month


def today_str() -> str:
    return date_cls.today().strftime(DATE_FMT)


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def format_amount(amount: float, currency: str) -> str:
    return f"{amount:.2f} {currency}"


def generate_id(expenses: list[dict], date_str: str) -> str:
    prefix = f"EXP-{date_str.replace('-', '')}-"
    seq = 1
    existing = [
        int(item["id"].split("-")[-1])
        for item in expenses
        if isinstance(item.get("id"), str) and item["id"].startswith(prefix)
    ]
    if existing:
        seq = max(existing) + 1
    return f"{prefix}{seq:04d}"
