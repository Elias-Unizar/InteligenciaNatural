from games_P3 import *
import time

def ejecutar_comparativa():
    juego = ConnectFour()
    jugador = 'X'
    resultados = []
    for d in range(1, 8):
        # Minimax con cutoff: devuelve (acción, valor, nodos)
        iniTimer = time.time()
        _, _, mm_nodos = minimax_cutoff_search(juego.initial, juego, max_depth=d,
                                               f_eval=juego.eval_conecta4_basica)
        mm_tiempo = time.time() - iniTimer

        # Alfa-Beta con cutoff: devuelve (acción, valor, nodos, podas).
        # Su depth empieza en 1 en los hijos de la raíz, así que se corta con depth >= d
        iniTimer = time.time()
        _, _, ab_nodos, ab_podas = alpha_beta_cutoff_search(juego.initial, juego, d=d, eval_fn=lambda s: juego.eval_conecta4_basica(s, jugador))
        ab_tiempo = time.time() - iniTimer

        ahorro = 100.0 * (mm_nodos - ab_nodos) / mm_nodos
        resultados.append((d, mm_nodos, mm_tiempo, ab_nodos, ab_podas, ab_tiempo, ahorro))
    return resultados


def ejecutar_traza(limiteProf):
    juego = ConnectFour()
    lineasTrazaLimite = "=" * 118
    jugadorInicial = 'X'

    print(lineasTrazaLimite)
    print("COMPARATIVA DE RENDIMIENTO: MINIMAX CUTOFF vs PODA ALFA-BETA CUTOFF")
    print(lineasTrazaLimite)
    print(f"{'Profundidad (d)':<16}| {'MM Nodos':<12}| {'MM Tiempo (s)':<14}| {'AB Nodos':<10}"
          f"| {'AB Podas':<10}| {'AB Tiempo (s)':<14}| {'Ahorro Nodos (%)'}")
    print("-" * 118)

    for d in range(limiteProf):
        # Minimax con cutoff: devuelve (acción, valor, nodos)
        iniTimer = time.time()
        #Al contrario que en el Alpha-Beta, yo he podido decidir que a f_eval dentro del minimax se le paso tanto el estado como el jugador, por tanto no necesito la función inline lambda
        _, bv_mm, mm_nodos = minimax_cutoff_search(juego.initial, juego, max_depth=d+1, f_eval=juego.eval_conecta4_basica)
        mm_tiempo = time.time() - iniTimer

        # Alfa-Beta con cutoff: devuelve (acción, valor, nodos, podas).
        iniTimer = time.time()
        _, bv_ab, ab_nodos, ab_podas = alpha_beta_cutoff_search(juego.initial, juego, d=d+1, eval_fn=lambda s: juego.eval_conecta4_basica(s, jugadorInicial))
        ab_tiempo = time.time() - iniTimer

        ahorronodos = 100.0 * (mm_nodos - ab_nodos) / mm_nodos
        print(f"{d+1:<16}| {mm_nodos:<12}| {mm_tiempo:<14.4f}| {ab_nodos:<10}| {ab_podas:<10}| {ab_tiempo:<14.4f}| {ahorronodos:.1f}%")
    #Fin del bucle de depth, ya hemos acabado la traza
    print(lineasTrazaLimite)
#Fin de la funcion ejecutarTraza

def play_console_game(hayHumano=True, empiezaHumano=True, d=4):
    juego = ConnectFour()
    jugador1, jugador2 = 'X', 'O'  #Por como esta construido el game, siempre empizan X
    # Por suerte para mi display, play_game() no hace displays intermedios, puedo asi formatearlos como quiera
    # play_game llama a cada jugador como jugador(game, state) y espera que se devuelva una accion (x, y)
    def turno_humano(game, state):
        pieza = game.to_move(state)
        game.display(state)
        jugadas = {y: (x, y) for (x, y) in game.actions(state)}   # columna -> casilla libre
        validas = sorted(jugadas)
        while True:
            texto = input(f"Turno de {pieza}. Elige columna {validas}: ")
            if texto.strip().isdigit() and int(texto) in jugadas:
                return jugadas[int(texto)]
            print("Columna no válida.")
 
    def turno_ia(game, state):
        pieza = game.to_move(state)
        game.display(state)
        print(f"Turno de IA ({pieza}) calculando a profundidad d={d}...")
        iniTimer = time.time()
        # d-1: alpha_beta_cutoff_search corta con depth > d y cuenta desde 1 en los hijos de la raíz
        accion, _, nodos, podas = alpha_beta_cutoff_search(
            state, game, d=d,
            eval_fn=lambda s: game.eval_conecta4_basica(s, pieza))
        tiempo = time.time() - iniTimer
        print(f">> IA colocó ficha en la columna {accion[1]} "
              f"(Nodos: {nodos}, Podas: {podas}, Tiempo: {tiempo:.3f}s)")
        return accion
 
    # play_game alterna los jugadores, dibuja el tablero final con display() y
    # devuelve la utilidad desde el punto de vista de X (el humano)
    resultado=None
    if hayHumano:
        print(  f"Iniciando partida interactiva: Humano ({jugador1 if empiezaHumano else jugador2}) vs "
                f"IA Alfa-Beta d={d} ({jugador2 if empiezaHumano else jugador1})...")
        resultado = juego.play_game(turno_humano, turno_ia) if empiezaHumano else juego.play_game(turno_ia, turno_humano)
    else:
        print(f"Iniciando partida entre IAs: IA1 ({jugador1}) vs IA2 ({jugador2}) con d={d}...")
        resultado = juego.play_game(turno_ia, turno_ia)
    if resultado > 0:
        print(f"¡Gana {jugador1} ({"Humano" if hayHumano and empiezaHumano else "IA"})!")
    elif resultado < 0:
        print(f"¡Gana {jugador2} ({"IA" if not hayHumano or empiezaHumano else "Humano"})!")
    else:
        print("¡Empate!")
#Fin de play_game

ejecutar_traza(7)

play_console_game(hayHumano=False, d=5)
play_console_game(d=5)