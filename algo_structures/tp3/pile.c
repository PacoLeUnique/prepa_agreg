#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

/*****************************************
  IMPLEMENTATION PILE OUAIS OUAIS OUAIS 
******************************************/

typedef struct p_queue_ { 
    int val;
    struct p_queue_ *next;
} p_queue;

typedef struct pile_ { 
    p_queue *top;
} pile;

void init_pile(pile *p){
    p->top = NULL;
}

bool is_empty(pile *p){
    return (p->top == NULL);
}

void empiler(int elm, pile *p){
    p_queue* q = (p_queue*) malloc(sizeof(p_queue));

    q->val = elm;
    q->next = p->top;
    p->top = q;
}

/*  Si la pile est vide, renvoie false.
    Sinon, renvoie true, dépile p et stocke la valeur dépilée dans v. */
bool depiler(int *v, pile *p){
    if (is_empty(p))
        return false;

    p_queue* oldTop = p->top;

    *v = oldTop->val;
    p->top = oldTop->next;
    
    free(oldTop);
    return true;
}

