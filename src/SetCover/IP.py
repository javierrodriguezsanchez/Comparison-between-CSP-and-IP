from ortools.linear_solver import pywraplp

# Definición del universo y los conjuntos
universe = [1, 2, 3, 4, 5]
sets = [
    {1, 2},      # Conjunto 0
    {2, 3},      # Conjunto 1
    {3, 4},      # Conjunto 2
    {4, 5},      # Conjunto 3
    {1, 5}       # Conjunto 4
]

def solve(problem):
    # Crear el solucionador
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("No se pudo crear el solucionador.")

    # Definir las variables
    x = []
    for i in range(len(problem.sets)):
        x.append(solver.BoolVar(f'x[{i}]'))

    # Añadir restricciones para cubrir cada elemento del universo
    for element in problem.universe:
        solver.Add(solver.Sum(x[i] for i in range(len(problem.sets)) if element in problem.sets[i]) >= 1)

    # Definir la función objetivo: minimizar el número de conjuntos seleccionados
    solver.Minimize(solver.Sum(x[i] for i in range(len(problem.sets))))

    # Resolver el problema
    status = solver.Solve()

    # Imprimir los resultados
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'x': [x_i.solution_value() for x_i in x],
            'status': 'OK',
            'result': solver.Objective().Value()
        }
    else:
        return { 'status': 'FAIL', 'result': None }
