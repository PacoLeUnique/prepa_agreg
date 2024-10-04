#include <stdlib.h>
#include <stdio.h>
#include <string.h>


struct bloc_1gramme {
    char c;
    
    int nb_suivants;
    char* suivants;
    int* occurences;
    double* probas;
};

struct modele_1gramme {
    unsigned int nb_1grammes;
    struct bloc_1gramme* un_grammes;
};


/* Renvoie le modèle 1-gramme d'un texte donné.
*/
struct modele_1gramme modele_1gramme_from_text(char* text){
    
    struct modele_1gramme modele;
    int n = strlen(text);

    int char_vus = 0;
    char caracteres[n];

    // 1. On récupère tous les différents caractères présents dans le tetxe.

    // On parcourt chaque caractère du texte.
    // S'il n'a pas déjà été vu, on le rajoute dans la liste caracteres
    for(int i=0; i<n; i++){
        char c = text[i];

        int vu = 0;
        for (int j=0; j<char_vus; j++){
            if(c == caracteres[j]){
                vu = 1;
                break;
            }
        } 

        if (!vu){
            caracteres[char_vus] = c;
            char_vus++;
        }
    }

    // Affichage des caractères
    printf("Caractères présents dans le texte : [");
    for(int i=0; i<char_vus; i++){
        printf("'%c',", caracteres[i]);
    }
    printf("\b]\n");


    modele.nb_1grammes = char_vus;
    modele.un_grammes = malloc(n * sizeof(struct bloc_1gramme));

    //2. On initialise un bloc_1gramme pour chacun des caractère
    for (int i=0; i<char_vus; i++){
        char c = caracteres[i];
        struct bloc_1gramme bloc;

        printf("Construction du bloc_1gramme '%c'\n", c);

        bloc.c = c;

        int nb_suivants = 0;
        char suivants[char_vus];
        int occurences[char_vus];
        double probas[char_vus];

        // On reparcourt le texte, et on cherche le caractère suivant au notre
        for(int j=0; j<n-1; j++){
            if (text[j] == c){
                char suivant = text[j+1];
                printf("On a croisé un '%c'\n", suivant);

                // Si suivant a déjà été vu, on incrémente l'index où on l'a vu
                int vu = 0;
                for (int k=0; k<nb_suivants; k++){
                    if (suivant == suivants[k]){
                        vu = 1;
                        occurences[k]++;
                        printf("'%c' = suivants[%d], on l'incrémente\n", suivant, k);
                        break;
                    }
                }

                // sinon on l'ajoute ce nouveau char dans le tableau suivants, et on l'incrémente  
                if(!vu){
                    suivants[nb_suivants] = suivant;
                    occurences[nb_suivants] = 1;
                    printf("'%c' n'a pas été vu, on l'ajoute dans suivants[%d]\n", suivant, nb_suivants);
                    nb_suivants++;
                }
            }
        }

        // Calcul des probabilités
        int occurences_totales = 0;
        for (int j=0; j<nb_suivants; j++){
            occurences_totales += occurences[j];
        }

        for (int j=0; j<nb_suivants; j++){
            probas[j] = (double)occurences[j] / (double)occurences_totales; 
        }

        //Affichage du bloc
        printf("Suivants : [");
        for(int j=0; j<nb_suivants; j++){
            printf("%c,", suivants[j]);
        }
        if(nb_suivants != 0)  printf("\b");
        printf("]\n");

        printf("Occurences : [");
        for(int j=0; j<nb_suivants; j++){
            printf("%d,", occurences[j]);
        }
        if(nb_suivants != 0)  printf("\b");
        printf("]\n");

        printf("Probas : [");
        for(int j=0; j<nb_suivants; j++){
            printf("%g,", probas[j]);
        }
        if(nb_suivants != 0)  printf("\b");
        printf("]\n");

        printf("\n");

        bloc.nb_suivants = nb_suivants;
        bloc.suivants = suivants;
        bloc.occurences = occurences;
        bloc.probas = probas;

        modele.un_grammes[i] = bloc;
    }

    printf("Modèle créé ! \n");
    return modele;
}




int main(){

    struct modele_1gramme modele = modele_1gramme_from_text("Bonjour, comment allez-vous ? Ca va, ca va aller bien mieux.");

    return 0;
} 