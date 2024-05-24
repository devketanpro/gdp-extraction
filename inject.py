import mysql.connector
import os
from fetch import fetch_data_from_api
from utils import chunks


def create_table(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS country (
        country_id VARCHAR(255),
        name VARCHAR(255),
        iso3_code VARCHAR(255)
    )
"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS gdp (
        country_id VARCHAR(255),
        year VARCHAR(4),
        value VARCHAR(255)
    )
    """
    )

    connection.commit()


def insert_data_in_chunks(connection, data, chunk_size=1000):
    cursor = connection.cursor()
    country_values = []
    gdp_values = []

    for item in data:
        country_values.append(
            (
                item.get("country")["id"],
                item.get("country")["value"],
                item["countryiso3code"],
            )
        )
        gdp_values.append((item.get("country")["id"], item["date"], item.get("value")))

    for chunk in chunks(country_values, chunk_size):
        cursor.executemany(
            """INSERT INTO country (country_id, name, iso3_code) VALUES (%s, %s, %s)""",
            chunk,
        )

    for chunk in chunks(gdp_values, chunk_size):
        cursor.executemany(
            """INSERT INTO gdp (country_id, year, value) VALUES (%s, %s, %s)""", chunk
        )

    connection.commit()


def main():
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("DB_NAME", "gdp"),
    }

    api_data = fetch_data_from_api()
    if api_data:
        try:
            connection = mysql.connector.connect(**db_config)
            create_table(connection)
            insert_data_in_chunks(connection, api_data)
            print("Data inserted into MySQL successfully.")
        except mysql.connector.Error as e:
            print("Error:", e)
        finally:
            if "connection" in locals() or "connection" in globals():
                connection.close()
    else:
        print("No data fetched from the API.")


if __name__ == "__main__":
    main()
