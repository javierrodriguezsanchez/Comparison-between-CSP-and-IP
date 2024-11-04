from ortools.linear_solver import pywraplp

def solve(problem):
    # Crear un solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    n = len(problem.aristas)  # Número de nodos
    # Crear variables: x[i] es 1 si el nodo i está en el clique, 0 si no
    x = [solver.BoolVar(f'x[{i}]') for i in range(n)]
    
    # Agregar restricciones para asegurar que todos los nodos en el clique están conectados
    for i in range(n):
        for j in range(i + 1, n):
            if problem.aristas[i][j] == 0:  # No hay conexión entre i y j
                solver.Add(x[i] + x[j] <= 1)  # No pueden estar ambos en el clique
    
    # Objetivo: maximizar la suma de las variables x (tamaño del clique)
    solver.Maximize(solver.Sum(x))
    
    # Resolver el modelo
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        max_clique = [i for i in range(n) if x[i].solution_value() == 1]
        return {
            'x': max_clique,
            'status': 'OK',
            'result': len(max_clique)
        }
    else:
        return  { 'status': 'FAIL', 'result':None}
