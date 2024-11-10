#ifndef TAS_C
#define TAS_C
#include "tas.c"
#endif

/** Trie t avec un tri par tas. */
void heap_sort(int *t, int n){
    tas h = new_tas(n);

    for(int i=0; i<n; i++)
        insert(&h, t[i]);

    for(int i=0; i<n; i++)
        t[i] = suppr_min(&h);

    return;
}

