CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory(
    store_id UUID NOT NULL,
    item_id UUID PRIMARY KEY,
    item_name VARCHAR(20) NOT NULL,
    item_description TEXT,
    price NUMERIC NOT NULL,
    quantity INTEGER NOT NULL,
    alert_threshold INTEGER NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payment(
    payment_id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    mode TEXT  NOT NULL,
    amount NUMERIC NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    user_id UUID NOT NULL,
    store_id UUID NOT NULL,
    total_amount NUMERIC NOT NULL,
    payment_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id UUID NOT NULL,
    item_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);
