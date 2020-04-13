#const k=3.

k { queen(C,Row,Col) : col(Col), row(Row) } k :- color(C).

color(b). color(w).
col(1..5).
row(1..5).

:- queen(w,Rw,Cw), queen(b,Rb,Cb), Rw = Rb.
:- queen(w,Rw,Cw), queen(b,Rb,Cb), Cw = Cb.
:- queen(w,Rw,Cw), queen(b,Rb,Cb), | Rw - Rb | = | Cw - Cb |.

#show queen/3.
