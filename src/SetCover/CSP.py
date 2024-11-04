from ortools.sat.python import cp_model

def solve(problem):
    # Crear el modelo
    model = cp_model.CpModel()

    # Definir las variables: x[i] es 1 si se selecciona el conjunto i, 0 en caso contrario
    x = []
    for i in range(len(problem.sets)):
        x.append(model.NewBoolVar(f'x[{i}]'))

    # Añadir restricciones para cubrir cada elemento del universo
    for element in problem.universe:
        model.Add(sum(x[i] for i in range(len(problem.sets)) if element in problem.sets[i]) >= 1)

    # Definir la función objetivo: minimizar el número de conjuntos seleccionados
    model.Minimize(sum(x[i] for i in range(len(problem.sets))))

    # Resolver el problema
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Mostrar los resultados
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return {
            'x': [solver.Value(x_i) for x_i in x],
            'status': 'OK',
            'result': sum(solver.Value(x[i]) for i in range(len(problem.sets)))
        }
    else:
        return {'x': [], 'status': 'Error', 'result': None}