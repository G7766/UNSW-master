
intents = [ [goal(5,3),[]],[goal(7,6),[]],[goal(8,6),[]],[goal(9,9),[]], [] ]
intentions（Intents,[])
% % ----- Q2:
% base case: if no new percepts, goal and goal rest are empty

agent_at(2,3).

trigger([],[]).

% case : if add events , and compute the corresponding list of goals

trigger([stone(X,Y)|Tail],[goal(X,Y)|Goals]):-
trigger(Tail,Goals).


% goal = [ ]



% % ----- Q3:

% incorporate_goals(+Goals, +Intentions, -Intentions1).

% Base case, no more Goals.
incorporate_goals([], Intentions, Intentions1).

% Case : Goal is already exist in the Intentions, pass it.
incorporate_goals([Goal|Tail], Intentions, Intentions1) :-
    is_member(Goal, Intentions),
    incorporate_goals(Tail, Intentions, Intentions1).

% Case : Goal is not exist in the Intentions, put it in the list.
incorporate_goals([Goal|Tail], Intentions, Intentions1) :-
    not(is_member(Goal, Intentions)),
    insert_goal(Goal, Intentions, NewIntentions),
    incorporate_goals(Tail, NewIntentions, Intentions1).

% is_member(+Goal, +Intentions).
%   Check whether a given Goal is exist in the Intentions list.
is_member(Goal, [Head|_]) :-
    member(Goal, Head).

is_member(Goal, [Head|Tail]) :-
    not(member(Goal, Head)),
	is_member(Goal, Tail).

% insert_goal(+Goal, +Intentions, -Intentions1).
%   Insert the Goal as an Intention whose formate is ( [goal, plan] ),add into the 
%   Intentions




insert_goal(Goal, intents(Int_Drop, Int_Pick), Intents(Int_Drop, Int_Pick1)):-
    solve(Goal, Path, G,_)),writeln(Path),
    insert_goal_h(Goal, G, Int_Pick, Int_Pick1).

insert_goal_h(Goal, _, [], [[Goal,[]]]).
insert_goal_h(Goal, _, [[Goal,Plan]|Tail], [[Goal,Plan]|Tail]).
insert_goal_h(Goal, G, [[Goal,Plan]|Tail], [[Goal,Plan]|Tail1] ):-
    solve(Goal,_,GHL),
    G < GHL,!.

insert_goal_h(Goal, G, [[Goal,Plan]|Tail], [[Goal,Plan]|Tail1] ):-
    solve(Goal,_,GHL),
    G >= GHL,
    insert_goal(Goal, G, Tail, Tail1).

s(goal(X1,Y1),goal(X2,Y2),1):-
    land_or_dropped(X2,Y2),
    distance(X1,Y1),(X2,Y2),1).


s(goal(X1,Y1),goal(X2,Y2),1000):-
    UX1 is X1 + 1,
    DX1 is X1 -1,
    UY1 is Y1 +1,
    DY1 is Y1-1,
    between(DY1, UY1, Y2),
    between(DX1, UX1, X2).








incorporate_goals(Goals, Intentions, Intentions1):-
insert_goal(Goal,Intentions, Intentions1)),




% insert_goal(+Goal, +Intentions, -Intentions1).
%   Insert the Goal as an Intention whose formate is ( [goal, plan] ),add into the
%   Intentions



insert_goal(Goal,intents(Int_drop, Int_pick), Intents(Int_drop, Int_pick1)):-
solve(Goal, Path, G, _),writeln(Path),
insert_goal_h(Goal, G, Int_Pick, Int_Pick1).

%[[Goal,[]]] is ( [goal, plan] )

insert_goal_h(Goal,_,[],[[Goal,[]]]).
insert_goal_h(Goal,_,[[Goal,Plan]|Tail], [[Goal,Plan]|Tail]).
insert_goal_h(Goal, G, [[Goal,Plan]|Tail], [[Goal,Plan]|Tail1]):-
solve(Goal,_,GHL),
G < GHL,!.

insert_goal_h(Goal, G, [[Goal,Plan]|Tail], [[Goal,Plan]|Tail1] ):-
solve(Goal,_,GHL),
G >= GHL,
insert_goal(Goal, G, Tail, Tail1).


s(goal(X1,Y1),goal(X2,Y2),1):-
land_or_dropped(X2,Y2),
distance(X1,Y1),(X2,Y2),1).


s(goal(X1,Y1),goal(X2,Y2),1000):-
UX1 is X1 + 1,
DX1 is X1 -1,
UY1 is Y1 +1,
DY1 is Y1-1,
between(DY1, UY1, Y2),
between(DX1, UX1, X2).

