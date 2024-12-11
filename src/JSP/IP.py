from ortools.linear_solver import pywraplp
import time

def solve(problem):
    # Crear el solucionador
    solver = pywraplp.Solver.CreateSolver('CBC')

    num_jobs = len(problem.jobs_data)
    # Calcular horizonte de tiempo (makespan máximo posible)
    horizon = sum(duration for job in problem.jobs_data for _, duration in job)

    # Definir las variables
    x = {} #momento en que empieza la tarea j del trabajo i

    for i in range(num_jobs):
        for j in range(len(problem.jobs_data[i])):
            x[i, j] = solver.IntVar(0,horizon,f'x[{i},{j}]')

    c = {} #La tarea j del trabajo i va primero que la tarea l del trabajo k
    
    #Valor de la función objetivo
    objective=solver.IntVar(0,horizon,'makespan')

    #Restricción 1: Orden entre tareas
    for i in range(num_jobs):
        for j,(_,duration) in enumerate(problem.jobs_data[i]):
            if j==len(problem.jobs_data[i])-1:
                break
            solver.Add(x[i, j+1]-x[i, j]>=duration)

    #Restricción 2: No mas de dos tareas en una misma maquina
    for i in range(num_jobs):
        for j,(machine_1,time_1) in enumerate(problem.jobs_data[i]):
            for k in range(num_jobs):
                if k==i:continue
                for l,(machine_2,time_2) in enumerate(problem.jobs_data[k]):
                    if machine_1 != machine_2:
                        continue
                    c[i,j,k,l]=solver.BoolVar(f'x[{i},{j},{k},{l}]')
                    solver.Add(x[i, j]+time_1-x[k,l]<=c[i,j,k,l]*horizon)
                    solver.Add(x[k, l]+time_2-x[i,j]<=horizon-c[i,j,k,l]*horizon)

    # Definir la función objetivo
    for i in range(num_jobs):
        for j in range(len(problem.jobs_data[i])):
            solver.Add(x[i, j]+problem.jobs_data[i][j][1]<=objective)

    solver.Minimize(objective)

    # Resolver el problema
    start_time = time.time()
    status = solver.Solve()
    elapsed_time = time.time() - start_time

    # Imprimir los resultados
    if status == pywraplp.Solver.OPTIMAL:
        asignaciones = []
        for i in range(num_jobs):
            job_asignaciones = []
            for j, (machine, duration) in enumerate(problem.jobs_data[i]):
                job_asignaciones.append((x[i,j].solution_value(),
                                        x[i,j].solution_value()+duration,
                                        machine))
            asignaciones.append(job_asignaciones)

        return {
            'x': asignaciones,
            'status': 'OK',
            'result': solver.Objective().Value(),
            'time': elapsed_time,
            'method': "IP"
        }
    else:
        return { 'status': 'FAIL',
            'time': elapsed_time,
            'method': "IP"
        }


class JSP:
    def __init__(self, jobs_data):
        self.jobs_data=jobs_data
    def __str__(self):
        return "JSP" + str(self.jobs_data)

