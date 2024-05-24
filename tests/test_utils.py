import unittest
from utils import chunks


class TestUtils(unittest.TestCase):

    def test_chunks(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chunk_size = 3
        expected_result = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
        result = list(chunks(lst, chunk_size))
        self.assertEqual(result, expected_result)

    def test_chunks_empty_list(self):
        lst = []
        chunk_size = 3
        expected_result = []
        result = list(chunks(lst, chunk_size))
        self.assertEqual(result, expected_result)

    def test_chunks_larger_chunk_size(self):
        lst = [1, 2, 3]
        chunk_size = 5
        expected_result = [[1, 2, 3]]
        result = list(chunks(lst, chunk_size))
        self.assertEqual(result, expected_result)

    def test_chunks_exact_division(self):
        lst = [1, 2, 3, 4, 5, 6]
        chunk_size = 2
        expected_result = [[1, 2], [3, 4], [5, 6]]
        result = list(chunks(lst, chunk_size))
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
