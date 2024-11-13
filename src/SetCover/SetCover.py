import random

class SetCover:
    def __init__(self, universe, sets):
        self.universe = universe
        self.sets = sets
        self.properties = {
            "universe": universe,
            "sets": sets,
        }
        sorted_sets=sorted([sorted(x) for x in sets])
        self.key = f"Tamaño {len(universe)}\n{sorted_sets}"
    def __str__(self):
        return self.key

def problem_builder(size, set_count):
    universe = list(range(1,size+1))
    sets = [
        random.sample(universe, random.randint(1, size)) for i in range(set_count)
    ]
    return SetCover(universe,sets)

