#ifndef TAS_C
#define TAS_C
#include "tas.c"
#endif
#include <stdio.h>


void exo1(){
    int tab[7] = {1,4,3,7,5};
    tas t = {7, 5, tab};
    
    print_tas(t);
    printf("min : %d\n", min(t));
    printf("is vide : %d\n", is_empty(t));
}

void exo23(){

    tas t = new_tas(7);
    print_tas(t);
    
    for(int i=2;i<=10;i+=2){
        insert(&t, i);
        print_tas(t);
    }

    insert(&t, 5);
    print_tas(t);
    insert(&t, 1);
    print_tas(t);

    insert(&t, 546);



    free(t.tab);
}

void exo4(){
    tas t = new_tas(7);

    for(int i=0;i<7;i++)
        insert(&t, i+1);
    print_tas(t);

    int a;
    for (int i=0;i<8;i++){
        a = suppr_min(&t);
        print_tas(t);
        //printf("%d\n", a);
    }

    free(t.tab);
}


int main(){
    
    exo4();
    return 0;
}