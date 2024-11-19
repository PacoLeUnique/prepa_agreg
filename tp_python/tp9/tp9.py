from itertools import product


# Exo 1.
Affecation = list[bool] #histoire de dire

class Formule:
    pass

class Var(Formule):
    def __init__(self, label:int):
        self.label : int = label

    def __str__(self):
        return str(self.label)
    def __repr__(self):
        return str(self.label)
    
    def __eq__(self, other):
        return (type(self) == type(other) 
            and self.label == other.label)

class Non(Formule):
    def __init__(self, φ:Formule):
        self.formule = φ

    def __str__(self):
        return f"¬({str(self.formule)})"
    
    def __repr__(self):
        return f"¬({str(self.formule)})"
    
    def __eq__(self, other):
        return (type(self) == type(other) 
            and self.formule == other.formule)
    

class Et(Formule):
    def __init__(self, *formules : list[Formule], flatten=True):
        assert all(isinstance(f, Formule) for f in formules)
        
        self.formules : list[Formule] = list(formules)
        if flatten:
            args = []
            for f in formules:
                if isinstance(f, Et):
                    args += [sf for sf in f.formules]
                else:
                    args += [f]
            self.formules = args


    def __str__(self):
        return f"Et({', '.join(str(f) for f in self.formules)})"
    def __repr__(self):
        return f"Et({', '.join(str(f) for f in self.formules)})"
    
    def __eq__(self, other):
        return (type(self) == type(other)
            and len(self.formules) == len(other.formules)
            and all(self.formules[i] == other.formules[i] for i in range(len(self.formules))))


class Ou(Formule):
    def __init__(self, *formules, flatten=True):
        assert all(isinstance(f, Formule) for f in formules)

        self.formules : list[Formule] = list(formules)
        if flatten:
            args = []
            for f in formules:
                if isinstance(f, Ou):
                    args += [sf for sf in f.formules]
                else:
                    args += [f]
            self.formules = args


    def __str__(self):
        return f"Ou({', '.join(str(f) for f in self.formules)})"
    def __repr__(self):
        return f"Ou({', '.join(str(f) for f in self.formules)})"

    def __eq__(self, other):
        return (type(self) == type(other)
            and len(self.formules) == len(other.formules)
            and all(self.formules[i] == other.formules[i] for i in range(len(self.formules))))



# Exo 2.
def max_var(f : Formule) -> int:
    match f:

        case Var():
            return f.label
        
        case Non():
            return max_var(f.formule)
        
        case Et() | Ou():
            return max(max_var(sf) for sf in f.formules)
        

def valeur_de_verite(f : Formule, I : Affecation) -> bool:
    """Donne la sémantique de f dans l'affectation I.
    En gros, calcule si f = V ou F."""

    if max_var(f) != len(I):
        raise ValueError(f"il y a {max_var(f)} variables, mais {len(I)} affectations")

    def eval(f : Formule) -> bool:
        match f:
            case Var():
                return I[f.label-1]
            
            case Non():
                return not eval(f.formule)
            
            case Et():
                return all(eval(sf) for sf in f.formules)
            
            case Ou():
                return any(eval(sf) for sf in f.formules)
            
    return eval(f)


# Exo 4.
def is_equiv(f : Formule, g : Formule) -> bool:
    """Renvoie vrai si f et g sont équivalentes."""

    vf : int = max_var(f)
    vg : int = max_var(g)

    # 1. On distingue la formule avec le + de variables de celle avec le moins

    f_min : Formule = f if vf < vg else g
    f_max : Formule = f if vf >= vg else g

    var_min : int = vf if vf < vg else vg
    var_max : int = vf if vf >= vg else vg

    affectations_min = product(*[[True, False] for i in range(var_min)])
    affectations_complementaires = product(*[[True, False] for i in range(var_max - var_min)])
    
    # 2. Pour chaque affectation min, on vérifie que ça check toutes les affectations pour les variables max
    for a_min in affectations_min:
        eval_min : bool = valeur_de_verite(f_min, list(a_min))
        
        for a_cmpl in affectations_complementaires:
            a_max : Affecation = list(a_min) + list(a_cmpl)
            eval_max : bool = valeur_de_verite(f_max, a_max)

            if eval_min != eval_max:
                return False
        
    return True



# ======= 2 - FORME NNF, CNF et clauses =======

# Exo 5.
def nnf(f : Formule) -> Formule:
    """Convertit une formule en forme NNF."""

    match f:
        
        case Var(): 
            return f 

        case Et():
            return Et(*(nnf(sf) for sf in f.formules))
        
        case Ou():
            return Ou(*(nnf(sf) for sf in f.formules))
        
        case Non():
            sf : Formule = f.formule
            match sf:
                case Non(): #Non(Non(p))
                    return nnf(sf.formule)   #On supprime les doubles négations 
                
                case Var(): #Non(p)
                    return f  

                case Et(): #Non(a ^ b) --> Ou(Non(a), Non(b))
                    return Ou(*(nnf(Non(ssf)) for ssf in sf.formules))
        
                case Ou(): #Non(a v b) --> Et(Non(a), Non(b))
                    return Et(*(nnf(Non(ssf)) for ssf in sf.formules))


# Exo 6.
def is_literal(f : Formule) -> bool:
    """Renvoie vrai si f est un littéral."""

    match f:
        case Var(): return True
        case Et() | Ou():  return False
        case Non():
            match f.formule:
                case Var(): return True
                case _ : return False

def is_clause(f : Formule) -> bool:
    """Renvoie vrai si f est une clause."""

    match f:
        case Var(): return True
        case Et(): return False
        case Non(): return is_literal(f)

        case Ou(): return all(is_literal(sf) for sf in f.formules)

def is_cnf(f : Formule) -> bool:
    """Renvoie vrai si f est sous forme CNF."""

    match f:
        case Var(): return True
        case Non(): return is_literal(f)
        case Ou():  return is_clause(f)

        case Et():  return all(is_clause(sf) for sf in f.formules)


# Exo 7.
def nb_litteraux(f : Formule) -> int:
    match f: 
        case Var(): return 1
        case Non(): return nb_litteraux(f.formule)
        case Ou() | Et(): return sum(nb_litteraux(sf) for sf in f.formules)

def width(f : Formule) -> int:
    """Renvoie la longueur max des clauses de f."""

    assert is_cnf(f)
    match f:
        case Var():   return 1
        case Non():   return 1
        case Ou():    return len(f.formules)
        case Et():    return max(nb_litteraux(sf) for sf in f.formules)



# 8. (Le maudit.)
def indice_et(formules : list[Formule]):
    """Renvoie l'indice du premier Et qu'on croise."""

    for i in range(len(formules)):
        if isinstance(formules[i], Et):
            return i
    return None

def cnf(f : Formule) -> Formule:
    """Convertit f sous forme CNF."""

    def aux(f):
        """La même chose, mais f est sous forme NNF."""

        match f:
            case Var() | Non(): return f

            case Et():  return Et(*(aux(sf) for sf in f.formules))

            case Ou():

                i = indice_et(f.formules) # i = l'indice du premier Et qu'on croise 
                if i is None:
                    return Ou(*(aux(sf) for sf in f.formules))
                else:
                    et_args : list[Formule] = [sf for sf in f.formules[i].formules]
                    return Et(*[aux(Ou(*([arg] + f.formules[:i] + f.formules[i+1:]))) for arg in et_args])

    return aux(nnf(f))


# Exo 9.
def list_of_clause(f : Formule) -> list[int]:
    """Renvoie la liste des valeurs de la clause.\n
    Exemple : Non(p1) v Non(p2) v p1 --> [-1, -2, 1]
    """

    assert is_clause(f)

    match f:
        case Var(): return [f.label]
        case Non(): return [-1 * f.formule.label]

        case Ou(): return [(sf.label if isinstance(sf, Var) else -1 * sf.formule.label) for sf in f.formules]


# Exo 10.
def list_of_list_of_cnf(f : Formule) -> list[list[int]]:
    """Renvoie la liste de liste de clauses de f.
    Précondition : f est en CNF.
    """

    assert is_cnf(f)

    match f:
        case Var() | Non() | Ou(): return [list_of_clause(f)]
        case Et(): return [list_of_clause(sf) for sf in f.formules]


# Exo 11.
def to_DIMACS(f : Formule) -> str:
    """Donne la chaine DIMACS d'une formule en CNF.
    
    Et( Ou(a,b), Ou(Non(b), c)) --->
        p cnf 3 2
        1 2 0
        -2 3 0
    """

    assert is_cnf(f)

    dimacs : str = ""
    clauses : list[list[Formule]] = list_of_list_of_cnf(f)

    # 1. l'en-tête
    x : int = max_var(f)   # Le nombres de variables
    y : int = len(clauses) # Le nombre de clauses
    dimacs += f"p cnf {str(x)} {str(y)}\n"

    # 2. les clauses
    for clause in clauses:
        dimacs += " ".join((str(litteral) for litteral in ( clause+[0] ))) + "\n"
    
    return dimacs[:-1] #c'est juste pour effacer le \n en trop à la fin


# ============== 3 - FORME DE TESITIN ==============

# Exo 13.
def binary_form(f : Formule):
    """Convertit f en forme binaire. Tous les Ou et le Et trop long, ça dégage."""

    match f:
        case Var(): return f
        
        case Non(): return Non(binary_form(f.formule))

        case Et():
            n = len(f.formules)
            if n > 2:
                return Et(binary_form(Et(*(sf for sf in f.formules[:n//2]), flatten=False)), binary_form(Et(*(sf for sf in f.formules[n//2:]), flatten=False)), flatten=False)
            else:
                return Et(*(binary_form(sf) for sf in f.formules), flatten=False)

        case Ou():
            n = len(f.formules)
            if n > 2:
                return Ou(binary_form(Ou(*(sf for sf in f.formules[:n//2]), flatten=False)), binary_form(Ou(*(sf for sf in f.formules[n//2:]), flatten=False)), flatten=False)
            else:
                return Ou(*((sf) for sf in f.formules), flatten=False)
            

# Exo 14.
def subformulas(f : Formule) -> list[Formule]:
    """Renvoie la liste des sous-formules de f."""

    match f:
        case Var(): return [f]
        case Non(): return [f] + subformulas(f.formule)
        case Et() | Ou():
            subforms = [f]
            for sf in f.formules:
                subforms += subformulas(sf)
            return subforms
        

# Exo 15.
