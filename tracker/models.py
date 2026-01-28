from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    id: str
    date: str
    category: str
    amount: float
    currency: str
    note: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=str(data["id"]),
            date=str(data["date"]),
            category=str(data["category"]),
            amount=float(data["amount"]),
            currency=str(data.get("currency", "BDT")),
            note=str(data.get("note", "")),
            created_at=str(data["created_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "currency": self.currency,
            "note": self.note,
            "created_at": self.created_at,
        }
