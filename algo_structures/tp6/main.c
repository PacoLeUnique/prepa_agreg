#include <stdio.h>

#ifndef GRAPHE_
#define GRAPHE_
#include "graphe.h"
#endif
#include "kruskal.h"


int main(int argc, char** argv){
    if (argc == 1){
        printf("faut choisir un graphe bg\n Exemple : ./kruskal 2\n");
        return -1;
    }

    graphe g = cree_graphe(8);
    ajoute_arete(&g, cree_arete(0, 2, 35));
    ajoute_arete(&g, cree_arete(0, 3, 300));
    ajoute_arete(&g, cree_arete(0, 4, 10));
    ajoute_arete(&g, cree_arete(1, 2, 200));
    ajoute_arete(&g, cree_arete(1, 3, 100));
    ajoute_arete(&g, cree_arete(1, 4, 150));
    ajoute_arete(&g, cree_arete(1, 5, 80));
    ajoute_arete(&g, cree_arete(1, 6, 300));
    ajoute_arete(&g, cree_arete(1, 7, 30));
    ajoute_arete(&g, cree_arete(2, 3, 200));
    ajoute_arete(&g, cree_arete(2, 4, 20));
    ajoute_arete(&g, cree_arete(3, 6, 180));
    ajoute_arete(&g, cree_arete(5, 6, 40));
    ajoute_arete(&g, cree_arete(5, 7, 50));
    ajoute_arete(&g, cree_arete(6, 7, 78));


    char filename[5000];
    sprintf(filename, "graphes/graphe%s.txt", argv[1]);

    printf("Go pour le fichier %s\n", filename);
    graphe g2 = graphe_from_file(filename);

    printf("fetched\n");

    graphe arbre1 = arbre_kruskal(g);
    graphe arbre2 = arbre_kruskal(g2);

    printf("Aretes de l'abre couvrant 1 :\n");
    for (int i=0; i<8; i++)
        for(int j=i; j<8; j++)
            if (arbre1.matrice_adj[i][j] != 0)
                printf("%d->%d\n", i,j);
        
    printf("=======================\n");
    
    printf("Aretes de l'abre couvrant 2 :\n");
    for (int i=0; i<arbre2.nb_sommet; i++)
        for(int j=i; j<arbre2.nb_sommet; j++)
            if (arbre2.matrice_adj[i][j] != 0)
                printf("%d->%d\n", i,j);

    printf("pipi ouais :D\n");
    return 0;
}