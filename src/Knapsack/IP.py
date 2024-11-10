from ortools.linear_solver import pywraplp
import time

def solve(problem):
    # Crear el solucionador
    solver = pywraplp.Solver.CreateSolver('CBC')

    # Definir las variables
    x = [solver.IntVar(0, 1, f'x_{i}') for i in range(len(problem.values))]

    # Definir la función objetivo
    solver.Maximize(sum([x[i]*problem.values[i] for i in range(len(problem.values))]))

    # Definir las restricciones
    solver.Add(sum([x[i]*problem.weights[i] for i in range(len(problem.weights))]) <= problem.capacity)

    # Resolver el problema
    start_time = time.time()
    status = solver.Solve()
    elapsed_time = time.time() - start_time

    # Imprimir los resultados
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'x': [x_i.solution_value() for x_i in x],
            'status': 'OK',
            'result': solver.Objective().Value(),
            'time': elapsed_time,
            'method': "IP"
        }
    else:
        return { 'status': 'FAIL',
            'time': elapsed_time,
            'method': "IP" }
