#include <stdio.h>


const int MAX_ERRORS = 8;

/** Choisit un mot au hasard parmi tout ceux du fichier.
 */
char* choose_word(char* path){
    FILE *f = fopen(path, "r");

    char ligne[100];
    fscanf(f, "%s", ligne);

    printf("%s", ligne);

}

int main(int argc, char* argv[]){
    choose_word("data/Fichier de mots pour l exercice 2 du TP no 2.txt");
}