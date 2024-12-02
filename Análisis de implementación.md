La implementación realizada consiste en una comparación objetiva entre los paradigmas IP y CSP mediante las bibliotecas de ortools en python *pywraplp* y *cp_model* respectivamente. Para ello, se abordan diferentes clases de problemas, simulando casos específicos y resolviéndolos mediante ambos enfoques. Una vez completado el proceso, se evalúa el rendimiento temporal de los solucionadores y se lleva a cabo un análisis detallado de los resultados obtenidos.

Las clases de problemas analizadas son: 
- *Bin Packing*: Dado una cantidad de objetos de diferentes tamaños determinar el menor número de agrupaciones que se pueden formar de forma que el tamaño total de un grupo no exceda cierto valor.
- *K-Coloración*: determinar el número cromático de un grafo.
- **Max-Clique*: hallar el mayor clique en un grafo
- *Knapsack Problem*: Se tienen varios objetos con diferentes pesos y valores. Encontrar la combinación de objetos de mayor valor tal que la suma de sus pesos no exceda determinado número 
- *Portfolio*: Dado un conjunto, determinar la combinación de cierta cantidad de subconjuntos de determinado tamaño que minimice la intersección 2 a 2 de dichos conjuntos.
- *Set Cover*: Dado un conjunto y una lista de subconjuntos de este encontrar la menor candida entre los subconjuntos cuya unión resulte en el conjunto original.
- *Traveling Salesman Problem*: Dado un grafo ponderado completo, encontrar el ciclo de Halminton de menor tamaño.

Para cada problema, las implementaciones se llevaron a cabo en dos bibliotecas de ortools en python: pywraplp y cp_model.

De los resultados, se puede observar como la complejidad temporal de los modelos lineales empeora drásticamente al aumentar el numero de restricciones con respecto a la cantidad de variables. Al analizar problemas como *Portfolio* o *K-Coloración* incluso para pequeñas cantidades de variables el carácter exponencial del problema se hace evidente para el problema de programación entera.