## 🧩 Architecture Overview

The Real-Time Order Management System is a distributed, event-driven application built using a microservices
architecture. It consists of three core services — **User Service**, **Order Service**, and **Inventory Service** — that
communicate over HTTP API calls and Kafka to manage users, orders, and inventory in real-time. The system is designed
for scalability, modularity, and asynchronous processing to support high-throughput order handling with minimal latency.

---

### Core Service Responsibilities

The **User Service** is responsible for creating new users and fetching the list of all existing users (The
authentication is avoided due to time crunch, hence all the apis are open). It interacts directly with a dedicated
PostgreSQL database to persist user data and exposes simple RESTful endpoints to user clients.

The **Order Service** allows users to place new orders and fetch existing orders for a specific user ID or order ID.
When an order is placed, the service first verifies the existence of all item IDs using a **Redis cache that mirrors the
current state of the inventory**. This ensures **minimal _latency_ during validation**. Once verified, the order and
associated items are saved to the database with a status of `PENDING`. Immediately after, the service publishes an
`order_placed` event to a Kafka topic to notify other services of the new order.

The **Inventory Service** is responsible for managing the lifecycle of items in the inventory. When it receives an
`order_placed` event from Kafka, it validates the availability of each item in its PostgreSQL-backed database. If the
_quantity is sufficient_, it deducts the stock accordingly and emits an `order_status_update` event back to Kafka, which
is then consumed by the Order Service to update the order status to `PREPARED`. If the _stock is insufficient_ for any
of the item in the order, the `order_status_update` event is again sent with the payload of order_id and status as
`CANCELLED`.

Additionally, the Inventory Service exposes endpoints for adding new items or updating existing stock quantities. When
stock is updated, it not only modifies the database but also refreshes the **Redis cache to maintain consistency**.
Redis is initially populated at service startup by prefetching all inventory items from the database. When inventory
levels fall below a configured threshold, the Inventory Service emits an `item_deficiency` event to Kafka. Though the *
*Notification Service** to act on this event is not yet implemented, the event stream is live and can be consumed by
future services.

---

### Asynchronous Communication & Data Flow

Kafka acts as the central event bus, decoupling the services and enabling them to react to changes in real time without
tight integration. Each service produces or consumes Kafka events depending on its role in the business logic. This
pattern supports **scalability and fault tolerance**, as services can be **independently scaled and deployed**.

Redis is used as a **high-performance, in-memory cache** to reduce database lookups during order placement. By caching
item metadata, the Order Service can **quickly validate** order requests without overloading the Inventory database.

**Each service** has its own **isolated PostgreSQL database** to ensure loose coupling and service autonomy. This also
allows each service to scale its database independently as load increases.

---

### Technology Stack

The system is built primarily with Python FastAPI, PostgreSQL for persistent storage, Redis for caching, and Apache
Kafka for asynchronous communication. It is well-suited for containerized environments and can be easily integrated with
orchestration platforms like Docker Compose or Kubernetes.

---

### Databases

Each service has its own dedicated **PostgreSQL** database for data isolation and scaling:

- `user_db` → User Service
- `order_db` → Order Service (includes `orders` and `order_items` tables)
- `inventory_db` → Inventory Service

This separation supports microservices best practices by decoupling data layers.

---

### Network & Service Communication Flow

1. **Client → Order Service**:
    - Sends a new order request.
    - Order Service checks Redis for item validity.
    - If valid, writes to order DB with status `PENDING`.

2. **Order Service → Kafka (`order_placed`)**:
    - Broadcasts event for order creation.

3. **Kafka → Inventory Service (Consumer)**:
    - Receives `order_placed`.
    - Validates item quantity in inventory DB.
    - Updates DB if possible.
    - Publishes event `order_status_update` with the appropriate status.

4. **Inventory Service → Kafka → Order Service**:
    - Order Service listens for update events to mark order status.

5. **Inventory Service → Kafka (`item_deficiency`)**:
    - Publishes low stock alerts for external notification system.

6. **Inventory Service → Kafka -> Order Service -> Redis**:
    - Updates cache after new item added to inventory.

7. **Startup Sync (Order Service)**:
    - Loads current inventory from Inventory Service into Redis on boot.

---

### Technologies Used

| Component      | Technology    |
|----------------|---------------|
| Language       | Python        |
| Framework      | FastAPI       |
| Database       | PostgreSQL    |
| Message Broker | Apache Kafka  |
| Cache Layer    | Redis         |
| API Clients    | REST (JSON)   |
| Architecture   | Microservices |

---

### Scalability Considerations

The system is designed to scale efficiently across services and workloads:

- **Service-Level Scaling**: Each microservice is independently deployable and can be scaled horizontally based on its
  load (e.g., Order Service under high order volume).

- **Kafka-Based Decoupling**: Kafka enables asynchronous communication, allowing producers and consumers to scale
  separately. Consumer groups can be used to parallelize processing.

- **Redis Caching**: Redis reduces load on the Inventory database by caching item data. It supports high read throughput
  and can be scaled using clustering.

- **Database Optimization**: Each service uses its own PostgreSQL instance. Scaling options include read replicas,
  indexing, connection pooling, and partitioning for large datasets.

- **Stateless Services**: All services are stateless, making them easy to replicate and balance using tools like Docker
  or Kubernetes.

- **Extensibility**: Kafka topics like `item_deficiency` allow seamless integration of additional services (e.g.,
  Notification Service) without affecting existing flows.

---

### Future Enhancements

- **Notification Service** to consume `item_deficiency` events and send alerts (email, SMS, etc.).
- **Authentication Layer** for secure API usage.
- **Rate Limiting / Throttling** on endpoints.
- **Monitoring & Logging** (e.g., Prometheus, Grafana, ELK stack).

---