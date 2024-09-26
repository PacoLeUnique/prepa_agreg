#include<stdio.h>
#include<limits.h>
#include<stdlib.h>
#include<assert.h>
#include<math.h>
#include<pthread.h>                                                            
//à compiler sous linux via gcc start_code.c -lm 

int  n    = 1000;
long pMax = 60000;
long poids_div = 5000;      //<pMAx
long vals_div  = 100;

long* vals;            //profits
long* poids;
int print_final_opt = 0;//afficher le optleau à la fin (pour un pb de petite taille)
int i;

void init_sad()
{
    assert(poids_div<pMax);
    vals = (long*) calloc(n, sizeof(long));
    poids = (long*) calloc(n, sizeof(long));
    long a = 7;
    long b = 11;
    for(i=0;i<n;i++){
        a = a *7 % vals_div;
        b = b *11% poids_div;
        vals[i]  =  a + 1;
        poids[i] =  b + 1;
        assert(poids[i]<=pMax);
    }
}

void print_sad(){
    printf("Articles: %d, pMax=%ld:\nProfs:", n,pMax);
    for(i=0;i<n;i++)
        printf("%5ld ",vals[i]);
    printf("\nPoids:");
    for(i=0;i<n;i++)
        printf("%5ld ",poids[i]);
    printf("\n");
}

void print_ratio(){
    for(i=0;i<n;i++){
        printf("(p%ld, v%ld) ", poids[i], vals[i]);
    }
}


/* échange p[i] et p[j], ainsi que v[i] et v[j]. */
void swap(int i, int j){
    assert(i < n);
    assert(j < n);

    long tmp = poids[i];
    poids[i] = poids[j];
    poids[j] = tmp;

    tmp = vals[i];
    vals[i] = vals[j];
    vals[j] = tmp;
}


/* Trie les objets du sac a dos (donc poids et vals), selon leur rapport poids/valeur. 
   Utilise le tri à bulle.*/
void trie_objs(){

    int fini = 0;
    while(!fini){
        fini = 1;
        for(int i=0; i<n-1; i++)
            if ((double)vals[i] / (double)poids[i]   <   (double)vals[i+1] / (double)poids[i+1]){
                fini = 0;
                swap(i, i+1);
            }
    }
    
}

/* calcule la borne sup, en utilisant */
long calc_valBorneSup(){
    trie_objs();
    print_ratio();

    long val_sup = 0;
    int place_restante = pMax;
    i = 0;

    while(place_restante >= poids[i]){
        val_sup += vals[i];
        place_restante -= poids[i];
        i++;
    }

    // il reste 3kg, le prochain obj pese 5
    //      place_restante             poids[i]
    // --> tu peux ajouter 3/5 de l'obj = place_restante/poids[i]

    double ratio =  (double)place_restante/(double)poids[i];
    val_sup +=  (long)(floor( ratio * (double)vals[i]));
    return val_sup; 
}

int main(int argc, char** argv){
    init_sad();
    if(print_final_opt)
        print_sad();

    long bsup = calc_valBorneSup();
    print_sad();
    printf("bsup=%ld\n",bsup);
}
