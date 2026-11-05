from __future__ import annotations

from datetime import date, datetime
from typing import Any


def normalize_status(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"done", "completed", "concluida", "concluída"}:
        return "completed"
    if text in {"in_progress", "in-progress", "em andamento"}:
        return "in_progress"
    return "pending" if text else "pending"


def status_label(value: Any) -> str:
    return {
        "pending": "Pendente",
        "in_progress": "Em andamento",
        "completed": "Concluída",
        "done": "Concluída",
    }.get(normalize_status(value), "Pendente")


def parse_xano_date(value: Any):
    if value in (None, "", "null", "None"):
        return None

    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 10000000000 else value
        try:
            return datetime.fromtimestamp(seconds).date()
        except (OverflowError, OSError, ValueError):
            return None

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            if text.isdigit():
                return datetime.fromtimestamp(int(text) / 1000 if len(text) > 10 else int(text)).date()
        except (OverflowError, OSError, ValueError):
            pass

        normalized = text.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized).date()
        except ValueError:
            try:
                return datetime.strptime(normalized, "%Y-%m-%d %H:%M:%S").date()
            except ValueError:
                try:
                    return datetime.strptime(normalized, "%d/%m/%Y").date()
                except ValueError:
                    return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    return None


def format_due_date(value: Any) -> str:
    parsed = parse_xano_date(value)
    if parsed is None:
        return "Sem prazo"
    return parsed.strftime("%d/%m/%Y")
