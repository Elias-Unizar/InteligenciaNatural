import random
import searchEina

def bissecion(a,b,error,d,g):
    """
    Funcion bissecion
    Args:
        a,b : Limites iniciales de la biseción
        error: Maximo error para considerar una solución
        d: Profundidad
        g: Numero de nodos Generados
    """
    def f(b, depth, gen):
        return ((b * (1 - b ** depth) / (1 - b)) - gen)
    m = 0.0
    if f(a,d,g)*f(b,d,g) > 0:
        print("no raiz")
        return -1
    else:
        m = (a+b)/2.0
        while(abs(a-b)>=error):
            if f(a,d,g)*f(m,d,g) > 0:
                a = m
            elif f(b,d,g)*f(m,d,g) > 0:
                b = m
            m = (a+b)/2.0
        return m


def calcularInicioAleatorio8Puzzle():
    estadoInicial = list((0,1,2,3,4,5,6,7,8))
    random.shuffle(estadoInicial)
    return estadoInicial

def calcularDestino(index_hueco):
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    if index_hueco % 3 == 0:
        possible_actions.remove('LEFT')
    if index_hueco < 3:
        possible_actions.remove('UP')
    if index_hueco % 3 == 2:
        possible_actions.remove('RIGHT')
    if index_hueco > 5:
        possible_actions.remove('DOWN')
    action = random.choice(possible_actions)

    delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
    destino = index_hueco + delta[action]
    return destino

def calcularSiguienteEstado(estadoExplorados, posHueco, estadoIni):
    while True:
        nuevoEstado = list(estadoIni)
        piezaAMover = calcularDestino(posHueco)
        nuevoEstado[piezaAMover], nuevoEstado[posHueco] = nuevoEstado[posHueco], nuevoEstado[piezaAMover]
        preLen = estadoExplorados.__len__()
        estadoExplorados.add(tuple(nuevoEstado))
        if (preLen != estadoExplorados.__len__()):
#           print(tuple(nuevoEstado))
            return nuevoEstado, piezaAMover
#           print(f"{tuple(nuevoEstado)} Fallo")


def calcularFinAXPasos(depth, ini):
    estadoAct = list(ini)
    posHueco = estadoAct.index(0)
    estadoExplorados = set()
    estadoExplorados.add(tuple(estadoAct))
#    print("\n\n Problema nuevo: \n" + f"{tuple(ini)}")
    i = 0
    while i < depth:
        nuevoEstado, posHueco = calcularSiguienteEstado(estadoExplorados, posHueco, estadoAct)
        if (i == depth//2 and
            searchEina.breadth_first_graph_search(searchEina.EightPuzzle(tuple(ini), tuple(nuevoEstado)))["profundidad"] != i+1): return False, None
        i += 1
        estadoAct = nuevoEstado
    return True, estadoAct


def calcularProblemas8Puzzle(d, cant):
    listaProblemas = []
    i = 0
    while i < cant:
        estadoIni = calcularInicioAleatorio8Puzzle()
        esValido, estadoFin = calcularFinAXPasos(d, estadoIni)
        if esValido == True: 
            problema = searchEina.EightPuzzle(tuple(estadoIni), tuple(estadoFin))
            if searchEina.breadth_first_graph_search(problema)["profundidad"] == d:
                listaProblemas.append(problema)
                i += 1
    return listaProblemas