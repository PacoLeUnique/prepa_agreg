from tp6 import *
import sys

a = Letter("a")
b = Letter("b")
c = Letter("c")
d = Letter("d")
#Pas de e pour éviter la confusion avec expression
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
    e2 = Plus(Times(a,b,d), Times(a,b,f), Times(a,c,d), Times(a,c,f))
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




# > python3 test.py exo1
if __name__ == '__main__':
    globals()[sys.argv[1]]()
