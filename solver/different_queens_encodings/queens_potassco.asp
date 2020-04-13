#const n = 8.

{ queen(1..n,1..n) }.

 :- not { queen(I,J) } == n.
 :- queen(I,J), queen(I,JJ), J != JJ.
 :- queen(I,J), queen(II,J), I != II.
 :- queen(I,J), queen(II,JJ), I != II, J != JJ, I-J == II-JJ.
 :- queen(I,J), queen(II,JJ), I != II, J != JJ, I+J == II+JJ.

