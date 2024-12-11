from ortools.sat.python import cp_model
import time

def solve(problem):
    """Minimiza el makespan en un problema de Job Shop Scheduling.

    Args:
        problem.jobs_data: Una lista de trabajos. Cada trabajo es una lista de tareas.
        Cada tarea es una tupla (máquina, tiempo_procesamiento).

    Returns:
        Una tupla (estado, makespan, asignaciones).
        - estado: El estado del solucionador (OPTIMAL, FEASIBLE, INFEASIBLE, etc.).
        - makespan: El tiempo total de procesamiento si se encuentra una solución.
        - asignaciones: Una lista de listas, donde cada lista interna representa un trabajo
                    y contiene tuplas (inicio, fin, máquina) para cada tarea.
                    Retorna None si no se encuentra una solución.
    """

    model = cp_model.CpModel()

    num_jobs = len(problem.jobs_data)
    all_machines = set()
    for job in problem.jobs_data:
        for machine, _ in job:
            all_machines.add(machine)
    all_machines = list(all_machines)  # Convertir a lista para indexación

    # Calcular horizonte de tiempo (makespan máximo posible)
    horizon = sum(duration for job in problem.jobs_data for _, duration in job)

    # Variables de decisión
    starts = {}
    ends = {}
    intervals = {}
    for job_id, job in enumerate(problem.jobs_data):
        for task_id, (machine, duration) in enumerate(job):
            start_var = model.NewIntVar(0, horizon, f'start_{job_id}_{task_id}')
            end_var = model.NewIntVar(0, horizon, f'end_{job_id}_{task_id}')
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                            f'interval_{job_id}_{task_id}')

            starts[(job_id, task_id)] = start_var
            ends[(job_id, task_id)] = end_var
            intervals[(job_id, task_id)] = interval_var

    # Restricciones
    for job_id, job in enumerate(problem.jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(starts[(job_id, task_id + 1)] >= ends[(job_id, task_id)])

    # Restricción acumulativa (NoOverlap2D)
    for machine in all_machines:
        intervals_on_machine = []
        demands_on_machine = []
        for job_id, job in enumerate(problem.jobs_data):
            for task_id, (task_machine, duration) in enumerate(job):
                if task_machine == machine:
                    intervals_on_machine.append(intervals[(job_id, task_id)])
                    demands_on_machine.append(1)  # Capacidad de la máquina es 1

        model.AddCumulative(intervals_on_machine, demands_on_machine, 1)


    # Minimizar el makespan
    makespan = model.NewIntVar(0, horizon, 'makespan')
    for job_id, job in enumerate(problem.jobs_data):
        for task_id in range(len(job)):
            model.Add(makespan >= ends[(job_id, task_id)])

    model.Minimize(makespan)

    # Resolver el modelo
    solver = cp_model.CpSolver()
    start_time = time.time()
    status = solver.Solve(model)
    elapsed_time = time.time() - start_time

    # Extraer la solución
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        asignaciones = []
        for job_id in range(num_jobs):
            job_asignaciones = []
            for task_id, (machine, _) in enumerate(problem.jobs_data[job_id]):
                job_asignaciones.append((solver.Value(starts[(job_id, task_id)]),
                                        solver.Value(ends[(job_id, task_id)]),
                                        machine))
            asignaciones.append(job_asignaciones)

        return {
            'x': asignaciones,
            'status': 'OK',
            'result': solver.Value(makespan),
            'time': elapsed_time,
            'method': "CSP"
        }
    else:
        return {
            'status': 'FAIL',
            'time': elapsed_time,
            'method': "CSP"
        }
