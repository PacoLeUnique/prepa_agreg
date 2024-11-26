type var = string
type state = var -> int

type aexp = N of int | Var of var | Plus of aexp*aexp | Moins of aexp*aexp | Mul of aexp*aexp
type bexp = True | False | Lq of aexp*aexp | Not of bexp
type cexp = Skip | Aff of var * aexp | If of bexp*cexp*cexp | While of bexp*cexp | Instr of cexp*cexp  

let (state0 : state) = fun (v: var) -> 0 


(* PARTIE 1 - EVALUATION DU LANGAGE *)

(* Question 2 *)
let state_set (s:state) (var:var) (v:int) : state = 
  fun x -> if x=var then v else s x

(* Question 3 *)
let rec aeval (state : state) a = match a with
  | N n -> n
  | Var v -> state v
  | Plus (a1, a2) -> aeval state a1 + aeval state a2
  | Moins (a1, a2) -> aeval state a1 - aeval state a2
  | Mul (a1, a2) -> aeval state a1 * aeval state a2
  

let rec beval state b = match b with
  | True -> true
  | False -> false
  | Lq (a1, a2) -> aeval state a1 < aeval state a2
  | Not b0 -> not (beval state b0)
  

let rec eval state c = match c with
  | Skip -> state
  | Aff(x, a) -> state_set state x (aeval state a)
  | If(b, c1, c2) -> if (beval state b) then eval state c1 else eval state c2
  | While(b, c0) -> if (beval state b) then eval (eval state c0) c else state
  | Instr(c1, c2) -> eval (eval state c1) c2


(* PARTIE 3 - REDUCTION *)

let rec ared (state:state) (a:aexp) = match a with
  | N n -> None
  | Var v -> Some (N (state v)) 
  
  | Plus(N m, N n) -> Some(N (m+n))
  | Plus(N n, a0) -> Option.bind (ared state a0) (fun a' -> Some(Plus(N n, a')))
  | Plus(a1, a2) -> Option.bind (ared state a1) (fun a' -> Some(Plus(a', a2)))

  | Moins(N m, N n) -> Some(N (m-n))
  | Moins(N n, a0) -> Option.bind (ared state a0) (fun a' -> Some(Moins(N n, a')))
  | Moins(a1, a2) -> Option.bind (ared state a1) (fun a' -> Some(Moins(a', a2)))
  
  | Mul(N m, N n) -> Some(N (m*n))
  | Mul(N n, a0) -> Option.bind (ared state a0) (fun a' -> Some(Mul(N n, a')))
  | Mul(a1, a2) -> Option.bind (ared state a1) (fun a' -> Some(Mul(a', a2)))
  

let rec bred (state:state) (b:bexp) = match b with
  | True -> None
  | False -> None

  | Not False -> Some True
  | Not True -> Some False
  | Not b0 -> Option.bind (bred state b0) (fun b0 -> Some(Not b0))

  | Lq(N n, N m) -> if n < m then Some True else Some False
  | Lq(N n, a) -> Option.bind (ared state a) (fun a' -> Some(Lq(N n, a')))
  | Lq(a1, a2) -> Option.bind (ared state a1) (fun a' -> Some(Lq(a', a2)))


let rec red (state:state) c = match c with
  | Skip -> None
  
  | Instr(Skip, c0) -> Some (c0, state)
  | Instr(c1 ,c2) -> Option.bind (red state c1) (fun (c',state') -> Some( Instr(c', c2), state' ))

  | Aff(v, N n) -> Some (Skip, (state_set state v n))
  | Aff(v, a) -> Option.bind (ared state a) (fun a' -> Some(Aff(v, a'), state))

  | If(True, c1, c2) -> Some(c1, state)
  | If(False, c1, c2) -> Some(c2, state)
  | If(b, c1, c2) -> Option.bind (bred state b) (fun b' -> Some ( If(b',c1,c2) , state))

  | While(b, c) -> Some( If(b, Instr(c, While(b,c)), Skip) , state)


let rec eval2 state c = 
  match red state c with 
    | None -> state
    | Some (c', state') -> eval2 state' c' 


(*====================================
  ============== TESTING =============
  ====================================*)

(* Factorielle *)
let fact = (
  Instr(Aff("y", N 1), 
  While(Not(Lq(Var "x", N 1)), 
    Instr(Aff("y", Mul(Var "y", Var "x")), 
    Aff("x", Moins(Var "x", N 1)))))
)

(* Division euclidienne *)
let div (a: var) (b : var) = ( 
  Instr(Aff("q", N 0),
  Instr(
  While(Not (Lq(Moins(Var a, Var b), N 0)), 
    Instr(Aff(a, Moins(Var a, Var b)),
    Aff("q", Plus(Var "q", N 1)))),
  Aff("r", Var a)
  ))
)


let () = 
  let s = state_set state0 "x" 5 in 
  let s = eval2 s fact in

  assert (s "y" = 120)
  

let () = 
  let s = state_set state0 "a" 279 in
  let s = state_set s "b" 15 in

  let s = eval2 s (div "a" "b") in
  let q = s "q" in
  let r = s "r" in

  assert (q=18 && r=9)


let a = Plus(Var "b", Mul(Plus(Moins(N 0, Var "a"), N 10), N 5))
let b = Not (Lq(a, N 6)) 

let s = state_set state0 "a" 6
let s = state_set s "b" 2
  
let r1 = bred s b
let r2 = Option.bind r1 (bred s)
let r3 = Option.bind r2 (bred s)
let r4 = Option.bind r3 (bred s)
let r5 = Option.bind r4 (bred s)
let r6 = Option.bind r5 (bred s)
let r7 = Option.bind r6 (bred s)
let r8 = Option.bind r7 (bred s)
let r9 = Option.bind r8 (bred s)
let r10 = Option.bind r9 (bred s)



;;

