
typedef struct tas_{
    int* cles;      // le tableau des clés
    int* vals;      // le tableau des valeurs
    int nb_elem;    // le nombre d'éléments présents
    int size;       // La taille max du tas
} tas;

/* Crée un tas vide, de taille n. */
tas init_tas(int n);

/* Renvoie 1 si le tas est vide, 0 sinon. */
int est_vide(tas t);

/* Insère un élement dans t. */
void insert(tas* t, int cle, int val);

/* Retire le minimum du tas, et renvoie sa valeur. */
int remove_min(tas* t);