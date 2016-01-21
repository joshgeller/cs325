import unittest
from project1.divide_and_conquer import divide_and_conquer_find_max_subarray

class TestDivideAndConquer(unittest.TestCase):
    def test_left_max_subarray(self):
        test = [1, 1, -1, -1]
        results = divide_and_conquer_find_max_subarray(test, 0, 3)
        self.assertEqual(results, (0, 1, 2))

    def test_right_max_subarray(self):
        test = [-1, -1, 1, 1]
        results = divide_and_conquer_find_max_subarray(test, 0, 3)
        self.assertEqual(results, (2, 3, 2))

    def test_crossing_max_subarray(self):
        test = [-1, 1, 1, -1]
        results = divide_and_conquer_find_max_subarray(test, 0, 3)
        self.assertEqual(results, (1, 2, 2))

    def test_no_negatives(self):
        test = [1, 1, 1, 1]
        results = divide_and_conquer_find_max_subarray(test, 0, 3)
        self.assertEqual(results, (0, 3, 4))

    def test_base_case(self):
        test = [1]
        results = divide_and_conquer_find_max_subarray(test, 0, 0)
        self.assertEqual(results, (0, 0, 1))

if __name__ == '__main__':
    unittest.main()
