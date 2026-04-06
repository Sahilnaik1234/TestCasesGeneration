import math
from typing import List, Union

class AdvancedCalculator:
    def __init__(self):
        self.history = []
        self.memory = 0.0

    def add(self, a: float, b: float) -> float:
        result = a + b
        self._record_history(f"Added {a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self._record_history(f"Subtracted {a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self._record_history(f"Multiplied {a} * {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            self._record_history(f"Attempted to divide {a} by 0 and failed")
            raise ValueError("Division by zero is not allowed.")
        result = a / b
        self._record_history(f"Divided {a} / {b} = {result}")
        return result

    def power(self, base: float, exponent: float) -> float:
        result = math.pow(base, exponent)
        self._record_history(f"{base} to the power of {exponent} = {result}")
        return result

    def square_root(self, a: float) -> float:
        if a < 0:
            self._record_history(f"Attempted to get square root of negative number {a}")
            raise ValueError("Cannot calculate square root of a negative number.")
        result = math.sqrt(a)
        self._record_history(f"Square root of {a} = {result}")
        return result

    def calculate_statistics(self, numbers: List[float]) -> dict:
        if not numbers:
            return {"mean": 0, "variance": 0, "std_dev": 0}
        
        n = len(numbers)
        mean = sum(numbers) / n
        variance = sum((x - mean) ** 2 for x in numbers) / n
        std_dev = math.sqrt(variance)
        
        result = {
            "mean": mean,
            "variance": variance,
            "std_dev": std_dev
        }
        self._record_history(f"Calculated stats for {n} numbers: {result}")
        return result

    def memory_store(self, value: float) -> None:
        self.memory = value
        self._record_history(f"Stored {value} to memory")

    def memory_recall(self) -> float:
        self._record_history(f"Recalled {self.memory} from memory")
        return self.memory

    def memory_clear(self) -> None:
        self.memory = 0.0
        self._record_history("Cleared memory")

    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if not isinstance(n, int):
            raise TypeError("Factorial requires an integer.")
            
        result = math.factorial(n)
        self._record_history(f"Factorial of {n} = {result}")
        return result

    def is_prime(self, n: int) -> bool:
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
            
        self._record_history(f"Checked if {n} is prime: True")
        return True

    def calculate_compound_interest(self, principal: float, rate: float, time: float, n_times: int) -> float:
        """
        principal: initial amount
        rate: annual interest rate (e.g. 0.05 for 5%)
        time: time in years
        n_times: number of times interest is compounded per year
        """
        if principal < 0 or rate < 0 or time < 0 or n_times <= 0:
            raise ValueError("All parameters must be positive numbers.")
            
        amount = principal * (math.pow((1 + (rate / n_times)), (n_times * time)))
        self._record_history(f"Compound interest for P={principal}, R={rate}, T={time}, N={n_times} is {amount}")
        return amount

    def get_history(self) -> List[str]:
        return self.history.copy()

    def clear_history(self) -> None:
        self.history.clear()

    def _record_history(self, operation: str) -> None:
        if len(self.history) >= 100:
            self.history.pop(0)
        self.history.append(operation)
