# Poll-a-Lot: A Microservice Polling Application

This project is a complete polling application built from scratch using a microservice architecture. It demonstrates the separation of concerns by splitting the application into three distinct, containerized services that work together.

The primary goal of this project was to gain hands-on experience with **Flask**, **Docker**, **Docker Compose**, and **microservice communication patterns**.

## 🚀 Tech Stack

* **Backend Services:** **Flask** & **Python 3.11**
* **Database:** **MongoDB**
* **Containerization:** **Docker**
* **Local Orchestration:** **Docker Compose**

---

## 🏛️ Application Architecture

The application is composed of three independent services, a database, and an internal Docker network, all managed by `docker-compose.yml`.

1.  **`web-frontend` (Port 5000)**
    * The user's single entry point. This service is the "Backend for Frontend" (BFF).
    * It serves all HTML pages.
    * It has **no direct database access**.
    * It communicates with the other services by making internal HTTP requests.

2.  **`poll-service` (Port 5001)**
    * Manages creating, reading, and listing all polls.
    * It is the *only* service that writes to the `polls` collection in MongoDB.

3.  **`vote-service` (Port 5002)**
    * Handles all voting logic.
    * Manages casting votes and aggregating results.
    * It is the *only* service that writes to the `votes` collection.

4.  **`mongo_db` (Port 27017)**
    * The persistent data store for the entire application.
    * A **Docker named volume** (`mongo-data`) is used to ensure all poll and vote data persists even when the containers are stopped and removed.

---

## ✨ Features

* **View All Polls:** The homepage queries the `poll-service` to display a list of all available polls.
* **Create a Poll:** A simple form that sends data to the `web-frontend`, which then forwards it to the `poll-service`.
* **Vote on a Poll:** Users can select an option and cast a vote. The `web-frontend` sends the request to the `vote-service`.
* **View Results:** The `web-frontend` fetches data from *both* the `poll-service` (for the question) and the `vote-service` (for the vote counts) and combines them into a single view.
* **Persistent Data:** All data is saved in a Docker volume, surviving container restarts.

---

## 🏁 Getting Started

This entire application stack can be launched with a single command.

### Prerequisites

* **Docker**
* **Docker Compose**

### Installation & Launch

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mhd-Asjad/poll-system.git
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    Open your web browser and navigate to:
    **`http://localhost:5000`**

To stop the entire application stack:
```bash
docker-compose down