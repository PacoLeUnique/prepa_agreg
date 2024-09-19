#include <ctype.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

const int MAX_ERRORS = 8;
int erreurs = 0;

int nb_lettres_jouees = 0;
char lettres_jouees[26] = {};

/** Choisit un mot au hasard parmi tout ceux du fichier.
 */
char* choose_word(char* path){
    srand(time(NULL));

    FILE *f = fopen(path, "r");

    // On choisit un nombre n au hasard
    char ligne[100]; //Buffer pour stocker nos lignes
    
    int nb_lignes;
    fscanf(f, "%d", &nb_lignes);
    int n = rand() % nb_lignes;

    // Puis on parcourt n lignes, et on choisit le mot sur lequel on s'est arreté
    for(int i=0; i<n; i++)
        fscanf(f, "%s", ligne);
    
    char* mot = malloc(strlen(ligne) * sizeof(char));
    strcpy(mot, ligne);
    
    fclose(f);
    return mot;
}


/** Demande une lettre au joueur, et la renvoie en minuscule.
    Ne prend pas en compte si elle a déjà été jouée ou non.
 */
char demande_lettre(){
    char rep;

    do{
        printf("Dis-moi une lettre : ");
        scanf("%c", &rep);

        if (!isalpha(rep)){
            printf("T'as pas écris une lettre, recommence\n");
            while ( (rep = getchar()) != '\n' && rep != EOF ) { } // On vide le tampon
        }  
    }while(!isalpha(rep));

    char c = rep;
    while ( (rep = getchar()) != '\n' && rep != EOF ) { } // On vide le tampon

    return tolower(c);
}


/* Renvoie 1 si la lettre a déjà été jouée, 0 sinon.
*/
int deja_jouee(char c){
    for(int i=0; i< nb_lettres_jouees; i++)
        if (lettres_jouees[i] == c)
            return 1;
    return 0;
}


/** Renvoie 1 si le c est inclus dans le mot, 0 sinon. */
int char_in_word(char* mot, int n, char c){
    for(int i=0; i<n; i++)
        if (mot[i] == c)
            return 1;
    return 0;
}


/** Affiche le mot, mais en affichant seulement les lettres déjà trouvées.
    @param mot : le mot
    @param n : la longueur du mot
 */
void affiche_mot(char* mot, int n){

    for(int i=0; i<n; i++){
        char c = mot[i];

        int trouve = 0;
        for (int j=0; j<nb_lettres_jouees; j++){
            if(c == lettres_jouees[j]){
                trouve = 1;
                printf("%c ", c);
            }
        } 
        if (!trouve)
            printf("_ ");
    }

    printf("\n");
}


/** Renvoie 1 si on a trouvé toutes les lettres, 0 sinon.
 */
int is_word_completed(char* mot, int n){
    //Pour chaque lettre du mot :
    for (int i=0; i<n; i++){
        
        int trouve = 0;
        for(int j=0; j<nb_lettres_jouees; j++){
            if(mot[i] == lettres_jouees[j]){
                trouve = 1;
                break;
            }
        }
        if (!trouve)
            return 0;
    }
    return 1;
}


/** joue un tour de pendu.
*   Après avoir effectué le tour, renvoie : 
    > 0 si la partie est toujours en cours,
    > 1 si c'est une victoire,
    > -1 si c'est une défaite (gros nullos).
*/
int joue_un_tour(char* mot, int n){
    
    //1. On affiche l'état de la game 
    printf("Mot : ");
    affiche_mot(mot, n);

    printf("Lettres saisies : ");
    for (int i=0; i<nb_lettres_jouees; i++){
        printf("%c ", lettres_jouees[i]);
    }
    printf("\n");

    int essais_restants = MAX_ERRORS - erreurs;
    printf("Essais restants : %d\n", essais_restants);


    //2. On demande quelle lettre on joue
    char c;
    do{
        c = demande_lettre();
        if (deja_jouee(c)){
            printf("Tu as déjà joué cette lettre, bg.\n");
        }
    } while(deja_jouee(c));


    //3. Update des variables
    lettres_jouees[nb_lettres_jouees] = c;
    nb_lettres_jouees++;

    //4. On check si c'est une bonne lettre ou pas
    if (!char_in_word(mot, n, c)){
        printf("\nAie aie aie, y'a pas de %c!!!!\n", c);
        erreurs++;
    }

    printf("\n");

    //5. On check si c'est une fin de partie
    if (is_word_completed(mot, n))
        return 1;

    if (essais_restants == 0)
        return -1;

    return 0;
}


int main(int argc, char* argv[]){

    printf("\n================ PARTIE DE PENDU DE FOU ================\n");
    printf("T'as %d essais. T'es chaud ? Allez c'est parti.\n\n", MAX_ERRORS);

    //NE PAS OUBLIER DE DESALLOUER LE MOT !!!!!!!
    char* mot = choose_word("data/Fichier de mots pour l exercice 2 du TP no 2.txt");
    int n = strlen(mot);

    //printf("(le mot c'est %s)\np", mot);

    int gamestate;
    while((gamestate = joue_un_tour(mot, n)) == 0) {}

    if (gamestate == 1)
        printf("LETTTTS GOOOOOOO TAS GAGNEEEEEEEEEEEEEEEEE OUAIIIIIIIIIIIIIIIIII\n");
    else
        printf("HAHAHAHHAHAHAHAH T'AS PERDU LE MOT C'ETAIT %s LOOOOOOOOOOOOOOOOOOOSEEEEEEEEEEEEEERRRRRRR\n", mot);

    free(mot);
}