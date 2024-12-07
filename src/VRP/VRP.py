import random

class VRP:
    def __init__(self, num_vehicles, distance_matrix, vehicle_capacities=None, demands=None):
        self.num_vehicles = num_vehicles
        self.distance_matrix=distance_matrix
        self.demands=demands
        self.vehicle_capacities=vehicle_capacities
        self.properties={
            "num_vehicles":num_vehicles,
            "distance_matrix":distance_matrix,
            "demands":demands,
            "vehicle_capacities":vehicle_capacities
        }
    def __str__(self):
        return f"{self.num_vehicles}\0{self.distance_matrix}\0{self.demands}\0{self.vehicle_capacities}"

def problem_builder(size, vehicles, demands=False, capacities=False, equal_capacities=True):
    edges = [[random.randint(1,100) for j in range(size+1)] for i in range(size+1)]
    for i in range(size+1):
        edges[i][i]=0
        for j in range(i+1,size+1):
            edges[j][i]=edges[i][j]
    d=None
    c=None
    if demands:
        d = [0]+[random.randint(1,10)  for j in range(size+1)]
        d[0] = 0   
    if capacities:
        if equal_capacities:
            c = [random.randint(1,10)]*vehicles
        else:
            c = [random.randint(1,20) for j in range(vehicles)]

    return VRP(vehicles,edges,c,d)
