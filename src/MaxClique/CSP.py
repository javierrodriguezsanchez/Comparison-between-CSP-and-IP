from ortools.sat.python import cp_model

def solve(problem):
    model = cp_model.CpModel()
    
    # Definir variables
    n = len(problem.aristas)  # Número de nodos
    x = [model.NewBoolVar(f'x[{i}]') for i in range(n)]  # Variables booleanas para cada nodo
    
    # Agregar restricciones para asegurar que todos los nodos en el clique están conectados
    for i in range(n):
        for j in range(i + 1, n):
            if problem.aristas[i][j] == 0:  # No hay conexión entre i y j
                model.Add(x[i] + x[j] <= 1)  # No pueden estar ambos en el clique
    
    # Maximizar la suma de las variables x (número total de nodos en el clique)
    model.Maximize(sum(x))
    
    # Resolver el modelo
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        max_clique = [i for i in range(n) if solver.Value(x[i]) == 1]
        return {
            'x': max_clique,
            'status': 'OK',
            'result': len(max_clique)
        }
    else:
        return { 'status': 'FAIL', 'result':None}


