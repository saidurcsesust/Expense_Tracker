from __future__ import annotations

import json
from pathlib import Path

from .logger import get_logger


_DEFAULT_DATA = {"version": 1, "expenses": []}


# Resolve path to the data file.
def _data_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "expenses.json"


# Load data from json file with validation.
def load_data() -> dict:
    path = _data_path()
    logger = get_logger()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        save_data(_DEFAULT_DATA)
        return dict(_DEFAULT_DATA)

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in %s", path)
        raise RuntimeError("Data file is corrupted") from exc
    except OSError as exc:
        logger.error("Failed to read data file %s: %s", path, exc)
        raise RuntimeError("Unable to read data file") from exc

    if "version" not in data or "expenses" not in data:
        logger.error("Unexpected schema in %s", path)
        raise RuntimeError("Data file has an invalid schema")

    return data


# Save data to json file.
def save_data(data: dict) -> None:
    path = _data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
    except OSError as exc:
        get_logger().error("Failed to write data file %s: %s", path, exc)
        raise RuntimeError("Unable to write data file") from exc
