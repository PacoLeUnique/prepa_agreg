
SCM = list[int]
Pile = list[SCM]

"""Fusionne les listes triées t1 et t2 en une seule, triée aussi."""
def fusion(t1 : SCM, t2 : SCM) -> SCM:

    n1 : int = len(t1)
    n2 : int = len(t2)

    t : list[int] = []

    # Initialisation des indices
    i, j = 0, 0

    # On remplit t jusqu'à ce qu'on soit arrivé au bout d'une des 2 listes...
    while i != n1 and j != n2:
        if t1[i] < t2[j]:
            t.append(t1[i])
            i += 1
        else:
            t.append(t2[j])
            j += 1
    
    # ...Puis on ajoute le restant de l'autre.
    if j == n2:
        while i != n1:
            t.append(t1[i])
            i += 1
    else:
        while j != n2:
            t.append(t2[j])
            j += 1

    assert len(t) == n1 + n2
    return t        


""" Prend une liste de SCM, et renvoie la liste fusionnée triée,    
    en appliquant l'algorimthme TimSort simplifié.  """
def tim_sort_simplifie(sequences : list[SCM]) -> list[int]:
    
    pile : Pile = []

    #On empile chaque séquence, en appliquant les fusions intermédaires
    for sequence in sequences:
        pile.append(sequence)

        while len(pile) >= 2 and pile[-2] <= 2*pile[-1]:
            t0 = pile.pop()
            t1 = pile.pop()
            pile.append(fusion(t0,t1))

    # Une fois fini, on fusionne ce qu'il reste
    while len(pile) != 1:
        t0 = pile.pop()
        t1 = pile.pop()
        pile.append(fusion(t0, t1))

    # Le tableau final est au fond de la pile, on a plus qu'à le cueillir
    return pile.pop()