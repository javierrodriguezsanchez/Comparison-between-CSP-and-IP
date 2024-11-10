import random

class Grafo:
    def __init__(self, vertices, aristas):
        self.vertices = vertices
        self.aristas = aristas
        self.properties = {
            "vertices": vertices,
            "aristas": aristas
        }
        sort_aristas = sorted(self.aristas)
        self.key = f"Grafo de tamaño {self.vertices}\n{sort_aristas}"
    
    def __str__(self):
        return self.key

def problem_builder(n, density):
    aristas=[]
    for i in range(n):
        for j in range(i+1,n):
            if random.random()<density:
                aristas.append((i,j))
    return Grafo(n, aristas)