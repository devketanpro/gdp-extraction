# GDP Data Extraction and Database Injection

This project aims to extract Gross Domestic Product (GDP) data from an external API, process it, and inject it into a MySQL database using Docker containers.

## Overview

The project comprises Python scripts (`fetch.py`, `inject.py`, `utils.py`) responsible for fetching GDP data from the World Bank API and injecting it into a MySQL database. Docker containers are utilized to encapsulate the Python application and MySQL database, ensuring portability and ease of deployment.

## Setup
### Requirements

- Docker: Ensure Docker is installed on your system to utilize containerization.
- Python: Python is required to run the Python scripts.
- MySQL Client: If interacting with the MySQL database outside of Docker, ensure a MySQL client is installed.

### Installation
1. Navigate to the project directory:

   cd <project_directory>

2. Build the Docker containers:
   docker-compose build

## Usage

1. Start the Docker containers:

   docker-compose up

2. You can access database container's bash to perform any operation on the database:

   "docker ps": to get the container_id_or_name
   "docker exec -it <container_id_or_name> mysql -u <username> -p"
    default password is "root"(mentioned in docker-compose.yml)

3. To get the expected output execute below query.
```
SELECT
	c.country_id,
	c.name,
	c.iso3_code,
	MAX(CASE WHEN g.year = 2019 THEN g.value END) AS "2019",
	MAX(CASE WHEN g.year = 2020 THEN g.value END) AS "2020",
	MAX(CASE WHEN g.year = 2021 THEN g.value END) AS "2021",
	MAX(CASE WHEN g.year = 2022 THEN g.value END) AS "2022",
	MAX(CASE WHEN g.year = 2023 THEN g.value END) AS "2023"
FROM
	country c
LEFT JOIN gdp g ON
	c.country_id = g.country_id
GROUP BY
	c.country_id,
	c.name,
	c.iso3_code
ORDER BY
	c.country_id;
```
##Sample output

+------------+---------------+-----------+------------------+------------------+------------------+------------------+------+
| country_id | name          | iso3_code | 2019             | 2020             | 2021             | 2022             | 2023 |
+------------+---------------+-----------+------------------+------------------+------------------+------------------+------+
| AR         | Argentina     | ARG       | 447754683615.225 | 385740508436.965 | 487902572164.348 | 631133384439.944 | NULL |
| BO         | Bolivia       | BOL       | 40895322850.9407 | 36629843806.0781 | 40406111695.179  | 44008282877.9606 | NULL |
| BR         | Brazil        | BRA       | 1873288205186.45 | 1476107231194.11 | 1649622821885.14 | 1920095779022.73 | NULL |
| CL         | Chile         | CHL       | 278598887622.96  | 254258196269.735 | 316581155648.871 | 301024724911.923 | NULL |
| CO         | Colombia      | COL       | 323031701210.765 | 270150956772.57  | 318511813576.97  | 343622114560.409 | NULL |
| EC         | Ecuador       | ECU       | 108108009000     | 99291124000      | 106165866000     | 115049476000     | NULL |
| GY         | Guyana        | GUY       | 5173760191.84652 | 5471256594.72422 | 8041362110.31175 | 14718388489.2086 | NULL |
| PE         | Peru          | PER       | 228325821196.153 | 201947615138.567 | 223717799056.526 | 242631573320.79  | NULL |
| PY         | Paraguay      | PRY       | 37925338329.1494 | 35432178068.1814 | 39950899938.7482 | 41722295229.2279 | NULL |
| SR         | Suriname      | SUR       | 4016040575.08796 | 2911807496.20227 | 3081401725.88833 | 3620987993.32637 | NULL |
| UY         | Uruguay       | URY       | 62048585618.505  | 53666908053.7655 | 61412268248.9461 | 71177146197.4951 | NULL |
| VE         | Venezuela, RB | VEN       | NULL             | NULL             | NULL             | NULL             | NULL |
+------------+---------------+-----------+------------------+------------------+------------------+------------------+------+
12 rows in set (0.06 sec)


## Testcases
1. To run the testcases:
```
python -m unittest discover
```

## Project Structure

```
.
├── docker-compose.yml    # Docker Compose configuration file
├── Dockerfile            # Dockerfile for building the Python application image
├── fetch.py              # Python script to fetch GDP data from the World Bank API
├── inject.py             # Python script to inject data into a MySQL database
├── requirements.txt      # Python dependencies
└── utils.py              # Utility functions used by Python scripts
```

## Components

- **fetch.py**: This script fetches GDP data from the World Bank API. It handles API requests, pagination, and data extraction.

- **inject.py**: This script inserts the fetched GDP data into a MySQL database. It connects to the MySQL database, creates tables if they don't exist, and inserts data in chunks.

- **docker-compose.yml**: This file defines the Docker services for the Python application and MySQL database, along with their configurations.

- **Dockerfile**: This file contains instructions for building the Docker image for the Python application.

- **requirements.txt**: This file lists the Python dependencies required by the project.

- **utils.py**: This file contains utility functions used by the Python scripts, such as database connection and data processing functions.
