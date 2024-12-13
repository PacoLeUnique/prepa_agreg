import sys
from timsort_variante import *

def test_fusion():
    t1 = [1,1,3,8,9]
    t2 = [2,4,4,5,7,8,8,9,10]

    assert fusion(t1,t2) == [1,1,2,3,4,4,5,7,8,8,8,9,9,10]

    assert fusion([], []) == []
    assert fusion([], [1,2,3]) == [1,2,3]




def test_tim():
    sequences = [[2,4,10,12],[3,3,4],[1,1,4,15],[10,12,14]]

    assert tim_sort_simplifie(sequences) == [1,1,2,3,3,4,4,4,10,10,12,12,14,15]





#   > python timsort_test [nom_fnction]
if __name__ == '__main__':
    locals()[sys.argv[1]]()
    print("c'est tout bon")