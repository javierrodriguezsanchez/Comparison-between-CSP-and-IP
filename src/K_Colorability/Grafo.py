import random

class Grafo:
    def __init__(self, vertices, aristas):
        self.vertices = vertices
        self.aristas = aristas

    def __str__(self):
        return f"Grafo de tamaño {self.vertices}\n{self.aristas}"

def problem_builder(n, density):
    aristas=[]
    for i in range(n):
        for j in range(i+1,n):
            if random.random()<density:
                aristas.append((i,j))
    return Grafo(n, aristas)