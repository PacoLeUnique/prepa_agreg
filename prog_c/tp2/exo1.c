#include <stdio.h>
#include <stdlib.h>

struct tableau {
    int *tab;
    int length;
};

void parties(struct tableau t, int i){

    // si i == len(t), alors on print le tableau
    if (i == t.length){

        //si t = {0,0,0,0,0}, on affiche rien
        int vide = 1;
        for (int j=0; j<t.length; j++)
            if (t.tab[j] == 1){
                vide = 0;
                break;
            }
        if (vide) return;

        printf("{");
        for(int j=0; j<t.length; j++)
            if (t.tab[j] == 1)  
                printf("%d, ", j+1);
        printf("\b\b}\n");
    
    // Sinon, soit t[i] vaut 0, soit 1, et on continue la recursion
    } else { 
        t.tab[i] = 0;
        parties(t, i+1);

        t.tab[i] = 1;
        parties(t, i+1);
    }
}


int main(int agrc, char* argv[]){
    
    printf("On va afficher toutes les parties de {1, ..., n}, yay :D\n");
    printf("\n");
    
    // On récupere n
    int n;
    do{
        printf("Dis moi ton n : ");
        scanf("%d", &n);

        if (n<=0)
            printf("C'est pas positif gros nul, recommence\n");
    } while (n <= 0);

    //On init le tableau 
    int* tab = malloc(n*sizeof(int));
    for (int i=0; i<n; i++)
        tab[i] = 0;    
    struct tableau t = {tab, n };

    // Affichage des parties de n
    printf("\n");

    printf("Voici toutes les parties de ");
    printf("{");
    for (int i=0; i<n; i++)
        printf("%d, ", i+1);
    printf("\b\b} : \n");

    parties(t, 0);

    printf("\nyay :D\n");

    return 0;
}