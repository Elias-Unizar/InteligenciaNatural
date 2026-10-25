from search_P3 import *

def test_hill_climbing():
    # Test de Hill Climbing con N-Reinas
    problem = NQueensLocalSearchProblem(8)
    result = hill_climbing_node(problem)
    if problem.goal_test(result.state):
        problem.print_board(result.state)
        return True, result.state, None
    else:
        return False, None, None

def test_simulated_annealing():
    # Test de Hill Climbing con N-Reinas
    problem = NQueensLocalSearchProblem(8)
    result = simulated_annealing_node(problem, schedule=exp_schedule(k=20, lam=0.005, limit=1000))
    if problem.goal_test(result.state):
        problem.print_board(result.state)
        return True, result.state, None
    else:
        return False, None, None

def test_genetic_algorithm():
    # Máximo de conflictos para N=8 es 28
    problem = NQueensLocalSearchProblem(N=8)
    max_conflicts = problem.N * (problem.N - 1) // 2
    # Adaptación del fitness: transforma el valor (-28 a 0) en una escala positiva (0 a 28)
    # requerida por el muestreo por ruleta de select()
    fitness_fn = lambda state: max_conflicts + problem.value(state)
    # Alfabeto de genes posibles [0, 1, 2, 3, 4, 5, 6, 7]
    gene_pool = list(range(problem.N))
    # Test del Algoritmo Genético
    pop = init_population(20, gene_pool, problem.N) #20 listas de 8 elementos, cada elemento es núm. del 0 al 7
    # f_thres = 28 representa 0 conflictos en 8-Reinas
    result, numGenHechas = genetic_algorithm(pop, fitness_fn, gene_pool=gene_pool, f_thres=max_conflicts, ngen=10000, pmut=0.17)
    if problem.goal_test(result):
        problem.print_board(result) # Imprime el tablero del mejor individuo encontrado
        return True, result, numGenHechas
    else:
        return False, None, numGenHechas

def testAll(limiteSimulaciones = 1):
    print("===PRUEBA DE LOCAL SEARCH===")
    algDict = {"Hill Climbing": test_hill_climbing, "Simulated Annealing": test_simulated_annealing, "Genetic Algorithm": test_genetic_algorithm}
    for (nombre, funcion) in algDict.items():
        solutionFound = False
        vecesSimulado = 0
        while (not solutionFound and vecesSimulado < limiteSimulaciones):
            vecesSimulado += 1
            solutionFound, solution, generacionesGeneticas = funcion()
        if (solutionFound):
            if(nombre == "Genetic Algorithm"):
                print(f"{nombre} ha encontrado una solución en {vecesSimulado} intentos y {generacionesGeneticas} generaciones en esta solución: \n {solution}\n")
            else:
                print(f"{nombre} ha encontrado una solución en {vecesSimulado} intentos: \n {solution}\n")       
        else:
            if(nombre == "Genetic Algorithm"):
                print(f"{nombre} no ha encontrado una solución en {vecesSimulado} intentos y {generacionesGeneticas} generaciones\n")
            else:
                print(f"{nombre} no ha encontrado una solución en {vecesSimulado} intentos\n")


def nQueensHillClimbingSearch_Statistics(numExperimentos = 1000):
    exitos, fallos = 0, 0
    mediaPasosExito, mediaPasosFallo, mediaEval = 0.0, 0.0, 0.0
    for i in range(numExperimentos):
        problem = NQueensLocalSearchProblem(8)
        result = hill_climbing_node(problem)
        mediaEval += problem.timeEvaluated()
        if problem.goal_test(result.state):
            exitos += 1
            mediaPasosExito += result.path_cost
        else:
            fallos += 1
            mediaPasosFallo += result.path_cost
    mediaPasosExito /= exitos
    porcentajeExito = exitos*100/numExperimentos
    mediaPasosFallo /= fallos
    porcentajeFallo = fallos*100/numExperimentos
    mediaEval /= numExperimentos
    print(f"===EXPERIMENTO 1. nQueens Hill Climbing. Coste medio de pasos en 1000 experimentos ===\n"
          f"Resultados de la búsqueda de 8 reinas con Hill Climbing:\n"
          f"Éxitos: {exitos}\nFallos: {fallos}\n"
          f"Porcentaje de éxito: {porcentajeExito:.2f}%\nMedia de pasos en éxitos: {mediaPasosExito:.2f}\n"
          f"Porcentaje de fallos: {porcentajeFallo:.2f}%\nMedia de pasos en fallos: {mediaPasosFallo:.2f}\n"
          #Porcentaje de fallo es 1-porcentaje de Exito (1-p)
          f"Media de pasos (hasta un éxito): {porcentajeFallo/porcentajeExito * mediaPasosFallo + mediaPasosExito:.2f}\n"
          f"Evaluaciones promedio: {mediaEval:.3f}")

def random_restart_hill_climbing(N=8, max_restarts=1000):
    result = None
    vecesSimulado, vecesEvaluado, pasosRealizados = 0, 0, 0
    for i in range(max_restarts):
        solutionFound = False
        while (not solutionFound and vecesSimulado < max_restarts):
            vecesSimulado += 1
            problem = NQueensLocalSearchProblem(N)
            result = hill_climbing_node(problem)
            vecesEvaluado += problem.timeEvaluated()
            pasosRealizados += result.path_cost
            if problem.goal_test(result.state):
                return result, vecesSimulado, pasosRealizados, vecesEvaluado
    return None, vecesSimulado, pasosRealizados, vecesEvaluado

def experiment_random_restart_hill_climbing():
    sol, vSimulado, pasos, vEval = random_restart_hill_climbing(8, 1000)
    print(f"===EXPERIMENTO 2. Random Restart Hill Climbing. Una ejecución ===")
    NQueensLocalSearchProblem(8).print_board(sol.state)
    print(f"=== Resultados de Random Restart Hill Climbing === \n"
          f"Solución {"no encontrada.\n" if sol == None else f"encontrada: {sol.state}"}\n"
          f"Número de intentos: {vSimulado}\n"
          f"Numero total de pasos (fallos + acierto): {pasos}\n")

def statistics_random_restart(n=1000):
    mediaPasos, mediaEval = 0.0, 0.0
    for i in range(n):
        _, _, pasos, vEval = random_restart_hill_climbing(8, 1000)
        mediaPasos += pasos
        mediaEval += vEval
    mediaPasos /= n
    mediaEval /= n
    print(f"===EXPERIMENTO 3. Random Restart Hill Climbing. Media de 1000 experimentos ===\nResultados de la búsqueda de 8 reinas con restart Hill Climbing:\n"
          f"Media de pasos: {mediaPasos:.2f}\n"
          f"Media de evaluaciones: {mediaEval:.2f}, debe ser cercano a ({mediaPasos:.3f}+7) * 58 = {(mediaPasos+7)*58:.2f}\n")

def statistics_simulated_annealing(n=1000):
    exitos = 0
    mediaPasosExito, mediaPasosFallo, mediaConflictos, mediaEval = 0.0, 0.0, 0.0, 0.0   
    for i in range(n):
        problem = NQueensLocalSearchProblem(8)
        result = simulated_annealing_node(problem, schedule=exp_schedule(k=20, lam=0.005, limit=1000))
        mediaEval += problem.timeEvaluated()
        mediaConflictos -= problem.value(result.state)
        if problem.goal_test(result.state):
            exitos += 1
            mediaPasosExito += result.path_cost
        else:
            mediaPasosFallo += result.path_cost
    mediaConflictos /= n
    mediaPasos = (mediaPasosExito + mediaPasosFallo) / n
    if exitos != 0: mediaPasosExito /= exitos
    if exitos != n: mediaPasosFallo /= (n-exitos)
    mediaEval /= n
    print(f"===EXPERIMENTO 4. {n} experimentos enfriamiento simulado ===\n"
          f"Estadísticas sobre {n} ejecuciones:\n"
          f"Tasa de éxito (0 conflictos): {exitos*100/n:.2f}%\nMedia de conflictos finales: {mediaConflictos:.2f}\n"
          f"Media de pasos en éxito: {mediaPasosExito:.2f}\nMedia de pasos en fracaso: {mediaPasosFallo:.2f}\n"
          f"Media de pasos: {mediaPasos:.2f}\nMedia de evaluaciones: {mediaEval:.2f}\n")

def statistics_simulated_annealing_BIS(n=1000):
    exitos = 0
    mediaPasosExito, mediaPasosFallo, mediaConflictos, mediaEval = 0.0, 0.0, 0.0, 0.0   
    for i in range(n):
        problem = NQueensLocalSearchProblem(8)
        result = simulated_annealing_node(problem, schedule=exp_schedule(k=10, lam=0.05, limit=200))
        mediaEval += problem.timeEvaluated()
        mediaConflictos -= problem.value(result.state)
        if problem.goal_test(result.state):
            exitos += 1
            mediaPasosExito += result.path_cost
        else:
            mediaPasosFallo += result.path_cost
    mediaConflictos /= n
    mediaPasos = (mediaPasosExito + mediaPasosFallo) / n
    if exitos != 0: mediaPasosExito /= exitos
    if exitos != n: mediaPasosFallo /= (n-exitos)
    mediaEval /= n
    print(f"=== EXPERIMENTO 4-BIS. {n} experimentos enfriamiento simulado ===\n"
          f"Estadísticas sobre {n} ejecuciones:\n"
          f"Tasa de éxito (0 conflictos): {exitos*100/n:.2f}%\nMedia de conflictos finales: {mediaConflictos:.2f}\n"
          f"Media de pasos en éxito: {mediaPasosExito:.2f}\nMedia de pasos en fracaso: {mediaPasosFallo:.2f}\n"
          f"Media de pasos: {mediaPasos:.2f}\nMedia de evaluaciones: {mediaEval:.2f}\n")

def experiment_genetic_algorithm():
    # Máximo de conflictos para N=8 es 28
    problem = NQueensLocalSearchProblem(N=8)
    max_conflicts = problem.N * (problem.N - 1) // 2
    # Adaptación del fitness: transforma el valor (-28 a 0) en una escala positiva (0 a 28)
    # requerida por el muestreo por ruleta de select()
    fitness_fn = lambda state: max_conflicts + problem.value(state)
    # Alfabeto de genes posibles [0, 1, 2, 3, 4, 5, 6, 7]
    gene_pool = list(range(problem.N))
    # Test del Algoritmo Genético
    pop = init_population(20, gene_pool, problem.N) #20 listas de 8 elementos, cada elemento es núm. del 0 al 7
    # f_thres = 28 representa 0 conflictos en 8-Reinas
    result, _ = genetic_algorithm(pop, fitness_fn, gene_pool=gene_pool, f_thres=max_conflicts, ngen=10000, pmut=0.17)

    print(f"===EXPERIMENTO 5. Genéticos una ejecución ===")
    print(f"Mejor individuo encontrado: {result}\n"
          f"Conflictos del estado {-problem.value(result)}\n"
          f"Es solución (IsGoal): {problem.goal_test(result)}\n"
          f"Algoritmo Genético: {problem.timeEvaluated()} evaluaciones | Éxito: {problem.goal_test(result)}\n")   

def statistics_genetic_algorithm(n=100):
    mediaEval = 0.0
    exitos = 0
    for i in range(n):
        # Máximo de conflictos para N=8 es 28
        problem = NQueensLocalSearchProblem(N=8)
        max_conflicts = problem.N * (problem.N - 1) // 2
        # Adaptación del fitness: transforma el valor (-28 a 0) en una escala positiva (0 a 28)
        # requerida por el muestreo por ruleta de select()
        fitness_fn = lambda state: max_conflicts + problem.value(state)
        # Alfabeto de genes posibles [0, 1, 2, 3, 4, 5, 6, 7]
        gene_pool = list(range(problem.N))
        # Test del Algoritmo Genético
        pop = init_population(20, gene_pool, problem.N) #20 listas de 8 elementos, cada elemento es núm. del 0 al 7
        # f_thres = 28 representa 0 conflictos en 8-Reinas
        result, _ = genetic_algorithm(pop, fitness_fn, gene_pool=gene_pool, f_thres=max_conflicts, ngen=10000, pmut=0.17)
        mediaEval += problem.timeEvaluated()
        if (problem.goal_test(result)): exitos += 1

    mediaEval /= n
    mediaExitos = 100*exitos/n
    print(f"===EXPERIMENTO 6. 100 experimentos Genéticos ===")
    print(f"Media de evaluaciones en 100 experimentos: {mediaEval}\n"
          f"Porcentaje de éxitos en 100 experimentos {mediaExitos}%\n")


testAll()
nQueensHillClimbingSearch_Statistics(10000)
experiment_random_restart_hill_climbing()
statistics_random_restart()
statistics_simulated_annealing()
statistics_simulated_annealing_BIS()
experiment_genetic_algorithm()
statistics_genetic_algorithm()