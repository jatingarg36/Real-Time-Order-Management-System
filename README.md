# Real-Time Order Management System

This repository contains a microservices-based application designed to manage orders in real-time. The system is
composed of three primary services:

- **OrderService**: Handles order creation and management.
- **InventoryService**: Manages inventory and stock levels.
- **UserService**: Manages user information and authentication.

**[Architectural Overview](./Architecture.md)**

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.x**: The application is built using Python.
- **pip**: Python package installer.
- **PostgreSQL**: The services use PostgreSql databases.
- **Apache Kafka**: Used for real-time messaging between services.
- **Redis Server**: Acts as a caching layer or message broker for fast data retrieval and pub/sub use cases.

---

## Repository Structure

The repository is organized as follows:

- `OrderService/`: Contains the code and resources for the Order Service.
- `InventoryService/`: Contains the code and resources for the Inventory Service.
- `UserService/`: Contains the code and resources for the User Service.
- `db_setup.sql`: SQL script to set up the necessary databases and tables.
- `requirements.txt`: Lists the Python dependencies for the project.
- `setup.py`: Script for setting up the Python packages.

---

## Database Configuration

1. **Set Up MySQL Databases**:

    - Create three separate databases for each service: `order_db`, `inventory_db`, and `user_db`.

    - Use the `db_setup.sql` script provided in the repository to set up the necessary tables. Execute the script for
      each database accordingly.

2. **Configure Database Connections**:

    - Each service has a configuration file where the database connection parameters are specified. Update these
      configurations with your MySQL credentials and the respective database names.

---

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/jatingarg36/Real-Time-Order-Management-System.git
   cd Real-Time-Order-Management-System
   ```

2. **Install Dependencies**:

    - It's recommended to use a virtual environment to manage dependencies:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - Install the required Python packages:

      ```bash
      pip install -r requirements.txt
      ```

3. **Set Up Environment Variables**:

    - Each service require specific environment variables for configuration. Create a `.env` file in the root
      directory of the individual service and add the necessary variables. 
    - Sample .env file is attached to the services.

 
## Install Kafka & Redis (locally)

**Kafka**:

1. Download Kafka from [https://kafka.apache.org/downloads](https://kafka.apache.org/downloads)
2. Start Zookeeper and Kafka broker:
   ```bash
   # Start Zookeeper
   bin/zookeeper-server-start.sh config/zookeeper.properties

   # Start Kafka
   bin/kafka-server-start.sh config/server.properties
   ```
3. Enable auto topic creation in Kafka. This can be done by setting the following configuration in your Kafka
   `server.properties` file:

  ```properties
  auto.create.topics.enable=true
  ```

This allows Kafka to automatically create new topics when producers or consumers reference them, which is critical for
seamless operation of the services.

**Redis**:

1. Install Redis via your OS package manager or from [https://redis.io/download](https://redis.io/download)
2. Start Redis server:
   ```bash
   redis-server
   ```

Alternatively, you can run both Kafka and Redis using Docker for convenience.

---

## Running the Services

Each service operates independently. Navigate to each service's directory and start them individually:

1. **Start OrderService**:

   ```bash
   cd OrderService
   python server.py
   ```

2. **Start InventoryService**:

   ```bash
   cd InventoryService
   python server.py
   ```

3. **Start UserService**:

   ```bash
   cd UserService
   python server.py
   ```

Each service will start on its configured port. Ensure that the ports do not conflict and are accessible.

## API Contract

Refer to each service's swagger docs for detailed information on request and response formats.

[API Contracts](./API_Contract.md)

---

## Testing the Services

After starting the services, you can test them using Postman tools on this
collection: [Postman Collection](https://gold-capsule-22351.postman.co/workspace/Moments~4135ee7f-dcf9-44bd-a778-b985a4095f98/collection/11458443-b4318938-829f-4ed4-9f83-48442c216110?action=share&creator=11458443&active-environment=11458443-67ecc061-5a25-4762-b960-978cb0403629)
or `curl`. Ensure
that each service is running on its respective port and that the endpoints are accessible.

---
