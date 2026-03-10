"""Legacy reporting endpoints.

The finance spreadsheet still pulls from /v1/bookings/export on a schedule. Drop
this once it has been pointed at the admin export.
"""

import csv
import io

from fastapi import APIRouter, Response

from app.db import cursor

router = APIRouter(prefix="/v1", tags=["legacy"])

COLUMNS = [
    "id",
    "operator_id",
    "customer_name",
    "customer_email",
    "customer_phone",
    "amount_cents",
    "status",
    "created_at",
]


@router.get("/bookings/export")
def legacy_export():
    with cursor() as cur:
        cur.execute(
            """
            SELECT id, operator_id, customer_name, customer_email,
                   customer_phone, amount_cents, status, created_at
            FROM bookings
            ORDER BY created_at DESC
            """
        )
        bookings = cur.fetchall()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(bookings)

    return Response(content=buffer.getvalue(), media_type="text/csv")
