from itertools import combinations

S = [0,2,1,4 ]
E = [3,5,3,10]
V = [2,5,10,8]

# ======== EXO 6 - PLANIFICATION DES TACHES =========
Plan = list[int] #Contient les i tq si i est dans la liste, la tache d'indice i est sélectionnée

def valeur_plan(p : Plan) -> int:
    """Donne la valeur d'un plan possible.
    Précondition : p doit etre un plan possible."""

    s : int = 0
    for i in p:
        sum += V[i]
    return s


def is_possible(p : Plan) -> bool:
    """Renvoie True si le plan est un plan possible."""

    pass



def max_plan_naif(S : list[int], E : list[int], V : list[int]) -> Plan:
    """Teste tous les plans possibles, et renvoie celui avec la meilleure valeur.
       Bref, une bonne complexité exponentielle, en somme.
    """

    assert len(S) == len(E) == len(V)
    n : int = len(S)

    #Init toutes les permutations possibles
    plans : list[Plan] = []
    for i in range(1, n+1):
        plans += list(combinations(range(n), i))
    
    pass #TODO


def max_plan_dyn(S, E, V):
    """On procède de manière dynamique, cette fois."""

    n : int = len(S)

    #On regroup les données en un triplet, et on les trie par temps de début (S)
    taches : list[tuple[int, int, int]] = [(S[i], E[i], V[i]) for i in n].sort(key= lambda x:x[0])

    cache = [-1] * n

    def aux(i : int):
        """Renvoie la valeur max, si on prend que les taches i ou plus."""

        # Si i >= n, on ne peut prendre aucune tache, donc c'est 0
        if i >= n: return 0

        #Sinon, 2 choix : 
        # - On execute la tache i, auquel cas v = V[i] + la val max du prochain i disponible,
        # - On execute pas i,      auquel cas v = val_max(i+1).

        next_temps_dispo : int = taches[i][1]
        j : int = i
        while (j < n) and (taches[j][0] < next_temps_dispo):
            j += 1

        return max(taches[i][2] + aux(j), aux(i+1))

    return aux(0)


def exo6():
    max_plan_naif(S,E,V)

exo6()

    
