from __future__ import annotations

import argparse
import sys

from .service import add_expense, export_csv, list_expenses, summary
from .utils import format_amount, parse_date, parse_month, today_str


def _positive_amount(value: str) -> float:
    try:
        amount = float(value)
    except ValueError as exc:
        raise ValueError("amount must be a number") from exc
    if amount <= 0:
        raise ValueError("amount must be > 0")
    return amount


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError("limit must be an integer") from exc
    if number <= 0:
        raise ValueError("limit must be > 0")
    return number


def _validate_month(value: str) -> None:
    parse_month(value)


def _render_table(expenses: list) -> str:
    headers = ["id", "date", "category", "amount", "note"]
    rows = [
        [
            exp.id,
            exp.date,
            exp.category,
            format_amount(exp.amount, exp.currency),
            exp.note,
        ]
        for exp in expenses
    ]

    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(widths[i], len(str(row[i]))) for i in range(len(headers))]

    def _format_row(values: list[str]) -> str:
        return "  ".join(str(values[i]).ljust(widths[i]) for i in range(len(values)))

    lines = [_format_row(headers)]
    lines.extend(_format_row(row) for row in rows)
    return "\n".join(lines)


def _print_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)


def _handle_add(args: argparse.Namespace) -> int:
    try:
        date = args.date or today_str()
        if args.date:
            parse_date(args.date)
        category = args.category.strip()
        if not category:
            raise ValueError("category is required")
        amount = _positive_amount(args.amount)
        expense = add_expense(
            date=date,
            category=category.lower(),
            amount=amount,
            note=args.note or "",
            currency=args.currency,
        )
    except ValueError as exc:
        _print_error(str(exc))
        return 1

    print(
        f"Added: {expense.id} | {expense.date} | {expense.category} | "
        f"{format_amount(expense.amount, expense.currency)} | {expense.note}"
    )
    return 0


def _handle_list(args: argparse.Namespace) -> int:
    try:
        if args.month:
            _validate_month(args.month)
        min_amount = _positive_amount(args.min) if args.min else None
        max_amount = _positive_amount(args.max) if args.max else None
        limit = _positive_int(args.limit) if args.limit else None
        expenses = list_expenses(
            month=args.month,
            category=args.category,
            min_amount=min_amount,
            max_amount=max_amount,
            sort_by=args.sort,
            desc=args.desc,
            limit=limit,
        )
    except ValueError as exc:
        _print_error(str(exc))
        return 1

    if not expenses:
        print("No expenses found.")
        return 0

    print(_render_table(expenses))
    return 0


def _handle_summary(args: argparse.Namespace) -> int:
    try:
        if args.month:
            _validate_month(args.month)
        if args.from_date:
            parse_date(args.from_date)
        if args.to_date:
            parse_date(args.to_date)
    except ValueError as exc:
        _print_error(str(exc))
        return 1

    expenses, categories, months = summary(
        month=args.month,
        category=args.category,
        from_date=args.from_date,
        to_date=args.to_date,
    )

    if not categories:
        print("No expenses to summarize.")
        return 0

    print(f"Total Expenses: {len(expenses)}")
    
    total_amount = 0


    for item in expenses:
        total_amount+=item.amount
    
    print(f"Grand Total: {total_amount} BDT \n")

    print("By category:")
    for category in sorted(categories):
        print(f"- {category}: {categories[category]:.2f} BDT")

    print("\nMonthly totals:")
    for month in sorted(months):
        print(f"- {month}: {months[month]:.2f} BDT")

    return 0


def _handle_export(args: argparse.Namespace) -> int:
    try:
        if args.month:
            _validate_month(args.month)
        min_amount = _positive_amount(args.min) if args.min else None
        max_amount = _positive_amount(args.max) if args.max else None
        limit = _positive_int(args.limit) if args.limit else None
    except ValueError as exc:
        _print_error(str(exc))
        return 1

    expenses = list_expenses(
        month=args.month,
        category=args.category,
        min_amount=min_amount,
        max_amount=max_amount,
        sort_by=args.sort,
        desc=args.desc,
        limit=limit,
    )
    path = export_csv(args.path, expenses)
    print(f"Exported {len(expenses)} expense(s) to {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tracker", description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)


    add_parser = subparsers.add_parser("add", help="Add an expense")

    # argument of add expenses command
    add_parser.add_argument("--date", help="YYYY-MM-DD")
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--amount", required=True)
    add_parser.add_argument("--note", default="")
    add_parser.add_argument("--currency", default="BDT")
    add_parser.set_defaults(func=_handle_add)



    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--month", help="YYYY-MM")
    list_parser.add_argument("--category")
    list_parser.add_argument("--min", dest="min")
    list_parser.add_argument("--max", dest="max")
    list_parser.add_argument(
        "--sort",
        choices=["date", "amount", "category", "created", "id"],
        default="date",
    )
    list_parser.add_argument("--desc", action="store_true")
    list_parser.add_argument("--limit")
    list_parser.set_defaults(func=_handle_list)

    summary_parser = subparsers.add_parser("summary", help="Show totals")
    summary_parser.add_argument("--month", help="YYYY-MM")
    summary_parser.add_argument("--from", dest="from_date", help="YYYY-MM-DD")
    summary_parser.add_argument("--to", dest="to_date", help="YYYY-MM-DD")
    summary_parser.add_argument("--category")
    summary_parser.set_defaults(func=_handle_summary)

    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("--path", default="data/expenses.csv")
    export_parser.add_argument("--month", help="YYYY-MM")
    export_parser.add_argument("--category")
    export_parser.add_argument("--min", dest="min")
    export_parser.add_argument("--max", dest="max")
    export_parser.add_argument(
        "--sort",
        choices=["date", "amount", "category", "created", "id"],
        default="date",
    )
    export_parser.add_argument("--desc", action="store_true")
    export_parser.add_argument("--limit")
    export_parser.set_defaults(func=_handle_export)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    exit_code = args.func(args)
    raise SystemExit(exit_code)
