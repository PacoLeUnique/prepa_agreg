type 'a elt =
  { vl : 'a
  ; mutable nxt : 'a elt option
  ; mutable prv : 'a elt option  (* ';' pas alignés*)
  }
type 'a dlist  = 'a elt option ref
let crdlist ()  = ref None
let edl t = Option.is_none !t 
let v e  = e.vl               
let f t    = !t
let n e   = e.nxt
let prv e   = e.prv
let ins t vl = 
  let ne = { prv = None; nxt = !t; vl } in
  (match !t with
  | Some oldf -> oldf.prv <- Some ne 
  | None           -> ()); 
  t := Some ne

let rem (t:'a dlist) (e:'a elt) =  
   let { prv; nxt; _ } = e in       
   (match prv with                  
   | Some p -> p.nxt <- nxt
   | None -> t := nxt);            
   (match nxt with
   | Some n -> n.prv <- prv
   | None -> ());
   e.prv <- None;
   e.nxt <- None
   
let iter (t:'a dlist) ~(f:'a elt -> unit) = 
  let rec loop = function 
    | None -> ()
    | Some el ->
      f el;
      loop (n el)
  in
  loop !t

let find t ~f =
  let rec loop = function
    | None -> None
    | Some elt -> if f (v elt) then Some elt else loop (n elt)
  in
  loop !t

;;