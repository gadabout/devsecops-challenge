import csv
import io

from fastapi import APIRouter, Depends, Response

from app.db import cursor
from app.security import CurrentUser, get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

COLUMNS = [
    "id",
    "operator_id",
    "activity_id",
    "customer_name",
    "customer_email",
    "customer_phone",
    "party_size",
    "amount_cents",
    "status",
    "created_at",
]


@router.get("/export")
def export_bookings(user: CurrentUser = Depends(get_current_user)):
    """Admin-only CSV export, used by the finance team for reconciliation."""
    with cursor() as cur:
        cur.execute(
            """
            SELECT id, operator_id, activity_id, customer_name, customer_email,
                   customer_phone, party_size, amount_cents, status, created_at
            FROM bookings
            ORDER BY created_at DESC
            """
        )
        bookings = cur.fetchall()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(bookings)

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=bookings.csv"},
    )
