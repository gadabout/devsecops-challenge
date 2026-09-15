## Bookings API

This app is written in Python and uses FastAPI to serve the booking endpoints used by the
public booking widget and by the operator dashboard. This application requires the following
environment variables to run:

```bash
# Database
DATABASE_URL=postgresql://peek:hunter2@localhost:5432/bookings

# Application
JWT_SECRET=dev-secret-change-me
TOKEN_TTL_MINUTES=60
DEBUG=true
```

See `.env.example` in the repository root for a complete example.

### Layout

```
config.py     Environment-backed settings
db.py         Database connection and cursor helper
security.py   Password hashing, token issuing, request authentication
schemas.py    Request and response models
routers/      One module per group of endpoints
tests/        Integration tests, run against a live Postgres
```

### Local Development

This app runs on **Python 3.11**. The pinned dependencies do not build on newer versions, so
Compose is the easiest way to get a database and the API running together. From the
repository root:

```bash
docker compose up --build
```

To run the app directly instead, use a Python 3.11 environment, start Postgres with the
schema in `db/init.sql` loaded, then:

```bash
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

### Tests

The tests talk to a real database and expect the seed data from `db/init.sql`. The simplest
way to run them is inside the running container:

```bash
docker compose up -d
docker compose exec bookings-api pytest
```

Or from a Python 3.11 environment on your machine, against the Compose database:

```bash
docker compose up -d db
DATABASE_URL=postgresql://peek:hunter2@localhost:5432/bookings pytest
```

### Seed accounts

| Email | Password | Operator | Role |
| --- | --- | --- | --- |
| `dana@cascadekayak.example` | `kayak123` | Cascade Kayak Tours | admin |
| `sam@cascadekayak.example` | `kayak123` | Cascade Kayak Tours | staff |
| `rem@oldtownghosts.example` | `ghosts123` | Old Town Ghost Walks | admin |

### API Endpoints

- `POST /auth/login` - Staff login, returns a JWT
- `GET /activities` - Public activity search, optional `search` and `limit` parameters
- `POST /bookings` - Create a booking
- `GET /bookings` - List bookings for the authenticated operator
- `GET /bookings/{id}` - Fetch a single booking
- `POST /bookings/{id}/cancel` - Cancel a booking
- `GET /webhooks` - Read the operator's notification URL
- `PUT /webhooks` - Set the operator's notification URL
- `POST /webhooks/test` - Check that a URL is reachable from our side
- `GET /admin/export` - CSV export of bookings
- `GET /healthz` - Health check endpoint
- `GET /metrics` - Prometheus metrics
