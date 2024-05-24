import requests


def fetch_data_from_api():
    try:
        page = 1
        all_data = []

        while True:
            api_url = f"https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&page={page}&per_page=200"
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if page == 1:
                pages = data[0].get("pages")

            all_data.extend(data[1])

            if page >= pages:
                break
            page += 1
        return all_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None
