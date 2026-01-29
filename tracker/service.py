from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .logger import get_logger
from .models import Expense
from .storage import load_data, save_data
from .utils import generate_id, now_iso


def add_expense(
    *,
    date: str,
    category: str,
    amount: float,
    note: str,
    currency: str,
) -> Expense:
    data = load_data()
    expense_id = generate_id(data["expenses"], date)
    expense = Expense(
        id=expense_id,
        date=date,
        category=category,
        amount=amount,
        currency=currency,
        note=note,
        created_at=now_iso(),
    )
    data["expenses"].append(expense.to_dict())
    save_data(data)
    get_logger().info("Added expense %s", expense_id)
    return expense


def list_expenses(
    *,
    month: str | None = None,
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    sort_by: str = "date",
    desc: bool = False,
    limit: int | None = None,
) -> list[Expense]:
    data = load_data()
    expenses = [Expense.from_dict(item) for item in data["expenses"]]

    filtered = [
        exp
        for exp in expenses
        if (month is None or exp.date.startswith(month))
        and (category is None or exp.category == category)
        and (min_amount is None or exp.amount >= min_amount)
        and (max_amount is None or exp.amount <= max_amount)
    ]

    sort_keys = {
        "date": lambda exp: exp.date,
        "amount": lambda exp: exp.amount,
        "category": lambda exp: exp.category,
        "created": lambda exp: exp.created_at,
        "id": lambda exp: exp.id,
    }
    filtered.sort(key=sort_keys[sort_by], reverse=desc)

    if limit is not None:
        filtered = filtered[:limit]

    return filtered


def summary(
    *,
    month: str | None = None,
    category: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> tuple[list[Expense], dict[str, float], dict[str, float]]:
    data = load_data()
    expenses = [Expense.from_dict(item) for item in data["expenses"]]

    filtered = [
        exp
        for exp in expenses
        if (month is None or exp.date.startswith(month))
        and (category is None or exp.category == category)
        and (from_date is None or exp.date >= from_date)
        and (to_date is None or exp.date <= to_date)
    ]

    category_totals: dict[str, float] = {}
    month_totals: dict[str, float] = {}

    for expense in filtered:
        category_totals[expense.category] = (
            category_totals.get(expense.category, 0.0) + expense.amount
        )
        month_key = expense.date[:7]
        month_totals[month_key] = month_totals.get(month_key, 0.0) + expense.amount

    return filtered, category_totals, month_totals


def export_csv(path: str, expenses: Iterable[Expense]) -> Path:
    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["id", "date", "category", "amount", "currency", "note", "created_at"]
        )
        for exp in expenses:
            writer.writerow(
                [
                    exp.id,
                    exp.date,
                    exp.category,
                    f"{exp.amount:.2f}",
                    exp.currency,
                    exp.note,
                    exp.created_at,
                ]
            )
    get_logger().info("Exported expenses to %s", csv_path)
    return csv_path
