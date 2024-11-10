#include <stdio.h>
#include <stdlib.h>

/** fusionne t1 et t2 dans t. */
void fusion(int* t1, int n1, int* t2, int n2, int* t){

    int i = 0;
    int j = 0;
    int k = 0;

    while(i < n1 && j < n2){
        if(t1[i] < t2[j]){
            t[k] = t1[i];
            i++;
            k++;
        } else {
            t[k] = t2[j];
            j++;
            k++;
        }
    }

    if (i == n1)
        while(j < n2){
            t[k] = t2[j];
            j++;
            k++;
        }
    else
        while(i < n1){
            t[k] = t1[i];
            i++;
            k++;
        }

}


void merge_sort(int* t, int n){
    
    // cas d'arret
    if (n == 1)
        return;

    // On sépare en 2
    int m = n/2;
    int n1 = m;
    int n2 = m + n%2;

    int* t1 = malloc(n1 * sizeof(int));
    int* t2 = malloc(n2 * sizeof(int));

    for (int i=0; i<n1; i++)
        t1[i] = t[i];
    for (int i=0; i<n2; i++)
        t2[i] = t[m+i];

    //2 - on les trie récursivement
    merge_sort(t1, n1);
    merge_sort(t2, n2);

    //3 - on fusionne
    fusion(t1, n1, t2, n2, t);

    free(t1);
    free(t2);
}



// int main(int argc, char* argv[]){
//     int t1[] = {1,4,6,7,10};
//     int t2[] = {2,7,8,9,11,15};

//     int n1 = 5;
//     int n2 = 6;

//     int *t = malloc(11 * sizeof(int));

//     fusion(t1, n1, t2, n2, t);

//     printf("==== Test 1 ====\n");
//     printf("tableau trié : [");
//     for(int i=0; i<n1+n2; i++)
//         printf("%d, ", t[i]);
//     printf("\b\b]\n");

//     free(t);


//     printf("\n==== Test 2 ====\n");
//     int a[] = {8,4,3,7,10,6,9,4,0};
//     int n = 9;

//     merge_sort(a,n);
    
//     printf("tableau trié : [");
//     for(int i=0; i<n; i++)
//         printf("%d, ", a[i]);
//     printf("\b\b]\n");




//     return 0;
// }