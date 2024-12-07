from ortools.linear_solver import pywraplp
import time

def solve(problem):
    """
    Resuelve un problema genérico de enrutamiento de vehículos usando PyWrapLP.
    
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
    
    # Crear el solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return {'status': 'Solver not available'}
    
    # Variables: x[i][j][v] indica si el vehículo v viaja de nodo i a nodo j
    x = [[[solver.BoolVar(f'x_{i}_{j}_{v}') for v in range(problem.num_vehicles)] 
            for j in range(num_nodes)] for i in range(num_nodes)]
    
    # Variables: carga en cada nodo para cada vehículo (si aplica)
    if problem.demands and problem.vehicle_capacities:
        load = [[solver.IntVar(0, problem.vehicle_capacities[v], f'load_{i}_{v}') for v in range(problem.num_vehicles)] 
                for i in range(num_nodes)]

    # Variables de orden de visita para evitar subciclos
    order = [solver.IntVar(0, num_nodes - 1, f'order_{i}') for i in range(num_nodes)]

    # Restricción 1: Cada nodo (excepto el depósito) debe ser visitado exactamente una vez
    for i in range(1,num_nodes):
        solver.Add(sum(x[i][j][v] for j in range(num_nodes) for v in range(problem.num_vehicles)) == 1)
    
    # Restricción 2: Balance de flujo para cada vehículo
    for v in range(problem.num_vehicles):
        for i in range(num_nodes):
            solver.Add(sum(x[i][j][v] for j in range(num_nodes)) == sum(x[j][i][v] for j in range(num_nodes)))
    
    # Restricción 3: Cada vehículo debe comenzar y terminar en el depósito
    for v in range(problem.num_vehicles):
        solver.Add(sum(x[0][j][v] for j in range(num_nodes)) >= 1)  # Salida desde el depósito
        solver.Add(sum(x[j][0][v] for j in range(num_nodes)) >= 1)  # Regreso al depósito

    # Restricción 4: Capacidad del vehículo (si aplica)
    if problem.demands and problem.vehicle_capacities:
        for v in range(problem.num_vehicles):
            for i in range(1,num_nodes):
                solver.Add(load[i][v] == sum(problem.demands[j] * x[j][i][v] for j in range(num_nodes)))
            for i in range(1,num_nodes):
                solver.Add(load[i][v] <= problem.vehicle_capacities[v])
    
    # Restricción 5: No circular (prohibir subciclos)
    for i in range(num_nodes):
        for j in range(num_nodes):
            for v in range(problem.num_vehicles):
                solver.Add(x[i][i][v] == 0)  # Prohibir autoloops
    
        # Restricción 6: Evitar subciclos usando variables de orden
    for i in range(1, num_nodes):  # Nodo 0 (depósito) no tiene restricción de orden
        for j in range(1, num_nodes):
            if i != j:
                for v in range(problem.num_vehicles):
                    solver.Add(order[i] + 1 <= order[j] + num_nodes * (1 - x[i][j][v]))

    # Función objetivo: Minimizar la distancia total recorrida
    solver.Minimize(
        sum(problem.distance_matrix[i][j] * x[i][j][v] 
            for i in range(num_nodes) for j in range(num_nodes) for v in range(problem.num_vehicles))
    )
    
    # Resolver el modelo
    start_time = time.time()
    status = solver.Solve()
    elapsed_time = time.time() - start_time
    
    # Procesar solución
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            'x': {},
            'status': 'OK',
            'result': solver.Objective().Value(),
            'time': elapsed_time,
            'method': "IP"
        }
        for v in range(problem.num_vehicles):
            route = []
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if x[i][j][v].solution_value() > 0.5:  # Solución binaria
                        route.append((i, j))
            solution['x'][f'vehicle_{v}'] = route
        return solution
    else:
        return {
            'status': 'FAIL',
            'time': elapsed_time,
            'method': "IP",
            'result': None
        }
