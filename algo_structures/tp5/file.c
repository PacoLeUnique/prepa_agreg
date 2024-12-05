#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "file.h"

file creer_file() {
	file f;
	f.nb_elements = 0;
	f.l = NULL;
	return f;
}

void vider_file(file f) {
	liste temp, l = f.l;
	while(l != NULL) { //permet de liberer l'espace reserve pour la file f
		temp = l;
		l = l->suivant;
		free(temp);
	}
}

bool est_vide(file f) {
	return(f.l == NULL);
}

int tete_file(file f) {
	return f.l->valeur;
}

void enfiler(file *f, int element) {
	liste nouveau_maillon = (liste)malloc(sizeof(maillon));
	nouveau_maillon->valeur = element; //on cree le nouvel element
	nouveau_maillon->suivant = NULL;
	nouveau_maillon->dernier = nouveau_maillon;
	if(!est_vide(*f)) { //si la liste n'est pas vide, alors il faut mettre a jour le champ dernier du 1er element, et le champ suivant de l'actuel dernier element
		f->l->dernier->suivant = nouveau_maillon;
		f->l->dernier = nouveau_maillon;
	}
	else
		f->l = nouveau_maillon; //sinon, le nouvel element est le 1er
	f->nb_elements++; //puis on augmente de 1 le nombre d'elements
}

int defiler(file *f) {
	assert(f != NULL);
	assert(f->l != NULL);
	liste temp = f->l; //on garde temporairement en memoire l'adresse du 1er element de la liste, qui est destine a etre "oublie"
	int retour = f->l->valeur; //valeur qui sera retournee
	if(f->l->suivant != NULL) //si la liste contient plus d'un element, alors il faut mettre a jour le champ dernier du 2e element (qui deviendra le 1er apres defilement)
		f->l->suivant->dernier = f->l->dernier;
	f->l = f->l->suivant; //on "oublie" le 1er element de la liste
	free(temp); //on libere ensuite l'espace memoire associe a cet element
	f->nb_elements--; //puis on diminue de 1 le nombre d'elements
	return retour;
}
