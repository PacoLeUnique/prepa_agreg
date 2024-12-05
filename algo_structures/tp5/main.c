#include "parcours_largeur.h"
#include <stdio.h>


int main(){
    int* distances_matrice_adj;
    int* distances_liste_adj;
    graphe_matriciel g_mat = construire_graphe_matriciel("graphes/graphe1.txt");
    graphe_avec_listes g_list = construire_graphe_avec_listes("graphes/graphe1.txt");

    int sommet_depart = 5;

    printf("============ PARCOURS EN LARGEUR ============\n");

    parcours_largeur_matrice_adj(g_mat, sommet_depart, &distances_matrice_adj);
    
    printf("Distance depuis le sommet %d (version matrice) : [", 4);
    for(int i=0; i<g_mat.nb_sommets; i++)
        printf("%d,", distances_matrice_adj[i]);
    printf("\b]\n");
    
    
    parcours_largeur_liste_adj(g_list, sommet_depart, &distances_liste_adj);
    printf("Distance depuis le sommet %d (version liste)   : [", 4);
    for(int i=0; i<g_mat.nb_sommets; i++)
        printf("%d,", distances_matrice_adj[i]);
    printf("\b]\n");
}