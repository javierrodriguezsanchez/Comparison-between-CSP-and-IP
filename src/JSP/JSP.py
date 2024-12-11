import random

class JSP:
    def __init__(self, jobs_data):
        self.jobs_data=jobs_data
        self.properties = {
            "data":jobs_data
        }
    def __str__(self):
        return "JSP" + str(self.jobs_data)


def problem_builder(jobs, machines, max_tasks, max_duration):
    jobs_data = [
        [
            (random.randint(1,machines),random.randint(1,max_duration))
            for j in range(random.randint(1,max_tasks))
        ] 
        for i in range(jobs)
    ]
    return JSP(jobs_data)