from ortools.sat.python import cp_model


def solve(problem):
    # Crear el modelo
    model = cp_model.CpModel()

    # Definir las variables
    num_vals = 3
    
    x = [model.NewIntVar(0, 1, f'x_{i}') for i in range(len(problem.values))]

    # Añadir restricciones
    model.Add(sum([x[i]*problem.weights[i] for i in range(len(problem.weights))])<=problem.capacity)

    # Definir la función objetivo (opcional)
    model.Maximize(sum([x[i]*problem.values[i] for i in range(len(problem.values))]))

    # Crear el solucionador
    solver = cp_model.CpSolver()

    # Resolver el modelo
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return {
            'x': [solver.Value(x_i) for x_i in x],
            'status': 'OK',
            'result': sum([solver.Value(x[i])*problem.values[i] for i in range(len(problem.values))])
        }
    else:
        return { 'status': 'FAIL' }
