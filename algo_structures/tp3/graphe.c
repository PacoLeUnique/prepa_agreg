#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <assert.h>
#include <stdbool.h>

#include "pile.c"

/********************************************************************
                        Structure liste chainée 
********************************************************************/
typedef struct queue_{
    int val;
    struct queue_* next;
} queue;

typedef struct liste_{
    queue* q ;
    queue* qfin ;
    queue* curr;       //le curseur courant pour parcourir
} liste;

liste ma_liste;

//Il faut toujours initialiser la liste avant de démarrer
void init_liste(liste*l){
    l->q = NULL;
    l->qfin = NULL;
    l->curr = NULL;
}
bool fixe_curr_au_debut(liste *l){
    if(l->q==NULL)
        return false;
    l-> curr = l->q;
    return true;
}
int get_curr(liste *l){
    assert(l!=NULL);
    return l-> curr -> val;
}
//return true si "next" existe
bool next(liste *l){
    l->curr = l->curr->next;
    if(l->curr==NULL)   
        return false;
    return true;
}
bool qVide(liste*l){ //renvoyer 1 si vrai, 0 sinon
    if(l->q==NULL)
        return true;
    else
        return false;
}
void qDefiler(liste*l){
    queue* qOld = l->q;
    l->q = l->q->next;
    free(qOld);
}
void qEnfiler(int x, liste* l){
    queue* qNew = (queue*) malloc(sizeof(queue));
    qNew -> val = x;
    qNew -> next = NULL;
    if(l->q==NULL){
        l->q = qNew;
        l->qfin = l->q;
    }else{
        l->qfin -> next = qNew;
        l->qfin = qNew;
    }
}
int qTete(liste* l){
    return l->q->val;
}


/********************************************************************
         Structure graphe par liste de successeurs/voisins
********************************************************************/
typedef struct graphe_{
    int n;                                          //nombre sommets
    bool oriente ;                                  //orientÃ©? 
    liste* succ;                                    //successeurs ou voisins
} graphe;

graphe g;

//nombre de sommets, ori=orientÃ© ou non
void init_graphe(int sommets, bool ori, graphe* g){  
    g->n       = sommets;
    g->oriente = ori;
    g->succ    = (liste*) calloc(g->n, sizeof(liste));
    for(int i=0;  i < g->n ;i++)
        init_liste(&(g->succ[i]));
}

//Si le graphe est orientÃ©, l'arc est vu comme une arÃªte
void ajouter_arc(int i, int j, graphe* g){

    qEnfiler(j,&g->succ[i]);
    if(!g->oriente)
        qEnfiler(i,&g->succ[j]);
}

//cette fonction renvoie true en cas de succès (le premier
//voisin existe) ou 0 sinon. On écrit ce voisin dans v.
bool premier_voisin(int i, int *v, graphe *g){
    bool liste_pas_finie = fixe_curr_au_debut(&(g->succ[i]));
    if(liste_pas_finie){
        *v = get_curr(&(g->succ[i]));
        return true;
    }
    return false;
}

//cette fonction renvoie true en cas de succÃ¨s (le voisin 
//suivant existe) ou 0 sinon. On Ã©crit ce voisin dans v
bool voisin_suivant(int i, int *v, graphe *g){
    bool liste_pas_finie = next(&(g->succ[i]));
    if(liste_pas_finie){
        *v = get_curr(&(g->succ[i])); 
        return true;
    } else 
        return false;
}
//Si le graphe est orientÃ©, l'arc est vu comme une arÃªte
bool arc_existe(int i, int j, graphe *g){
    int v;
    if(premier_voisin(i,&v,g)){
        if(v==j)
            return true;
        while(voisin_suivant(i,&v,g))
            if(v==j)
                return true;
    }
    //Arc pas trouvÃ©:
    return false;       
}
bool arete_existe(int i, int j, graphe *g){
    if(g->oriente){
        printf("Attention: on cherche une arÃªte dans un graphe orientÃ©. Return 0");
        return false;
    }
    return arc_existe(i,j,g);
}
void afficher_arcs (graphe* g){
    if(g->oriente)
        printf("Voici la liste d'arcs:\n");
    else
        printf("Voici la liste d'arÃªtes:\n");
    for(int i=0;i<g->n;i++){
        int voisin;
        bool liste_pas_finie = fixe_curr_au_debut(&(g->succ[i]));
        while(liste_pas_finie){
            voisin = get_curr(&(g->succ[i]));
            printf("%d---%d\n", i, voisin);
            liste_pas_finie = next(&(g->succ[i]));
        }
    }
    printf("\n");
    
}


int** get_matrice_adj(graphe g){
    int n = g.n;
    int** matrice;

    /* Allcoation d'espace pour la matrice */
    matrice = (int**) calloc(n, sizeof(int*));
    for (int i=0; i<n; i++)
        (matrice)[i] = (int*) calloc(n, sizeof(int));

    /* On remplit la matrice ligne par ligne */
    int v;
    for (int i=0; i<n; i++){
        if(premier_voisin(i, &v, &g)){
            (matrice)[i][v] = 1;

            while(voisin_suivant(i, &v, &g))
                (matrice)[i][v] = 1;
        }
    }
    return matrice;
}

void print_matrice(int** matrice, int n){
    
    printf("{");

    for (int i=0; i<n; i++){
        printf("{");
        for(int j=0; j<n; j++)
            printf("%d, ", matrice[i][j]);
        printf("\b\b}\n");
    }

    printf("\b\b}\n");

}


void print_aretes_from_matrice(int** matrice, int n){
    printf("Arêtes du graphe :\n");

    for(int i=0; i<n; i++)
        for(int j=0; j<n; j++)
            if(matrice[i][j])
                printf("%d-->%d\n", i, j);
}


/* Renvoie le degre du sommet i dans g. */
int degre(int i, graphe *g){
    int degre = 0;

    /* Degré sortant | Degré tout court, si le grpahe est pas orienté */
    int v;
    if(premier_voisin(i, &v, g)){
        degre++;
        while(voisin_suivant(i, &v, g))
            degre++;
    }

    /* Degrés entrants (si le graphe est orienté) */
    if (!g->oriente)
        return degre;
    else {

        int v;
        for(int j=0; j<(g->n); j++){

            if(!premier_voisin(j, &v, g))
                continue;
            
            if(v == i)
                degre++;
            while(voisin_suivant(j, &v, g))
                if (v == i){
                    degre++;
                    break;
                }
        }
    }
    return degre;
}


void graphe_from_matrice_adj(int** matrice, int n, graphe *g){
    init_graphe(n, true, g);

    for(int i=0; i<n; i++)
        for (int j=0; j<n; j++)
            if (matrice[i][j])
                ajouter_arc(i, j, g);

    printf("ca a marché\n");

    return;
}


void test_grapĥes(){
        int n = 5;
    init_graphe(n, true, &g);  //true=graphe orienté
    ajouter_arc(0, 3, &g);
    ajouter_arc(0, 4, &g);
    ajouter_arc(0, 2, &g);
    ajouter_arc(1, 3, &g);
    ajouter_arc(3, 4, &g);
    ajouter_arc(4, 0, &g);

    afficher_arcs(&g);
    for(int i=0;i<n;i++){
        int v;
        if(premier_voisin(i,&v,&g)){
            printf("voisins de %d: %d, ", i, v);
            while(voisin_suivant(i,&v,&g)){
                printf("%d, ",v);
            }
            printf("\n");
        }
    }
    printf("L'arc 3-9 existe:%s\n",
            arc_existe(3,9,&g)?"true":"false"
          );


    int** matrice_adj = get_matrice_adj(g);
    print_matrice(matrice_adj, g.n);
    print_aretes_from_matrice(matrice_adj, n);
    
    int deg =  degre(0, &g);
    printf("degre de 0 : %d\n", deg);


    graphe g2;

    int l1[3] = {0,1,0};
    int l2[3] = {0,1,0};
    int l3[3] = {0,1,0};
    int* a [3] ={l1,l2,l3};
    // malloc(n*sizeof(int));

    graphe_from_matrice_adj(a, 2, &g2);

}


void test_pile(){
    pile p;

    init_pile(&p);
    assert(is_empty(&p));

    empiler(1, &p);
    empiler(2, &p);
    empiler(3, &p);
    empiler(4, &p);
    empiler(5, &p);
    empiler(6, &p);

    printf("Dans ma pile, il y a : ");
    int v;
    while (depiler(&v, &p)){
        printf("%d, ", v);
    }
    printf("\b\b \n");
}


int main(){

    test_pile();
    
}

