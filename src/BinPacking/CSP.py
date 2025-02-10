from ortools.sat.python import cp_model
import time

def solve(problem):
    num_bins = len(problem.objects)  # Número máximo de bins necesarios en el peor de los casos

    # Crear el modelo de CP-SAT
    model = cp_model.CpModel()

    # Variables de decisión
    # x[i]= bin en el que esta
    x = []
    for i in range(num_bins):
        x.append(model.NewIntVar(0,len(problem.objects), f'x_{i}'))

    # y = tamaño de bins
    y = model.NewIntVar(0,len(problem.objects),f'b')

    interval_x = []
    for i in range(num_bins):
        # Crear las tareas como intervalos
        interval_x.append(model.NewIntervalVar(x[i], 1, x[i] + 1, 'interval_x'))

    # Restricción de problem.capacity para cada bin
    model.AddCumulative(interval_x, problem.objects, problem.capacity)

    # Restricción de asignación única: cada objeto debe estar en un solo bin
    for i in range(num_bins):
        model.Add(x[i]+1 <= y)

    # Función objetivo: minimizar el número de bins utilizados
    model.Minimize(y)

    # Crear el solver
    solver = cp_model.CpSolver()
    start_time = time.time()
    status = solver.Solve(model)
    elapsed_time = time.time() - start_time

    # Mostrar resultados
    if status == cp_model.OPTIMAL:
        
        return {
            'x': [solver.value(i)+1 for i in x],
            'status': 'OK',
            'result': solver.ObjectiveValue(),
            'time': elapsed_time,
            'method': "CSP"
        }
    else:
        return {'status': 'FAIL', 
            'result': "FAIL",
            'time': elapsed_time,
            'method': "CSP"}
