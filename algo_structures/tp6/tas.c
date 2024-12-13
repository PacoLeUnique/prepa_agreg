#include "tas.h"
#include <stdio.h>
#include <stdlib.h>

tas init_tas(int n){
    tas t;
    t.size = n;
    t.nb_elem = 0;
    t.cles = (int *) malloc((n+1) * sizeof(int));
    t.vals = (int *) malloc((n+1) * sizeof(int));

    return t;
}


void swap(tas *t, int i, int j){
    int tmp = t->cles[j];
    t->cles[j] = t->cles[i];
    t->cles[i] = tmp;

    tmp = t->vals[j];
    t->vals[j] = t->vals[i];
    t->vals[i] = tmp;
}


void insert(tas *t, int cle, int val){
    if (t->nb_elem == t->size){
        printf("Erreur : tas plein\n");
        exit(-1);
    }

    t->cles[t->nb_elem] = cle;
    t->vals[t->nb_elem] = val;
    t->nb_elem++;

    int i = t->nb_elem - 1;
    while (t->cles[i] < t->cles[i/2]){
        swap(t, i, i/2);
        i /= 2;
    } 
}

int est_vide(tas t){
    return t.nb_elem == 0;
}

int remove_min(tas *t){
    if (t->nb_elem == 0){
        printf("Erreur : remove d'un tas vide\n");
        exit(-1);
    }

    printf("(cle, val) choisie : (%d,%d)\n", t->cles[0], t->vals[0]);
    int min = t->vals[0];
    
    // On met le dernier en premier
    t->cles[0] = t->cles[t->nb_elem - 1];
    t->vals[0] = t->vals[t->nb_elem - 1];    
    t->nb_elem--;

    //puis on le fait descendre
    int i = 0;
    while ( (i < t->nb_elem) 
         && (   (2*i+1 < t->nb_elem  &&  t->cles[i] > t->cles[2*i + 1])  
            ||  (2*i+1 < t->nb_elem  &&  t->cles[i] > t->cles[2*i + 2])) ){

        if (t->cles[2*i + 1] < t->cles[2*i + 2]){ 
            swap(t, i, 2*i + 1);
            i = 2*i + 1;

        } else {
            swap(t, i, 2*i + 2);
            i = 2*i + 2;
        }
    }

    return min;
}