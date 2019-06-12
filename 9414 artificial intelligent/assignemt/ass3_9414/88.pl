
% % % % % % % %  pathsearch.pl   % % % % % % % % % % %

% This file provides code for insert_legs(), head_member() and build_path()
% used by bfsdijkstra(), ucsdijkstra(), greedy() and astar().

% insert_legs(Generated, Legs, Generated1).
% insert new legs into list of generated legs,
% by repeatedly calling insert_one_leg()

% base case: no legs to be inserted
insert_legs(Generated, [], Generated).

% Insert the first leg using insert_one_leg(); and continue.
insert_legs(Generated, [Leg|Legs], Generated2) :-
insert_one_leg(Generated, Leg, Generated1),
insert_legs(Generated1, Legs, Generated2).

% head_member(Node, List)
% check whether Node is the head of a member of List.

% base case: node is the head of first item in list.
head_member(Node,[[Node,_]|_]).

% otherwise, keep searching for node in the tail.
head_member(Node,[_|Tail]) :-
head_member(Node,Tail).

% build_path(Expanded, [[Node,Pred]], Path).

% build_path(Legs, Path)
% Construct a path from a list of legs, by joining the ones that match.

% base case: join the last two legs to form a path of one step.
build_path([[Next,Start],[Start,Start]], [Next,Start]).

% If the first two legs match, add to the front of the path.
build_path([[C,B],[B,A]|Expanded],[C,B,A|Path]) :-
build_path([[B,A]|Expanded],[B,A|Path]), ! .

% If the above rule fails, we skip the next leg in the list.
build_path([Leg,_SkipLeg|Expanded],Path) :-
build_path([Leg|Expanded],Path).



% % % % % % % %  ucsdijkstra.pl   % % % % % % % % % % %

solve(Start, Solution, G, N)  :-
    %consult(pathsearch), % insert_legs(), head_member(), build_path()
    ucsdijkstra([[Start,Start,0]], [], Solution, G, 1, N).

ucsdijkstra([[Node,Pred,G]|_Generated], Expanded, Path, G, N, N)  :-
    goal(Node),
    build_path([[Node,Pred]|Expanded], Path).


ucsdijkstra([[Node,Pred,G]| Generated], Expanded, Solution, G1, L, N) :-
    extend(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    ucsdijkstra(Generated1, [[Node,Pred]|Expanded], Solution, G1, M, N).


extend(Node, G, Expanded, NewLegs) :-
    findall([NewNode, Node, G1], (s(Node, NewNode, C)
    , not(head_member(NewNode, Expanded))
    , G1 is G + C
    ), NewLegs).

insert_one_leg([], Leg, [Leg]).

insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated]) :-
    Leg  = [Node,_Pred, G ],
    Leg1 = [Node,_Pred1,G1],
    G >= G1, ! .

insert_one_leg([Leg1|Generated], Leg, [Leg,Leg1|Generated]) :-
    Leg  = [_Node, _Pred, G ],
    Leg1 = [_Node1,_Pred1,G1],
    G < G1, ! .

insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated1]) :-
    insert_one_leg(Generated, Leg, Generated1).





% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 1 Write a Prolog procedure
% -initial_intentions(Intentions):
% -binds Intentions to intents(L,[])
% -L in the form [[goal(X1,Y1),[]], ... , [goal(Xn,Yn),[]]]
% -(Xn,Yn) s the location of the monster
% -(X1,Y1), ... , (Xn-1,Yn-1) are places stones need to be dropped  
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %


% % ----- Q1:

% use path search and disj to get the total path include land_path + water_path

find_path(Intentions):-
    Start = state(9,9),
    solve(Start,Path,_,_),
    reverse(Path,Intentions).

% find the path without land_path
% and the ouput is our water_path needs to dropped

find_repath(Intents0,Intents):-
    find_land_or_water(Intents0,[],Intents).

% base case

find_land_or_water([],Intents,Intents).

% if path in land_path, pass.
find_land_or_water([state(X,Y)|Tail], Intents0, Intents):-
    land(X,Y),
    find_land_or_water(Tail, Intents0,Intents).

% else add in Intents.
find_land_or_water([state(X,Y)|Tail], Intents0,Intents):-
    find_land_or_water(Tail,[[goal(X,Y),[]]|Intents0], Intents).


initial_intentions(intents(Intentions)):-
    find_path(Path),
    find_repath(Path,Intentions),!.

%iniii(intents(L,[])):-
%    assert(goal(goal(1,1))),
%    solve(goal(9,9),Path,_,_),
%    finall(X,(member(goal(G1,G2),Path) , not(land(G1,G2)),X=[goal(G1,G2),[]]),L),
%    retract(goal(goal(1,1))),
%    retractall(s(_,_,1000)).




% s(+state(start),-state(trans),-cost)
% cost land = 1 ,sea = 1000

s(state(X1,Y1),state(X2,Y2),1):-
    land(X2,Y2),
    mandist(X1/Y1,X2/Y2,1).

s(state(X1,Y1),state(X2,Y2),1000):-
    between(1, 100, X2),
    between(1, 100, Y2),
    not(land(X2,Y2)),
    mandist(X1/Y1,X2/Y2,1).

goal(state(1,1)).

% D is Manhattan Dist between two positions
mandist(X/Y,X1/Y1,D):-
    dif(X,X1,Dx),
    dif(Y,Y1,Dy),
    D is Dx+Dy.

% D is |A-B|
dif(A,B,D):-
    D is A-B, D >=0 ,!.
dif(A,B,D):-
    D is B-A.



% % ----- Q2:
% case : if add events , and compute the corresponding list of goals

% change stone(X,Y) to goal(X,Y)
trigger([],[]).
trigger([stone(X,Y)|Tail],[goal(X,Y)|Goals]):-
    trigger(Tail,Goals).

% change goal(X,Y) to move(X,Y)
trigger_goal_to_move([],[]).
trigger_goal_to_move([goal(X,Y)|Tail],[move(X,Y)|Goals]):-
    trigger_goal_to_move(Tail,Goals).

% change goal(X,Y) to drop(X,Y)
trigger_goal_to_drop([],[]).
trigger_goal_to_drop([goal(X,Y)|Tail],[drop(X,Y)|Goals]):-
    trigger_goal_to_move(Tail,Goals).

% change goal(X,Y) to pick(X,Y)
trigger_goal_to_pick([],[]).
trigger_goal_to_pick([goal(X,Y)|Tail],[drop(X,Y)|Goals]):-
    trigger_goal_to_move(Tail,Goals).



%---------- q3
% incorporate_goals(Goal, Belief, Intentions, Intentions1)
% Base case : In case no new goals for both rest and truff, Intentions
% stay same.
incorporate_goals([], Intentions, Intentions):-!.

% In case only new rest goal
% In case existed goal, loop to next stone goal
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
        member([goal(X,Y),_], Int_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,Int_pick), Intentions1),!.

% Insert new stone goal to correct position in Int_pick
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
        update_intents_goal(goal(X,Y), Int_pick, NewInt_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,NewInt_pick), Intentions1).
 
% Base case : Insert first new goal to list as intention in the form of [goal(X,Y),[]]
update_intents_goal(goal(X,Y), [], [[goal(X,Y),[]]]):-!.

% Find one item of intentions list, compare Stock S1 of its goal with Stock S of new goal
% In case S1 < S, in other words new goal has higher stock, insert the intention of new goal before that item
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail],[Head1|[goal(X,Y),[]]]):-
        Head1 = [[goal(X1,Y1),Plan]|Tail],!.