from ortools.sat.python import cp_model

def solve(problem):
    # Número de ciudades
    n = problem.vertices
    
    # Creamos el modelo de CP
    model = cp_model.CpModel()
    
    # Creamos las variables para cada ciudad
    # x[i][j] es una variable booleana que indica si el viajero va de ciudad i a ciudad j
    x = [[model.NewBoolVar(f"x[{i},{j}]") for j in range(n)] for i in range(n)]
    
    # Crear las variables de circuito
    arcs = []
    for i in range(n):
        for j in range(n):
            if i != j:
                arcs.append((i, j, x[i][j]))

    # Añadir la restricción de circuito para evitar subtours
    # Esto asegura que el recorrido sea un único circuito que visita cada ciudad exactamente una vez
    model.AddCircuit(arcs)

    # Definir el costo total del viaje
    total_cost = model.NewIntVar(0, sum(map(sum, problem.aristas)), "total_cost")
    model.Add(total_cost == sum(problem.aristas[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j))

    # Definir la función objetivo: minimizar el costo total del viaje
    model.Minimize(total_cost)

    # Resolver el modelo
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return {
            'x': [(i,j) for i in range(n) for j in range(n) if i!=j and solver.value(x[i][j])==1],
            'status': 'OK',
            'result': solver.Value(total_cost)
        }
    else:
        return { 'status': 'FAIL' }
