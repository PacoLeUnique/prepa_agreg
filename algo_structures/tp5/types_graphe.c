#include "types_graphe.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int PAS_ARETE = 100000;

graphe_matriciel construire_graphe_matriciel(char nom_fichier[]) {
	graphe_matriciel g;
	int i, j, s1, s2, val;
	char temp[4];
	FILE *f = fopen(nom_fichier, "r");
	
	fscanf(f, "%s", temp);
	if(strcmp(temp, "oui") == 0)
		g.oriente = true;
	else
		g.oriente = false;
	fscanf(f, "%d", &(g.nb_sommets));
	fscanf(f, "%d", &(g.nb_aretes));
	g.mat_adj = (int **)malloc(g.nb_sommets*sizeof(int *));
	for(i=0;i<g.nb_sommets;i++)
		g.mat_adj[i] = (int *)malloc(g.nb_sommets*sizeof(int));
	for(i=0;i<g.nb_sommets;i++)
		for(j=0;j<g.nb_sommets;j++)
			g.mat_adj[i][j] = PAS_ARETE;
	for(i=0;i<g.nb_aretes;i++) {
		fscanf(f, "%d,%d:%d", &s1, &s2, &val);
		g.mat_adj[s1-1][s2-1] = val;
		if(!g.oriente)
			g.mat_adj[s2-1][s1-1] = val;
	}
	fclose(f);
	return g;
}

graphe_avec_listes construire_graphe_avec_listes(char nom_fichier[]) {
	graphe_avec_listes g;
	int i, s1, s2, val;
	char str_temp[4];
	sommet *temp;
	FILE *f = fopen(nom_fichier, "r");	
	
	fscanf(f, "%s", str_temp);
	if(strcmp(str_temp, "oui") == 0)
		g.oriente = true;
	else
		g.oriente = false;
	fscanf(f, "%d", &(g.nb_sommets));
	fscanf(f, "%d", &(g.nb_aretes));
	g.tab_listes_adjacence = (sommet **)malloc(g.nb_sommets*sizeof(sommet *));
	for(i=0;i<g.nb_sommets;i++)
		g.tab_listes_adjacence[i] = NULL;
	for(i=0;i<g.nb_aretes;i++) {
		fscanf(f, "%d,%d:%d", &s1, &s2, &val);
		temp = g.tab_listes_adjacence[s1-1];
		g.tab_listes_adjacence[s1-1] = (sommet *)malloc(sizeof(sommet));
		g.tab_listes_adjacence[s1-1]->numero = s2;
		g.tab_listes_adjacence[s1-1]->valeur = val;
		g.tab_listes_adjacence[s1-1]->sommet_suivant = temp;
		if(!g.oriente) {
			temp = g.tab_listes_adjacence[s2-1];
			g.tab_listes_adjacence[s2-1] = (sommet *)malloc(sizeof(sommet));
			g.tab_listes_adjacence[s2-1]->numero = s1;
			g.tab_listes_adjacence[s2-1]->valeur = val;
			g.tab_listes_adjacence[s2-1]->sommet_suivant = temp;
		}
	}
	fclose(f);
	return g;
}
