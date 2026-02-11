from fastapi import APIRouter

from app.db import cursor

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("")
def list_activities(search: str | None = None, limit: int = 50):
    """Public activity search. Used by the booking widget on operator sites."""
    query = """
        SELECT id, operator_id, title, description, price_cents, capacity
        FROM activities
        WHERE published = true
    """

    if search:
        query += f" AND (title ILIKE '%{search}%' OR description ILIKE '%{search}%')"

    query += f" ORDER BY title LIMIT {limit}"

    with cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
