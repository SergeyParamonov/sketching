#const k=3.

k { s(Id) : t(Id,_,_) } k.

:- s(Id1), s(Id2), t(Id1,Indx,V), t(Id2,Indx,V), Id1 != Id2.

t(1,1,1). t(1,2,2). t(1,3,2).
t(2,1,2). t(2,2,1). t(2,3,1).
t(3,1,3). t(3,2,2). t(3,3,3).
t(4,1,3). t(4,2,3). t(4,3,4).

#show s/1.
