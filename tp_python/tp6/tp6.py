from enum import Enum
from copy import deepcopy

# ============= 1. EXPRESSIONS REGULIERES ================

# 1.
class Op(Enum):
    EMPTY = 0
    EPSILON = 1
    LETTER = 2
    PLUS = 3
    TIMES = 4
    STAR = 5

# 2.
class Expression:
    """Définit une expression régulière."""

    def __init__(self, op : Op, *args : list["Expression"]):
        """Op : l'opération de l'expression, i.e EMPTY, PLUS, etc.
        
        args : les arguments nécessaires à chaque opération.
        à noter : args est de type list[Expression], sauf dans le cas où on a une LETTER, auquel cas c'est un str.

        """
        
        self.op : Op = op
        self.args : list[Expression] = args

    # 3.
    def __str__(self):
        match self.op:
            case Op.EMPTY:
                return "Ø"

            case Op.EPSILON:
                return "ε"
            
            #Précondition : len(self.args) = 0
            case Op.LETTER:  
                return self.args[0]
            
            #Précondition : len(self.args) >= 2
            case Op.PLUS:
                str_args = [str(arg) for arg in self.args]
                return "(" + " + ".join(str_args) + ")"
            
            #Précondition : len(self.args) >= 2
            case Op.TIMES:
                str_args = [str(arg) for arg in self.args]
                return "[" + "·".join(str_args) + "]"
            
            #Précondition : len(self.args) = 1
            case Op.STAR:
                expr : Expression = str(self.args[0])
                return f"{expr}*"
            

    # Juste parce que c'est pratique de pouvoir comparer 2 expressions régulières
    def __eq__(self, other: "Expression"):
        return (self.op == other.op
            and len(self.args) == len(other.args)
            and all(self.args[i] == other.args[i] for i in range(len(self.args))))



# 4. Constructeurs
def Letter(l : str) -> Expression:
    """Crée une expression ne contenant que la lettre l."""
    return Expression(Op.LETTER, l)

def Plus(*args : Expression) -> Expression:
    """Crée une expression avec des plus."""
    if len(args) == 0:  return Empty()
    if len(args) == 1:  return args[0]

    #Si 2 arguments sont égaux, on le supprime
    new_args = []
    for arg in args:
        if arg not in new_args:
            new_args.append(arg)

    return Expression(Op.PLUS, *new_args)

def Times(*args : Expression) -> Expression:
    """Crée une expression avec des times."""
    if len(args) == 0: return Epsilon()
    if len(args) == 1: return args[0]

    return Expression(Op.TIMES, *args)

def Empty() -> Expression:
    """Renvoie l'expression nulle."""
    return Expression(Op.EMPTY)

def Epsilon() -> Expression:
    """Renvoie le mot vide."""
    return Expression(Op.EPSILON)

def Star(arg : Expression) -> Expression:
    """Renvoie l'expression (arg)*."""
    return Expression(Op.STAR, arg)


def distribue(k : Expression, *termes : Expression) -> Expression:
    """Distribue l'expression k·(a+b+...+n) en l'expression k·a + k·b + ... k·n."""

    termes_distribues : list[Expression] = [Times(k, t) for t in termes]
    return Plus(*termes_distribues)


# 5.
def expand(e : Expression) -> Expression:
    """Simplifie et développe l'expression e."""

    match e.op:

        #Rien a faire
        case Op.EMPTY | Op.EPSILON | Op.LETTER:
            return e

        # 2 règles :
        #  1 :  ε*   --> ε
        #  2 :  Ø*   --> ε
        #  3 : (a*)* --> a*  
        case Op.STAR:
            a: Expression = e.args[0]
            a = expand(a)

            # règle 1
            if a.op == Op.EPSILON:
                return Epsilon()

            # règle 2
            if a.op == Op.EMPTY:
                return Epsilon()
            
            # règle 3
            if a.op == Op.STAR:
                return Star( (a.args[0]) )
            
            # Sinon, on continue la récurrence
            return Star(a)

        # 2 règles :
        #   1 : a + Ø --> a
        #   2 : a + (b+c) --> a+b+c
        case Op.PLUS:
            
            # 0. On expand récursivement
            args : list[Expression] = [expand(arg) for arg in e.args]

            # Règle 1 : on vire les empty
            args = [arg for arg in args if arg != Empty()]

            # Règle 2 : si on trouve un + dans les args, on l'ajoute dans new_args
            new_args : list[Expression] = []
            for arg in args:
                if arg.op == Op.PLUS:
                    new_args += arg.args
                else:
                    new_args.append(arg)
            
            # --> Une fois tout concaténé,et on renvoie la nouvelle liste
            return Plus(*(new_args))


        # 3 règles : 
        #   1 : a·Ø --> Ø   (multiplication par 0)
        #   2 : a·ε --> a   (multiplication par 1)
        #   3 : a·(b·c) --> a·b·c
        #   4 : a·(b+c) --> a·b + a·c 
        case Op.TIMES:

            # 0. On expand récursivement
            args : list[Expression] = [expand(arg) for arg in e.args]

            # Regle 1 : si y'a un empty, c'est cuit
            if Empty() in (arg for arg in e.args):
                return Empty()

            # Règle 2 : on vire les ε
            args = [arg for arg in args if arg != Epsilon()]

            # Règle 3 : si on trouve un · dans les args, on l'expand new_args
            new_args : list[Expression] = []
            for arg in args:
                if arg.op == Op.TIMES:
                    new_args += arg.args
                else:
                    new_args.append(arg)
    

            # Règle 4 : on distribue 
            # 1. On cherche le premier facteur +
            for i, arg in enumerate(new_args):
                if arg.op == Op.PLUS:

                    termes_distribues : Expression = [
                        expand(Times(*new_args[:i], a, *new_args[i+1: ]))
                        for a in arg.args
                    ]
                    return expand(Plus(*termes_distribues)) # Pour gérer le cas ((a+b) + (c+d))

            # Si on a pas de facteurs +, pas besoin de distribuer
            return Times(*new_args)


# ============ 2 . AUTOMATES ET CONVERSION ===============

Arete = tuple[int, str, int]
class Automaton:
    """Classe qui représente un automate.
    Il est de la forme Ä = (Q, A, E, I, F)."""

    #6.
    def __init__(self, Q : set[int], A : set[str], E : set[Arete], I : set[int], F : set[int]):
        self.Q : set[int] = Q
        self.A : set[str] = A
        self.E : set[Arete] = E
        self.I : set[int] = I
        self.F : set[int] = F

        n : int = len(Q)
        assert all((i+1 in Q) for i in range(n))    #Les états sont numérotés de 1 à n
        assert all( i in range(1,n+1) for i in I )  #Les états initiaux sont tous dans [1..n]
        assert all( f in range(1,n+1) for f in F )  #Les états finaux sont tous dans [1..n]

        assert all (                # Pour une transition p --a--> q :
                p in range(1, n+1)  # p doit etre dans [1..n]
            and q in range(1, n+1)  # q doit etre dans [1..n]
            and a in A              # a doit etre une lettre de l'alphabet
            for p, a, q in E)       


    def __eq__(self, other : "Automaton"):
        return (self.Q == other.Q
            and self.A == other.A
            and self.E == other.E
            and self.I == other.I
            and self.F == other.F)


    def __repr__(self):
        return f"Automate(Q:{self.Q}, A:{self.A}, E:{self.E}, I:{self.I}, F:{self.F})"

    #7.
    def K(self, p : int, q : int, r: int) -> Expression:
        """Renvoie l'expression régulière de toutes les transitions possibles de p-->q,
        en ne passant que par des états <= r."""

        if r == 0:
            lettres : list[str] = [Letter(a) for q1, a, q2 in self.E if p==q1 and q==q2]
            if p==q:  
                lettres.append(Epsilon())
            return Plus(*lettres)

        else:
            return Plus(self.K(p,q, r-1), Times(self.K(p,r, r-1), 
                                                Star(self.K(r,r, r-1)), 
                                                self.K(r,q, r-1)))

    #8.
    def expressionK(self) -> Expression:
        """Renvoie l'expression régulière de l'automate."""
        n = len(self.Q)
        return Plus(*[self.K(p,q,n)
                        for p in self.I
                        for q in self.F])

    #9.
    def normalize(self):
        """Normalise l'automate, c'est-a-dire lui laisser 1 seul état initial et 1 seul état final."""

        n = len(self.Q)
        i,f = n+1, n+2

        Q_ = self.Q | {i,f}
        I_ = {i}
        F_ = {f}
        E_ = (self.E 
            | {(i,a,q) for p,a,q in self.E if p in self.I}
            | {(p,a,f) for p,a,q in self.E if q in self.F}
            | {(i,a,f) for p,a,q in self.E if p in self.I and q in self.F}
        )

        self.Q = Q_
        self.I = I_
        self.F = F_
        self.E = E_


    # 10.
    def expressionN(self) -> Expression:
        """Calcule l'expression de l'automate avec la méthode par élimination d'états.
        
        Précondition : l'automate doit être normalisé.
        """

        A = deepcopy(self) # On utilise cette instance de travail pour éviter de modifier l'objet initial*
        
        n = len(A.Q)
        while(n > 2):

            q_enleve = n-2
            A.Q.remove(q_enleve) #On retire l'état n-2 (n-1 état initial, n état final)

            for (p,e,q) in A.E:
                if p == q_enleve or q == q_enleve:
                    A.E.remove()
                    #eh flemme c bon frrrrrr 
                else:




        


