import requests
from fastapi import APIRouter, Depends, HTTPException

from app.db import cursor
from app.schemas import WebhookRequest
from app.security import CurrentUser, get_current_user

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("")
def get_webhook(user: CurrentUser = Depends(get_current_user)):
    with cursor() as cur:
        cur.execute(
            "SELECT operator_id, url FROM webhooks WHERE operator_id = %s",
            (user.operator_id,),
        )
        return cur.fetchone() or {"operator_id": user.operator_id, "url": None}


@router.put("")
def set_webhook(body: WebhookRequest, user: CurrentUser = Depends(get_current_user)):
    with cursor() as cur:
        cur.execute(
            """
            INSERT INTO webhooks (operator_id, url)
            VALUES (%s, %s)
            ON CONFLICT (operator_id) DO UPDATE SET url = EXCLUDED.url
            RETURNING operator_id, url
            """,
            (user.operator_id, body.url),
        )
        return cur.fetchone()


@router.post("/test")
def test_webhook(body: WebhookRequest, user: CurrentUser = Depends(get_current_user)):
    """Fetch a URL from our side so operators can check it is reachable.

    Most 'the webhook never fired' tickets turn out to be a firewall, so showing
    the operator what we actually get back saves a support round trip.
    """
    try:
        response = requests.get(body.url, timeout=5)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach {body.url}: {exc}")

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text[:1000],
    }
