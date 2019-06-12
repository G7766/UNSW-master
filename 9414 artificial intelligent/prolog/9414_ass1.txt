%Name:Guan PeiGuo 
%Student Number:z5143964
%Assignment Name: Assignment 1 - Prolog Programming 

%q1

%empty list
sumsq_neg([],0).
%nonempty list
sumsq_neg([Item|Rest],Sum):-
	Item <0,
	sumsq_neg(Rest,SumOfNeg),
	Sum is Item * Item + SumOfNeg.	  
sumsq_neg([Item|Rest],Sum):-
	Item >=0,
	sumsq_neg(Rest,SumOfNeg),
	Sum is SumOfNeg.



%q2

%likes(Who,What):Who likes What. 
all_like_all([],[]).
all_like_all([],[WhatI|WhatR]):-
	not(likes(X,WhatI)),
	all_like_all(X,WhatR).
all_like_all([WhoI|WhoR],[]):-
	not(likes(WhoI,X)),
	all_like_all(WhoR,X).
all_like_all([WhoI|WhoR],[WhatI|WhatR]):-
	likes(WhoI,WhatI),
	all_like_all(WhoR,WhatR).


%q3
%sqrt_table(N, M, Result):N>=M,Result is N's square root,M number.
sqrt_table(0,0,[]).
sqrt_table(N,M,Result):-
	N>=M,
	M>=0,
	P is N-1,
	SS is sqrt(N),
	Head=[N,SS],
	Result=[Head|Result1],
	sqrt_table(P,M,Result1).

sqrt_table(X,Y,Result):-
	X=Y,
	SS is sqrt(X),
	Head=[X,SS],
	Result=[Head|[]].





%q4
%chop_up(List, NewList):takes list and binds NewList to list with all sequences of %successive increasing whole numbers replaced by a two-item list containing only the first %and last number in the sequence.

chop_up(NewList,Result) :- 
	chop_up(NewList, Result, [], []).

chop_up([], NewList, NewList, []).

chop_up([], NewList, Acum, [HT|TT]):-
        get_first_last([HT|TT],Head_LT),
        append(Acum,Head_LT,NewList).

chop_up([HeadList|TailList], NewList, Acum, []):-
	chop_up(TailList,NewList,Acum,[HeadList]).

chop_up([HeadList|TailList], NewList, Acum, [HT|TT]) :-
        last([HT|TT],LT),
        LT is HeadList - 1,
        append([HT|TT],[HeadList],NT),
        chop_up(TailList,NewList,Acum,NT).

chop_up([HeadList|TailList], NewList, Acum, [HT|TT]) :-
        last([HT|TT],LT),
        \+(LT is HeadList - 1),
        get_first_last([HT|TT],Head_LT),
        append(Acum,Head_LT,NewAcum),
        chop_up(TailList,NewList,NewAcum,[HeadList]).

get_first_last(List,List):- 
	length(List,1).

get_first_last(List,[[Head,Last]]) :- 
	length(List,Len), Len > 1,
	List = [Head|_],last(List,Last).



%q5
tree_eval(_,tree(empty,X,empty),Result):-
	number(X),
	Result is X.
tree_eval(Num,tree(empty,X,empty),Result):-
	X=z,
	Result is Num.	
tree_eval(Num, tree(tree(LL,LOp,LR),Op,tree(RL,ROp,RR)), Result) :-
	tree_eval(Num,tree(LL,LOp,LR), LResult),
	tree_eval(Num,tree(RL,ROp,RR), RResult),
	exp(LResult,Op, RResult,Exp),
	Result is Exp.

exp(L,'+',R,Result):-
	Result is L+R.
exp(L,'-',R,Result):-
	Result is L-R.
exp(L,'*',R,Result):-
	Result is L*R.
exp(L,'/',R,Result):-
	Result is L/R.
