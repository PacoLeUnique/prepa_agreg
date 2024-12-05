#ifndef BOOL_H
#define BOOL_H
#include <stdbool.h>
#endif

/* type structuré correspondant à un maillon d'une liste chaînée : chaque maillon contient une référence vers le maillon suivant, et vers le dernier maillon de la liste */
typedef struct s_maillon {
	int valeur;
	struct s_maillon *suivant;
	struct s_maillon *dernier;
} maillon;

/* type liste chaînée */
typedef maillon* liste;

/* type file, où la file est gérée à l'aide d'une liste chaînée */
typedef struct {
	liste l; //liste chaînée contenant les éléments de la file
	int nb_elements; //nombre d'éléments actuellement stockés dans la file
} file;

/* crée une file vide ; à appeler avant toute utilisation de la file */
file creer_file();

/* désalloue TOUT l'espace mémoire occupé par la file f ; à appeler à la fin de l'utilisation de la file */
void vider_file(file f);

/* renvoie true si la file f ne contient aucun élément, et false sinon */
bool est_vide(file f);

/* renvoie la valeur de l'élément en tête de la file f */
int tete_file(file f);

/* insère l'élément passé en 2ème paramètre en queue de la file passée en 1er paramètre */
void enfiler(file *f, int element);

/* supprime l'élément en tête de la file passée en paramètre, puis renvoie la valeur de cet élément */
int defiler(file *f);
