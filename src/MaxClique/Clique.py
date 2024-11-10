import random

class Clique:
    def __init__(self, vertices, aristas):
        self.vertices = vertices
        self.aristas = aristas

    def __str__(self):
        return f"Grafo de tamaño {self.vertices}\n{self.aristas}"

def problem_builder(size):
    edges = [[random.randint(0,1) for j in range(size)] for i in range(size)]
    for i in range(size):
        edges[i][i]=0
        for j in range(i+1,size):
            edges[j][i]=edges[i][j]
    return Clique(size,edges)