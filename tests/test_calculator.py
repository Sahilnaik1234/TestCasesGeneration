import unittest
from example.calculator import AdvancedCalculator

class TestAdvancedCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = AdvancedCalculator()

    def test_add(self):
        result = self.calculator.add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(len(self.calculator.history), 1)

    def test_subtract(self):
        result = self.calculator.subtract(5, 3)
        self.assertEqual(result, 2)
        self.assertEqual(len(self.calculator.history), 1)

    def test_multiply(self):
        result = self.calculator.multiply(2, 3)
        self.assertEqual(result, 6)
        self.assertEqual(len(self.calculator.history), 1)

    def test_divide(self):
        with self.assertRaises(ValueError):
            self.calculator.divide(6, 0)

        result = self.calculator.divide(6, 2)
        self.assertEqual(result, 3)
        self.assertEqual(len(self.calculator.history), 2)

    def test_power(self):
        result = self.calculator.power(2, 3)
        self.assertEqual(result, 8)
        self.assertEqual(len(self.calculator.history), 1)

    def test_square_root(self):
        with self.assertRaises(ValueError):
            self.calculator.square_root(-1)

        result = self.calculator.square_root(9)
        self.assertEqual(result, 3)
        self.assertEqual(len(self.calculator.history), 2)

    def test_calculate_statistics(self):
        self.assertEqual(self.calculator.calculate_statistics([]), {'mean': 0, 'variance': 0, 'std_dev': 0})

        numbers = [1, 2, 3, 4, 5]
        result = self.calculator.calculate_statistics(numbers)
        self.assertAlmostEqual(result['mean'], 3)
        self.assertAlmostEqual(result['variance'], 2.5)
        self.assertAlmostEqual(result['std_dev'], 1.5811388300841898)
        self.assertEqual(len(self.calculator.history), 3)

    def test_memory_store(self):
        self.calculator.memory_store(10)
        self.assertEqual(self.calculator.memory, 10)
        self.assertEqual(len(self.calculator.history), 1)

    def test_memory_recall(self):
        self.calculator.memory_store(10)
        result = self.calculator.memory_recall()
        self.assertEqual(result, 10)
        self.assertEqual(len(self.calculator.history), 2)

    def test_memory_clear(self):
        self.calculator.memory_store(10)
        self.calculator.memory_clear()
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(len(self.calculator.history), 3)

    def test_factorial(self):
        result = self.calculator.factorial(5)
        self.assertEqual(result, 120)
        self.assertEqual(len(self.calculator.history), 1)

    def test_is_prime(self):
        self.assertTrue(self.calculator.is_prime(11))
        self.assertFalse(self.calculator.is_prime(10))
        self.assertEqual(len(self.calculator.history), 2)

    def test_calculate_compound_interest(self):
        result = self.calculator.calculate_compound_interest(1000, 0.05, 1, 1)
        self.assertAlmostEqual(result, 1050.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_get_history(self):
        self.calculator.add(2, 3)
        self.calculator.calculate_statistics([1, 2, 3, 4, 5])
        self.calculator.memory_store(10)
        result = self.calculator.get_history()
        self.assertEqual(len(result), 3)

    def test_clear_history(self):
        self.calculator.add(2, 3)
        self.calculator.calculate_statistics([1, 2, 3, 4, 5])
        self.calculator.memory_store(10)
        self.calculator.clear_history()
        result = self.calculator.get_history()
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
