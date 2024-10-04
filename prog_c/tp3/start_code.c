#include<stdio.h>
#include<limits.h>
#include<stdlib.h>
#include<assert.h>
#include<math.h>
#include<pthread.h>                                                            
#include <time.h>
//à compiler sous linux via gcc start_code.c -lm 

int  n    = 1000;
long pMax = 60000;
long poids_div = 5000;      //<pMAx
long vals_div  = 100;

long* vals;            //profits
long* poids;
long valBorneSup;
int print_final_opt = 0;//afficher le optleau à la fin (pour un pb de petite taille)


long min(long a, long b){
    if (a<b) return a;
    return b;
}


void init_sad()
{
    assert(poids_div<pMax);
    vals = (long*) calloc(n, sizeof(long));
    poids = (long*) calloc(n, sizeof(long));
    long a = 7;
    long b = 11;
    for(int i=0;i<n;i++){
        a = a *7 % vals_div;
        b = b *11% poids_div;
        vals[i]  =  a + 1;
        poids[i] =  b + 1;
        assert(poids[i]<=pMax);
    }
}

void print_sad(){
    printf("Articles: %d, pMax=%ld:\nProfs:", n,pMax);
    for(int i=0;i<n;i++)
        printf("%5ld ",vals[i]);
    printf("\nPoids:");
    for(int i=0;i<n;i++)
        printf("%5ld ",poids[i]);
    printf("\n");
}

void print_ratio(){
    for(int i=0;i<n;i++){
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
    //print_ratio();

    long val_sup = 0;
    int place_restante = pMax;
    int i = 0;

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



void* prog_dyn_poids_idx(){
    int k;

    long**opt;
    opt = (long**)calloc(n, sizeof(long*));
    for(int i=0;i<n;i++)
        opt[i] = (long*)calloc((pMax+1), sizeof(long)); 
    long j;

    long best_ever = 0;
    opt[0][poids[0]] = vals[0];
    for(int i=1;i<n;i++){
        for(j=0;j<pMax;j++)
            opt[i][j] = opt[i-1][j];
        for(j=poids[i];j<=pMax;j++){
            if( opt[i][j] <opt[i-1][j-poids[i]] + vals[i]){
                opt[i][j] =opt[i-1][j-poids[i]] + vals[i];
                if(opt[i][j]>best_ever)
                    best_ever = opt[i][j];
            }
        }
    }


    if(print_final_opt){
        printf("n=%d\n",n);
        for(int i=n-1;i>=0;i--){
            for(j=0;j<=pMax;j++)
                printf("%4ld ",opt[i][j]);
            printf("\n");
        }
    }
 
    printf("Best profit par poids : %ld\n", best_ever);

    for(int i=0;i<n;i++)
        free(opt[i]);
    free(opt);

    return NULL;
}


void* prog_dyn_tableau_val_idx(){

    long** opt;
    size_t max_val = valBorneSup;
    printf("%lo\n", valBorneSup);

    // 1. init le tableau de taille [n][sum(vals[i])], et on mets tout à pMax + 1
    opt = (long**) malloc(n * sizeof(long*));
    for (int i=0; i<n; i++)
        opt[i] = malloc(max_val * sizeof(long));

    for(int i=0; i<n; i++)
        for(int j=0; j<max_val; j++)
            opt[i][j] = pMax +1;


    // 2. on remplit le tableau
    opt[0][vals[0]] = poids[0];

    for(int i=1; i<n; i++){
        for (int j=0; j<max_val; j++){
            opt[i][j] = min(opt[i-1][j], opt[i-1][j - vals[i]] + poids[i]);
        }
    }


    // 3. On calcule la val max qu'on a trouvée
    long jMax = 0L;

    for (int j=0; j<max_val; j++){
        if (opt[n-1][j] != pMax + 1){
            jMax = j;
        }
    }

    // On oublie pas de free !
    for(int i=0; i<n; i++)
        free(opt[i]);
    free(opt);

    printf("Best profit par valeur : %lo\n", jMax);
    return NULL;
}



int main(int argc, char** argv){
    init_sad();
    
    valBorneSup = calc_valBorneSup();
    
    //print_sad();


    pthread_t t1, t2;
    if (pthread_create(&t1, NULL, prog_dyn_poids_idx, NULL) != 0){
        perror("erreur lors de création du thread 1\n");
        exit(5);
    }
    printf("Création du 1er thread\n");

    if (pthread_create(&t2, NULL, prog_dyn_tableau_val_idx, NULL) != 0){
        perror("erreur lors de création du thread 2\n");
        exit(5);
    }
    printf("Création du 2e thread\n");
        
    pthread_join(t1, NULL);        
    pthread_join(t2, NULL);
}
