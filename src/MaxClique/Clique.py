import random

class Clique:
    def __init__(self, vertices, aristas):
        self.vertices = vertices
        self.aristas = aristas
        self.properties = {
            "vertices": vertices,
            "aristas": aristas
        }
    
    def __str__(self):
        return f"Grafo de tamaño {self.vertices}\n{self.aristas}"

def problem_builder(size, density):
    aristas=[[1 if (random.random()<density and i!=j) else 0 for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(i):
            aristas[i][j]=aristas[j][i]
    return Clique(size, aristas)