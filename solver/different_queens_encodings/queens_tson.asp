#const n = 8.

row(1..n). % n row
col(1..n). % n col
%% generating solutions
1 {cell(I,J) : row(J)} 1:- col(I).
% two queens cannot be on the same row/column
:- col(I), row(J1), row(J2), J1 != J2, cell(I,J1), cell(I,J2).
:- row(J), col(I1), col(I2), I1 != I2, cell(I1,J), cell(I2,J).
% two queens cannot be on a diagonal
:- row(J1), row(J2), J1 > J2, col(I1), col(I2), I1 > I2, cell(I1,J1), cell(I2,J2), I1 - I2 == J1 - J2.
:- row(J1), row(J2), J1 > J2, col(I1), col(I2), I1 < I2, cell(I1,J1), cell(I2,J2), I2 - I1 == J1 - J2.
