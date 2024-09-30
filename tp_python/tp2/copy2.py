l1 = [1, [2,3,4], (7,8,9)]
l2 = [x for x in l1]
l1[1].append(5)
l1[2] += (10,11)
print(l2)