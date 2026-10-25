import searchEina
nuevePuzzle = searchEina.EightPuzzle((1,2,3,4,5,6,7,0,8))
threeSteps = searchEina.EightPuzzle((1, 2, 5, 3, 4, 0, 6, 7, 8))
nineSteps = searchEina.EightPuzzle((1, 4, 2, 7, 5, 8, 3, 0, 6))
thirtySteps = searchEina.EightPuzzle((0, 8, 7, 6, 5, 4, 3, 2, 1))


ANCHO = 17

def printAlgoritmo(nomAlgoritmo, dicts):
    linea = (nomAlgoritmo + "|").rjust(10)
    linea = linea + (str(dicts["profundidad"]) + "|").rjust(ANCHO)
    linea = linea + (str(dicts["expandidos"]) + "|").rjust(ANCHO)
    linea = linea + (str(dicts["qSize"]) + "|").rjust(ANCHO)
    linea = linea + (str(dicts["maxQS"]) + "|").rjust(ANCHO)
    linea = linea + (f"{dicts['tiempo']:.4f}|").rjust(ANCHO)
    linea = linea + (str(dicts["generados"]) + "|").rjust(ANCHO)
    print(linea)

cabecera = ("Problema|".rjust(10) + "Profundidad|".rjust(ANCHO) + "Expand|".rjust(ANCHO) + "Q.size|".rjust(ANCHO) + 
            "MaxQS|".rjust(ANCHO) + "Tiempo|".rjust(ANCHO) + "Generados|".rjust(ANCHO))
print(cabecera)
print("-" * (ANCHO * 7))
algoritmoNoPara = (("---|").rjust(ANCHO) + ("---|").rjust(ANCHO) + ("---|").rjust(ANCHO)
                     + ("---|").rjust(ANCHO) + ("---|").rjust(ANCHO) + ("---|").rjust(ANCHO))


solDict = searchEina.breadth_first_graph_search(threeSteps)
printAlgoritmo("BFS-G-3", solDict)
solDict = searchEina.breadth_first_tree_search(threeSteps)
printAlgoritmo("BFS-T-3", solDict)
solDict = searchEina.depth_first_graph_search(threeSteps)
printAlgoritmo("DFS-G-3", solDict)
#solDict = searchEina.depth_first_tree_search(threeSteps)
print(("DFS-T-3|").rjust(10) + algoritmoNoPara)
solDict = searchEina.depth_limited_search(threeSteps, 3)
printAlgoritmo("DLS-3-3", solDict)
solDict = searchEina.depth_limited_search(threeSteps, 9)
printAlgoritmo("DLS-9-3", solDict)
solDict = searchEina.iterative_deepening_search(threeSteps)
printAlgoritmo("IDS-3", solDict)
solDict = searchEina.uniform_cost_search(threeSteps)
printAlgoritmo("UCS-3", solDict)


solDict = searchEina.breadth_first_graph_search(nineSteps)
printAlgoritmo("BFS-G-9", solDict)
solDict = searchEina.breadth_first_tree_search(nineSteps)
printAlgoritmo("BFS-T-9", solDict)
solDict = searchEina.depth_first_graph_search(nineSteps)
printAlgoritmo("DFS-G-9", solDict)
#solDict = searchEina.depth_first_tree_search(nineSteps)
print(("DFS-T-9|").rjust(10) + algoritmoNoPara)
solDict = searchEina.depth_limited_search(nineSteps, 3)
printAlgoritmo("DLS-3-9", solDict)
solDict = searchEina.depth_limited_search(nineSteps, 9)
printAlgoritmo("DLS-9-9", solDict)
solDict = searchEina.iterative_deepening_search(nineSteps)
printAlgoritmo("IDS-9", solDict)
solDict = searchEina.uniform_cost_search(nineSteps)
printAlgoritmo("UCS-9", solDict)


solDict = searchEina.breadth_first_graph_search(thirtySteps)
printAlgoritmo("BFS-G-30", solDict)
#solDict = searchEina.breadth_first_tree_search(thirtySteps)
print(("BFS-T-30|").rjust(10) + algoritmoNoPara)
solDict = searchEina.depth_first_graph_search(thirtySteps)
printAlgoritmo("DFS-G-30", solDict)
#solDict = searchEina.depth_first_tree_search(thirtySteps)
print(("DFS-T-30|").rjust(10) + algoritmoNoPara)
solDict = searchEina.depth_limited_search(thirtySteps, 3)
printAlgoritmo("DLS-3-30", solDict)
solDict = searchEina.depth_limited_search(thirtySteps, 9)
printAlgoritmo("DLS-9-30", solDict)
#solDict = searchEina.iterative_deepening_search(thirtySteps)
print(("IDS-30|").rjust(10) + algoritmoNoPara)
solDict = searchEina.uniform_cost_search(thirtySteps)
printAlgoritmo("UCS-30", solDict)



