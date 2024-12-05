parcours: main.o parcours_largeur.o file.o types_graphe.o
	gcc -o parcours main.o parcours_largeur.o file.o types_graphe.o

main.o: main.c parcours_largeur.h
	gcc -o main.o -c main.c 

dijkstra.o: dijkstra.c dijkstra.h
	gcc -o dijkstra.o -c dijkstra.c

parcours_largeur.o: parcours_largeur.c parcours_largeur.h
	gcc -o parcours_largeur.o -c parcours_largeur.c