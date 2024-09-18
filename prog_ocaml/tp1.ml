(* Exo 1 *)
let min (tab : int list) : int  = 
  let rec aux tab acc = 
    match tab with
    | [] -> acc
    | x :: t -> 
      let new_acc = if x < acc then x else acc in
      aux t new_acc 
    in 

    if tab = [] then max_int
    else aux tab (List.hd tab) 


let min_iter (tab : int array) : int =
  (* on initialise min, le plus petit élem qu'on a vu jusqu'à présent *) 
  let min = ref max_int in
  let n = Array.length tab in

  (*Si on rencontre un élement plus petit que min, celle-ci devient le nouveau min *)
  for i=0 to (n-1) do 
    if tab.(i) < !min then 
      min := tab.(i);
  done;

  (* et a la fin, on renvoie notre min*)
  !min 


(* Exo 2 *)
let rec sum (tab : int list) : int = 
  match tab with 
  | [] -> 0
  | x :: t -> x + sum t


(* Exo 3 *)
let est_trie tab = 
  let rec est_trie_rec t courant =
    match t with 
    | [] -> true
    | x :: l -> 
      if x < courant then false
      else est_trie_rec l x
  in

  if tab = [] then true
  else est_trie_rec tab (List.hd tab)


let est_trie_iter tab = 

  let exception Nontrie in
  try
    if tab = [||] then true 
    else
      let n = Array.length tab in

      let precedent = ref tab.(0) in 
      for i=0 to (n-1) do 
        if tab.(i) < !precedent then raise Nontrie
        else precedent := tab.(i);
      done; 

      true

  with Nontrie -> false





(* Exo 4 *)
let array_to_list_iter arr = 
  let n = Array.length arr in
  let l = ref [] in

  for i=0 to n-1 do
    l := !l @ [arr.(i)] 
  done;
  !l

let rec list_to_array_rec l =
  match l with 
  | [] -> [||]
  | x :: l0 -> Array.append [|x|] (list_to_array_rec l0)




(* Exo 5 *)
(* Renvoie vrai si elm est dans le tableau t. 
   t est supposé TRIE
   et on fait par recherche dichotomique.
*)
let recherche_rec (t : 'a array) (elm : 'a): bool =  
  
  let rec aux (g:int) (d:int) : bool =
    let _ = print_endline ("Passe rec a g=" ^ string_of_int g ^ ", d=" ^ string_of_int d) in
    if g = d then elm = t.(g)
    else 
      let m = (g+d)/2 in
      if elm > t.(m) then aux (m+1) d
      else aux g m
  in

  let n = Array.length t in
  aux 0 (n-1) 


let recherche_iter t elm = 
  let n = Array.length t in 

  let g = ref 0 in
  let d = ref (n-1) in

  while g < d do 
    let _ = print_endline ("Passe iter a g=" ^ string_of_int !g ^ ", d=" ^ string_of_int !d) in
    let m = (!g + !d)/2 in    

    if elm > t.(m) then
      g := m+1
    else 
      d := m 
  done;


  let _ = print_endline ("Final : g=" ^ string_of_int !g ^ ", d=" ^ string_of_int !d) in
  t.(!g) = elm




(* Exo 6 *)
let rec fact n = 
  if n=1 then 1
  else n * fact (n-1)
  
let fact_iter n = 
  if n <= 0 then raise (Invalid_argument "n doit etre positif!!!!!!!!!!!!!!!!!!!")
  else
    let r = ref 1 in
    for i=1 to n do
      r := !r * i
    done;
    !r


(* Exo 7 *)
let prime_fact (n : int) : int list = 
  
  let r = ref n in
  let primes = ref [] in
  
  for i=2 to n do
    while (!r mod i) = 0 do
      primes := i :: !primes;
      r := !r / i;
    done;
  done;

  !primes

(* //////////////////////////// *)
(* //////// LES TESTS ///////// *)
(* //////////////////////////// *)


(*test min*)
let t = [5;7;12;3;4;2;4;9]
let t2 = [|5;7;12;3;4;2;4;9|]
let a = min t
let a2 = min_iter t2



(*test somme *)
let somme = (sum t)


(* test tri *)

let t3 = [1;2;3;4;5;6;7;9;11;11;13]
let arr3 = [|1;2;3;4;5;6;7;9;11;11;13|]
let arr4 = [|4;4;4;2|]

let e = est_trie t3
let e2 = est_trie_iter arr3
let e3 = est_trie_iter arr4


(* test conversion *)
let t = [|5;3;4;2|]
let a = array_to_list_iter t
let t2 = list_to_array_rec a



(* test recherche dicho *)
let t = [|1;3;5;7;9;11;15;15;16|]
let is_dedans = recherche_rec t 2
let is_dedans_it = recherche_iter t 2
let is_dedans2 = recherche_rec t 7
let is_dedans2_it = recherche_iter t 7

(* test fact *)

let n = 40
let f = fact n
let f2 = fact_iter n
(*Omg ça donne des trucs negatifs*)


(* Test facteur premiers *)
let facts = prime_fact 8
let fACTS = prime_fact 168
let nan_vraiment_les_FACTS = prime_fact 7811


;;