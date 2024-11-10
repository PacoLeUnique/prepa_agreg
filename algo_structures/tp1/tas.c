#include "tas.h"
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>


/*============== EXERCICE 1 ==============*/

/* 1 */
tas new_tas(int MAX_SIZE){
    int *tab = malloc(MAX_SIZE * sizeof(int));
    tas t = {MAX_SIZE, 0, tab};
    return t;
}

/* 2 */
int min(tas t){
    return t.tab[0];
}

bool is_full(tas t){
    return (t.n == t.MAX_SIZE);
}

bool is_empty(tas t){
    return (t.n == 0);
}

void print_tas(tas t){

    printf("[");
    for (int i=0; i<t.MAX_SIZE; i++)
        if (i < t.n)
            printf("%d ", t.tab[i]);
        else 
            printf("_ ");
        
    printf("\b]\n");
    
    return;
}

/* 3 */

void swap(int *t, int i, int j){
    int tmp = t[i];
    t[i] = t[j];
    t[j] = tmp;
}
int min_ab(int a, int b){
    if (a < b) return a;
    else return b;
}

void insert(tas *t, int elm){
    
    if (is_full(*t)){
        printf("Erreur insertion : tas plein\n");
        exit(-1);
    }

    // 1 - on insère en dernier élement
    t->tab[t->n] = elm;
    t->n++;
    
    // 2 - on rééquilibre pour retrouver notre tas min
    int i = (t->n) - 1;
    while (i != 0 && t->tab[i] < t->tab[(i-1)/2]){   
        swap(t->tab, i, (i-1)/2);
        i = (i-1)/2;
    }

    return;
}

int suppr_min(tas *t){

    if (is_empty(*t)){
        printf("Erreur suppression : Tas vide\n");
        exit(-1);
    }

    // 1 - supprimer le min
    swap(t->tab, 0, (t->n) - 1);
    int min = t->tab[(t->n) - 1];
    t->n--;

    // 2 - on rééquilibre
    int i = 0;
    while(2*i + 1 < t->n) { // Tant qu'on est pas sur une feuille
        
        // Cas où on a qu'1 fils
        if (2*i + 2 == t->n){

            if(t->tab[i] > t->tab[2*i+1])
                swap(t->tab, i, 2*i+1);
            i = 2*i+1;

        } else {

            // Si on est plus petit que nos 2 fils, c'est gagné
            if (t->tab[i] <= t->tab[2*i+1] && t->tab[i] <= t->tab[2*i+2]){
                break;
            
            // Sinon, on swap avec notre fils le plus petit
            } else {

                if (t->tab[2*i+1] < t->tab[2*i+2]){
                    swap(t->tab, i, 2*i+1);
                    i = 2*i + 1;
                } else {
                    swap(t->tab, i, 2*i+2);
                    i = 2*i + 2;
                }

            }
        
        }
    }   

    return min; 
}