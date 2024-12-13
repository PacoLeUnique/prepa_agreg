CC= gcc

kruskal: main.o kruskal.o graphe.o tas.o
	$(CC) -o kruskal main.o kruskal.o graphe.o tas.o

main.o: main.c
	$(CC) -c main.c

kruskal.o: kruskal.c kruskal.h
	$(CC) -c kruskal.c

graphe.o: graphe.c graphe.h
	$(CC) -c graphe.c

tas.o: tas.c tas.h
	$(CC) -c tas.c

union_find.o: union_find.c union_find.h
	$(CC) -c union_find.c

clean:
	rm -f *.o kruskal