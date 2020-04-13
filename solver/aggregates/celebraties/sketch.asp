knows(0,adam,  dan).
knows(0,adam, alice).
knows(0,adam, peter).
knows(0,adam, eva).
knows(0,dan,   adam).
knows(0,dan,alice).
knows(0,dan,peter).
knows(0,eva,alice).
knows(0,eva,peter).
knows(0,alice, peter).
knows(0,peter, alice).
positive(0).
examples(E) :- positive(E).
examples(E) :- negative(E).
% auxiliary extract some info
person(E,X) :- knows(E,_, X).

aggregates(sum). aggregates(count). aggregates(min). aggregates(max). 

1 { num_decision(D) : aggregates(D) } 1.

num_p(E,N) :- N = #count {P:person(E,P)}, examples(E).
% 1) a person is a celebrity if everyone
% knows P
celebrity(E,C) :- 
    person(E,C),
    num_p(E,N),
    N-1 { knows(E,P, C) : person(E,P) } N-1, 
    examples(E).

% 2) and the celebrities only know other
% celebrities, i.e.
% C is not a celebrity if he/she
% knows anyone that is not a celebrity)
:- celebrity(E,C), person(E,C), not celebrity(E,P), knows(E, C, P), examples(E).

#show celebrity/2.
#show num_p/2.
#show num_decision/1.
