import sys
from tp9 import *

a = Var(1)
b = Var(2)
c = Var(3)
d = Var(4)
e = Var(5)

def exo1():
    f = Non(a)
    f2 = Et(Ou(a, Non(b)), b, c)
    f3 = Non(Ou(a,b,b,b,Non(Et(c, Non(c)))))

    print(str(f))
    print(f2)
    print(f3)

def exo2():

    f = a
    f2 = Et(Ou(a,a), a)
    f3 = Ou(b, Non(e), c, Et(d, a))

    assert max_var(f) == 1
    assert max_var(f2) == 1
    assert max_var(f3) == 5


def exo3():
    f = a
    f2 = Non(Non(a))
    f3 = Et(Ou(a,b), c, d)

    assert valeur_de_verite(f, [True])
    assert valeur_de_verite(f2, [True])
    assert not valeur_de_verite(f, [False])

    assert valeur_de_verite(f3, [True, False, True, True])
    assert not valeur_de_verite(f3, [False, False, True, True])


def exo4():
    f = a
    g = Non(Non(a))
    g2 = Et(a, Ou(b, Non(b)))

    assert is_equiv(f, g)
    assert not is_equiv(f, Non(g))

    assert is_equiv(f, g2)
    assert is_equiv(Non(Ou(a,b)), Et(Non(b), Non(a)))


# ===== NNF, CNF, clauses =====
def exo5():
    f = Non(Non(a))
    f2 = Ou(Non( Ou(Non( Ou(Non(a), b)), a)),   a)

    print(nnf(f))
    print(nnf(f2))

def exo6():

    assert is_literal(Non(a))
    assert is_literal(b)
    assert not is_literal(Non(Et(a,b)))

    assert not is_clause(Non(Et(a,b)))
    assert is_clause(Ou(a,b, Non(b), Non(c), e))
    assert not is_clause(Ou(a,b, Et(b, c), Non(c), e))
    
    assert not is_cnf(Ou(a,b, Et(b, c), Non(c), e))
    assert is_cnf(Et(a, Ou(b,Non(d)), Ou(b, c), Non(c), e))

    """!!!!! ATTENTION !!!!!!   Et(Et(a,b), c) n'est PAS considéré comme une forme CNF.
                                Pareil pour Ou(Ou(a,b), c), c'est pas une clause."""


def exo7():
    f = a
    f2 = Ou(Non(a), b, Non(b))
    f3 = Et(Ou(a, Non(a)), b, Non(c),  Ou(b, Non(b), b, Non(e)), Ou(Non(c), c))

    assert width(f) == 1
    assert width(f2) == 3
    assert width(f3) == 4


def flatten():
    f = Et(a, Et(b, c), a)
    f2 = f = Et(a, Et(b, Et(c,d)), a)
    
    print(f)
    print(f2)


def exo8():
    f = Non(Et(a,b))
    f2 = Non(Et(Ou(Non(a),Non(b)), Ou(Non(c),Non(d))))
    f3 = Non(Et(Ou(a,b), Ou(c,d)))

    f4 = Ou(Et(Non(a), b, Non(Et(Non(Ou(a,Et(e,e,Non(a)))), b, e, e))))

    print(cnf(f))
    print(cnf(f2))
    print(cnf(f3))

    assert is_cnf(cnf(f))
    assert is_cnf(cnf(f2))
    assert is_cnf(cnf(f3))
    assert is_cnf(cnf(f4))


def exo9():
    f = Non(c)
    f2 = Ou(a,b,a, Non(e))

    assert list_of_clause(f) == [-3]
    assert list_of_clause(f2) == [1,2,1,-5]

def exo10():
    f = Ou(a,b,a, Non(e))    
    f2 = Et(Ou(c, Non(a)), Ou(d, a, Non(c)), Ou(Non(c), b), Ou(Non(d), Non(b)))
    f3 = a

    assert list_of_list_of_cnf(f) == [[1,2,1,-5]]
    assert list_of_list_of_cnf(f2) == [[3,-1],[4,1,-3],[-3,2],[-4,-2]]
    assert list_of_list_of_cnf(f3) == [[1]]


def exo11():
    f = Non(a)
    f2 = Et(Ou(a,b), Ou(Non(b), c))

    #print(to_DIMACS(f2))
    assert to_DIMACS(f) == "p cnf 1 1\n-1 0"
    assert to_DIMACS(f2) == "p cnf 3 2\n1 2 0\n-2 3 0"


# 3 - Forme de Tseitin

def exo13():
    f = Ou(a,b,c,d,e,d,c,b,a)
    f2 = Et(a,a,Non(a), Ou(b,b,Non(b), Non(b), b), a, a, Non(a))

    print(binary_form(f))
    print(binary_form(f2))

def exo14():
    f = Et(Ou(a, Non(b)))
    f2 = Non(Non(Non(a)))

    assert(subformulas(f)) == [Et(Ou(a, Non(b))), Ou(a, Non(b)), a, Non(b), b]
    assert subformulas(f2) == [f2, Non(Non(a)), Non(a), a]




if __name__ == '__main__':
    globals()[sys.argv[1]]()
    print(f"Test {sys.argv[1]} tout bon")