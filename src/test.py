from ortools.linear_solver import pywraplp

# Crear el solucionador
solver = pywraplp.Solver.CreateSolver('CBC')

# Definir las variables
x = solver.IntVar(0, 10, 'x')
y = solver.IntVar(0, 10, 'y')

# Definir la función objetivo
solver.Maximize(3 * x + 4 * y)

# Definir las restricciones
solver.Add(x + 2 * y <= 14)
solver.Add(3 * x + y <= 18)

# Resolver el problema
status = solver.Solve()

# Imprimir los resultados
if status == pywraplp.Solver.OPTIMAL:
    print('Solución óptima:')
    print('x =', x.solution_value())
    print('y =', y.solution_value())
    print('Valor objetivo =', solver.Objective().Value())
else:
    print('No se encontró solución óptima.')
