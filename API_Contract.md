## API Endpoints Overview

Each service exposes specific API endpoints:

- **OrderService**:
    - `POST api/v1/orders/place_order`: Place a new order.
    - `GET /orders?user_id=<user_id>`: Retrieve list of all the orders for a user_id.
    - `GET /orders?user_id=<user_id>&order_id=<order_id>`: Retrieve information about an order.
    - `PATCH /orders/cancel_order?order_id=<order_id>`: Cancel the order.

  **_Swagger API Docs_**: `/order/api/docs`


- **InventoryService**:
    - `GET /inventory/all_items`: Check all inventory items present.
    - `POST /inventory/add_item`: Add new item to the inventory.
    - `PATCH /inventory/update_item`: Update item with (more quantity, new_price, new_alert_threshold).
    - `PATCH /orders/update_status`: Update order status to mark it as prepared, delivered, etc.

  **_Swagger API Docs_**: `/inventory/api/docs`


- **UserService**:
    - `POST /users`: Create a new user.
    - `GET /users`: Retrieve all user information.

  **_Swagger API Docs_**: `/user/api/docs`

---

## Request/Response Format

### **OrderService**:

- `POST /api/v1/orders/place_order`  
  **Request:**
  ```json
  {
  "items": [
    {
      "item_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "quantity": 1
    }
  ],
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "total_price": 0,
  "store_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
  ```
  **Response:**
  ```json
  {
  "order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "pending",
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "store_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "total_amount": 0,
  "payment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "items": [
    {
      "item_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "item_name": "string",
      "quantity": 0
    }
  ],
  "created_at": "2025-04-08T18:47:16.313Z",
  "updated_at": "2025-04-08T18:47:16.313Z"
  }
  ```

- `GET /orders?user_id=<user_id>`  
  **Response:**
  ```json
  [
    {
      "order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "status": "pending",
      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "store_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "total_amount": 0,
      "payment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "items": [
        {
          "item_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "item_name": "string",
          "quantity": 0
        }
      ],
      "created_at": "2025-04-08T18:48:41.604Z",
      "updated_at": "2025-04-08T18:48:41.604Z"
    }
  ]
  ```

- `GET /orders?user_id=<user_id>&order_id=<order_id>`  
  **Response:**
  ```json
  {
    "order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "pending",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "store_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "total_amount": 0,
    "payment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "items": [
      {
        "item_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "item_name": "string",
        "quantity": 0
      }
    ],
    "created_at": "2025-04-08T18:47:55.292Z",
    "updated_at": "2025-04-08T18:47:55.292Z"
  }
  ```

- `PATCH /orders/cancel_order?order_id=<order_id>`  
  **Response:**
  ```json
   true
  ```

**_Swagger API Docs_**: `/order/api/docs`

---

### **InventoryService**:

- `GET /inventory/all_items`  
  **Response:**
  ```json
  [
    {
      "alert_threshold": 10,
      "item_description": "A juicy cheeseburger with lettuce and tomato.",
      "item_id": "123e4567-e89b-12d3-a456-426614174000",
      "item_name": "Cheeseburger",
      "price": 9.99,
      "quantity": 50,
      "store_id": "011ae52d-929f-44a7-af32-6141dcd14f0d",
      "updated_at": "2023-12-31T23:59:59Z"
    }
  ]
  ```

- `POST /inventory/add_item`  
  **Request:**
  ```json
  {
  "store_id": "0a550a86-b290-4be3-8e79-abab51bb4786",
  "item_name": "string",
  "item_description": "string",
  "price": 1,
  "quantity": 0,
  "alert_threshold": 0
  }
  ```
  **Response:**
  ```json
  {
  "alert_threshold": 10,
  "item_description": "A juicy cheeseburger with lettuce and tomato.",
  "item_id": "123e4567-e89b-12d3-a456-426614174000",
  "item_name": "Cheeseburger",
  "price": 9.99,
  "quantity": 50,
  "store_id": "011ae52d-929f-44a7-af32-6141dcd14f0d",
  "updated_at": "2023-12-31T23:59:59Z"
  }
  ```

- `PATCH /inventory/update_item`  
  **Request:**
  ```json
  {
  "store_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "item_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "add_quantity": 0, //Optional
  "new_price": 0, //Optional
  "new_alert_threshold": 0 //Optional
  }
  ```
  **Response:**
  ```json
  {
  "alert_threshold": 10,
  "item_description": "A juicy cheeseburger with lettuce and tomato.",
  "item_id": "123e4567-e89b-12d3-a456-426614174000",
  "item_name": "Cheeseburger",
  "price": 9.99,
  "quantity": 50,
  "store_id": "011ae52d-929f-44a7-af32-6141dcd14f0d",
  "updated_at": "2023-12-31T23:59:59Z"
  }
  ```

- `PATCH /orders/update_status`  
  **Request:**
  ```json
  {
    "order_id":"3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "prepared" | "delivered" | "returned"
  }
  ```
  **Response:**
  ```json
  true
  ```

**_Swagger API Docs_**: `/inventory/api/docs`

---

### **UserService**:

- `POST /users`  
  **Request:**
  ```json
  {
  "username": "string"
  }
  ```
  **Response:**
  ```json
  {
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "username": "string",
  "created_at": "2025-04-08T18:54:10.206Z"
  }
  ```

- `GET /users`  
  **Response:**
  ```json
  [
  {
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "username": "string",
    "created_at": "2025-04-08T18:53:52.659Z"
  }
  ]
  ```

**_Swagger API Docs_**: `/user/api/docs`

---
