
(* Exo 1 *)
let min l = 
  if l = [] then raise (Invalid_argument "La liste doit pas etre vide")
  else 
    let m a b = if a < b then a else b in
    List.fold_left m (List.hd l) l

let somme a = Array.fold_left (+) 0 a 

let is_trie l = 
  if l = [] then raise (Invalid_argument "La liste est vide bf")
  else
    let exception PasTrie in 
    let current = ref (List.hd l) in

    let f a = if a >= !current then current := a else raise PasTrie in
    try
      List.iter f l;
      true
    with PasTrie -> false

let list_to_array l =
  let f a b = Array.append a [|b|] in
  List.fold_left f [||] l

let array_to_list a =
  let f a b = List.append a [b] in
  Array.fold_left f [] a


(* Exo 2 *)
(* Incrémente chaque valeur du tableau a de x*)
let increment a n = Array.map (fun x -> x+n) a


(* Exo 3 *)

(* Applique f( f( f( ... (f x)))) n fois.*)
let rec iter f n x =
  if n < 1 then raise (Invalid_argument "n doit etre >= 2")
  else
    if n = 1 then f x 
    else iter f (n-1) (f x)


(* Exo 4 *)

(* Prends une liste de prédicat (donc de type 'a->bool), une valeur (donc de type 'a) 
   et renvoie le résulat de tous les prédicats sur cette valeur.*)
let teste_predicats (l : ('a->bool) list) (n : 'a) : bool list =
  let teste_sur_n pred = pred n in
  List.map teste_sur_n l


(* Exo 5 *)

(* Renvoie la somme des fi, pour i=debut à fin.
   comme la somme en math. *)
let sum debut fin f = 
  let s = ref 0 in
  for index=debut to fin do
    s := !s + (f index) 
  done;
  !s


(* Exo 6 *)
let wrap a = fun () -> a



(* =====================*)
(* ======TEST EXOS======*)
(* =====================*)


(* Test exo 1 *)
let l = [5;4;1;6;0;2;4;0;3;7]
let l2 = [1;2;3;4;5;6;7;8]
let m = min l

let tri = is_trie l
let tri2 = is_trie l2

let a = list_to_array l
let a2 = array_to_list a

(* Test exo 2 *)
let a_incr = increment a 100

(* test exo 3 *)
let yoooo = iter (fun x->2*x) 11 1

(* Test exo 5 *)
let un_to_cent = sum 1 100 (fun i-> i*i)

(* Test exo 6 *)
let renvoie_32 = wrap 32
let trente_deux = renvoie_32() 

;;