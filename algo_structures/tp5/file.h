#ifndef BOOL_H
#define BOOL_H
#include <stdbool.h>
#endif

/* type structur� correspondant � un maillon d'une liste cha�n�e : chaque maillon contient une r�f�rence vers le maillon suivant, et vers le dernier maillon de la liste */
typedef struct s_maillon {
	int valeur;
	struct s_maillon *suivant;
	struct s_maillon *dernier;
} maillon;

/* type liste cha�n�e */
typedef maillon* liste;

/* type file, o� la file est g�r�e � l'aide d'une liste cha�n�e */
typedef struct {
	liste l; //liste cha�n�e contenant les �l�ments de la file
	int nb_elements; //nombre d'�l�ments actuellement stock�s dans la file
} file;

/* cr�e une file vide ; � appeler avant toute utilisation de la file */
file creer_file();

/* d�salloue TOUT l'espace m�moire occup� par la file f ; � appeler � la fin de l'utilisation de la file */
void vider_file(file f);

/* renvoie true si la file f ne contient aucun �l�ment, et false sinon */
bool est_vide(file f);

/* renvoie la valeur de l'�l�ment en t�te de la file f */
int tete_file(file f);

/* ins�re l'�l�ment pass� en 2�me param�tre en queue de la file pass�e en 1er param�tre */
void enfiler(file *f, int element);

/* supprime l'�l�ment en t�te de la file pass�e en param�tre, puis renvoie la valeur de cet �l�ment */
int defiler(file *f);
