from ortools.sat.python import cp_model
import time

def solve(problem):
    model = cp_model.CpModel()
    
    n = problem.vertices
    x = []

    # Crear variables: x[i] es el color de i
    for i in range(n):
            x.append(model.NewIntVar(1,n,f'x[{i}]'))

    # Restricción: Dos vértices adyacentes no pueden tener el mismo color
    for i, j in problem.aristas:
            model.Add(x[i] != x[j])

    # Variable para contar el número total de colores utilizados
    y = model.NewIntVar(1,n,'y')
    
    # Relación entre los colores utilizados y los vértices coloreados
    for i in range(n):
        model.Add(x[i] <= y)

    # Función objetivo: minimizar el número de colores utilizados
    model.Minimize(y)

    # Resolver el modelo
    solver = cp_model.CpSolver()

    start_time = time.time()
    status = solver.Solve(model)
    elapsed_time = time.time() - start_time

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return {
            'x': [solver.value(i)+1 for i in x],
            'status': 'OK',
            'result': solver.ObjectiveValue(),
            'time': elapsed_time,
            'method': "CSP"
        }
    else:
        return {'status': 'FAIL',
            'time': elapsed_time,
            'method': "CSP"
        }
