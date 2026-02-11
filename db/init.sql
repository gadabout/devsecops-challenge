CREATE TABLE operators (
    id          serial PRIMARY KEY,
    name        text NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id            serial PRIMARY KEY,
    operator_id   integer NOT NULL REFERENCES operators (id),
    email         text NOT NULL UNIQUE,
    password_hash text NOT NULL,
    role          text NOT NULL DEFAULT 'staff',
    created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE activities (
    id          serial PRIMARY KEY,
    operator_id integer NOT NULL REFERENCES operators (id),
    title       text NOT NULL,
    description text NOT NULL DEFAULT '',
    price_cents integer NOT NULL,
    capacity    integer NOT NULL,
    published   boolean NOT NULL DEFAULT true
);

CREATE TABLE bookings (
    id             serial PRIMARY KEY,
    operator_id    integer NOT NULL REFERENCES operators (id),
    activity_id    integer NOT NULL REFERENCES activities (id),
    customer_name  text NOT NULL,
    customer_email text NOT NULL,
    customer_phone text,
    party_size     integer NOT NULL,
    amount_cents   integer NOT NULL,
    status         text NOT NULL DEFAULT 'confirmed',
    created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE webhooks (
    operator_id integer PRIMARY KEY REFERENCES operators (id),
    url         text NOT NULL
);

CREATE INDEX bookings_operator_idx ON bookings (operator_id, created_at DESC);
CREATE INDEX activities_operator_idx ON activities (operator_id);

INSERT INTO operators (name) VALUES
    ('Cascade Kayak Tours'),
    ('Old Town Ghost Walks');

-- Passwords are 'kayak123' and 'ghosts123' respectively.
INSERT INTO users (operator_id, email, password_hash, role) VALUES
    (1, 'dana@cascadekayak.example', 'eb041d0f8f70b0705aaddc327c79c069', 'admin'),
    (1, 'sam@cascadekayak.example',  'eb041d0f8f70b0705aaddc327c79c069', 'staff'),
    (2, 'rem@oldtownghosts.example', '7f6609699e99812159a591333545d9e2', 'admin');

INSERT INTO activities (operator_id, title, description, price_cents, capacity) VALUES
    (1, 'Sunrise Kayak Paddle',   'Two hours on the water before the wind picks up.', 6500,  12),
    (1, 'Half Day Sea Cave Tour', 'Guided paddle out to the sea caves and back.',      12000, 8),
    (2, 'Lantern Ghost Walk',     'Ninety minutes through the old quarter after dark.', 2500, 25),
    (2, 'Cemetery Night Tour',    'Small group tour of the historic cemetery.',         3500, 10);

INSERT INTO bookings (operator_id, activity_id, customer_name, customer_email, customer_phone, party_size, amount_cents) VALUES
    (1, 1, 'Priya Raman',   'priya.raman@example.com',   '+1-503-555-0142', 2, 13000),
    (1, 2, 'Tom Alvarez',   'tom.alvarez@example.com',   '+1-503-555-0177', 1, 12000),
    (2, 3, 'Grace Okafor',  'grace.okafor@example.com',  '+1-212-555-0119', 4, 10000),
    (2, 4, 'Henrik Lund',   'henrik.lund@example.com',   NULL,              2, 7000);

INSERT INTO webhooks (operator_id, url) VALUES
    (1, 'https://cascadekayak.example/hooks/peek');
