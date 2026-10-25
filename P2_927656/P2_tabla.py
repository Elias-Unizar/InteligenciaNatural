import searchEina
import tablaTools

ALGORITMOS = ["BFS", "IDS", "A*h(1)", "A*h(2)"]

ANCHO_D = 4      # ancho de la columna de profundidad
ANCHO_COL = 14    # ancho de cada columna de algoritmo




def imprimir_tabla(d_min=2, d_max=24):
    """
    Imprime por pantalla la tabla de nodos generados y b* por profundidad.

    obtener_resultados(d) -> dict {nombre_algoritmo: (nodos_generados, b_asterisco)}
    Si un algoritmo no tiene resultado para esa profundidad, puede faltar la clave
    o valer None (se imprime "---").
    """
    ancho_bloque = len(ALGORITMOS) * ANCHO_COL + (len(ALGORITMOS) - 1)
    ancho_total = 2 + ANCHO_D + 2 + ancho_bloque + 2 + ancho_bloque + 2
    lineaPunteada = "-" * ancho_total
        
    # Cabecera
    print(lineaPunteada)
    print(f"||{' ' * ANCHO_D}||{'Nodos Generados':^{ancho_bloque}}||{'b*':^{ancho_bloque}}||")    
    print(lineaPunteada)
    print(f"||" f"{'d':>{ANCHO_D}}" f"||"
          f"{"BFS":^{ANCHO_COL}}|" f"{"IDS":^{ANCHO_COL}}|" f"{"A*h1(1)":^{ANCHO_COL}}|" f"{"A*h(2)":^{ANCHO_COL}}" f"||"
          f"{"BFS":^{ANCHO_COL}}|" f"{"IDS":^{ANCHO_COL}}|" f"{"A*h1(1)":^{ANCHO_COL}}|" f"{"A*h(2)":^{ANCHO_COL}}" f"||")
    print(lineaPunteada)

    # Filas de datos
    ejecutarIDS = True
    nextejecutarIDS = True
    for d in range(d_min, d_max+1):
        nodosGeneradosTotal = {"BFS":0.0,"IDS":0.0,"A*1":0.0,"A*2":0.0}
        factorRamificacion = {"BFS":0.0,"IDS":0.0,"A*1":0.0,"A*2":0.0}
        listaProblemasProfundidad_d = tablaTools.calcularProblemas8Puzzle(d, 100)
        
        #
        #ALGORITMO BFSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        for i in listaProblemasProfundidad_d:
            solAlg = searchEina.breadth_first_graph_search(i)
            nodosGeneradosTotal["BFS"] += solAlg["generados"]
            if(solAlg["profundidad"] != d): print(f"{solAlg["profundidad"]} ERRRROOOOOOORBFS")
        nodosGeneradosTotal["BFS"] /= 100
        factorRamificacion["BFS"] = tablaTools.bissecion(1.00000001, 4, 0.0000001, d, nodosGeneradosTotal["BFS"]) #Para ahorrar ni que sea un minimo de rendimiento, esto en vez de hacerlo 100 veces y hacer la media, le pasamos
        #
        #ALGORITMO IDSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        
        if(ejecutarIDS): #Una vez que el IDS se ha acercado tanto a no ser optimo ya lo paramos las siguientes veces
            for i in listaProblemasProfundidad_d:
                solAlg = searchEina.iterative_deepening_search(i)
                nodosGeneradosTotal["IDS"] += solAlg["generados"]
                if(solAlg["profundidad"] != d): print(f"{solAlg["profundidad"]} ERRRROOOOOOORIDS")
            nodosGeneradosTotal["IDS"] /= 100
            factorRamificacion["IDS"] = tablaTools.bissecion(1.00000001, 4, 0.0000001, d, nodosGeneradosTotal["IDS"]) #Para ahorrar ni que sea un minimo de rendimiento, esto en vez de hacerlo 100 veces y hacer la media, le pasamos
            if(factorRamificacion["IDS"] > 2.65): nextejecutarIDS = False 
        else:#Ya dejamos de ejecutar IDS
            nodosGeneradosTotal["IDS"] = "---"
            factorRamificacion["IDS"] = "---"
        #
        #ALGORITMO A*ESTRELLLLLLLLLLLAAAAAAAAAAAAAAA
        for i in listaProblemasProfundidad_d:
            solAlg = searchEina.astar_search(i, i.h)
            nodosGeneradosTotal["A*1"] += solAlg["generados"]
            if(solAlg["profundidad"] != d): print(f"{solAlg["profundidad"]} ERRRROOOOOOORA1")
        nodosGeneradosTotal["A*1"] /= 100
        factorRamificacion["A*1"] = tablaTools.bissecion(1.00000001, 4, 0.0000001, d, nodosGeneradosTotal["A*1"]) #Para ahorrar ni que sea un minimo de rendimiento, esto en vez de hacerlo 100 veces y hacer la media, le pasamos
        #
        #ALGORITMO A********ESTRALLAAAAAAAAAA
        for i in listaProblemasProfundidad_d:
            solAlg = searchEina.astar_search(i, i.h_mahattan)
            nodosGeneradosTotal["A*2"] += solAlg["generados"]
            if(solAlg["profundidad"] != d): print(f"{solAlg["profundidad"]} ERRRROOOOOOORA2")
        nodosGeneradosTotal["A*2"] /= 100
        factorRamificacion["A*2"] = tablaTools.bissecion(1.00000001, 4, 0.0000001, d, nodosGeneradosTotal["A*2"]) #Para ahorrar ni que sea un minimo de rendimiento, esto en vez de hacerlo 100 veces y hacer la media, le pasamos
        
        nodos = []
        factores = []
        for nodosGen in nodosGeneradosTotal.values():
            nodos.append(f"{nodosGen:>{ANCHO_COL}}")
        for nombre, factor in factorRamificacion.items():
            if(not ejecutarIDS and nombre == "IDS"):
                factores.append(f"{factor:^{ANCHO_COL}}")
                continue
            factores.append(f"{factor:^{ANCHO_COL}.3f}")
        linea = f"||" f"{d:>{ANCHO_D}}" f"||"
        for i in range(nodos.__len__()):
            linea += (f"{nodos[i]:^{ANCHO_COL}}" f"|")
        for i in range(factores.__len__()):
            linea += (f"|" f"{factores[i]:^{ANCHO_COL}}")
        linea += f"||"
        print(linea)
        if (not nextejecutarIDS): ejecutarIDS = False
    print(lineaPunteada)


# Ejemplo de uso (tu función real sustituye a esta)
if __name__ == "__main__":
    imprimir_tabla(2,20)