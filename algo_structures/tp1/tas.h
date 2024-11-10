#include <stdbool.h>

/* Question 1.1 */
typedef struct tas{
    int MAX_SIZE;  // La taille max du tableau
    int n;         // Le nb d'élem dans le tas
    int *tab;      // Les éléments
} tas;


/* Question 1.2 */
tas new_tas(int MAX_SIZE);
int min(tas t);
bool is_full(tas t);
bool is_empty(tas t);
void print_tas(tas t);

/* Question 1.3 */
void insert(tas *t, int elm);

/* Question 1.4 */
int suppr_min(tas *t);