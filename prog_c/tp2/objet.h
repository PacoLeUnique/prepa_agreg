struct objet {
    int p;
    int v;
};

/** Extrait les données du fichier.
 */
struct objet* extract_object(char* path, int* n_Pmax);