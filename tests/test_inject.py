import unittest
from unittest.mock import MagicMock, patch
from inject import create_table, insert_data_in_chunks, main


class TestDatabaseFunctions(unittest.TestCase):

    @patch("mysql.connector.connect")
    def test_insert_data_in_chunks(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        data = [
            {
                "country": {"id": "1", "value": "USA"},
                "countryiso3code": "USA",
                "date": "2023",
                "value": "1000",
            },
            {
                "country": {"id": "2", "value": "Canada"},
                "countryiso3code": "CAN",
                "date": "2023",
                "value": "2000",
            },
        ]

        insert_data_in_chunks(mock_connect.return_value, data)

        mock_cursor.executemany.assert_any_call(
            """INSERT INTO country (country_id, name, iso3_code) VALUES (%s, %s, %s)""",
            [("1", "USA", "USA"), ("2", "Canada", "CAN")],
        )

        mock_cursor.executemany.assert_any_call(
            """INSERT INTO gdp (country_id, year, value) VALUES (%s, %s, %s)""",
            [("1", "2023", "1000"), ("2", "2023", "2000")],
        )

    @patch("mysql.connector.connect")
    @patch("inject.fetch_data_from_api")
    def test_main(self, mock_fetch_data, mock_connect):
        mock_fetch_data.return_value = [
            {
                "country": {"id": "1", "value": "USA"},
                "countryiso3code": "USA",
                "date": "2023",
                "value": "1000",
            },
            {
                "country": {"id": "2", "value": "Canada"},
                "countryiso3code": "CAN",
                "date": "2023",
                "value": "2000",
            },
        ]
        main()

        mock_connect.assert_called_once()
        mock_fetch_data.assert_called_once()
        self.assertTrue(mock_connect.return_value.close.called)


if __name__ == "__main__":
    unittest.main()
