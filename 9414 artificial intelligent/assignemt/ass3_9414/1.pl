
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


initial_intentions(intents(Intentions,[])):-
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
% dif(A,B,D):-
%    D is A-B, D >=0 ,!.
% dif(A,B,D):-
%    D is B-A.



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



% % ----- Q3:

% ### test1

% incorporate_goals(+Goals, +Intentions, -Intentions1).

% Base case, no more Goals.
%incorporate_goals(goals([],[]), Intentions, Intentions1).

% Case : Goal is already exist in the Intentions, pass it.

%incorporate_goals(goals([goal(X,Y)|Goal_Rest],[]), intents(Int_drop,Int_pick), Intentions1) :-
%    member([goal(X,Y),_], Int_drop),
%    incorporate_goals(goals([Goal_Rest,[]), intents(Int_drop,Int_pick), Intentions1).


% Case : Goal is not exist in the Intentions, put it in the list.

%incorporate_goals(goals([goal(X,Y)|Goal_Rest],[]), intents(Int_drop,Int_pick), Intentions1) :-
%    update_intents_goal(goal(X,Y), Int_drop, NewInt_drop),
%    incorporate_goals(goals([Goal_Rest,[]), intents(NewInt_drop,Int_pick), Intentions1).


% is_member(+Goal, +Intentions).
%   Check whether a given Goal is exist in the Intentions list.
%is_member(Goal, [Head|_]) :-
    %member(Goal, Head).

%is_member(Goal, [Head|Tail]) :-
%    not(member(Goal, Head)),
%    is_member(Goal, Tail).

% insert_goal(+Goal, +Intentions, -Intentions1).
%   Insert the Goal as an Intention whose formate is ( [goal, plan] ),add into the 
%   Intentions

% ### test2 
incorporate_goals([],Intentions,Intentions):- !.
incorporate_goals([Goal|Goals],Intentions,Intentions1):-
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    insert_goal(Goal,Intentions,NewIntentions),
    retract(goal(goal(X0,Y0))),
    incorporate_goals(Goals,NewIntentions,Intentions1),!.


% insert_goal(+Goal, +Intentions, -Intentions1).
%   Insert the Goal as an Intention whose formate is ( [goal, plan] ),add into the
%   Intentions

insert_goal(Goal,intents(Int_drop, Int_pick), Intents(Int_drop, Int_pick1)):-
    solve(Goal, Path, G, _),
    insert_goal_h(Goal, G, Int_pick, Int_pick1),!.

% when solve is false, this is invalid path,so pass

insert_goal(Goal,intents(Int_drop, Int_pick), Intents(Int_drop, Int_pick)):-
    not(solve(Goal, Path, G, _)),!.


%[[Goal,[]]] is ( [goal, plan] )

insert_goal_h(Goal,_,[],[[Goal,[]]]).
insert_goal_h(Goal,_,[[Goal,Plan]|Tail], [[Goal,Plan]|Tail]).
insert_goal_h(Goal, G, [[HGoal,HPlan]|Tail], [[HGoal,HPlan]|Tail1]):-
    solve(HGoal,_,GHL),
    G < GHL,!.

insert_goal_h(Goal, G, [[HGoal,HPlan]|Tail], [[HGoal,HPlan]|Tail1] ):-
    solve(HGoal,_,GHL),
    G >= GHL,
    insert_goal_h(Goal, G, Tail, Tail1).


s(goal(X1,Y1),goal(X2,Y2),1):-
    land_or_dropped(X2,Y2),
    distance(X1,Y1),(X2,Y2),D).


s(goal(X1,Y1),goal(X2,Y2),1000):-
    UX1 is X1 + 1,
    DX1 is X1 -1,
    UY1 is Y1 +1,
    DY1 is Y1 -1,
    between(DY1, UY1, Y2),
    between(DX1, UX1, X2),
    distance((X1,Y1),(X2,Y2),D).





% % ----- Q4:

%get_action(Intentions,Intentions1,Action)

% agent_stones(1) if already have a stone, go to drop
get_action(intents([HInt_drop|TInt_drop],Int_pick),intents([HInt_drop1|TInt_drop],Int_pick),Action):-
    agent_stones(1),
    get_action_drop(HInt_drop,HInt_drop1,Action),!.


% agent_stones(0) if do not have a stone, go to pick 
get_action(intents([Int_drop,[HInt_pick]|TInt_pick]),Intents([Int_drop,[HInt_pick1]|TInt_pick]),Action):-
    agent_stones(0),
    get_action_pick(HInt_pick,HInt_pick1,Action),!.

get_action(Int_drop,[]),Intents(Int_drop,[HInt_pick1|TInt_pick]),Action):-
    agent_at(X0,Y0),
    move(X0,Y0).

% -----------------   
% get_action_drop(goal, plan, plan1, action)

get_action_drop([],[],move(X0,Y0]):-
        agent_at(X0,Y0).

get_action_drop([goal(X,Y),[HPlan|TPlan]],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan.

get_action_drop([goal(X,Y),[HPlan|TPlan]],[[goal(X,Y),Plan1]|Tpick],Action):-
    not(applicable(HPlan)),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    solve(goal(X,Y),NewPlan,_,_),
    retract(goal(goal(X0,Y0))),
    append(Move_Path,[_],NewPlan),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

get_action_drop([goal(X,Y),[]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    solve(goal(X,Y),NewPlan,_,_),
    retract(goal(goal(X0,Y0))),
    append(Move_Path,[_],NewPlan),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

%[_|Move_Path]
% ----------------- 
% get_action_pick(goal, plan, plan1, action)

get_action_pick([],[],move(X0,Y0)):-
    agent_at(X0,Y0).

get_action_pick([[goal(X,Y),[HPlan|TPlan]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan.

get_action_pick([[goal(X,Y),[]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    solve(goal(X,Y),NewPlan,_,_),
    retract(goal(goal(X0,Y0))),
    append(Move_Path,[_],NewPlan),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

get_action_pick([goal(X,Y),[HPlan|TPlan]],[goal(X,Y),Plan1],Action):-
    not(applicable(HPlan)),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    solve(goal(X,Y),NewPlan,_,_),
    retract(goal(goal(X0,Y0))),
    append(Move_Path,[_],NewPlan),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].






% % ----- Q5:

update_intentions(at(_,_),Intentions,Intentions).
update_intentions(dropped(_,_),Intents([_|Int_drop],Int_pick),Intents(TInt_drop,Int_pick]).
update_intentions(picked(_,_),Intents(Int_drop,[_|Int_pick]),Intents(Int_drop,TInt_pick]).
