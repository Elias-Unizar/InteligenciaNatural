import searchEina

class Canibals(searchEina.Problem):
    """ El problema favorito de los exploradores de los Andes y de Hanibal Lecter """

    def __init__(self, initial, goal=(0,0,1,3,3)):
        """ tupla (C_izq, M_izq, Bote, C_der, M_der) """
        """ Objetivo del problema es tener a tanto los misioneros como canibales en el lado derecho, el barco da igual,
            pero al tener que definir solo 1 estado final lo pongo en la orilla derecha, el momento de dejar a los ultimos pasajeros"""
        super().__init__(initial, goal)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['1C', '2C', '1M', '2M', '1C1M']
        alternadorDeOrilla = 3*state[2] #Asi en funcion de donde esta el barco, sabe a que orilla no puede mover canibales/misioneros0
        #No materializar personas de la nada
        if state[0+alternadorDeOrilla] < 2: possible_actions.remove('2C')
        if state[0+alternadorDeOrilla] < 1: 
            possible_actions.remove('1C1M')
            possible_actions.remove('1C')
        if state[1+alternadorDeOrilla] < 2: possible_actions.remove('2M')
        if state[1+alternadorDeOrilla] < 1: 
            possible_actions.remove('1C1M')
            possible_actions.remove('1M')
        #Ahora si, que no se maten entre ellos en mi orilla, pero si saco a todos los misioneros daria igual
        if (state[0+alternadorDeOrilla] > state[1+alternadorDeOrilla] - 2) and (state[1+alternadorDeOrilla] > 2): 
            if '2M' in possible_actions: possible_actions.remove('2M')
        if (state[0+alternadorDeOrilla] > state[1+alternadorDeOrilla] - 1) and (state[1+alternadorDeOrilla] > 1): 
            if '1M' in possible_actions: possible_actions.remove('1M')
        #Ahora que no se maten en la otra orilla
        if(state[4-alternadorDeOrilla] != 0): #Si no hay misioneros al otro lado, daria igual cuantos canibales se envian
            if state[3-alternadorDeOrilla] + 2 > state[4-alternadorDeOrilla]: 
                if '2C' in possible_actions: possible_actions.remove('2C')
            if state[3-alternadorDeOrilla] + 1 > state[4-alternadorDeOrilla]: 
                if '1C' in possible_actions: possible_actions.remove('1C')
        else: #Hay 0 misioneros en la otra orilla
            if state[3-alternadorDeOrilla] > 0: 
                if '1C1M' in possible_actions: possible_actions.remove('1C1M')
            if state[3-alternadorDeOrilla] > 1: 
                if '1M' in possible_actions: possible_actions.remove('1M')
            if state[3-alternadorDeOrilla] > 2: 
                if '2M' in possible_actions: possible_actions.remove('2M')
            
        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """
        new_state = list(state)
        alternadorDeOrilla = 3*state[2]
        new_state[2] = (new_state[2] + 1) % 2
        match action:
            case '2M':
                new_state[1+alternadorDeOrilla] -= 2
                new_state[4-alternadorDeOrilla] += 2
            case '1M':
                new_state[1+alternadorDeOrilla] -= 1
                new_state[4-alternadorDeOrilla] += 1                
            case '1C1M':
                new_state[1+alternadorDeOrilla] -= 1
                new_state[4-alternadorDeOrilla] += 1
                new_state[0+alternadorDeOrilla] -= 1
                new_state[3-alternadorDeOrilla] += 1
            case '1C':
                new_state[0+alternadorDeOrilla] -= 1
                new_state[3-alternadorDeOrilla] += 1                
            case '2C':
                new_state[0+alternadorDeOrilla] -= 2
                new_state[3-alternadorDeOrilla] += 2                
                
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

def print_state(state):
    """ Ejemplo de ejecución:
         RIBERA-IZQ M M M C BOTE --RIO-- C C RIBERA-DCH
    """
    return (f"RIBERA-IZQ {"M " * state[1]}{"C " * state[0]}" #Orilla IZquierda
          f"{'BOTE --RIO-- ' if state[2] == 0 else '--RIO-- BOTE '}"#Posicion Bote
          f"{"M " * state[4]}{"C " * state[3]}RIBERA-DCHA")
    
def imprimirSolucion(nodoSolucion):
    for nodo in nodoSolucion.path():
        lineaNodo = f"|" + print_state(nodo.state)
        if(nodo.action != None):
            lineaNodo = f"{nodo.action:^8}" + lineaNodo
        else:
            lineaNodo = f"{" " * 8}" + lineaNodo
        print(lineaNodo)

solDict = searchEina.breadth_first_graph_search(Canibals((3,3,0,0,0)))
imprimirSolucion(solDict["nodo"])
    