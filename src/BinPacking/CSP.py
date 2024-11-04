from ortools.sat.python import cp_model

def solve(problem):
    num_bins = len(problem.objects)  # Número máximo de bins necesarios en el peor de los casos

    # Crear el modelo de CP-SAT
    model = cp_model.CpModel()

    # Variables de decisión
    # x[i][j] = 1 si el objeto i está en el bin j, 0 en caso contrario
    x = {}
    for i in range(num_bins):
        for j in range(num_bins):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # y[j] = 1 si el bin j es utilizado, 0 si está vacío
    y = {}
    for j in range(num_bins):
        y[j] = model.NewBoolVar(f'y_{j}')

    # Restricción de problem.capacity para cada bin
    for j in range(num_bins):
        model.Add(sum(problem.objects[i] * x[i, j] for i in range(num_bins)) <= problem.capacity * y[j])

    # Restricción de asignación única: cada objeto debe estar en un solo bin
    for i in range(num_bins):
        model.Add(sum(x[i, j] for j in range(num_bins)) == 1)

    # Función objetivo: minimizar el número de bins utilizados
    model.Minimize(sum(y[j] for j in range(num_bins)))

    # Crear el solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Mostrar resultados
    if status == cp_model.OPTIMAL:
        values = {}
        count = 1
        for j in range(num_bins):
            if solver.Value(y[j]) == 1:
                values[j] = count
                count+=1
        
        solution = [[values[j] for j in range(num_bins) if solver.Value(x[i, j]) == 1][0] for i in range(num_bins)]

        return {
            'x': solution,
            'status': 'OK',
            'result': solver.ObjectiveValue()
        }
    else:
        return {'status': 'FAIL', 
            'result': "FAIL"}
