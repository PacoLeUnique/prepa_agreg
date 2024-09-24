
(* Exo 1*)
type formule = 
  | TRUE 
  | FALSE
  | VAR of string
  | AND of formule * formule
  | OR of formule * formule
  | NOT of formule
  | FORALL of string * formule
  | EXISTS of string * formule
  

let rec exists l elm =
  match l with
  | [] -> false
  | x :: l0 -> if x=elm then true else exists l0 elm
  
  let rec remove l elm = 
    match l with 
    | [] -> []
    | x :: l0 -> if x=elm then l0 else x :: (remove l0 elm)
    
  
(* Exo 2 *)
let var_libres (f : formule) = 
  let rec aux f liees = 
    match f with
    | TRUE -> []
    | FALSE -> []
    | AND (f1,f2) -> (aux f1 liees) @ (aux f2 liees)
    | OR (f1, f2) -> (aux f1 liees) @ (aux f2 liees)
    | NOT f0 -> aux f0 liees
    | FORALL (x, f0) -> aux f0 (x :: liees) 
    | EXISTS (x, f0) -> aux f0 (x :: liees) 
    | VAR x -> if (exists liees x) then [] else [x]
    in
  aux f []
        
        
(* Exo 3 *)
let rec substitue (f : formule) (v : string) (subst : formule) : formule = 
  match f with
    | TRUE -> TRUE
    | FALSE -> FALSE
    | AND (f1,f2) -> AND ((substitue f1 v subst), (substitue f2 v subst))
    | OR (f1,f2) -> OR ((substitue f1 v subst), (substitue f2 v subst))
    | NOT f0 -> NOT (substitue f0 v subst)
    
    | FORALL (y, f0) -> 
      if v=y 
        then FORALL (y, f)
        else FORALL (y, (substitue f0 v subst) )
    
    | EXISTS (y, f0) -> 
      if v=y 
        then f
        else EXISTS (y, (substitue f0 v subst) )
    
    | VAR x -> 
      if x=v
        then subst
        else VAR x 
    
(* Exo 4 *)
let rec expand f = 
  match f with 
    | TRUE -> TRUE
    | FALSE -> FALSE
    | VAR x -> f
    | AND (f1, f2) -> AND (expand f1, expand f2)
    | OR (f1, f2) -> OR (expand f1, expand f2)
    | NOT f0 -> NOT (expand f0)
    | FORALL (x, f0) -> AND ((expand (substitue f0 x TRUE)), (expand (substitue f0 x FALSE)))
    | EXISTS (x, f0) -> OR ((expand (substitue f0 x TRUE)), (expand (substitue f0 x FALSE)))
  
  
(* Exo 5 *)
let rec eval f = 
  (* Précondition : f est close*)
  match f with 
  | TRUE -> true
  | FALSE -> false
  | VAR _ -> raise (Invalid_argument "la formule n'est pas close") 
  | AND (f1, f2) -> ((eval f1) && (eval f2))
  | OR (f1, f2) -> (eval f1) || (eval f2)
  | NOT f0 -> not (eval f0)
  | FORALL (x, f0) -> eval (expand f)
  | EXISTS (x, f0) -> eval (expand f)

  
(* ============ TEST ===========*)

let x = VAR "x" 
let y = VAR "y"
let z = VAR "z"


let (&) a b = AND (a,b)
let (^) a b = OR (a,b)
let (!) a = NOT a

(* Mes formules *)
let f = FORALL ("z" ,EXISTS ("y", (!z ^ EXISTS ("x", (y & FALSE)))))
let e = EXISTS ("x", AND(x, y))
let a = FORALL ("x", OR(x, y)) 
let f2 = substitue f "x" (VAR "GROS CACA")


(* Variables libres *)
let vf = var_libres f
let vg = var_libres e


(* On enleve les quantificateurs *)
let eee = expand e
let aaa = expand a

let b = eval f
let _ = if b then print_endline "vrai" else print_endline "faux"

;;


