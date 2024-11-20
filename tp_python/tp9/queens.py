from tp9 import *

# ============= 4 - Problème des reines =============

def queens(n):
    """Modélise le problèmes des n reines sur un échiquier n*n, sous forme de pb de logique."""

    # 1. on crée n² variables dans un tableau p[n][n]
    #    p[i][j] <==> il y a une reine dans la case (i,j)
    
    var_count = 1
    P : list[list[Var]] = [[None for _ in range(n)] for _ in range(n)] #Notre tableau de propositions

    for i in range(n):
        for j in range(n):
            P[i][j] = Var(var_count)
            var_count +=1


    # 2. On modélises les contraintes

