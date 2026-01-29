Expense Tracker CLI
===================

Track expenses in a simple, file-backed CLI. Supports add, list, edit, delete, summary, and CSV export.

Project structure
-----------------
```
Expense_Tracker/
├─ data/
│  └─ expenses.json
├─ logs/
│  └─ tracker.log
├─ tracker/
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ cli.py
│  ├─ logger.py
│  ├─ models.py
│  ├─ service.py
│  ├─ storage.py
│  └─ utils.py
└─ readme.md
```


Setup
-----
Requirements:
- Python 3.10+

Clone:
```bash
git clone https://github.com/saidurcsesust/Expense_Tracker.git
cd Expense_Tracker
```

Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```


Features
--------
- Add expenses with date, category, amount, note, and currency
- List and filter expenses (month/category/min/max), sort and limit
- Summary totals (overall, by category, by month) with filters
- Edit or delete an expense by id
- Export filtered results to CSV
- Logging for commands, validation failures, and file read/write errors

Commands (with examples)
------------------------

## Add
```bash
python3 -m tracker add --date 2026-01-26 --category food --amount 250.5 --note "Lunch"
```

## List
```bash
python3 -m tracker list
python3 -m tracker list --month 2026-01 --category food --sort amount --desc --limit 10
python3 -m tracker list --min 100 --max 500
python3 -m tracker list --sort category
```

## Summary
```bash
python3 -m tracker summary
python3 -m tracker summary --month 2026-01
python3 -m tracker summary --from 2026-01-01 --to 2026-01-31
python3 -m tracker summary --category food
python3 -m tracker summary --month 2026-01 --category food
python3 -m tracker summary --from 2026-01-01 --to 2026-01-31 --category food
```

## Edit
```bash
python3 -m tracker edit --id EXP-20260126-0002 --amount 300 --note "Lunch+coffee"
```

## Delete
```bash
python3 -m tracker delete --id EXP-20260126-0001
```

## Export
```bash
python3 -m tracker export --path data/expenses.csv
```

Command options
---------------

### Add
- Required: `--category`, `--amount`, `--date` (YYYY-MM-DD)
- Optional:  `--note`, `--currency` (default: BDT)

### List
- Optional filters: `--month` (YYYY-MM), `--category`, `--min`, `--max`
- Sorting: `--sort` (date, amount, category, created, id), `--desc`
- Limit: `--limit`

### Summary
- Prints total count, grand total, totals by category, and monthly totals
- Optional filters: `--month` (YYYY-MM), `--from` (YYYY-MM-DD), `--to` (YYYY-MM-DD), `--category`

### Edit
- Required: `--id`
- Optional: `--date` (YYYY-MM-DD), `--category`, `--amount`, `--note`, `--currency`

### Delete
- Required: `--id`

### Export
- Output path: `--path` (default: `data/expenses.csv`)
