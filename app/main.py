import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

from app.config import settings
from app.db import cursor
from app.routers import activities, admin, auth, bookings, legacy, webhooks

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("bookings")

app = FastAPI(title="Peek Bookings API", version="1.4.0")

# The booking widget is embedded on operator sites, so it can be served from any
# domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(bookings.router)
app.include_router(webhooks.router)
app.include_router(admin.router)
app.include_router(legacy.router)


@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception):
    log.exception("unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "path": request.url.path,
            "trace": traceback.format_exc(),
        },
    )


@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": app.version}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    with cursor() as cur:
        cur.execute(
            """
            SELECT o.name,
                   count(b.id) AS bookings,
                   coalesce(sum(b.amount_cents), 0) AS revenue_cents
            FROM operators o
            LEFT JOIN bookings b ON b.operator_id = o.id AND b.status <> 'cancelled'
            GROUP BY o.id, o.name
            ORDER BY o.id
            """
        )
        operators = cur.fetchall()

    lines = []

    lines.append("# HELP peek_bookings_total Confirmed bookings per operator")
    lines.append("# TYPE peek_bookings_total counter")
    for operator in operators:
        lines.append(
            f'peek_bookings_total{{operator="{operator["name"]}"}} '
            f'{operator["bookings"]}'
        )

    lines.append("# HELP peek_booking_revenue_cents Confirmed revenue per operator")
    lines.append("# TYPE peek_booking_revenue_cents counter")
    for operator in operators:
        lines.append(
            f'peek_booking_revenue_cents{{operator="{operator["name"]}"}} '
            f'{operator["revenue_cents"]}'
        )

    return "\n".join(lines) + "\n"
