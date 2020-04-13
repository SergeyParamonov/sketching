% Problem: Given a list of people at a party and for each person the list of
% people they know at the party, we want to find the celebrities at the party. 
% A celebrity is a person that everybody at the party knows but that 
% only knows other celebrities. At least one celebrity is present at the party.

people(adam).
people(dan).
people(eva).
people(alice).
people(peter).

knows(adam,  dan).
knows(adam, alice).
knows(adam, peter).
knows(adam, eva).
knows(dan,   adam).
knows(dan,alice).
knows(dan,peter).
knows(eva,   alice).
knows(eva,peter).
%knows(alice, peter).
knows(peter, alice).
% auxiliary extract some info
person(X) :- knows(_, X).
num_p(N) :- N = #count {P:person(P)}.
% 1) a person is a celebrity if everyone
% knows P
celebrity(C) :- 
    person(C),
    num_p(N),
    N-1 { knows(P, C) : person(P) } N-1.

% 2) and the celebrities only know other
% celebrities, i.e.
% C is not a celebrity if he/she
% knows anyone that is not a celebrity)
:- celebrity(C), person(C), not celebrity(P), knows(C, P).

#show celebrity/1.
#show num_p/1.
