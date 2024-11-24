*"Dado que el tejido del Universo es de la mayor perfección y la obra del más sabio Creador, nada en absoluto tiene lugar en el Universo sin que una regla de máximo o mínimo aparezca"* 
<p style="text-align: right">Leonard Euler</p>

# Marco teórico

Un problema de optimización consiste en encontrar una asignación de valores a un conjunto de variables de forma que cumplan un conjunto de restricciones y maximicen o minimicen una función de costo. Estos se pueden clasificar de acuerdo con los los valores que pueden tener las variables que intervienen. Si los dominios de alguna de sus variables es el conjunto de los enteros estamos en un problema de optimización en enteros mixta. Dentro de la anterior categoría, se dice que se trabaja en enteros puros si todas sus variables son de dominio entero. Un caso de especial en la anterior categoría es cuando todas las variables son binarias (pueden adoptar solamente 0 o 1 como valores).

Estos problemas son fundamentales en diversas áreas como logística, planificación, asignación de tareas y de forma general todas aquellos escenarios donde se disponen de con recursos limitados para resolver determinada situación. La naturaleza combinatoria de estos problemas a menudo implica que el número de soluciones posibles crezca exponencialmente con el tamaño del problema, lo que potencia la necesidad de descubrir nuevas técnicas y heurísticas para mejorar la eficiencia los algoritmos exactos que garanticen soluciones óptimas. Dicha eficiencia depende, en primer lugar, de cómo se construyen los modelos y, en segundo lugar, de los métodos computacionales utilizados. 

Para esto podemos seguir dos paradigmas diferentes: la programación entera y la programación de satisfacción de restricciones

## Programación en enteros

La programación en enteros es un conjunto de herramientas ampliamente utilizadas para resolver el siguiente problema: Cual es el máximo/mínimo que alcanza la función $c^Tx+d^Ty$ sujeto a las restricciones: $Ax≤p$, $By≤q$, $x≥0$, $y≥0$, $x∈ \R^n$, $y∈ \Z^m$.  

### Programación lineal como base de la programación en enteros

El paradigma antes mencionado es una extensión de la programación lineal, ya que, de forma general, resolver un problema de programación en enteros requiere resolver uno o varios problemas lineales.

El principal algoritmo utilizado para resolver un problema de optimización lineal es el método Simplex. Se centra en la resolución de los modelos en su llamada forma estándar: $min$ $c^Tx$ $s.a.$ $Ax=b$, $x≥0$. Es importante notar que todo modelo puede llevarse a forma estándar siguiendo los siguientes pasos:
- Si el objetivo es maximizar $c^Tx$, este es equivalente a minimizar $-c^Tx$.
- Si hay una restricción de la forma $a^Tx≤b$, entonces se puede introducir una variable nueva $x^h=b-a^Tx$, de forma que la restricción se puede escribir como $a^Tx+x^h=b$. Homológamente, si existe una restricción de la forma $a^Tx≥b$ se puede redefinir como $a^Tx-x^h=b$. Las nuevas variables se suelen llamar variables de holguras.
- Si una variable $x_i$ es irrestricta en signo, esta se puede expresar como la resta de dos variables positivas $x_i^+$ y $x_i^-$.

Ejemplo:
$$max \text{ }z= -3x_1-x_2+x_3$$

$$s.a.$$

$$x_1+2x_2+x_3≥5$$

$$x_1-3x_2+5x_3≥-10$$

$$x_1,x_2≥0$$

Al estandarizar este problema obtenemos
$$min \text{ }z= 3x_1+x_2-x_3^++x_3^-$$

$$s.a.$$

$$x_1+2x_2+x_3^+-x_3^--x_1^h=5$$

$$-x_1+3x_2-5x_3^++5x_3^-+x_2^h=10$$

$$x_1,x_2,x_3^+,x_3^-,x_1^h,x_2^h≥0$$

Se dice que $x$ es solución factible de un problema lineal en su forma estándar si $Ax=b$. Si $x$ tiene un número de componentes nulas menor o igual al número de restricciones, se dice que $x$ es solución factible básica. De estas definiciones se deriva el Teorema Fundamental de la Programación Lineal, el cual garantiza que si existe una solución factible óptima, entonces también existe una solución factible básica óptima. Este teorema es la base del método Simplex, que consiste en explorar únicamente las soluciones factibles básicas del problema en búsqueda del óptimo.

El primer paso del algoritmo es encontrar una solución factible básica. Para eso se selecciona una cantidad de componentes de $x$ igual a la cantidad de restricciones. Sea $x_B$ las componentes elegidas y $x_r$ el resto. Entonces la matriz $A$ de la forma estándar del problema se puede descomponer en dos matrices $B$ y $C$ de forma que:

$$Bx_B+Cx_r=b$$

Luego, se multiplican ambos miembros por $B^{-1}$, resultando:

$$x_B+Rx_r=y$$

Donde $R=B^{-1}C$ y $y=B^{-1}b$.

Esta es la llamada forma explícita del problema, donde a los componentes de $x_B$ se les conoce como componentes básicos de la solución. Y permite realizar la asignación $x_B=y, x_r=0$. Garantizando una solución básica. 

En la forma explícita es importante asegurar que $y≥0$. Esto sumado a la dificultad computacional de calcular la inversa de una matriz, se suele usar el método Simplex de dos fases para la obtención de la primera solución factible básica.

Una vez con la solución factible básica inicial, el algoritmo compara las evaluaciones entre la solución actual y las adyacentes (aquellas que se obtienen al cambiar un componente básico por uno no básico). Si ninguna solución adyacente tiene una evaluación menor que la actual, entonces hemos encontrado una solución óptima, lo cual se asegura debido a la convexidad del conjunto de soluciones factibles. De lo contrario, se cambia de solución factible básica y se vuelve repite el proceso.

Aunque el método Simplex tiene un tiempo de ejecución exponencial en el peor de los casos, en la práctica, es muy eficiente y rápido para la mayoría de los problemas reales, siendo la herramienta por excelencia para su solución. 

### Planos cortantes

En el siguiente problema de optimización:

$$max \text{ } 20x_1+10x_2+x_3$$

$$s.a.$$

$$3x_1+2x_2+10x_3=10$$

$$2x_1+4x_2+20x_3=15$$

$$x_1,x_2,x_3≥0$$

La solución  de este problema es: $𝑥_1 = \frac54,𝑥_2 = \frac{25}{8},𝑥_3 = 0$. Sin embargo, si las variables involucradas fueran enteras, esta solución no es factible. La solución redondeada es: $𝑥_1 = 1,𝑥_2 = 3,𝑥_3 = 0$, con valor de la función objetivo igual a 50. Sin embargo, la solución $𝑥_1 = 2,𝑥_2 = 2,𝑥_3 = 0$, proporciona un valor de la función objetivo igual a 60. Por otra parte, la solución redondeada no satisface las restricciones del problema. Resulta por tanto de interés diseñar algoritmos que manejen la condición de las variables de ser enteras.

Una forma de extender la programación lineal a la programación entera podría plantearse como encontrar la menor cobertura convexa que contiene todas las asignaciones satisfacibles del problema. Si $S$ es el conjunto de asignaciones reales posibles del problema, $conv(S)$ se denota como la menor cobertura convexa del mismo. Ejemplo:

$$max \text{ } 5x_1+6x_2$$

$$s.a.$$

$$10x_1+14x_2 ≤ 35$$

$$x_1,x_2≥0$$

$$x_1,x_2∈\Z$$

La menor cobertura convexa es:

$$conv(S)=\{(x_1,x_2)|x_1+x_2≤3 ∧ x_1+2x_2≤4 ∧ x_1,x_2≥0\}$$

En si hacemos Simplex al nuevo problema:

$$max \text{ } 5x_1+6x_2$$

$$s.a.$$

$$(x,y) ∈ conv(S)$$

$$x_1,x_2∈\Z$$

Obtendremos la solución $x_1=2, x_2=1$.

En la práctica, buscar la menor cobertura convexa es difícil e ineficiente. Sin embargo, es posible calcular algunas de las restricciones de una cobertura convexa que no descarte soluciones enteras y excluya soluciones reales a conveniencia. Se trata de trabajar con un conjunto convexo $Q$ tal que $conv(S)⊆Q⊆S$. Si en la asignación óptima de $Q$ las variables enteras poseen valores enteros, entonces esa es la solución del problema. De lo contrario, se busca un nuevo conjunto convexo $Q'$ que no incluya dicha solución, tal que $conv(S)⊆Q'⊆Q$. Este nuevo conjunto convexo se obtiene a partir de la introducción de una nueva restricción que no excluye variables reales. Y se repite el proceso.

Todos los procedimientos basados en la explicación anteriormente planteada son conocidos como métodos de planos cortantes, y a las restricciones que se agregan se les denomina corte. Estos métodos comienzan con una relajación inicial de las restricciones de números enteros, lo que da como resultado una solución fraccionaria. Posteriormente, se añaden iterativamente cortes para reforzar la relajación hasta que se obtiene una solución entera.

Existen varias técnicas para generar planos de corte, pero la mayoría se deriva del corte fundamental, y a partir de este se derivan los mas usados, como el corte de Gomory, el corte Primal Todo Entero y el corte  de Chvátal-Gomory.


### Ramificación y acotación

Sea un problema de optimización en enteros tal que, al resolver el problema relajado, una de sus variables enteras $x_i$ tenga un valor real $p$. Como su valor puede ser entero, se cumple que $x ≤ [p] ∨ x ≥ [p]+1$. Sabiendo esto, se pueden resolver 2 nuevos problemas de optimización, con cada uno con las restricciones del problema original adicionando las restricciones anteriores respectivamente a cada 1.  Finalmente, el óptimo será el menor (si se está minimizando; de lo contrario, será el mayor) de los óptimos de ambas ramas. El método descrito es conocido como Ramificación y acotación. 

Veámoslo en el siguiente ejemplo:

Maximizar
$$x_1 + x_2$$
sujeto a:
$$2x_1 + 2x_2 ≥ 3$$

$$−2x_1 + 2x_2 ≤ 3$$

$$4x_1 + 2x_2 ≤ 19$$

$$x_1, x_2 ≥ 0$$

$$x_1, x_2 ∈ \Z$$

Solución óptima: $x_1=2.67, x_2=4.16, Objective=6.83$

Entonces, el problema se divide en dos  subproblemas distintos: uno con la restricción extra $x_1≤2$ (Caso 1) y otro con la restricción extra $x_1≥3$ (Caso 2).

Para el caso 1 la solución óptima es: $x_1=2, x_2=3.5, Objective=5.5$

Para el caso 2 esta es: $x_1=2, x_2=3.5, Objective=6.5$.

En este caso se puede seguir ramificando por ambas vias. Específicamente, si ramificamos el caso 2, este se dividiría en el caso donde $x_2≥4$ y el caso donde $x_2≤3$.

Finalmente. Tras otras dos ramificaciones se puede llegar a que el óptimo es $x1=3, x2=3, Objective=6$.

Ramificación y acotación permite explorar diferentes posibilidades de solución dividiendo el problema en subproblemas más manejables, mientras que los planos cortantes ayudan a eliminar soluciones no viables, mejorando la eficiencia del proceso de búsqueda. Ambas metodologías, aunque pueden ser aplicadas por separado, se complementan eficazmente en la búsqueda soluciones óptimas. Dicha combinación es conocida como *Branch and Cut*. 

### Uso de variables binarias para la modelación de problemas

Es fundamental identificar qué problemas pueden ser representados como problemas de programación entera. Para ello, resulta interesante explorar cómo diversas restricciones de la lógica de predicados pueden ser modeladas en este contexto. Al comprender esta relación, podemos traducir enunciados lógicos complejos en formulaciones matemáticas que se pueden resolver mediante técnicas de optimización discreta, ampliando así el alcance de los problemas que podemos abordar.

Supongamos que queramos introducir las siguientes restricciones:

$$ ∑_j a_{ij}x_j ≤ b_i ⟹ δ_i = 1$$

$$  δ_i = 1 ⟹ ∑_j a_{ij}x_j ≤ b_i$$

Si estas restricciones se logran, se podría saber cuantas restricciones se cumplen en un modelo, haciendo bisección entre una restricción y una variable binaria.

Para la primera fórmula, al aplicar contrarrecíproco, se quiere que $∑_j a_{ij}x_j > b_i$, pero si $∃ m:∑_j a_{ij}x_j≥ m$ , entonces se puede crear la restricción $∑_j a_{ij}x_j ≥ b_i+ϵ+(m-b-ϵ)δ_i$. De esa forma, si $δ_i=1$ es una restricción redundante, si $δ_i=0$ entonces fuerza a incumplir la restricción objetivo.

Para la segunda, si $∃ M:∑_j a_{ij}x_j≤ M$ entonces se puede introducir la restricción $∑_j a_{ij}x_j ≤ M-(M-b_i)δ_i$. 

Luego, si no existieran dichos valores(máximos o mínimos alcanzables), entonces se dice que el problema no es MIP representable. Un ejemplo de esto seria: $x=0∨ y=0$.

Una vez haciendo biyección entre variables lógicas y restricciones lineales, se pueden hacer operaciones lógicas elementales:

$δ_1 ∨ δ_2:δ_1+δ_2≥1$
$δ_1 ∧ δ_2:δ_1+δ_2=2$
$¬δ_1 :δ_1=0$
$δ_1 ⟹ δ_2:δ_1≤ δ_2$
$δ_1 ⟺ δ_2:δ_1=δ_2$

De esta forma se podrían modelar problemas escritos en formas normales conjuntivas y disyuntivas.


## Programación de satisfacción de restricciones

Una forma de analizar un problema de optimización es como un problema de satisfacción de restricciones, que consiste en una tupla $(V,D,C)$ donde $V$ es un conjunto de variables, $D=\{D_v|v∈ V\}$ es el conjunto de los conjuntos de los posibles valores que pueden tomar cada variable, y $C$ es un conjunto finito de restricciones de la forma $(R_i,S_i)$, con $S_i$ es un subconjunto ordenado de $V$ y $R_i$ es una relación de tamaño $|S_i|$. Una solución es una asignación a cada variable que pertenece a $V$ con uno de sus correspondientes valores en $D$ tal que se cumplan todas las restricciones en $C$.

La programación de satisfacción de restricciones (CSP) es aquella especializada en resolver este tipo de problemas. Algunas de las operaciones (por ejemplo, la ramificación) utilizadas son similares a las de IP, y tiene muchas características en común con los procedimientos de reducción que ahora se usan comúnmente para preprocesar modelos. Este enfoque no está concebido como un método de optimización propiamente, aunque se puede adaptar a él haciendo que el objetivo, con límites cada vez más estrictos, sea una restricción.

### SAT como base de la satisfacción de restricciones

No siempre es obvio, con un solo problema, hasta qué punto se utiliza la lógica o cuando se utilizan métodos más analíticos. Sin embargo, hay una gran ventaja en poder moverse entre los dos y reconocer las relaciones entre ellos. En este sentido, la programación entera y la lógica son simbióticas.

En este contexto, el problema de satisfacibilidad booleana (SAT) emerge como un caso paradigmático donde la lógica y la optimización discreta se cruzan. El Teorema de Cook, propuesto por Stephen Cook en 1971, es un hito fundamental en la teoría de la complejidad computacional, pues plantea que todo problema de la categoría NP es reducible a SAT. Este consiste en determinar dado una fórmula lógica, si existe una interpretación de la misma tal que esta sea verdadera. 

Todo lo anteriormente planteado permite resaltar la gran importancia que cobra la lógica en este tipo de problemas, pues es la que permite deducir enunciados a partir de otros en función de las reglas de deducción que lo conforman. Más específicamente, la lógica proposicional y la lógica de predicados proporcionan un marco teórico robusto para abordar los problemas SAT.

Como forma general, todo problema SAT se representa en su Forma Normal Conjuntiva(CNF) debido a las ventajas que ésta posee, y todos los cuantificadores se sitúan al principio de la expresión (Prenex Normal Form). Es necesario señalar que toda expresión válida de la lógica de predicados puede llevarse a dicha forma.

Ejemplo:

$$∀x(∃y(Q(y)∨R(x))⟹P(x))$$

Primero, eliminamos la implicación utilizando la equivalencia $A→B≡¬A∨B$:

$$∀x(¬∃y(Q(y)∨R(x)) ∨ P(x))$$

A continuación, aplicamos la equivalencia $¬∃y(A)≡∀x(¬A)$


$$∀x(∀y¬(Q(y)∨R(x)) ∨ P(x))$$

Luego, movemos los cuantificadores hacia el exterior. Para esto último, aplicamos las reglas de distribución de cuantificadores. En este caso, podemos mover el cuantificador universal hacia afuera:

$$∀x∀y(¬(Q(y)∨R(x))∨ P(x))$$

Aplicamos la equivalencia: $¬(A∨B)≡¬A∧¬B$

$$∀x∀y((¬Q(y)∧¬R(x))∨ P(x))$$

Finalmente, usamos la equivalencia $(A∧B)∨C≡(A∨C)∧(B∨C)$

$$∀x∀y((¬Q(y)∨ P(x))∧(¬R(x)∨ P(x)))$$

Cuando los dominios de las variables son finitos, entonces cualquier formula de la lógica de predicados puede expresarse como una conjunción de clausulas de la lógica proposicional. Esto es importante porque dicha lógica es consistente y completa. Se dice que un sistema es consistente si no se pueden derivar contradicciones dentro de él, es decir, no se puede demostrar que un enunciado sea verdadero y falso simultáneamente. Un sistema es completo si se puede deducir la veracidad o falsedad de cualquier enunciado que pueda ser formulado en el modelo del sistema. Sin embargo, estas dos propiedades no siempre pueden coexistir en todos los sistemas. Este dilema es especialmente relevante en el contexto de la teoría de Gödel, que establece que en cualquier sistema formal consistente que sea capaz de expresar la aritmética básica, incluye proposiciones que no pueden ser ni demostradas ni refutadas dentro del propio sistema. Lo cual significa que no puede ser completo.

A la hora de encarar un problema de optimización usando lógica de predicados, es necesario añadir funciones, constantes y reglas que la involucren. Aunque la aritmética completa sea no decidible, hay "teorías" más pequeñas dentro de ella que sí lo son. Entre estas están la aritmética sin multiplicación y la teoría de orden lineal denso. Estas bastan para resolver cualquier modelo de optimización lineal.

Veamos lo anteriormente planteado en el siguiente ejemplo:

**Maximizar:** $$2x_1 + 3x_2 − x_3 $$

*subject to:*
$$ x_1 + x_2 ≤ 3 $$

$$ −x_1 + 2x_3 ≥ −2 $$

$$ −2x_1 + x_2 − x_3 = 0 $$

$$ x_1, x_2, x_3 ∈ \R $$

Esto planteado en lógica de predicados sería:

$∃ z,x_1,x_2,x_3 ($
- $z - 2x_1 - 3x_2 + x_3 = 0$ $∧$
- $ x_1 + x_2 ≤ 3 $ $∧$
- $ −x_1 + 2x_3 ≥ −2 $ $∧$
- $ −2x_1 + x_2 − x_3 = 0 $ $∧$
- $ x_1≥ 0 $ $∧$ 
- $ x_2≥ 0 $ $∧$ 
- $ x_3≥ 0 $ 

$)$

Luego, podríamos despejar $x_3$ en la cuarta restricción y sustituir en el resto, eliminando asi una variable del problema.

$∃ z,x_1,x_2($
- $z - 2x_1 - 3x_2 + (−2x_1 + x_2) = 0$ $∧$
- $ x_1 + x_2 ≤ 3 $ $∧$
- $ −x_1 + 2(−2x_1 + x_2) ≥ −2 $ $∧$
- $ x_1≥ 0 $ $∧$ 
- $ x_2≥ 0 $ $∧$ 
- $ −2x_1 + x_2≥ 0 $ 

$)$

De forma homóloga, podríamos despejar la variable $x_2$ en la primera restricción:

$∃ z,x_1 ($
- $ x_1 + \frac z 2 -2x_1 ≤ 3 $ $∧$
- $ −5x_1 + 2(\frac z 2 -2x_1) ≥ −2 $ $∧$
- $ x_1≥ 0 $ $∧$ 
- $ \frac z 2 -2x_1 ≥ 0 $ $∧$ 
- $ −2x_1 + \frac z 2 -2x_1 ≥ 0 $

$)$

Luego despejemos la variable $x_1$ en todas las restricciones

$∃ z (∃ x_1 ($
- $ \frac z 2 - 3 ≤  x_1 $ $∧$
- $ \frac z 9 + \frac 2 9 ≥ x_1 $ $∧$
- $ x_1≥ 0 $ $∧$ 
- $ \frac z 4 ≥ x_1 $ $∧$ 
- $ \frac z 8 ≥ x_1 $ $))$

Notar que aquí deducimos que:

$∃ z ($
- $ \frac z 2 - 3 ≤  \frac z 9 + \frac 2 9 $ $∧$
- $ \frac z 2 - 3 ≤ \frac z 4  $ $∧$
- $ \frac z 2 - 3 ≤ \frac z 8 $ $∧$
- $ 0 ≤  \frac z 9 + \frac 2 9 $ $∧$
- $ 0 ≤ \frac z 4  $ $∧$
- $ 0 ≤ \frac z 8 $ 

$)$

Concluyendo que $-2≤ z ≤ 8$. Y como el objetivo es maximizar. Se toma $z=8$. De aquí vemos que $0≤ x_1 ≤1$. Que tomando a $x_1=1$ nos queda que $x_2=2$ y $x_3 = 0$

Este procedimiento es conocido como método de eliminación de cuantificadores, que si bien no es utilizado actualmente por existir soluciones mucho más eficientes dentro de la programación lineal como el método Simplex, teóricamente demuestra que la programación lineal es una teoría decidible.

### Davis-Putnam

El algoritmo de Davis-Putnam(DP)  es un precursor de los algoritmos modernos para resolver SAT, el cual utiliza el principio de resolución. Sea una instancia de SAT en CNF, sea $p$ una variable proposicional y sean $C_1=p ∨ Q_1$  y  $C_2 = ¬p ∨ Q_2$ cláusulas del problema, con $Q_1$ y $Q_2$ disyunciones de literales. Como $(p=1)⟹ Q_2$ y $(p=0)⟹ Q_1$ se puede deducir $Q_1∨ Q_2$. Al aplicar iterativamente resolución, podemos deducir posibles valores de variables o una contradicción. En este último caso, se dice que el problema es insatisfacible. 

Veamos el siguiente ejemplo: La siguiente formula sera satisfacible:

$$(a∨ b) ∧(a∨ ¬b) ∧ (¬a∨ c) ∧(¬a∨ ¬c)$$

Al aplicar la regla de resolución entre las primeras dos cláusulas obtenemos la nueva restricción $(a ∨ a)$, la cual es lógicamente equivalente a $(a)$. Si aplicamos nuevamente resolución entre esta cláusula y las dos ultimas, deducimos $(c)$ y $(¬c)$. Si aplicamos resolución somos capaces de ver que llegamos a un absurdo, por lo que la formula nunca será satisfacible. 

El algoritmo de Davis-Putnam sirve como base para el desarrollo de todos los algoritmos utilizados para resolver el problema SAT, estableciendo un marco teórico importante para la lógica computacional.

### Davis-Logemann-Loveland

Por otra parte, Davis-Logemann-Loveland(DLL/DPLL) se centra en asignar iterativamente valores a las variables y deshaciendo dichas asignaciones en caso de conflicto. Este algoritmo refina Davis-Putnam e introduce técnicas cruciales  como el backjumping y el aprendizaje de cláusulas. Se basa en tres hechos: 
1- Todo literal puro (se dice puro si el literal opuesto no esta presente) es asignado como cierto. Ejemplo: $(a∨ b) ∧ (a∨ ¬c) ∧ (d∨ ¬c) ∧ (¬d∨ ¬b) ∧ (b∨ c) $. Aquí al no estar $¬a$ en ninguna cláusula, se puede asignar $a=1$ y reducir el problema a $(d∨ ¬c) ∧ (¬d∨ ¬b) ∧ (b∨ c) $.
2- si una cláusula tiene todos sus literales negados excepto uno este ultimo debe ser cierto. Ejemplo $(a ∨ b ∨ c)∧(a∨¬b∨¬c)∧(¬a∨ b∨¬c) ∧(¬a∨ ¬b∨ c).$ Si se hace la asignación parcial $a=1, ¬c=1$, entonces la tercera clausula $(¬a∨ ¬b∨ c)$ solo puede cumplirse si $¬b=1$.
3- Si todos los literales de una cláusula están negados, entonces la asignación hecha hasta dicho punto es falsa.

El algoritmo tiene 5 etapas: 
1- Preprocesamiento: Aquí se buscan todos los literales puros y se les asigna valor 1.
2- ramificación: Aquí se asigna valor a un literal. Una buena heurística a la hora de decidir que literal escoger es Variable State Independent Decaying Sum(VSIDS), que consiste en asignar un numero a cada literal, el cual empieza siendo la cantidad de cláusulas en las que aparece, se divide entre una constante (usualmente 2) periódicamente y se le suma 1 cada vez que aparece en una cláusula conflicto.
3- propagación unitaria (llamado en ingles Unit Propagation), en esta etapa se asignan valores a aquellos literales cuyo valor se pueden deducir. Es una de las mejoras clave del DPLL sobre su predecesor
4- análisis de conflicto: aquí se busca agregar restricciones adicionales basada en la asignación parcial en caso de hallar una contradicción.
5- retroceso (comúnmente llamado  Backtracking), deshace asignaciones hechas en caso de darse una contradicción, para asi explorar nuevos casos.


**Ejemplo de SAT utilizando DPLL**

Consideremos la siguiente fórmula en FNC:
$F=(A∨¬B)∧(B∨C)∧(¬A∨¬C)∧(¬B∨¬A)∧(D∨¬C)∧(¬A∨D)$

Paso 1: Preprocesamiento
Se buscan literales puros. En este caso, como $¬D$ no esta presente en ninguna cláusula, se asigna $D=true$, reduciendo $F$ a:
$$F=(A∨¬B)∧(B∨C)∧(¬A∨¬C)∧(¬B∨¬A)$$

Paso 2: Ramificación
El algoritmo DPLL selecciona un literal para asignar un valor. Supongamos que elegimos $A$ y lo asignamos a verdadero:
$A=true$

Paso 3: Propagación Unitaria
Después de asignar $A=true$, actualizamos la fórmula. La cláusula $(A∨¬B)$ se satisface y se elimina por lo que $F$ se reduce a $F^′=(B∨C)∧(¬C)∧(¬B)$
Ahora, observamos las cláusulas $(¬C)$ y $(¬B)$. Esto implica que $C=false$ y $B=false$. Sin embargo, esto hace falsa la segunda cláusula.

Paso 4: Análisis del conflicto.
Debido a que la asignación parcial conlleva a la cláusula vacía, se puede adicionar una nueva cláusula $(¬A)$. Siendo ahora:
$$F=(A∨¬B)∧(B∨C)∧(¬A∨¬C)∧(¬B∨¬A)∧(¬A)$$

Paso 5: Retroceso
Se deshace la asignación $A=true$.

Luego, al volver al paso 1 y ejecutar luego ejecutar el paso 2, se llega a que la asignación:
$A=false, B=false,C=true, D=true$

Haciendo $F$ satisfacible.

### Consistencia como forma de propagación de restricciones

La mayoría de los algoritmos usados recaen en la propagación de restricciones (constraint propagation) y se realiza mediante la comprobación de consistencia entre los valores de las variables. Este proceso implica analizar las restricciones que vinculan diferentes variables y ajustar sus dominios en consecuencia, lo que implica eliminar aquellos que violen alguna restricción. Entre las formas de comprobar consistencia está la consistencia de nodo, que reduce el dominio de una variable a aquellos valores que cumplen con todas las restricciones unarias.

También se habla de la consistencia de arco, centrada en eliminar aquellos valores $a$ de una variable $x$ si no existen valores $b$ de una variable $y$ tales que $(a,b)$ satisfagan a todas las restricciones entre $x$ y $y$. Uno de los algoritmos más utilizados para comprobar consistencia de arco es el algoritmo AC-3, el cual guarda todos los pares ordenados de variables en una cola. Luego saca iterativamente cada uno de estos pares $<x,y>$ hasta que la cola se quede vacía, y comprueba la consistencia de arco para cada posible valor de $x$. Si un valor no cumple la consistencia de arcos, este valor es eliminado del dominio de $x$, y todos los pares de variables de la forma $<z,x>$ son reinsertados en la cola. El algoritmo tiene una complejidad de tiempo en el peor de los casos de $O(ed^3 )$, donde $e$ es la cantidad de pares y $d$ es el tamaño de dominio más grande. Tras aplicar la consistencia de arco, pueden surgir tres posibles escenarios: si todos los dominios de las variables quedan con exactamente 1 valor (en cuyo caso tenemos la asignación satisfacible), si un dominio queda vacío (en cuyo caso ocurriría una contradicción y se debe hacer backtrack en una asignación) o si al menos un dominio queda con más de un posible valor, en cuyo caso se le debe asignar un valor y volver a realizar consistencia de arco.

Otras formas de consistencia existentes son la consistencia de camino y la $k$-consistencia. La consistencia de camino considera no solo las restricciones binarias entre pares de variables, sino también las relaciones a través de secuencias más largas de variables. Aquí, $u$ es un valor consistente de $x$ si para todo $y$ existe un $w$ tal que dado cualquier secuencia de variables $a_1, a_2, ... a_n$, con $a_1=x$ y $a_n=y$ tenga la secuencia de valores $v_1, v_2, ... v_n$ con $v_1=u$ y $v_n=w$ de forma que el par $<v_i,v_{i+1}>$ cumpla con todas las restricciones binarias entre $a_i$ y $a_{i+1}$, con $1≤ i ≤ n$. Si bien la aplicación de la consistencia de camino garantiza un mayor nivel de consistencia que la consistencia del arco, todavía no es suficiente para resolver CSP en general. Esto significa que garantizando dicha consistencia, no todas las asignaciones garantizadas por esta son necesariamente soluciones satisfacible. Por otra parte, la $k$-consistencia, se logra al garantizar que cualquier asignación válida de valores a $k-1$ variables garantiza la posibilidad de asignación de un valor a otra cualquier otra variable. Se dice que se es fuertemente $k$-consistente si para todo $j<k$ se es $j$-consistente. Ambos tipos de consistencias son bastante costosos computacionalmente por lo que no es muy utilizado en la práctica en comparación con la consistencia de arco.

Ahora, si se desea optimizar usando CSP, una forma de lograrlo es hacer búsqueda binaria sobre la función objetivo. Sea $f(x)$ la función objetivo a maximizar y sean $m$ y $M$ tales que $∀ x:m≤ f(x)≤ M$. Esto permite hacer un problema de satisfacibilidad adicionando la restricción $f(x)≥ \frac{M+m}2$. Si el problema es satisfacible con $f(x)=m'$ entonces se puede resolver el modelo nuevamente, pero esta vez con la restricción $f(x)≥ \frac{M+m'}2$. En caso contrario se puede volver a realizar la búsqueda con la restricción $f(x)≥ \frac{M'+m}2$ con $M'=\frac{M+m'}2$. El caso de parada es cuando $M=m$, haciendo que la respuesta final sea la ultima solución encontrada.

### Restricciones globales de la programación de satisfacción de restricciones

A diferencia de la programación en enteros, que restringe su modelado a expresiones lineales, En la programación por restricciones, los modelos suelen expresarse en forma de predicados, que si bien pudieran ser convertidos a modelos lineales, dicha conversión puede ser engorrosa. Dichos predicados suelen depender del software utilizado, y en muchos casos se da la oportunidad al usuario de definir predicados locales. Pero de forma general existen restricciones globales que suelen ser semánticamente redundantes y permiten filtrar el dominio de las variables.

**Restricciones globales fundamentales:**

- **All Different**: Esta restricción fuerza a que todos los valores de las variables sean diferentes entre si.
- **Global Cardinality**: Estas restricciones controlan la cantidad de veces que ciertos valores pueden aparecer en un conjunto de variables. Por ejemplo, global_cardinality permite especificar cuántas veces debe aparecer cada valor en un array de variables.
- **Inverse**: Esta restricción asegura que si un valor se asigna a una variable, entonces otro conjunto de variables debe reflejar esa asignación en un orden inverso. Es útil para problemas donde la relación entre las variables es crucial.
- **Table**: Permite definir restricciones basadas en una tabla predefinida que especifica combinaciones válidas de valores para un conjunto de variables. Esto es útil para modelar relaciones complejas entre variables.
- **Circuit**: Asegura que un conjunto de variables forma un circuito, lo cual es esencial en problemas como el Traveling Salesman Problem. Esta restricción garantiza que no haya subcircuitos y que todos los nodos sean visitados.
- **Lexicographic Order (Lex)**: Se utiliza para imponer un orden lexicográfico entre dos o más secuencias de variables, lo que puede ser útil en problemas donde el orden relativo es importante.
- **Element**: Esta restricción permite acceder a los elementos de un array mediante índices definidos por otras variables, facilitando la modelización de problemas donde se necesita seleccionar entre múltiples opciones.
- **Cumulative**: Se utiliza para gestionar recursos limitados en el tiempo, asegurando que las demandas no excedan la capacidad disponible en cada momento.
- **Regular**: Permite definir restricciones sobre cadenas de longitud variable y es útil en problemas relacionados con autómatas y gramáticas formales.