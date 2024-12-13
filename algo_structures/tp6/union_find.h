
typedef struct maillon_{
    struct maillon_ *next;
    struct maillon_ *first;
    struct maillon_ *last;

    int val;
    int length;
} uf_bloc;

/* Crée un bloc singleton de valeur n. */
uf_bloc singleton(int n);

/* Renvoie le représentant du bloc. */
int find(uf_bloc b);

/* Fusionne les 2 classes des 2 blocs respectifs. */
void merge(uf_bloc b1, uf_bloc b2);
