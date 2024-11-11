import random

class BinPacking:
    def __init__(self, capacity, objects):
        self.capacity = capacity
        self.objects = objects
        self.properties = {
            "capacity": capacity,
            "objects": objects,
        }

        sort_objects = sorted(self.objects)
        self.key = f"Tamaño {self.capacity}\n{sort_objects}"

    def __str__(self):
        return self.key

def problem_builder(size, capacity):
    objects = [random.randint(1,capacity-1) for i in range(size)]
    return BinPacking(capacity,objects)