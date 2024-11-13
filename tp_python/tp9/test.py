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

def exo8():
    pass


if __name__ == '__main__':
    globals()[sys.argv[1]]()
    print(f"Test {sys.argv[1]} tout bon")