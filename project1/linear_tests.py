import unittest
from proj1_main import mss_linear

class TestLinear(unittest.TestCase):
    def test_left_max_subarray(self):
        test = [1, 1, -1, -1]
        results = mss_linear(test)
        self.assertEqual(results, (0, 1, 2))

    def test_right_max_subarray(self):
        test = [-1, -1, 1, 1]
        results = mss_linear(test)
        self.assertEqual(results, (2, 3, 2))

    def test_crossing_max_subarray(self):
        test = [-1, 1, 1, -1]
        results = mss_linear(test)
        self.assertEqual(results, (1, 2, 2))

    def test_no_negatives(self):
        test = [1, 1, 1, 1]
        results = mss_linear(test)
        self.assertEqual(results, (0, 3, 4))

    def test_base_case(self):
        test = [1]
        results = mss_linear(test)
        self.assertEqual(results, (0, 0, 1))

    def test_MSS_TestProblems_1(self):
        test = [1, 4, -9, 8, 1, 3, 3, 1, -1, -4, -6, 2, 8, 19, -10, -11] 
        results = mss_linear(test)
        expected = ([8, 1, 3, 3, 1, -1, -4, -6, 2, 8, 19], 34)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_2(self):
        test = [2, 9, 8, 6, 5, -11, 9, -11, 7, 5, -1, -8, -3, 7, -2]
        results = mss_linear(test)
        expected = ([2, 9, 8, 6, 5], 30)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_3(self):
        test = [10, -11, -1, -9, 33, -45, 23, 24, -1, -7, -8, 19] 
        results = mss_linear(test)
        expected = ([23, 24, -1, -7, -8, 19], 50)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_4(self):
        test = [31,-41, 59, 26, -53, 58, 97, -93, -23, 84] 
        results = mss_linear(test)
        expected = ([59, 26, -53, 58, 97], 187)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_5(self):
        test = [3, 2, 1, 1, -8, 1, 1, 2, 3]
        results = mss_linear(test)
        expected = ([3, 2, 1, 1], 7)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_6(self):
        test = [12, 99, 99, -99, -27, 0, 0, 0, -3, 10] 
        results = mss_linear(test)
        expected = ([12, 99, 99], 210)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)

    def test_MSS_TestProblems_7(self):
        test = [-2, 1, -3, 4, -1, 2, 1, -5, 4] 
        results = mss_linear(test)
        expected = ([4, -1, 2, 1], 6)
        self.assertEqual((test[results[0]:results[1] + 1], results[2]), 
                          expected)


if __name__ == '__main__':
    unittest.main()
