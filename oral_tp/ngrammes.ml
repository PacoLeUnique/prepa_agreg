open String

type suivant = {
  c : char;
  occurences : int;
  proba : float
}

type bloc_ngramme = {
  s : string;
  suivants : suivant list;
}

type n_gramme = { 
  n : int;
  n_grammes : bloc_ngramme list;
  n_moins1_grammes : n_gramme option
}

(* Renvoie la liste de tous les n-grammes dans le texte, au format textuel. *)
let rec find_n_grammes text n : string list = 
  if n > String.length text then []
  else 
    let f i = text.[i] in
    fold_left (@.)


let n_gramme_from_text (text : string) (n : int) : n_gramme = 
  
  let rec n_gramme_rec (n : int) : n_gramme option =
    if n = 0 then None
    else 
  in
  

let a : n_gramme = {n=3; n_grammes=[]; n_moins1_grammes=None}

;;