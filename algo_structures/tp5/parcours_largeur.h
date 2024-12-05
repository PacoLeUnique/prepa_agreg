#include "types_graphe.h"

/* Calcule les distances des sommets au sommet de départ, avec un parcours en largeur. */
void parcours_largeur_matrice_adj(graphe_matriciel g, int depart, int** distances);

void parcours_largeur_liste_adj(graphe_avec_listes g, int depart, int** distances);
