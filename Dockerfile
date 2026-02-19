FROM python:3.11

WORKDIR /srv/bookings

# Compose brings the API up before Postgres finishes initialising, so block until
# the port answers.
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql://peek:hunter2@db:5432/bookings
ENV JWT_SECRET=dev-secret-change-me

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . .

EXPOSE 8000

CMD ["wait-for-it", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
