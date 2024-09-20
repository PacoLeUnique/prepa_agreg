
module Double_liste = 
  struct
    type 'a bloc = {v : 'a; mutable next : 'a bloc option; prev : 'a bloc option }
    
    let empty = {v = None; next = None; prev = None}
    
    let single valeur = {v = valeur; next = None; prev = None}
    
    let is_empty l = 
      match l with 
      | {v=None; next=None; prev=None} -> true
      | _ -> false 

    let push l e = 

  end


let e = Double_liste.empty
let l = Double_liste.single 5
let l2 = Double_liste.append l 3


;;


(*
module Double_liste : 
  sig
    type 'a bloc = { v : 'a; next : 'a bloc option; prev : 'a bloc option }
    
    val empty : 'a bloc
    val append : 'a -> 'a bloc
    val is_empty : 'a bloc -> bool
    val len : 'a bloc -> int
    val get : 'a bloc -> int -> 'a
    val insert : 'a bloc -> int -> 'a bloc

  end

  *)
;;