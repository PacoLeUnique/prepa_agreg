from tp6 import *
import sys

a = Letter("a")
b = Letter("b")
c = Letter("c")
d = Letter("d")
#Pas de e pour éviter la confusion avec expression/epsilon
f = Letter("f")


def test_eq():
    """Teste si l'égalité entre expression marche bien."""

    assert (Epsilon() == Epsilon())
    assert (Empty() == Empty())
    assert (Letter("a") == Letter("a"))
    assert (Letter("a") != Letter("f"))

    a = Letter("a")
    b = Letter("b")

    e1 = Plus(a, Times(a, b), Star(a))
    e2 = Plus(Letter("a"), Times(Letter("a"), Letter("b")), Star(Letter("a")))
    e3 = Plus(a, a, Star(a))
    
    assert e1 == e2
    assert e2 != e3

    print("test passés :D")


def test_distrib():
    k = Letter("k")
    e = Times(k, Plus(a, b), Plus(b,a,b))
    
    e2 = distribue(Plus(a, b), a, b, k)
    print(e2)


def question3():
    #On crée l'expression (b + ab*a)*

    a = Expression(Op.LETTER, "a")
    b = Expression(Op.LETTER, "b")

    b_star = Expression(Op.STAR, b)
    aba = Expression(Op.TIMES, a, b_star, a)
    b_aba = Expression(Op.PLUS, b, aba)

    expr = Expression(Op.STAR, b_aba)

    print(expr)


def question4():
    #On crée l'expression (b + ab*a)*
    a = Letter("a")
    b = Letter("b")

    expr : Expression = Star(Plus( b , Times(a, Star(b), a) ))
    print(expr)


def question5():
    a = Letter("a")
    b = Letter("b")

    #Test flattening : a+ (b+c) = a+b+c
    print("test flattening...")
    e1 = Plus(a, Times(b,a), Plus(b, Star(a)))
    e2 = Plus(a, Times(b,a), b, Star(a))
    
    assert expand(e1) == e2
    print("flattening OK.")

    #Test idempotence a**
    print("test idempotence...")
    e3 = Plus( Star(Star(a)), b, Star(Star( Plus(a,b) ))  )
    e4 = Plus( Star(a), b, Star(Plus(a,b)) )

    assert expand(e3) == e4
    print("idempotence OK.")


    print("Test multiplication par zéro...")
    e = Times( a, b, b, Plus(a, b), Empty(), Star(Epsilon()) )
    assert expand(e) == Empty()
    print("OK.")

    print("Test distrib....")
    e = Times(Plus(b,c), Plus(d,f), a)
    e2 = Plus(Times(b,d,a), Times(b,f,a), Times(c,d,a), Times(c,f,a))
    print(expand(e))
    assert expand(e) == e2

    e3 = Times(a, Plus(b,c))
    print(expand(e3))
    assert expand(e3) == Plus(Times(a,b), Times(a,c))
    
    e4 = Times(a, Plus(b, Epsilon()), Epsilon())
    print(expand(e4))
    assert expand(e4) == Plus(Times(a,b), a)

    e5 = Times(a, Plus(Star(b),c))
    print(expand(e5))
    assert expand(e5) == Plus(Times(a,Star(b)), Times(a,c))
    print("OK.")

    print("test 3star...")
    e6 = Star(Star(Star(a)))
    assert expand(e6) == Star(a)
    print("Test 3-star OK")


    print("Tests du prof....")
    assert expand(Times(Plus(a,b), Plus(c,d), Empty())) == Empty()

    assert expand(Star(Star(Star(Times(a,b))))) == Star(Times(a,b))
    assert expand(Star(Times(Plus(a,b,c) ,d))) == Star(Plus(Times(a,d), Times(b,d), Times(c,d)))
    
    e7 = Times(Plus(a,b), Plus(c, Epsilon()))
    print(expand(e7))
    assert expand(e7) == Plus(Times(a,c), a, Times(b,c), b)
    print("Tests OK.")


# ================ AUTOMATES =============
A = {"a", "b"}

def question6():

    print("Création d'un automate qui marche...")

    Q = [1,2]
    I = [1]
    F = [2]
    E = [(1,"b",2), (1,"a",2), (2,"a",2), (2,"b",1)]

    automate = Automaton(Q,A,E,I,F)
    print("ça marche bien.")

#Pour la suite, voici des automates
a_star = Automaton({1}, A, {(1,"a",1)}, {1}, {1})
ab = Automaton({1,2}, A, {(1,"a",2), (2,"b",1)}, {1}, {2})
a_impair = Automaton({1,2}, A, {(1,"a",2), (1,"b",1), (2,"a",1), (2,"b",2)}, {1}, {2})

def question7():

    print(a_star.K(1,1,1))
    print(expand(ab.K(1,2,2)))
    print(a_impair.K(1,2,2))


def question8():
    print(a_star.expressionK())
    print(expand(ab.expressionK()))
    print(a_impair.expressionK())


def question9():
    a_star.normalize()
    a_impair.normalize()

    assert a_star == Automaton({1,2,3}, A, {(1,"a",1),(2,"a",1),(1,"a",3),(2,"a",3)}, {2}, {3})
    assert a_impair == Automaton({1,2,3,4}, A, {(1,"b",1),(1,"a",2),(2,"b",2),(2,"a",1),
                                                (3,"b",1),(3,"a",2),(1,"a",4),(2,"b",4),(3,"a",4)}, {3}, {4})

    print("normalisation okayyyyyy")


# > python3 test.py exo1
if __name__ == '__main__':
    globals()[sys.argv[1]]()
