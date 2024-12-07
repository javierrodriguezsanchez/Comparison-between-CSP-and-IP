from ortools.sat.python import cp_model
from VRP import VRP
import time

def solve(problem):
    """
    Resuelve un problema genérico de enrutamiento de vehículos usando OR-Tools.
    
    Args:
        num_vehicles (int): Número de vehículos disponibles.
        distance_matrix (list[list[int]]): Matriz de distancias entre nodos.
        demands (list[int], opcional): Demanda en cada nodo (0 si no hay demanda).
        vehicle_capacities (list[int], opcional): Capacidad máxima de cada vehículo.
        depot (int, opcional): Índice del nodo que representa el depósito.

    Returns:
        dict: Solución con las rutas y costos por vehículo.
    """
    num_nodes = len(problem.distance_matrix)
    model = cp_model.CpModel()

    # Variables: x[i][j][v] indica si el vehículo v viaja de nodo i a nodo j
    x = [[[model.NewBoolVar(f'x_{i}_{j}_{v}') for v in range(problem.num_vehicles)] for j in range(num_nodes)] for i in range(num_nodes)]

    # Variables: carga en cada nodo para cada vehículo (si aplica)
    if problem.demands and problem.vehicle_capacities:
        load = [[model.NewIntVar(0, problem.vehicle_capacities[v], f'load_{i}_{v}') for v in range(problem.num_vehicles)] for i in range(num_nodes)]
    
     # Variables: orden de visita de los nodos para cada vehículo
    order = [model.NewIntVar(0, num_nodes - 1, f'order_{i}') for i in range(num_nodes)]


    # Restricción 1: Cada nodo debe ser visitado exactamente una vez (excepto el depósito)
    for i in range(1,num_nodes):
        model.Add(sum(x[i][j][v] for j in range(num_nodes) for v in range(problem.num_vehicles)) == 1)
    
    # Restricción 2: Balance de flujo para cada vehículo
    for v in range(problem.num_vehicles):
        for i in range(num_nodes):
            model.Add(sum(x[i][j][v] for j in range(num_nodes)) == sum(x[j][i][v] for j in range(num_nodes)))
    
    # Restricción 3: Cada vehículo debe comenzar y terminar en el depósito
    for v in range(problem.num_vehicles):
        model.Add(sum(x[0][j][v] for j in range(num_nodes)) >= 1)  # Máximo un viaje desde el depósito
        model.Add(sum(x[j][0][v] for j in range(num_nodes)) >= 1)  # Máximo un regreso al depósito

    # Restricción 4: Capacidad de los vehículos (si aplica)
    if problem.demands and problem.vehicle_capacities:
        for v in range(problem.num_vehicles):
            for i in range(1,num_nodes):
                model.Add(load[i][v] == sum(problem.demands[j] * x[j][i][v] for j in range(num_nodes)))
            for i in range(1,num_nodes):
                model.Add(load[i][v] <= problem.vehicle_capacities[v])
    
    # Restricción 5: No circular (prohibir subciclos en un solo vehículo)
    for v in range(problem.num_vehicles):
        for i in range(num_nodes):
            model.Add(x[i][i][v] == 0)  # Prohibir autoloops
    
     # Restricción 6: Restricciones MTZ para evitar subrutas
    for i in range(1, num_nodes):  # Nodo 0 (depósito) no tiene restricción de orden
        for j in range(1, num_nodes):
            if i != j:
                for v in range(problem.num_vehicles):
                    model.Add(order[i-1] + 1 <= order[j-1]).OnlyEnforceIf(x[i][j][v])

    # Función objetivo: Minimizar la distancia total recorrida
    model.Minimize(
        sum(problem.distance_matrix[i][j] * x[i][j][v] for i in range(num_nodes) for j in range(num_nodes) for v in range(problem.num_vehicles))
    )

    # Resolver el modelo
    solver = cp_model.CpSolver()
    start_time = time.time()
    status = solver.Solve(model)
    elapsed_time = time.time() - start_time

    # Procesar solución
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {
            'x': {},
            'status': 'OK',
            'result': solver.ObjectiveValue(),
            'time': elapsed_time,
            'method': "CSP"
        }
        for v in range(problem.num_vehicles):
            route = []
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if solver.Value(x[i][j][v]) == 1:
                        route.append((i, j))
            solution['x'][f'vehicle_{v}'] = route
        return solution
    else:
        return {
            'status': 'FAIL',
            'time': elapsed_time,
            'method': "CSP",
            'result': None
        }
