"""Data access abstraction layer — keeps domain logic DB-agnostic."""

from __future__ import annotations

from typing import Any

import aiosqlite


class BaseRepository:
    """Base repository with common CRUD helpers."""

    def __init__(self, conn: aiosqlite.Connection, table: str):
        self.conn = conn
        self.table = table

    async def find_by_id(self, id: str) -> dict | None:
        cursor = await self.conn.execute(
            f"SELECT * FROM {self.table} WHERE id = ?", (id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def find_all(self, limit: int = 100, offset: int = 0) -> list[dict]:
        cursor = await self.conn.execute(
            f"SELECT * FROM {self.table} ORDER BY rowid DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        return [dict(row) for row in await cursor.fetchall()]

    async def insert(self, data: dict) -> str:
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        await self.conn.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )
        await self.conn.commit()
        return data.get("id", "")

    async def update(self, id: str, data: dict) -> bool:
        set_clause = ", ".join(f"{k} = ?" for k in data)
        result = await self.conn.execute(
            f"UPDATE {self.table} SET {set_clause} WHERE id = ?",
            (*data.values(), id),
        )
        await self.conn.commit()
        return result.rowcount > 0

    async def delete(self, id: str) -> bool:
        result = await self.conn.execute(
            f"DELETE FROM {self.table} WHERE id = ?", (id,)
        )
        await self.conn.commit()
        return result.rowcount > 0
