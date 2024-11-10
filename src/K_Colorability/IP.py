from ortools.linear_solver import pywraplp
import time

def solve(problem):
    # Crear el solucionador
    solver = pywraplp.Solver.CreateSolver('CBC')

    n = problem.vertices

    # Definir las variables
    v = [
        [
            solver.IntVar(0, 1, f'v_{i}_{j}') for i in range(n)
        ] 
        for j in range(n)
    ] #vértice i en color j

    c = [
            solver.IntVar(0, 1, f'c_{i}') for i in range(n)
    ]  #color i es usado

    # Definir la función objetivo
    solver.Minimize(sum(c))

    # Definir las restricciones
    for i in range(n):
        # Un vértice debe estar en un color
        solver.Add(sum([v[i][j] for j in range(n)]) == 1)
        # Un vértice en un color fuerza el color 
        solver.Add(sum([v[j][i] for j in range(n)]) - n*c[i] <= 0)

    for i, j in problem.aristas:
        for k in range(n):
            # Si hay una arista entre dos vértices, no pueden estar en el mismo color
            solver.Add(v[i][k]+v[j][k]<=1)

    # Resolver el problema
    start_time = time.time()
    status = solver.Solve()
    elapsed_time = time.time() - start_time

    # Imprimir los resultados
    if status == pywraplp.Solver.OPTIMAL:
        colors = [
            next(j for j in range(n) if v[i][j].solution_value() == 1)
            for i in range(n)
        ]

        correct_assignment = {}
        value = 1

        for i in range(n):
            if colors[i] in correct_assignment:
                colors[i] = correct_assignment[colors[i]]
                continue
            correct_assignment[colors[i]] = value
            colors[i]=value
            value += 1


        return {
            'x': colors[i],
            'status': 'OK',
            'result': solver.Objective().Value(),
            'time': elapsed_time,
            'method': "IP"
        }
    else:
        return { 'status': 'FAIL',
            'time': elapsed_time,
            'method': "IP"
        }
