from ortools.linear_solver import pywraplp

def solve(problem):
    # Crear el solucionador
    solver = pywraplp.Solver.CreateSolver('CBC')

    n = problem.vertices
    # Definir las variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:  # No puede haber un bucle (i, i)
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    # Variables para el orden de las ciudades
    u = [solver.NumVar(0, n - 1, f'u[{i}]') for i in range(n)]

    # Definir la función objetivo
    solver.Minimize(sum([sum([x[i,j]*problem.aristas[i][j] for i in range(n) if i!=j]) for j in range(n)]))

    # Restricciones: cada ciudad debe ser visitada exactamente una vez
    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n) if (i, j) in x) == 1)  # Salida
        solver.Add(solver.Sum(x[j, i] for j in range(n) if (j, i) in x) == 1)  # Entrada

    # Restricciones para evitar subtours
    for i in range(1, n):  # No aplicar a la ciudad inicial
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + (n - 1) * x[i, j] <= n - 2)

    # Resolver el problema
    status = solver.Solve()

    # Imprimir los resultados
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'x': [(i,j) for i in range(n) for(j) in range(n) if i!=j and x[i,j].solution_value()==1],
            'status': 'OK',
            'result': solver.Objective().Value()
        }
    else:
        return { 'status': 'FAIL' }
