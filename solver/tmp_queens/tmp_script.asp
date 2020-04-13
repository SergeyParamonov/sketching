% some constraints on rows, columns and diagonals
[SKETCH]
:- queen(R1,C1) & queen(R2,C2) & R1 ?= R2 & C1 != C2.
:- queen(R1,C1) & queen(R2,C2) & R1 ?= R2 & C1 = C2.
:- queen(R1,C1) & queen(R2,C2) & R1 ?= R2 & | R1 - R2 | ?= [ C1 ?+ C2 ] .

[DOMAIN]
?= : -10..20
?+ : -10..20



[PREFERENCES]
?= : = -> max, != -> max.

[EXAMPLES]


positive : queen(1,6). queen(8,3). queen(7,5). queen(4,4). queen(6,7). queen(3,2). queen(2,8). queen(5,1). 
positive : queen(4,8). queen(1,7). queen(7,2). queen(2,1). queen(3,3). queen(8,5). queen(5,6). queen(6,4). 
positive : queen(8,4). queen(5,2). queen(6,8). queen(2,3). queen(3,1). queen(7,6). queen(4,7). queen(1,5). 
positive : queen(8,4). queen(4,1). queen(6,8). queen(1,7). queen(2,5). queen(7,2). queen(3,3). queen(5,6). 
positive : queen(1,2). queen(4,8). queen(8,3). queen(3,5). queen(7,6). queen(5,1). queen(2,7). queen(6,4). 
positive : queen(5,2). queen(4,4). queen(6,7). queen(8,6). queen(2,1). queen(3,8). queen(7,3). queen(1,5). 
positive : queen(5,2). queen(6,8). queen(8,3). queen(4,4). queen(3,1). queen(7,6). queen(1,5). queen(2,7). 
positive : queen(5,7). queen(2,6). queen(7,2). queen(4,3). queen(1,1). queen(3,8). queen(8,5). queen(6,4). 
positive : queen(4,4). queen(1,3). queen(6,7). queen(2,5). queen(8,6). queen(7,2). queen(3,8). queen(5,1). 
positive : queen(6,8). queen(7,1). queen(2,2). queen(4,3). queen(1,4). queen(3,7). queen(8,5). queen(5,6). 
negative : queen(4,1). queen(1,6). queen(8,7). queen(1,7). queen(8,2). queen(1,1). queen(8,1). queen(1,2). 
negative : queen(4,1). queen(1,6). queen(8,7). queen(8,6). queen(1,1). queen(6,1). queen(8,5). queen(1,2). 
negative : queen(1,6). queen(1,3). queen(8,7). queen(7,1). queen(1,7). queen(8,1). queen(7,8). queen(1,2). 
negative : queen(8,4). queen(1,6). queen(8,7). queen(8,6). queen(6,1). queen(3,8). queen(7,8). queen(1,2). 
negative : queen(8,4). queen(8,7). queen(7,1). queen(8,6). queen(6,1). queen(8,1). queen(7,8). queen(1,2). 
negative : queen(8,4). queen(4,1). queen(1,3). queen(1,7). queen(8,2). queen(1,1). queen(8,1). queen(7,8). 
negative : queen(4,1). queen(6,8). queen(1,6). queen(8,7). queen(5,8). queen(8,2). queen(8,6). queen(3,8). 
negative : queen(1,6). queen(8,3). queen(1,7). queen(8,6). queen(1,1). queen(8,5). queen(7,8). queen(1,2). 
negative : queen(4,1). queen(6,8). queen(8,2). queen(8,6). queen(1,1). queen(6,1). queen(8,1). queen(7,8). 
negative : queen(7,1). queen(8,6). queen(1,1). queen(6,1). queen(3,8). queen(8,1). queen(7,8). queen(1,2). 
