import unittest
from unittest.mock import patch
from fetch import fetch_data_from_api


class TestFetchData(unittest.TestCase):

    @patch("fetch.requests.get")
    def test_fetch_data_from_api(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"page": 1, "pages": 1, "per_page": 200, "total": 1},
            [
                {
                    "country": {"id": "ARG", "value": "Argentina"},
                    "countryiso3code": "ARG",
                    "date": "2020",
                    "value": "450000000000",
                }
            ],
        ]

        result = fetch_data_from_api()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["country"]["id"], "ARG")
        self.assertEqual(result[0]["value"], "450000000000")


if __name__ == "__main__":
    unittest.main()
