from ortools.sat.python import cp_model
import time

def solve(problem):
    model = cp_model.CpModel()
    
    n = problem.vertices
    x = {}

    # Crear variables: x[i, j] es True si el vértice i tiene el color j
    for i in range(n):
        for j in range(n):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Restricción: Cada vértice debe tener exactamente un color
    for i in range(n):
        model.AddExactlyOne(x[i, j] for j in range(n))

    # Restricción: Dos vértices adyacentes no pueden tener el mismo color
    for i, j in problem.aristas:
        for k in range(n):
            model.Add(x[i, k] + x[j, k] <= 1)

    # Variable para contar el número total de colores utilizados
    y = [model.NewBoolVar(f'y[{j}]') for j in range(n)]
    
    # Relación entre los colores utilizados y los vértices coloreados
    for j in range(n):
        model.Add(sum(x[i, j] for i in range(n)) <= n*y[j])

    # Función objetivo: minimizar el número de colores utilizados
    model.Minimize(sum(y[j] for j in range(n)))

    # Resolver el modelo
    solver = cp_model.CpSolver()

    start_time = time.time()
    status = solver.Solve(model)
    elapsed_time = time.time() - start_time

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        colors = [
            next(j for j in range(n) if solver.Value(x[i, j]) == 1)
            for i in range(n)
        ]

        correct_assignment = {}
        value = 1

        for i in range(n):
            if colors[i] in correct_assignment:
                colors[i] = correct_assignment[colors[i]]
                continue
            correct_assignment[colors[i]] = value
            colors[i]=value
            value += 1

        
        return {
            'x': colors,
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
