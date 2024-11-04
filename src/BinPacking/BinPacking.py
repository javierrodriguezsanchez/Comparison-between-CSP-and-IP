import random

class BinPacking:
    def __init__(self, capacity, objects):
        self.capacity = capacity
        self.objects = objects

    def __str__(self):
        return f"Tamaño {self.capacity}\n{self.objects}"

def problem_builder(size, capacity):
    objects = [random.randint(1,capacity-1) for i in range(size)]
    return BinPacking(size,objects)