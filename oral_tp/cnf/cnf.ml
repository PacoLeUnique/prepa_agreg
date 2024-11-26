

(*Exercice 1*)
type litteral = int
type clause = litteral list
type cnf = clause list 

let get_var l = if l=0 then assert false else abs l


(* Exercice 2 *)

(* Cherche un element dans une liste, et renvoie true si il existe. *)
let rec find elm = function
  | [] -> false
  | x :: l -> if x=elm then true else find elm l

(* Simplification *)
let rec simplifie (l:litteral) (f:cnf) : cnf = 
  match f with 
    | [] -> []
    | clause :: f' -> 
      if find l clause then simplifie l f' (* Si le litteral satisfait la clause, on peut l'ignorer *)
      else 
        (* Sinon, on retire toutes les instances du littéral dans les autres clauses *)
        let new_clause = List.filter (fun x -> get_var l != get_var x) clause in
        
        if (new_clause = []) then 
          simplifie l f' 
        else
          (new_clause :: simplifie l f')


(* Retourne la premiere clause unitaire de f, et renvoie une erreur si il n'y en a pas.*)
let rec clause_unitaire (f:cnf) : litteral list = 
  match f with
  | [] -> raise Not_found 
  | clause :: f' -> 
    match clause with
    | [l] -> [l]
    | _ -> clause_unitaire f'


(* Exercice 3 - 4 *)
type interpretation = bool list

(* Renvoie la variable d'indice maximum d'une clause. *)
let rec max_var_clause (c:clause) : int =
  match c with
  | [] -> 0
  | l :: c' -> max (get_var l) (max_var_clause c')


(* Renvoie la variable d'indice maximum d'une cnf. *)
let rec max_var (f:cnf) : int = 
  match f with
  | [] -> 0
  | c :: f' -> max (max_var_clause c) (max_var f')


(* Renvoie une interprétation qui satisfait f, si f est satisifiable. Sinon, renvoie None. *)
let satisfiable (f:cnf) : interpretation option = 
  let n = max_var f in

  (* Simplifie f sur la variable i, et construit une interprétation valide, pas à pas.*)
  let rec aux (f:cnf) (i:int) (interpret : interpretation) = 
    if i>=n then
      Some interpret
    
    else 
      (* on met i à true*)
      try 
        let c_unit = clause_unitaire f in
        
      with Not_found ->  

      (* on met i à false*)




(* TESTING *)

let test1 : cnf = [[1;2;-3];[2;3];[-1;-2;3];[-1;-3];[1;-2]] 
let test2 : cnf = [[1;-1;-3];[-2;3];[-2]]
let test3 : cnf = [[1;2;3];[-2;3];[-3]]
let test4 : cnf = [[1;2;3];[-1;2;3];[3];[1;-2;-3];[-1;-2;-3];[-3]]
let test5 : cnf = [[1;-2;3];[1;-3];[2;3];[1;-2]]
let test6 : cnf = [[-1;2];[1;-2];[1;-3];[1;2;3];[-1;-2]]


(* Tests 1 *)
let () = assert (get_var (-2) = 2)
let () = assert (get_var 3 = 3)

(* Tests 2 *)
let () = assert (simplifie 1 test1 = [[2;3];[-2;3];[-3]])
let () = assert (simplifie (-3) test4 = [[1;2];[-1;2]])

let () = assert (clause_unitaire test3 = [-3])
let () = assert ((try let _ = clause_unitaire test1 in "pas ok" with Not_found -> "ok") = "ok")

;;
