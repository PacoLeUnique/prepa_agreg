#ifndef TAS_C
#define TAS_C
#include "tas.c"
#endif


/** trie t, seulement entre [g,d]. */
void qsort_aux(int *t, int g, int d){
    
    // Cas d'arret
    if (g >= d)
        return;
    
    int p = (g+d)/2;
    swap(t, p, d); //On met le pivot a droite

    int pgg = g; 
    for(int i=g; i<d; i++){
        if (t[i] < t[d]){
            swap(t, i, pgg);
            pgg++;
        }
    }
    swap(t, d, pgg);

    qsort_aux(t, g, pgg-1);
    qsort_aux(t, pgg+1, d);

}

/* Trie le tableau t, avec un tri rapide. */
void quick_sort(int *t, int n){
    qsort_aux(t, 0, n-1);    
}
