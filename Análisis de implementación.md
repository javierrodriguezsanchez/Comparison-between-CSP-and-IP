Para llevar a cabo la comparación entre ambos paradigmas fueron utilizadas las siguientes clases de problemas:
- *Bin Packing*: Dado una cantidad de objetos de diferentes tamaños determinar el menor número de agrupaciones que se pueden formar tal que el la suma total dentro de un grupo no exceda cierto valor.
- *K-Coloración*: determinar el número cromático de un grafo, en otras palabras, la menor cantidad de colores necesarios para colorear sus vértices sin que dos vertices vecinos (unidos por una arista) tengan el mismo color.
- **Max-Clique*: hallar el mayor conjunto de vertices de un grafo tal que para todo par de vertices hay una arista que los une.
- *Portfolio*: Dado un conjunto, determinar la combinación de cierta cantidad de subconjuntos de determinado tamaño que minimice la intersección 2 a 2 de dichos conjuntos.
- *Set Cover*: Dado un conjunto y una lista de subconjuntos de este encontrar la menor cantidad entre los subconjuntos cuya unión resulte en el conjunto original.
- *Traveling Salesman Problem*: Dado un grafo ponderado completo, encontrar el ciclo simple que pase por todos los nodos tal que la suma de aristas sea mínima.
- *Vehicle Routing Problem*:  Hallar el conjunto óptimo de rutas para una flota de vehículos que debe satisfacer las demandas de un conjunto dado de clientes
- *Job Shop Problem*: Hallar la mínima cantidad de tiempo que hace falta para realizar un conjunto de trabajos sin que estos se solapen. Cada trabajo esta caracterizado por un conjunto de tareas, las cuales deben hacerse en máquinas específicas.

Para la modelación de cada problema, se realizó un modelo por cada paradigma. Para esto se utilizó Ortools, que es un paquete de software de código abierto desarrollado por Google para resolver problemas complejos de optimización. Ortools facilita la comparación entre ambos paradigmas al ofrecer un entorno flexible y accesible para el modelado y la resolución de problemas. Para resolver los modelos de programación entera se usó la biblioteca pywraplp, mientras que para resolver los modelos de la programación de satisfacción de  restricciones se utilizó cp_model.

Para cada clase de problema, una vez implementada la solución genérica en ambos paradigmas, se simulan diferentes instancias de la clase y se guardan los tiempos empleados. Una vez con los tiempos medidos, se agrupan los problemas según propiedades a analizar, y se investiga una posible correlación entre el desempeño de cada solución y la propiedad.
