from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import settings


@contextmanager
def cursor():
    """Open a connection, hand out a cursor, and commit if the block succeeds.

    Rows come back as dictionaries so handlers can return them directly.
    """
    connection = psycopg2.connect(settings.database_url)
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        connection.commit()
    finally:
        connection.close()
