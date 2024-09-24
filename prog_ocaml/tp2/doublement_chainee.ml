
module Double_liste = 
  struct
    type 'a bloc = {v : 'a; 
                    mutable next : 'a bloc option; 
                    mutable prev : 'a bloc option }

    type 'a double_liste = {mutable tete : 'a bloc option}
    
    (*    let empty_bloc = {v = None; next = None; prev = None} *)
    let single_bloc v = {v = v; next = None; prev = None} 
    
    let empty = {tete = None}

    let single valeur = 
      let first = single_bloc valeur in
      {tete = Some first}
    
    let is_empty l = 
      match l with 
      | {tete = Some empty_bloc} -> true
      | _ -> false 

    let head l = l.tete
    
    let print l = 

      let rec bloc_to_string b = 
        match b with
        | None -> ""
        | Some bloc -> string_of_int bloc.v ^ " " ^ (bloc_to_string (bloc.next))
      in

      print_endline ("[ " ^ (bloc_to_string (l.tete)) ^ "]")

    let push l e = 
      match (head l) with
      | None -> (l.tete <- Some (single_bloc e)) 
      | Some bloc -> 
        let new_bloc = single_bloc e in
        
        (l.tete <- Some new_bloc;
        new_bloc.next <- Some bloc;
        bloc.prev <- Some new_bloc;)

    let len l = 
      let rec aux b = 
        match b with
        | None -> 0
        | Some bloc -> 1 + aux bloc.next
        in
      aux l.tete

    let get l elm = 
      let exception PasTrouve in

      let rec get_b b elm acc = 
        match b with 
        | None -> raise PasTrouve
        | Some bloc -> 
            if bloc.v = elm then acc 
            else get_b (bloc.next) elm (acc+1)
      in
      get_b (l.tete) elm 0


      let is l1 l2 = (l1 == l2)

      



  end


let e = Double_liste.empty
let l = Double_liste.single 5

let _ = Double_liste.push l 3
let _ = Double_liste.print l


;;


(*
module Double_liste : 
  sig
    
    val empty : 'a bloc
    val append : 'a -> 'a bloc
    val is_empty : 'a bloc -> bool
    val len : 'a bloc -> int
    val get : 'a bloc -> int -> 'a
    val insert : 'a bloc -> int -> 'a bloc

  end

  *)
;;