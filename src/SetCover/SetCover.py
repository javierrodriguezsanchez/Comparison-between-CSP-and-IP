import random

class SetCover:
    def __init__(self, universe, sets):
        self.universe = universe
        self.sets = sets

    def __str__(self):
        return f"Tamaño {self.universe}\n{self.sets}"

def problem_builder(size, set_count):
    universe = list(range(1,size+1))
    sets = [
        random.sample(universe, random.randint(1, size)) for i in range(set_count)
    ]
    return SetCover(universe,sets)