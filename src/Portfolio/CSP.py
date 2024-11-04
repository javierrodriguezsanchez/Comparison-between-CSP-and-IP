from ortools.sat.python import cp_model

def solve(problem):
    # Crear el modelo de CSP
    model = cp_model.CpModel()

    # Variables de decisión
    # x[i, j] = 1 si el elemento i está en el subconjunto j, 0 en caso contrario
    x = {}
    for i in range(problem.b):
        for j in range(problem.n):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # Variables de intersección entre pares de subconjuntos
    I = {}
    for k in range(problem.n):
        for l in range(k + 1, problem.n):
            I[k, l] = model.NewIntVar(0, problem.r, f'I_{k}_{l}')

    # Variable que representa la mayor intersección entre cualquier par de subconjuntos
    M = model.NewIntVar(0, problem.r, 'M')

    # Restricción de cardinalidad fija: cada subconjunto tiene exactamente m elementos
    for j in range(problem.n):
        model.Add(sum(x[i, j] for i in range(problem.b)) == problem.r)

    # Variables auxiliares y restricciones de intersección
    for k in range(problem.n):
        for l in range(k + 1, problem.n):
            # Variables auxiliares para representar x[i, k] AND x[i, l]
            aux_vars = []
            for i in range(problem.b):
                aux = model.NewBoolVar(f'aux_{i}_{k}_{l}')
                aux_vars.append(aux)
                # aux == 1 solo si x[i, k] == 1 y x[i, l] == 1
                model.AddBoolAnd([x[i, k], x[i, l]]).OnlyEnforceIf(aux)
                model.AddBoolOr([x[i, k].Not(), x[i, l].Not()]).OnlyEnforceIf(aux.Not())
            
            # Definir I[k, l] como la suma de las variables auxiliares
            model.Add(I[k, l] == sum(aux_vars))

            # M debe ser mayor o igual que todas las intersecciones I[k, l]
            model.Add(I[k, l] <= M)

    # Minimizar M
    model.Minimize(M)

    # Crear el solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Mostrar resultados
    if status == cp_model.OPTIMAL:
        subsets = [[i for i in range(problem.b) if solver.Value(x[i, j]) == 1] for j in range(problem.n)]
        return {
            'x': subsets,
            'status': 'OK',
            'result': solver.Value(M)
        }
    else:
        return { 'status': 'FAIL', 'result': None }
