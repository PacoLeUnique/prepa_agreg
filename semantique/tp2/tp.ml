
(* 1 - Inférence de type *)

(* Exercice 1-2 *)
type typ = Int | Bool | Fun of typ*typ | Pair of typ * typ

type prog =
  | N of int | B of bool | Var of string 
  | Add | Abs of (string * typ) * prog | App of prog * prog | Pair of prog*prog
  | Fst of prog | Snd of prog 


(* 3. *)
let rec infer env p = 
  match p with
  | N n -> Int
  | B b -> Bool
  | Var x -> List.assoc x env
  | Add -> Fun (Fun(Int, Int), Int)
  
  | Pair(p1, p2) -> Pair(infer env p1, infer env p2)
  
  | Fst (Pair(a, b)) -> infer env a 
  | Snd (Pair(a,b)) -> infer env b
  
  | Abs ((x,t), p') -> Fun(t, infer ((x,t) :: env) p')
  
  | App(Add, _) -> Fun(Int, Int)
  | App(App(Add, x), y) -> Int
  | App(Abs ((x,t), p1), p2) -> 
    if infer env p2 != t then raise Not_found else infer env p1

  | Fst _ | Snd _ | App(_, _) -> raise Not_found


let rec typable p = match p with
  | 


;;

(* ================= Testing ================ *)
let plus x y = App(App(Add, x), y)


let a = Pair(plus (N 3) (N 2), B true) 
let b = App(Abs(("x", Int), plus (Var "x") (N 1)), N 2) 

;;
let ta = infer [] a 
let tb = infer [] b


;;
let () = assert (infer [] a = Pair(Int, Bool))


;;