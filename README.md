# Organization Directory API

REST API for managing organizations, buildings, and activities.

## Features

- Search for organizations by name, activity, and location.
- Filter organizations by radius or rectangular area.
- Hierarchical activities (up to 3 levels).

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Build and run the application using Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`.

## Creating Test Data

To populate the database with some test data, run the following command in a separate terminal after the application is running:

```bash
docker-compose exec web python seed_data.py
```

This will create:
- 2 buildings
- 5 activities (with a 2-level hierarchy)
- 3 organizations

## API Endpoints

A full list of available endpoints can be found in the OpenAPI documentation, which is available at `http://localhost:8000/docs` when the application is running.

Here are some examples:

- `GET /organizations/{organization_id}`: Get a specific organization by ID.
- `GET /organizations/`: Search for organizations with various filters.
- `GET /organizations/buildings/{building_id}/organizations`: Get all organizations in a specific building.
- `GET /organizations/activities/{activity_id}/organizations`: Get all organizations with a specific activity.

### Search Examples

**Search by name:**

`GET /organizations/?name=Tech`

**Search by activity (including child activities):**

`GET /organizations/?activity_id=1`

**Search by radius:**

`GET /organizations/?lat=55.75&lng=37.61&radius_km=5`

**Search by rectangular area:**

`GET /organizations/?min_lat=55.7&min_lng=37.6&max_lat=55.8&max_lng=37.7`
