import logging

from fastapi import APIRouter, Depends, HTTPException

from app.db import cursor
from app.schemas import BookingRequest
from app.security import CurrentUser, get_current_user

log = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", status_code=201)
def create_booking(body: BookingRequest):
    """Create a booking. Called by the public booking widget, so there is no auth."""
    log.info("new booking request: %s", body.dict())

    with cursor() as cur:
        cur.execute(
            """
            SELECT id, operator_id, price_cents, capacity
            FROM activities
            WHERE id = %s AND published = true
            """,
            (body.activity_id,),
        )
        activity = cur.fetchone()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

        cur.execute(
            """
            SELECT coalesce(sum(party_size), 0) AS taken
            FROM bookings
            WHERE activity_id = %s AND status <> 'cancelled'
            """,
            (body.activity_id,),
        )
        taken = cur.fetchone()["taken"]
        if taken + body.party_size > activity["capacity"]:
            raise HTTPException(status_code=409, detail="Activity is sold out")

        cur.execute(
            """
            INSERT INTO bookings (
                operator_id, activity_id, customer_name, customer_email,
                customer_phone, party_size, amount_cents, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'confirmed')
            RETURNING id, status, amount_cents
            """,
            (
                activity["operator_id"],
                activity["id"],
                body.customer_name,
                body.customer_email,
                body.customer_phone,
                body.party_size,
                activity["price_cents"] * body.party_size,
            ),
        )
        return cur.fetchone()


@router.get("")
def list_bookings(user: CurrentUser = Depends(get_current_user), limit: int = 100):
    with cursor() as cur:
        cur.execute(
            """
            SELECT id, operator_id, activity_id, customer_name, customer_email,
                   customer_phone, party_size, amount_cents, status, created_at
            FROM bookings
            WHERE operator_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (user.operator_id, limit),
        )
        return cur.fetchall()


@router.get("/{booking_id}")
def get_booking(booking_id: int, user: CurrentUser = Depends(get_current_user)):
    with cursor() as cur:
        cur.execute(
            """
            SELECT id, operator_id, activity_id, customer_name, customer_email,
                   customer_phone, party_size, amount_cents, status, created_at
            FROM bookings
            WHERE id = %s
            """,
            (booking_id,),
        )
        booking = cur.fetchone()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, user: CurrentUser = Depends(get_current_user)):
    with cursor() as cur:
        cur.execute(
            """
            UPDATE bookings
            SET status = 'cancelled'
            WHERE id = %s AND operator_id = %s
            RETURNING id, status
            """,
            (booking_id, user.operator_id),
        )
        booking = cur.fetchone()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking
