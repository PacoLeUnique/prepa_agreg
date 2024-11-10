#include <string.h>
#include <stdio.h>
#include "exo2.c"
#include "exo3.c"
#include "exo4.c"

int main(int argc, char* argv[]){

    if(argc == 1 || argc == 2){
        printf("Faut donner des trucs a trier bg\n");
        exit(-1);
    }

    if (strcmp(argv[1], "quick")!=0 
        && strcmp(argv[1], "heap")!=0
        && strcmp(argv[1], "merge")!=0){
        printf("C'est pas un algo de tri ça. faut faire ./tri quick ou ./tri heap\n");
        exit(-1);
    }

    char* tri = argv[1];
    int n = argc - 2;
    int *t = malloc(n*sizeof(int));
    
    for(int i=2; i<argc; i++){
        t[i-2] = atoi(argv[i]);    
    }

    printf("On a donc le tableau [");
    for (int i=0;i<n;i++)
        printf("%d ", t[i]);
    printf("\b].\n");

    printf("On trie... ");
    if (!(strcmp(tri, "quick"))){
        printf("(mode quick sort)");
        quick_sort(t, n);
    } else if (!(strcmp(tri, "heap"))){
        printf("(mode heap sort)");
        heap_sort(t, n);
    } else {
        printf("(mode merge sort)");
        merge_sort(t, n);
    }


    printf("\n");

    printf("ça nous donne le tableau [");
    for (int i=0;i<n;i++)
        printf("%d ", t[i]);
    printf("\b]. Zinzin !\n");

    return 0;
}