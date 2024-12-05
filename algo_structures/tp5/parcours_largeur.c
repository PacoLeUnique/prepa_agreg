#include "file.h"
#include "types_graphe.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


/* Calcule les distances des sommets au sommet de départ, avec un parcours en largeur. */
void parcours_largeur_matrice_adj(graphe_matriciel g, int depart, int** distances){

    /* Initialisation de la file et du tableau des visités, et de distances */
    int n = g.nb_sommets;
    *distances = (int*) malloc(n * sizeof(int));
    
    int nb_visites = 0;
    bool visited[n];
    for (int i=0; i<n; i++)
        visited[i] = false;

    file f = creer_file();
    enfiler(&f, depart-1);

    printf("Parcouring en largeur\n");

    /* Parcours en largeur */
    (*distances)[depart-1] = 0;
    visited[depart-1] = true;
    int s;
    while (nb_visites != n) {

        s = defiler(&f);
        nb_visites++;

        for (int j=0; j<n; j++)
            if ((!visited[j]) && g.mat_adj[s][j] != PAS_ARETE){
                visited[j] = true; // On est assuré qu'on visite toujours un nouveau sommet
                enfiler(&f, j);
                (*distances)[j] = (*distances)[s] + g.mat_adj[s][j];
            } 
    }
}


void parcours_largeur_liste_adj(graphe_avec_listes g, int depart, int** distances){
    
    /* Initialisation de la file et du tableau des visités, et de distances */
    int n = g.nb_sommets;
    *distances = (int*) calloc(n, sizeof(int));
    
    int nb_visites = 0;
    bool visited[n];
    for (int i=0; i<n; i++)
        visited[i] = false;

    file f = creer_file();
    enfiler(&f, depart-1);

    (*distances)[depart-1] = 0;
    visited[depart-1] = true;
    nb_visites++;
    
    int i;
    int j;

    while (nb_visites != n){

        i = defiler(&f);
        nb_visites++;

        sommet* sommet_adj = g.tab_listes_adjacence[i];

        while (sommet_adj != NULL){
            j = sommet_adj->numero - 1;
            if (!visited[j]){
                visited[j] = true;
                enfiler(&f, j);
                (*distances)[j] = (*distances)[i] + sommet_adj->valeur;
            }

            sommet_adj = sommet_adj->sommet_suivant;
        }

    }

}