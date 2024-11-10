import sys

# ============== TP 7 ==============


# Partie 1 -- Recherche de point fixe, cas général 

# 1.
def admet_point_fixe(t : list[int]) -> bool:
    """Renvoie True si la liste t admet un point fixe.
    --> f(5) = 5  <==>   t[5] = 5
    """
    return any(t[i] == i for i in range(len(t)))

# 2.
def nb_points_fixes(t : list[int]) -> int:
    """Renvoie le nombre de points fixe de la fonction représentée par t."""
    return sum(1 for i in range(len(t)) if t[i] == i)


# 3.
def itere(t,x,k) -> int:
    """calcule f(f(f(f....f(x)))) (k fois)."""
    res = t[x]
    for _ in range(k):
        res = t[res]
    return res


# 4.
def nb_points_fixes_iteres(t, k) -> int:
    """Renvoie le nombre de points fixes de f^k(x)."""
    return sum(1 for i in range(len(t)) if itere(t,i,k) == i)


# 5.
def admet_attracteur_principal(t) -> bool:
    """Renvoie True si t admet un attracteur principal."""

    n = len(t)

    #on teste chaque valeur du tableau
    for i in range(n):
        
        # i doit etre un point fixe de t
        if t[i] != i:
            continue
        
        # pour tout x, on arrive a i en itérant suffisemment
        if all( any(itere(t,x,k) == i  for k in range(n)) 
                    for x in range(n)):
            return True
        
    return False


# 6.
def temps_de_convergence(t,x) -> int:
    """ Calcule le temps de convergence de f en x.
        Précondition : t admet un attracteur principal.
    """
    temps : int = 0
    while t[x] != x:
        x = t[x]
        temps += 1
    return temps


# 7.
def temps_de_convergence_max(t) -> int:
    """Calcule le temps de convergence maximum de f."""

    n = len(t)

    tps_convergence : list[int] = [0 for _ in range(n)]
    vus : list[bool] = [False for _ in range(n)]

    for i in range(n):
        if vus[i]:
            continue

        vus[i] = True
        current = i
        tps = 0
        chemin = [current]

        while t[current] != current or vus[t[current]] :
            tps += 1
            vus[current] = True






# Partie 2 -- Recherche efficace de points fixes

# 8. 
def est_croissante(t) -> bool:
    """Renvoie True si la fonction est croissante.
    En gros si la liste est triée.
    """

    if len(t) == 0:
        return True
    
    current = t[0]
    for elm in t:
        if elm < current : 
            return False
        current = elm
    return True


# 9.
def point_fixe(t) -> int:
    """ Renvoie un point fixe de t.
        Précondition : t est une fonction croissante.
    """

    # Juste au cas où
    assert est_croissante(t)
    
    def aux(d,g):
        if d > g: raise ValueError

        if d == g: return d

        m = (d+g)//2
        if t[m] == m:
            return m
        
        if t[m] < m: return aux(d, m-1)
        else:        return aux(m, g)
    
    return aux(0, len(t)-1)


# ---  3 - ordre de divisibilité  ---
def pgcd_points_fixes(t):
    """Renvoie le pgcd des points fixes de t."""
    for i 



# ==== TESTING ====
t = [1,3,5,7,9,1,3,5,7,9]
t2 = [5,5,2,2,0,2,2]
def exo1():
    assert admet_point_fixe(t)
    assert nb_points_fixes(t) == 1

def exo3():
    assert itere(t,0,0) == 1
    assert itere(t,0,1) == 3
    assert itere(t,0,2) == 7
    assert itere(t,0,3) == 5
    assert itere(t,0,4) == 1
    assert itere(t,0,5) == 3

    assert all(itere(t,9,i) == 9 for i in range(100))

def exo4():
    print(nb_points_fixes_iteres(t,0))
    print(nb_points_fixes_iteres(t,1))
    print(nb_points_fixes_iteres(t,2))
    print(nb_points_fixes_iteres(t,3))
    print(nb_points_fixes_iteres(t,4))
    print(nb_points_fixes_iteres(t,5))

def exo5():
    assert admet_attracteur_principal(t2)

def exo6():
    t2 = [5,5,2,2,0,2,2]
    assert temps_de_convergence(t2, 2) == 0
    
    assert temps_de_convergence(t2, 3) == 1
    assert temps_de_convergence(t2, 4) == 3

def exo8():
    t3 = [1,2,2,4,4,5]
    assert not est_croissante(t)
    assert not est_croissante(t2)
    assert est_croissante(t3)

def exo9():
    t4 = [1,3,3,5,5,5,7,7,7,8]
    assert point_fixe(t4) == 7


if __name__ == '__main__':
    locals()[sys.argv[1]]()