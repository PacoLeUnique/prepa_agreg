

def c(h : int, w : int):
    
    #Initialisation du cache
    cache = [[0] * (w+1) for _ in range(h+1)]

    for x in range(1, h+1):
        cache[x][1] = 1
    for y in range(1, w+1):
        cache[1][y] = 1

    def rec(h, w):
        if cache[h][w] == 0:
            cache[h][w] = rec(h, w-1) + rec(h-1, w)

        return cache[h][w]
    
    a = rec(h, w)
    for line in cache:
        print(line)
    return a
    

def exo5():
    a = c(2, 10)
    print(a)

exo5()
