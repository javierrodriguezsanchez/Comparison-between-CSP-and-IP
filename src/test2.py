from ortools.sat.python import cp_model

# Crear el modelo
model = cp_model.CpModel()

# Definir las variables
num_vals = 3
a = model.NewIntVar(0, num_vals - 1, 'a')
b = model.NewIntVar(0, num_vals - 1, 'b')
c = model.NewIntVar(0, num_vals - 1, 'c')

# Añadir restricciones
model.Add(a == b)
model.Add(b != c)

# Definir la función objetivo (opcional)
model.Maximize(a + b + c)

# Crear el solucionador
solver = cp_model.CpSolver()

# Resolver el modelo
status = solver.Solve(model)

# Imprimir los resultados
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Soluciones encontradas:')
    print('a =', solver.Value(a))
    print('b =', solver.Value(b))
    print('c =', solver.Value(c))
else:
    print('No se encontró solución.')
