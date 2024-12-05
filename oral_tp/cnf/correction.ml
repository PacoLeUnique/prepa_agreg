type 'a elt ={ 
  vl : 'a;
  mutable nxt : 'a elt option;
  mutable prv : 'a elt option
}
type 'a dlist  = 'a elt option ref

let creeliste ()  = ref None
let empty (t : 'a dlist) : bool = Option.is_none !t
let vl (elt:'a elt) = elt.vl
let first (t: 'a dlist) = !t
let next (elt: 'a elt) = elt.nxt
let prv (elt: 'a elt) = elt.prv

let ins (t : 'a dlist) (vl : 'a) : unit =
  let new_elm = { prv = None; nxt = !t; vl } in
  (match !t with
  | Some oldf -> oldf.prv <- Some new_elm
  | None -> ());
  t := Some new_elm

let rem (t:'a dlist) (elt:'a elt) =
   let { vl=_ ; nxt=nxt ; prv=prv } = elt in
   
   (match prv with
   | Some p -> p.nxt <- nxt
   | None -> t := nxt);
   (match nxt with
   | Some n -> n.prv <- prv
   | None -> ());
   elt.prv <- None;
   elt.nxt <- None
   
let iter (t:'a dlist) ~(f:'a -> unit) =
  let rec loop = function
    | None -> ()
    | Some elt ->
      f (vl elt);
      loop (next elt)
  in
  loop !t

let find (t:'a dlist)  ~(f:'a -> bool) =
  let rec loop = function
    | None -> raise Not_found
    | Some elt -> 
      if f (vl elt) then
       elt
      else
       loop (next elt)
  in
  loop !t

  
;;

let l = creeliste()
let () = assert (empty l)

let _ = ins l 3
let _ = ins l 2
let _ = ins l 1

;;

let _ = iter l ~f:(fun x -> print_int x) 

;;

let deux = find l ~f:(fun x -> x=2)
let () = rem l deux

;;

