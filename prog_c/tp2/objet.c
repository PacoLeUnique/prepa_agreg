#include "objet.h"
#include <stdio.h>
#include <stdlib.h>

struct objet* extract_object(char* path, int* n_Pmax){

    //printf("Extraction de fichier\n");

    FILE *f = fopen(path, "r");

    // === On fetch l'en-tete ===
    int n;
    int P_max;
    fscanf(f, "%d", &n);
    fscanf(f, "%d", &P_max);
    
    struct objet* tab = malloc(n*sizeof(struct objet));

    // === On recup le reste ===
    int p;
    int v;

    for(int i=0; i<n; i++){
        fscanf(f, "%d,%d", &p, &v);

        struct objet e = {p, v};
        tab[i] = e;
    } 

    fclose(f);

    // On renvoie tout
    n_Pmax[0] = n;
    n_Pmax[1] = P_max;
    return tab;
}