# 🛫 Airport API & Map Explorer

## 1. Project Overview

This project is a comprehensive full-stack application that demonstrates the powerful integration of multiple NoSQL database paradigms to solve distinct data problems efficiently. 

Designed as an academic assignment for NoSQL databases, the system handles airport data using a polyglot persistence architecture:
- **MongoDB** acts as the primary source of truth, providing robust, persistent document storage for all airport metadata (CRUD operations).
- **Redis GEO (`redis-geo`)** is an independent Redis instance dedicated exclusively to spatial operations. It leverages Redis's in-memory Geospatial indexes and the `GEORADIUS` command to perform lightning-fast proximity searches.
- **Redis Popularity (`redis-pop`)** is a second Redis instance focused on high-performance, real-time analytics. It tracks the most frequently accessed airports using Sorted Sets (`ZSET`), allowing the application to instantly retrieve a dynamic popularity ranking using the `ZREVRANGE` command.

## 2. Tech Stack

- **Backend:** FastAPI (Python), Uvicorn
- **Frontend:** React, Vite, Leaflet.js (for map rendering and marker clustering)
- **Primary Database:** MongoDB (Document Store)
- **In-Memory Stores:** Redis (Key-Value, Spatial Indexes, Sorted Sets)
- **Infrastructure:** Docker & Docker Compose

## 3. How to Run the Project

The entire application architecture is containerised. To run the project locally, you only need to have Docker and Docker Compose installed on your system.

Simply open your terminal in the root directory of the project and run:

```bash
docker compose up --build
```

**What happens at startup?**
Upon the initial startup, the backend application triggers an automated seeding process. It reads the provided `airports.json` data file and automatically:
1. Loads the structural airport documents into **MongoDB**.
2. Extracts coordinates and populates the **`redis-geo`** instance.
3. Initializes the **`redis-pop`** instance to prepare for incoming analytics tracking.

## 4. How to Test & Verify (CRITICAL SECTION)

Follow this testing guide to verify that all layers of the NoSQL architecture are functioning and communicating correctly.

### A. Terminal & Database Verification

**1. Monitor Backend Logs**
Ensure there are no application errors and verify the automated seeding process executed successfully:
```bash
docker compose logs -f backend
```

**2. Verify Redis Popularity State**
You can access the dedicated popularity container directly to inspect the raw `ZSET` structure in real-time. Open a new terminal and run:
```bash
docker exec -it redis-pop redis-cli ZREVRANGE airport_popularity 0 -1 WITHSCORES
```
*(This will return the list of airport IATA codes alongside their current visit counts).*

---

### B. REST API Verification (via Postman/cURL)

You can verify the core business logic by hitting the exposed REST API endpoints (hosted by default at `http://localhost:8000`).

**1. Test General CRUD Operations**
Fetch the complete list of airports directly from MongoDB:
```http
GET http://localhost:8000/airports
```

**2. Test the Popularity Flow (Redis ZSET)**
Simulate user visits by repeatedly requesting the details of a specific airport (e.g., Ezeiza International Airport):
```http
GET http://localhost:8000/airports/EZE
```
After executing this request multiple times, query the popularity endpoint:
```http
GET http://localhost:8000/airports/popular
```
*Expected Result:* You should see "EZE" elevated to the top of the ranking with the correct hit count. **Note:** This popularity set is configured to automatically expire after 24 hours using the Redis `EXPIRE` command (rolling TTL of 86400 seconds).

**3. Test Geospatial Search (Redis GEO)**
Verify the `GEORADIUS` implementation by searching for airports within a 50 km radius of Buenos Aires:
```http
GET http://localhost:8000/airports/nearby?lat=-34.822&lng=-58.535&radius=50
```

---

### C. Frontend & UX Verification

Finally, test the integration from the end-user perspective using the React interface:

1. **Load the Application:** Open the application in your web browser (e.g., `http://localhost:5173`). Verify that the Leaflet map loads successfully and displays the clustered airport markers across the globe.
2. **Network Inspection:** Open your Browser Developer Tools and navigate to the **Network** tab.
3. **Popup Interaction:** Click on any airport marker on the map to open its Popup details. In the Network tab, verify that a background request is fired to `GET /airports/{iata_code}` and returns a `200 OK` status.
4. **Reactive Analytics:** Immediately after the popup loads, observe the UI's Popularity Ranking widget. Verify that the widget updates reactively, reflecting the new view you just triggered for that specific airport.
