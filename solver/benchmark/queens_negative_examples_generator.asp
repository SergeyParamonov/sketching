#const k=3.

k { queen(C,Row,Col) : col(Col), row(Row) } k :- color(C).

color(b). color(w).
col(1..6).
row(1..6).

fail :- queen(w,Rw,Cw), queen(b,Rb,Cb), Rw = Rb.
fail :- queen(w,Rw,Cw), queen(b,Rb,Cb), Cw = Cb.
fail :- queen(w,Rw,Cw), queen(b,Rb,Cb), | Rw - Rb | = | Cw - Cb |.

:- not fail.

#show queen/3.
