
/* Rerésente une arete qui relie 2 sommets (i,j). */
typedef struct arrete_ {
    int i;      // le sommet à 'gauche' de l'arete
    int j;      // le sommet à 'droite'
    int poids;  // le poids de cette arete
} arete;

typedef struct graphe_ {
    int ** matrice_adj; // la matrice d'adjacence du graphe
    int nb_sommet;      // le nombre de sommets du graphe
} graphe;

graphe cree_graphe(int n);
arete cree_arete(int i, int j, int poids);

graphe graphe_from_file(char filename[]);

void ajoute_arete(graphe* g, arete a);

