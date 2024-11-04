import random

class Portfolio:
    def __init__(self, b, n, r):
        self.b = b
        self.n = n
        self.r = r

    def __str__(self):
        return f"<{self.b}\n{self.n}\n{self.r}>"

def problem_builder(b, n, r):
    
    return Portfolio(b, n, r)