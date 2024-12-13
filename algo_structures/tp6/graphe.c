#ifndef GRAPHE_
#define GRAPHE_
#include "graphe.h"
#include <stdio.h>
#endif

#include <stdlib.h>

/* Crée un graphe vide, sans arete. */
graphe cree_graphe(int n){
    graphe g;

    int** matrice = (int**) calloc(n, sizeof(int*));
    for (int i=0;i<n;i++)
        matrice[i] = (int*) calloc(n, sizeof(int));

    g.matrice_adj = matrice;
    g.nb_sommet = n;

    return g;
}

arete cree_arete(int i, int j, int poids){
    arete a;
    a.i = i;
    a.j = j;
    a.poids = poids;
    return a;
}

/* Ajoute l'arete (i,j) dans le grpahe. */
void ajoute_arete(graphe *g, arete a){
    g->matrice_adj[a.i][a.j] = a.poids;
    g->matrice_adj[a.j][a.i] = a.poids;
}

/* TODO : implanter les graphes orientés. */
graphe graphe_from_file(char filename[]){
    graphe g;
    int i, j, s1, s2, poids;
    char temp[4];

    FILE *f = fopen(filename, "r");
	fscanf(f, "%s", temp);
	// if(strcmp(temp, "oui") == 0)
	// 	g.oriente = true;
	// else
	// 	g.oriente = false;

    int nb_aretes;
	fscanf(f, "%d", &(g.nb_sommet));
	fscanf(f, "%d", &(nb_aretes));
    g.matrice_adj = (int **)malloc(g.nb_sommet *sizeof(int *));

    /* Init matrice d'adj */
    for(i=0;i<g.nb_sommet;i++)
		g.matrice_adj[i] = (int *)malloc(g.nb_sommet*sizeof(int));
	for(i=0; i<g.nb_sommet; i++)
		for(j=0; j<g.nb_sommet; j++)
			g.matrice_adj[i][j] = 0;

    for(i=0; i<nb_aretes; i++) {
		fscanf(f, "%d,%d:%d", &s1, &s2, &poids);
        ajoute_arete(&g, cree_arete(s1 - 1, s2 - 1, poids));
		// if(!g.oriente)
		// 	g.mat_adj[s2-1][s1-1] = val;
	}

	fclose(f);
    return g;
}