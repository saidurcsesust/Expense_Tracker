from __future__ import annotations

from datetime import date as date_cls, datetime


DATE_FMT = "%Y-%m-%d"
MONTH_FMT = "%Y-%m"


# Parse YYYY-MM-DD date.
def parse_date(date_str: str) -> date_cls:
    try:
        return datetime.strptime(date_str, DATE_FMT).date()
    except ValueError as exc:
        raise ValueError("date must be YYYY-MM-DD") from exc


# Parse YYYY-MM month.
def parse_month(month_str: str) -> tuple[int, int]:
    try:
        parsed = datetime.strptime(month_str, MONTH_FMT)
    except ValueError as exc:
        raise ValueError("month must be YYYY-MM") from exc
    return parsed.year, parsed.month


# Today's date in YYYY-MM-DD.
def today_str() -> str:
    return date_cls.today().strftime(DATE_FMT)


# Current timestamp in ISO format.
def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


# Format amount with currency.
def format_amount(amount: float, currency: str) -> str:
    return f"{amount:.2f} {currency}"


# Generate unique expense id for a date.
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
