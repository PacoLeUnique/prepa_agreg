
(*Exercice 1*)
type litteral = int
type clause = litteral list
type cnf = clause list 

type interpretation = bool list


let get_var l = abs l
let signe l = l > 0


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



let solve (f:cnf) : interpretation option = 
  let n = max_var f in

  (* Simplifie f sur le litteral l, et construit une interprétation valide, pas à pas.*)
  let rec aux (f:cnf) (l:litteral) (interpret : interpretation) = 

    (* Si f est une clause incompatible, c'est perdu *)
    if f = [[]] then None 
    else 

    (* on teste les clauses unitaires *)
    let i = get_var l in
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
      let res = (aux f 0 []) in
      match res with
      | None -> None
      | Some interpretation -> Some (List.rev interpretation)


;;






(* 3. INTERPRETATIONS MUTABLES *)
type pinterpretation = bool option array

(* Exercice 6 *)

(* Renvoie le 1er littéral vide d'une interprétation partielle. Renvoie Not_found si il n'y en a pas. *)
let rec premier_litteral_vide (p : pinterpretation) = 
  if p = [||] then raise Not_found
  else

    let n = Array.length p in
    let r = ref (-1) in 

    for i=0 to (n-1) do
      if p.(i) = None && (!r = -1) 
      then r := i + 1
      else ()
    done;

    if !r = -1 then raise Not_found
    else !r
        

let is_litteral_satisfait (p: pinterpretation) (l:litteral) =
  match p.(get_var l - 1) with
  | None -> false
  | Some b -> 
    b = signe l 


  

(* Exercice 7 *)
(* Renvoie vrai si f est satisfaite dans l'interprétation partielle p. *)
let rec is_satisfaite (f:cnf) (p:pinterpretation) = 
  match f with
  | [] -> true
  | clause :: f' -> List.exists (fun l -> is_litteral_satisfait p l) clause && (is_satisfaite f' p)


(* Renvoie vrai si f est insatisfaite dans l'interprétation partielle p. *)
let is_instatisfaite f p = 
  let rec aux f p = 
    match f with 
    | [] -> true
    | clause :: f' -> List.for_all (fun l -> not (is_litteral_satisfait p l)) clause && (aux f' p)
  in 
  
  if f = [] then false else aux f p


(* Exercice 8 *)
type historique = int Stack.t
exception Incompatible

(* Complète une interprétation partielle pour satisfaire le littéral l. *)
let satisfait_litteral (l:litteral) (p:pinterpretation) (h:historique) = 
  let i = get_var l - 1 in

  match p.(i) with 
  | Some eval -> 
    if signe l = eval then ()
    else raise Incompatible 
  
  | None -> (
    Stack.push (get_var l) h; (* on garde en mémoire dans l'historique *)
    p.(i) <- Some (signe l);
  )


(* Exercice 9 *)
(* Efface chaque interprétation partielle depuis le dernier point de choix. *)
let annule_choix (p:pinterpretation) (h:historique) = 
  
  while not(Stack.is_empty h) && Stack.top h != 0 do 
    let i = Stack.pop h in  (* On retire la variable... *)
    p.(i - 1) <- None       (* ...Et on retire sa valeur dans l'interprétation. *)
  done;
  
  if not(Stack.is_empty h) then 
    let _ = Stack.pop h in (* Et on retire le 0 *)
  ()


(* Exercice 10 *)
(* Ajoute tous les littéraux unitaires de f dans l'interprétation partielle et l'historique.
  Si des littéraux sont incompatibles avec l'expression, renvoie une erreur. *)
let rec ajoute_litteraux_unitaires f p h = 
  (* pour toutes les clauses : 
    si clause est unitaire : on l'ajoute
    si erreur : on propage l'erreur*)

    match f with 
    | [] -> ()
    | clause :: f' -> (
      match clause with 
      | [] -> ajoute_litteraux_unitaires f' p h
      | [l] -> (  (* Si clause unitaire : on complète notre interprétation partielle *)
        try 
          satisfait_litteral l p h;
          ajoute_litteraux_unitaires f' p h
        with Incompatible -> raise Incompatible
        )
      
      | _ -> ajoute_litteraux_unitaires f' p h
    )
    

(* Exercice 11 *)
(* cherche une interprétaton satisfaisant f. *)
let rec solve2 (f:cnf) : pinterpretation option = 

  let rec aux f p h = 
    (* 
     - si p satisfait f, on peut s'arreter, c'est gagné
     - si il n'y a plus de littéraux vide et que p instatisfait f, c'est perdu 

     - Chercher les clauses unitaires de f
      - Si il y en a, on complète 
        - Si incompatible, c'est perdu
      
     - on prend le 1er littéral vide, et on fait un choix arbitraire (true false)
      - si compatible avec true -> renvoyer la réponse
      - sinon -> vider l'historique, et tester avec false
    *)

    if is_satisfaite f p then Some p 
    else 

    (* On complète p avec les littéreaux unitaires *)
    try 
      ajoute_litteraux_unitaires f p h; 
      
      (* On prend le 1er littéral vide, et on teste les 2 cas de figure*)
      try
        let l = premier_litteral_vide p in 
        Stack.push 0 h;
        p.(l - 1) <- Some true;

        let true_branch = aux f p h in
        match true_branch with
        | Some interpretation -> Some interpretation
        | None -> (
          annule_choix p h;
          p.(l - 1) <- Some false;
          aux f p h
        )

      (* Pas de littéraux vides, on a complété notre interprétation *)
      with Not_found -> 
        if is_satisfaite f p then Some p else None    
    
    (* On est arrivé à une contradiction dans l'ajout des littéreaux unitaires
      -> interprétation ne satisfait pas f *)
    with Incompatible -> None  
  in
  
  let n = max_var f in 
  aux f (Array.make n None) (Stack.create())











(* ===================================================== *)
(* ====================== TESTING ====================== *)
(* ==================================================== *)


(* Fonctions de printage -- pour le debug*)
let rec string_of_list l = match l with
| [] -> ""
| x:: l' -> (string_of_int x) ^ "," ^ string_of_list l' 
      
let rec string_of_cnf f = match f with
| [] -> ""
| clause :: f' -> "[" ^ string_of_list clause ^ "]" ^ string_of_cnf f'



let test1 : cnf = [[1;2;-3];[2;3];[-1;-2;3];[-1;-3];[1;-2]] 
let test2 : cnf = [[1;-1;-3];[-2;3];[-2]]
let test3 : cnf = [[1;2;3];[-2;3];[-3]]
let test4 : cnf = [[1;2;3];[-1;2;3];[3];[1;-2;-3];[-1;-2;-3];[-3]]
let test5 : cnf = [[1;-2;3];[1;-3];[2;3];[1;-2]]
let test6 : cnf = [[-1;2];[1;-2];[1;-3];[1;2;3];[-1;-2]]

;;

(* Tests 1 *)
let () = assert (get_var (-2) = 2)
let () = assert (get_var 3 = 3)
;;


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
;;


(* Tests solve *)
let sat1 = solve test1 
let sat2 = solve test2
let sat3 = solve test3
let sat4 = solve test4
let sat5 = solve test5
let sat6 = solve test6

;;

let () = assert (solve [[]] = None)
let () = assert (solve [[1]] = Some [true])
let () = assert (solve [[-1]] = Some [false])
let () = assert (solve [[1]; [-1]] = None)

;;


(* 3 - interprétations mutables *)
let p1 = [|Some true; Some false; None|]
let p2 = [|None; None; None|]
let p3 = [|Some true; Some false; Some false|]
let p4 = [|None; Some true; None|]

;;

(* Tests 6 *)
let () = assert (premier_litteral_vide p1 = 3)
let () = assert (premier_litteral_vide p2 = 1)
let () = assert ((try let _ = premier_litteral_vide p3 in "pas ok" with Not_found -> "ok") = "ok")

let () = assert (is_litteral_satisfait p1 1)
let () = assert  (not (is_litteral_satisfait p1 (-1)))
let () = assert (not (is_litteral_satisfait p2 3))

;;

(* Tests 7 *)
let () = assert (not (is_satisfaite test1 p2))
let () = assert (is_satisfaite test2 p1)

let () = assert (is_instatisfaite test4 p2)
let () = assert (is_instatisfaite test2 p4)

;; 

(* Tests 8-9 *)
let (h:historique) = Stack.create()

let () = (
  satisfait_litteral (-1) p2 h;
  satisfait_litteral 3 p2 h;
  
  assert (p2 = [|Some false; None; Some true|]);
  assert (Stack.length h = 2);
  assert (Stack.top h = 3);

  annule_choix p2 h;
  assert (p2 = [|None; None; None|]);
  assert (Stack.length h = 0);

)

;;

(* Test 11 *)
let p1 = solve2 test1
let p2 = solve2 test2
let p3 = solve2 test3
let p4 = solve2 test4
let p5 = solve2 test5
let p6 = solve2 test6

;;