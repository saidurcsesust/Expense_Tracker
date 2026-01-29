Expense Tracker CLI
===================

Simple, file-backed expense tracker with add, list, summary, and export commands.

Requirements
------------
- Python 3.10+

Quick start
-----------
Run commands from the repo root:

```bash
python3 -m tracker --help
```

Add an expense:

```bash
python3 -m tracker add --date 2026-01-26 --category food --amount 250.5 --note "Lunch"
```

List expenses:

```bash
python3 -m tracker list
python3 -m tracker list --month 2026-01 --category food --sort amount --desc
```

Show summary:

```bash
python3 -m tracker summary
```

Export to CSV:

```bash
python3 -m tracker export --path data/expenses.csv
```

Delete an expense:

```bash
python3 -m tracker delete --id EXP-20260126-0001
```

Commands
--------
add
- Required: `--category`, `--amount`
- Optional: `--date` (YYYY-MM-DD), `--note`, `--currency` (default: BDT)

list
- Optional filters: `--month` (YYYY-MM), `--category`, `--min`, `--max`
- Sorting: `--sort` (date, amount, category, created, id), `--desc`
- Limit: `--limit`

summary
- Prints total expense count, grand total, totals by category, and monthly totals.
- Optional filters: `--month` (YYYY-MM), `--from` (YYYY-MM-DD), `--to` (YYYY-MM-DD), `--category`

export
- Exports current list view to CSV.
- Optional filters: same as `list`
- Output path: `--path` (default: `data/expenses.csv`)

delete
- Deletes an expense by id.
- Required: `--id`

Data & logs
-----------
- Data is stored in `data/expenses.json`.
- Logs are written to `logs/tracker.log`.
