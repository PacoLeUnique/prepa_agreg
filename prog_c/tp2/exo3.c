#include "objet.c"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


int max (int a, int b){
    if (a > b)
        return a;
    else return b;
}

/** Renvoie la valeur optimale que l'on peut mettre dans le sac à dos.
 */
int solve_kn(struct objet* data, int n, int Pmax){
    
    printf("On solve le sac a dos, c'est parti\n");
    int** f;

    // Allocation de la mémoire
    f = malloc((n+1)*sizeof(int*));
    for (int i=0; i<=n; i++)
        f[i] = malloc((Pmax+1)*sizeof(struct objet));

    //On init le tableau...
    for (int j=0; j<=Pmax; j++){
        if (j >= data[0].p)
            f[1][j] = data[0].v;
        else
            f[1][j] = 0;
    }

    // ...puis on remplit le tableau
    for (int i=2; i<=n; i++){
        for(int j=0; j<=Pmax; j++){
            //Un peu de sucre syntaxique
            int pi = data[i-1].p;
            int vi = data[i-1].v;

            if (j < pi)
                f[i][j] = f[i-1][j];
            else
                f[i][j] = max(f[i-1][j], vi + f[i-1][j-pi]);
        }
    }

    int res = f[n][Pmax]; 

    //On déalloue tout
    for (int i=0; i<=n; i++)
        free(f[i]);
    free(f);

    return res;
}



int main(int argc, char* args[]){

    assert(argc == 2);

    char* path = args[1];
    printf("Go résoudre le sac à dos %s\n\n", path);

    // Extraction de la data
    int* n_Pmax = malloc(2*sizeof(int));
    struct objet* data = extract_object(path, n_Pmax);
    int n = n_Pmax[0];
    int Pmax = n_Pmax[1];

    // On solve le bail
    int res = solve_kn(data, n, Pmax);

    printf("La valeur max c'est %d !!!!!!\n", res);

    // Et on désalloue tout
    free(data);
    free(n_Pmax);
}