from ortools.linear_solver import pywraplp

def solve(problem):
    # Crear el solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("Solver no disponible.")

    num_bins = len(problem.objects)

    # Variables de decisión
    # x[i][j] = 1 si el objeto i está en el bin j
    x = {}
    for i in range(num_bins):
        for j in range(num_bins):
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # y[j] = 1 si el bin j es utilizado
    y = {}
    for j in range(num_bins):
        y[j] = solver.BoolVar(f'y_{j}')

    # Restricción de problem.capacity para cada bin
    for j in range(num_bins):
        solver.Add(sum(problem.objects[i] * x[i, j] for i in range(num_bins)) <= problem.capacity * y[j])

    # Restricción de asignación única: cada objeto debe estar en un solo bin
    for i in range(num_bins):
        solver.Add(sum(x[i, j] for j in range(num_bins)) == 1)

    # Función objetivo: minimizar el número de bins utilizados
    solver.Minimize(solver.Sum(y[j] for j in range(num_bins)))

    # Resolver el problema
    status = solver.Solve()

    # Mostrar resultados
    if status == pywraplp.Solver.OPTIMAL:
        values = {}
        count = 1
        for j in range(num_bins):
            if y[j].solution_value() == 1:
                values[j] = count
                count+=1
        
        solution = [[values[j] for j in range(num_bins) if x[i,j].solution_value() == 1][0] for i in range(num_bins)]
        
        return {
            'x': solution,
            'status': 'OK',
            'result': solver.Objective().Value()
        }
    else:
        return { 'status': 'FAIL', 
            'result': "FAIL"
        }
