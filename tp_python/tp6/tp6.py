from enum import Enum


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
                return f"({expr})*"
            

    # Juste parce que c'est pratique de pouvoir comparer 2 expressions régulières
    def __eq__(self, other: "Expression"):
        match self.op:
            case Op.EMPTY:
                return other.op == Op.EMPTY

            case Op.EPSILON:
                return other.op == Op.EPSILON
            
            case Op.LETTER:
                return (other.op == Op.LETTER
                    and self.args[0] == other.args[0])

            case Op.PLUS:
                return (other.op == Op.PLUS 
                    and len(self.args) == len(other.args)
                    and all(self.args[i] == other.args[i] for i in range(len(self.args))))

            case Op.TIMES:
                return (other.op == Op.TIMES 
                    and len(self.args) == len(other.args)
                    and all(self.args[i] == other.args[i] for i in range(len(self.args))))

            case Op.STAR:
                if other.op != Op.STAR:
                    return False
                return self.args[0] == other.args[0]
            

# 4. Constructeurs
def Letter(l : str) -> Expression:
    """Crée une expression ne contenant que la lettre l."""
    return Expression(Op.LETTER, l)

def Plus(*args : Expression) -> Expression:
    """Crée une expression avec des plus."""
    assert len(args) >= 2
    return Expression(Op.PLUS, *args)

def Times(*args : Expression) -> Expression:
    """Crée une expression avec des times."""
    assert len(args) >= 2
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
    """Distribue l'expression k·(a+b+...+n) en l'expression k·a + k·b + ... k·n.
    """

    termes_distribues : list[Expression] = [Times(k, t) for t in termes]
    return Plus(*termes_distribues)


# 5.
def expand(e : Expression) -> Expression:
    """Simplifie et développe l'expression e."""

    match e.op:

        #Rien a faire
        case Op.EMPTY:
            return e
        
        #Rien a faire non plus
        case Op.EPSILON:
            return e
        
        #Toujours rien pour l'instant
        case Op.LETTER:
            return e

        # 2 règles :
        #  1 : (a*)* --> a*  
        #  2 :  Ø*   --> ε
        case Op.STAR:
            a: Expression = e.args[0]
            
            # règle 1
            if a.op == Op.STAR:
                return Star( expand(a.args[0]) )

            #règle 2
            elif a.op == Op.EMPTY:
                return Epsilon()
            
            # Sinon, on continue la récurrence
            return Star( expand(a) )

        # 2 règles :
        #   1 : a + Ø --> a
        #   2 : a + (b+c) --> a+b+c
        case Op.PLUS:
            
            # Règle 1 : on vire les empty, et on expand récursivement
            args : list[Expression] = [expand(arg) for arg in e.args if arg != Empty()]

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

            # Regle 1 : si y'a un empty, c'est cuit
            if Empty() in (arg for arg in e.args):
                return Empty()

            # Règle 2 : on vire les ε
            args : list[Expression] = [arg for arg in e.args if arg != Epsilon()]

            # Règle 3 : si on trouve un · dans les args, on l'expand new_args
            new_args : list[Expression] = []
            for arg in args:
                if arg.op == Op.TIMES:
                    new_args += arg.args
                else:
                    new_args.append(arg)
            
            # Si, après simplification, il nous reste rien, pas besoin de distribuer
            n : int = len(new_args)
            if n == 0: return Epsilon()            # ε·ε --> ε   
            if n == 1: return expand(new_args[0])  # Times(a) --> a

            # Règle 4 : on distribue 
            # 1. On cherche le premier facteur +
            for i, arg in enumerate(new_args):
                if arg.op == Op.PLUS:
                    # 2. On distribue le plus sur tout le reste
            
                    # On extrait les termes à distribuer...
                    termes : list[Expression] = arg.args
                    if n == 2:
                        k = new_args[0] if i == 1 else new_args[1]
                    else:
                        k = (Times(*[ new_args[j] for j in range(len(new_args)) if j!=i ]))

                    # ... et on distribue
                    e_distribuee = distribue(k, *termes) 

                    # 3. Expand recursivement les nouveaux termes
                    new_args = [arg for arg in e_distribuee.args]
                    return expand(Plus(*new_args))  #le expand est ici pour éviter le cas ((a+b) + (c+d)) 


            # Si on a pas de facteurs +, pas besoin de distribuer 
            new_args = [expand(arg) for arg in new_args]
            return Times(*new_args)


# ============ 2 . AUTOMATES ET CONVERSION ===============

# 6.
class Automaton:
    """Classe qui représente un automate.
    Il est de la forme Ä = (Q, A, E, I, F)."""

    def __init__(Q : list[int], A ):
        pass