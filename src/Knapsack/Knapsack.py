import random

class Knapsack:
    def __init__(self, capacity, weights, values):
        self.weights = weights
        self.values = values
        self.capacity = capacity

    def __str__(self):
        return f"Knapsack:\ncapacity={self.capacity}\nweights={self.weights}\nvalues={self.values})"

def problem_builder(size, max_capacity):
    capacity = random.randint(1,max_capacity)
    weights = [random.randint(1,capacity) for _ in range(size)]
    values = [random.randint(1,100) for _ in range(size)]
    return Knapsack(capacity, weights, values)