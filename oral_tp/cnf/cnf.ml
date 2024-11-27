

(*Exercice 1*)
type litteral = int
type clause = litteral list
type cnf = clause list 

let get_var l = abs l


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
      let sf' = simplifie l f' in 
      if sf' = [[]] then [[]] 
      else 

      if find l clause then sf' (* Si le litteral satisfait la clause, on peut l'ignorer *)
      else 
        (* Sinon, on retire toutes les instances du littéral dans les autres clauses *)
        let new_clause = List.filter (fun x -> get_var l != get_var x) clause in
        
        if (new_clause = []) then 
          [[]] (* J'ai une clause incompatible, la cnf est incompatible *)
        else
          (new_clause :: sf')


(* Retourne la premiere clause unitaire de f, et renvoie une erreur si il n'y en a pas.*)
let rec clause_unitaire (f:cnf) : litteral list = 
  match f with
  | [] -> raise Not_found 
  | clause :: f' -> 
    match clause with
    | [l] -> [l]
    | _ -> clause_unitaire f'


(* Renvoie toutes les littéraux des clauses unitaires de f, pour une variable choisie. *)
let rec litteraux_unitaires (f:cnf) i = 
  match f with
  | [] -> []
  | clause :: f' -> 
    match clause with 
    | [l] -> if get_var l = i then l :: litteraux_unitaires f' i else litteraux_unitaires f' i 
    | _ -> litteraux_unitaires f' i

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
 

let rec string_of_list l = match l with
| [] -> ""
| x:: l' -> (string_of_int x) ^ "," ^ string_of_list l' 
      
let rec string_of_cnf f = match f with
| [] -> ""
| clause :: f' -> "[" ^ string_of_list clause ^ "]" ^ string_of_cnf f'



let solve2 (f:cnf) : interpretation option = 
  let n = max_var f in

  (* Simplifie f sur le litteral i, et construit une interprétation valide, pas à pas.*)
  let rec aux (f:cnf) (l:litteral) (interpret : interpretation) = 

    (* Si f est une clause incompatible, c'est perdu *)
    if f = [[]] then None 
    else 

    (* on teste les clauses unitaires *)
    let i = get_var l in
    let signe l = l > 0 in
    let l_units = litteraux_unitaires f i in 
    
    (* Si l'une des clauses unitaires ne vérifie pas l'interprétation, c'est mort *)
    if List.exists (fun x -> signe x != signe l) l_units then None 
    else 
    
    (* Si on a testé toutes les variables, on a fini, l'interprétation est bonne *)
    if i >= n 
      then Some interpret 
    else 
    
        (* Sinon, on peut continuer d'explorer les branches récursivement *)
        let simplif_true = aux (simplifie l f) (i+1) (true :: interpret) in
        match simplif_true with 
        | None -> aux (simplifie l f) (-(i+1)) (false :: interpret)
        | Some res -> Some res  
    in
  
    (* Attention ! aux renvoie la liste dans le sens inverse. Il faut la renverser *)
    if n=0 then None
    else 
      let first_true = aux f 1 [true] in
      match first_true with
      | Some interpret -> Some (List.rev interpret)
      | None -> Option.bind (aux f (-1) [false]) (fun x -> Some (List.rev x))




(* 3. INTERPRETATIONS MUTABLES *)
type pinterpretation = bool option array

(* 6. *)


(* ============= *)
(* == TESTING == *)
(* ============= *)

let test1 : cnf = [[1;2;-3];[2;3];[-1;-2;3];[-1;-3];[1;-2]] 
let test2 : cnf = [[1;-1;-3];[-2;3];[-2]]
let test3 : cnf = [[1;2;3];[-2;3];[-3]]
let test4 : cnf = [[1;2;3];[-1;2;3];[3];[1;-2;-3];[-1;-2;-3];[-3]]
let test5 : cnf = [[1;-2;3];[1;-3];[2;3];[1;-2]]
let test6 : cnf = [[-1;2];[1;-2];[1;-3];[1;2;3];[-1;-2]]


(* Tests 1 *)
let () = assert (get_var (-2) = 2)
let () = assert (get_var 3 = 3)

let a = simplifie 1 test1

(* Tests 2 *)
let () = assert (simplifie 1 test1 = [[2;3];[-2;3];[-3]])
let () = assert (simplifie (-3) test4 = [[]])

let () = assert (simplifie 1 test2 = [[-2;3];[-2]])
let () = assert (simplifie (-1) test2 = [[-2;3];[-2]])


let () = assert (clause_unitaire test3 = [-3])
let () = assert ((try let _ = clause_unitaire test1 in "pas ok" with Not_found -> "ok") = "ok")

let () = assert (litteraux_unitaires test1 2 = [])
let () = assert (litteraux_unitaires test4 3 = [3;-3])  

(* Tests solve *)
let sat1 = solve2 test1 
let sat2 = solve2 test2
let sat3 = solve2 test3
let sat4 = solve2 test4


let () = assert (solve2 [[]] = None)
let () = assert (solve2 [[1]] = Some [true])
let () = assert (solve2 [[-1]] = Some [false])
let () = assert (solve2 [[1]; [-1]] = None)

(* let f = [[2]; [-1;-2]]
let s1 = simplifie (-1) f



let e = solve2 f
 *)

;;
