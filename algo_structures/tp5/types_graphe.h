#ifndef BOOL_H
#define BOOL_H
#include <stdbool.h>
#endif

/* constante enti�re correspondant � une valeur indiquant qu'il n'existe pas d'ar�te/arc entre 2 sommets, qui est d�finie dans types_graphe.c */
extern const int PAS_ARETE;

/* type structur� correspondant � un graphe donn� sous la forme d'une matrice de distances :
- le i�me sommet est associ� � la ligne d'indice (i-1) et � la colonne d'indice (i-1) de la matrice mat_adj,
- l'�l�ment sur la ligne i et colonne j est donc �gal � la distance de l'ar�te/arc entre les (i+1)�me et (j+1)�me sommets si elle/il existe, et � PAS_ARETE sinon */
typedef struct {
	int nb_sommets; //nombre de sommets du graphe
	int nb_aretes; //nombre d'ar�tes/arcs du graphe
	int **mat_adj; //matrice des distances du graphe
	bool oriente; //vaut true si le graphe est orient�, et false sinon
} graphe_matriciel;

typedef struct s_sommet { //liste cha�n�es d'arcs/ar�tes
	int numero;
	int valeur;
	struct s_sommet *sommet_suivant;
} sommet;

/* type structur� correspondant � un graphe donn� sous la forme d'un tableau de listes d'adjacence :
- le ième sommet est associé à la case d'indice (i-1) du tableau tab_listes_adjacence,
- la liste cha�n�e r�f�renc�e � la case d'indice i contient les indices des successeurs (ou des voisins, si le graphe est non orient�) du (i+1)�me sommet, et les longueurs des ar�tes/arcs associ�(e)s  */
typedef struct {
	int nb_sommets; //nombre de sommets du graphe
	int nb_aretes; //nombre d'ar�tes/arcs du graphe
	sommet **tab_listes_adjacence; //tableau des listes d'adjacence du graphe
	bool oriente; //vaut true si le graphe est orient�, et false sinon
} graphe_avec_listes;

/* dans les deux fonctions suivantes, le param�tre est le nom du fichier de donn�es contenant la description du graphe � construire */
graphe_matriciel construire_graphe_matriciel(char nom_fichier[]); //construit un graphe sous la forme d'une matrice de distances
graphe_avec_listes construire_graphe_avec_listes(char nom_fichier[]); //construit un graphe sous la forme d'un tableau de listes d'adjacence
