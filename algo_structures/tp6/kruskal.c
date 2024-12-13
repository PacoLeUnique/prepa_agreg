#include "kruskal.h"
#include "tas.h"
#include <stdio.h>

graphe arbre_kruskal(graphe g){
    
    /*  Init arbre/tableau de composantes connexes.
        Au début, tout le monde est sa propre composante. */
    int n = g.nb_sommet;
    int cc[n];
    for (int i=0; i<n; i++)
        cc[i] = i;

    graphe arbre = cree_graphe(n);

    /* 1. Trier les aretes par poids */
    arete aretes[n*n]; // Un graphe peut avoir au plus n² aretes
    int nb_aretes = 0; 

    /* On remplit le tableau arete */
    int poids;
    for(int i=0; i<n; i++)
        for(int j=i; j<n; j++){
            if ((poids = g.matrice_adj[i][j]) != 0){
                aretes[nb_aretes] = cree_arete(i,j,poids);
                nb_aretes++;
            }
        }
    
    // printf("On a fetch les aretes \n");
    // printf("aretes répertoriées :\n");
    // for (int i=0; i<nb_aretes; i++)
    //     printf("(%d->%d), %d\n", aretes[i].i, aretes[i].j, aretes[i].poids);

    /* Puis on trie le tableau avec un tas. */
    tas t = init_tas(nb_aretes);
    for (int i=0; i<nb_aretes; i++)
        insert(&t, aretes[i].poids, i);

    // /* check que c'est bien trié */
    for(int i=0; i<nb_aretes; i++)
        printf("(%d,%d),", t.cles[i], t.vals[i]);
    printf("\n");

    /* 2. Pour chaque arete, si elle est dans 2 composantes connexes,
          on l'ajoute et on fusionne les composantes */
    arete a;
    int indice;
    while (!est_vide(t)){

        indice = remove_min(&t);
        a = aretes[indice];

        // printf("arete %d->%d (poids %d), ", a.i, a.j, a.poids);
        // printf("composantes : [");
        // for(int i=0; i<n; i++)
        //     printf("%d,", cc[i]);
        // printf("\b]\n");

        if (cc[a.i] != cc[a.j]){
            ajoute_arete(&arbre, a);

            /* et on fusionne les composantes */
            for (int i=0; i<n; i++){
                if (cc[i] == cc[a.j])
                    cc[i] = cc[a.i];         
            }
            printf("\n");
        }
    }

    return arbre;

}