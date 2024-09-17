students = [["Adam", 20], ["Adam", 14]]
students[1][1] = 20
x1 = students[0] == students[1]
x2 = students[0] is students[1]
x3 = id(students[0]) == id(students[1])
print(f"{x1=}, {x2=}, {x3=}")