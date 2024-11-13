from ortools.linear_solver import pywraplp
import time

def solve(problem):
    # Crear el solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("Solver no disponible.")

    # Variables de decisión
    # x[i, j] = 1 si el elemento i está en el subconjunto j
    x = {}
    for i in range(problem.b):
        for j in range(problem.n):
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # Variables de intersección entre pares de subconjuntos
    I = {}
    for k in range(problem.n):
        for l in range(k + 1, problem.n):
            I[k, l] = solver.IntVar(0, problem.r, f'I_{k}_{l}')

    # Variable que representa la mayor intersección entre cualquier par de subconjuntos
    M = solver.IntVar(0, problem.r, 'M')

    # Restricción de cardinalidad fija: cada subconjunto tiene exactamente m elementos
    for j in range(problem.n):
        solver.Add(sum(x[i, j] for i in range(problem.b)) == problem.r)

    # Variables auxiliares y restricciones de intersección
    for k in range(problem.n):
        for l in range(k + 1, problem.n):
            # Variables auxiliares para representar x[i, k] * x[i, l]
            aux_vars = []
            for i in range(problem.b):
                aux = solver.BoolVar(f'aux_{i}_{k}_{l}')
                aux_vars.append(aux)
                # aux == x[i, k] AND x[i, l] (representado mediante restricciones)
                solver.Add(aux <= x[i, k])
                solver.Add(aux <= x[i, l])
                solver.Add(aux >= x[i, k] + x[i, l] - 1)
            
            # Definir I[k, l] como la suma de las variables auxiliares
            solver.Add(I[k, l] == sum(aux_vars))

            # M debe ser mayor o igual que todas las intersecciones I[k, l]
            solver.Add(I[k, l] <= M)

    # Minimizar M
    solver.Minimize(M)

    # Resolver el problema
    start_time = time.time()
    status = solver.Solve()
    elapsed_time = time.time() - start_time

    # Mostrar resultados
    if status == pywraplp.Solver.OPTIMAL:
        subsets = [[i for i in range(problem.b) if x[i, j].solution_value() == 1] for j in range(problem.n)]
        return {
            'x': subsets,
            'status': 'OK',
            'result': M.solution_value(),
            'time': elapsed_time,
            'method': "IP"
        }
    else:
        return { 'status': 'FAIL', 'result': None,
            'time': elapsed_time,
            'method': "IP" }
