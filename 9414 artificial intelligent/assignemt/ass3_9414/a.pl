insert(N,[],[N]).
insert(N,[H|T],[N,H|T]):-
    N=<H.
insert(N,[H|T],[H|T1]):-
    N>H,
    insert(N,T,T1).

isort([],[]).
%isort([H|T],L):-
%    isort(T,TS),
%    insert(H,TS,L).

isort([H|T],L):-
    insert(H,TS,L),
    isort(T,TS).