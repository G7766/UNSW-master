
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
intents([],[]).

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
    % D is A-B, D >=0 ,!.
% dif(A,B,D):-
    % D is B-A.



% % ----- Q2:
% case : if add events , and compute the corresponding list of goals
% goals([]).
% change stone(X,Y) to goal(X,Y)
trigger([],[]):-!.
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
	
	
	
% % -- Q3


% incorporate_goals(Goals, Intentions, Intentions1)
% Base case : In case no new goals for both rest and truff, Intentions
% stay same.
incorporate_goals([], Intentions, Intentions1):-
		Intentions1 = Intentions.

% In case only new rest goal
% In case existed goal, loop to next stone goal
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
        member([goal(X,Y),_], Int_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,Int_pick), Intentions1).
		
% Insert new stone goal to correct position in Int_pick
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
        update_intents_goal(goal(X,Y), Int_pick, NewInt_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,NewInt_pick), Intentions1).
	
% Base case : Insert first new goal to list as intention in the form of [goal(X,Y),[]]
update_intents_goal(goal(X,Y), [], [goal(X,Y),[]]).


% Find one item of intentions list, compare Stock S1 of its goal with Stock S of new goal
% In case D =< D1, in other words new goal has higher stock, insert the intention of new goal before that item
% compare distance
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail1], [[goal(X,Y),Plan]|Tail]):-
		agent_at(X0,Y0),
	    distance((X,Y), (X0,Y0), D),
		distance((X1,Y1), (X0,Y0), D1),
		D =< D1,
		Tail = [[goal(X1,Y1),Plan]|Tail1].
		
% D > D1
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail1], [[goal(X1,Y1),Plan]|Tail]):-
		agent_at(X0,Y0),
	    distance((X,Y), (X0,Y0), D),
		distance((X1,Y1), (X0,Y0), D1),
		D > D1,
		update_intents_goal(goal(X,Y), Tail1, Tail, agent_at(X0,Y0)).
		
		
		

		
% % -- Q4


% get_action(Intentions, Intentions1, Action)
% Base case: at starting point, set Action to move(1,1)
get_action(intents([[goal(X,Y),[]]|Tail],[]), Intentions2, move(1,1)):-
		Intentions2 = intents([[goal(X,Y),[]]|Tail],[]).

% Base case: in case no new goals for both rest and truff, stay there
get_action(intents([[goal(X,Y),Plan]|Tail],[]), Intentions2, move(X,Y)):-
		Intentions2 = intents([[goal(X,Y),Plan]|Tail],[]).







% If Int_sell is not empty and first item satisfies S<=T. Select this intention.
% If first action in this plan is applicable, select this action, update intention.
get_action(intents([Int_drop|Int_sell_rest],Int_pick),intents([[Goal,RestofActions]|Int_sell_rest],Int_pick),Action) :-
        first_action(Int_sell,Goal,[Action|RestofActions]),
        Goal=goal(_,_,S),
        S=<T,
        applicable(Action).


% If first action is not applicable,
% Construct a new plan
% Select the first action, update intention .
get_action(beliefs(at(X,Y),stock(T)),intents([Int_sell|Int_sell_rest],Int_pick),intents([[Goal,New_rest_actions1]|Int_sell_rest],Int_pick),Action) :-
        first_action(Int_sell,Goal,[Wrong_Action|_]),
        Goal=goal(_,_,S),
        S=<T,
        not(applicable(Wrong_Action)),
        new_action_sell(Goal,beliefs(at(X,Y),stock(T)),New_action),
        new_first_action(New_action,New_rest_actions1,Action).


% If there is no plan for the goal,
% Construct a new plan
% Select the first action, update intention.
get_action(beliefs(at(X,Y),stock(T)),intents([[Goal,[]]|Int_sell_rest],Int_pick),intents([[Goal,New_rest_action1]|Int_sell_rest],Int_pick), Action) :-
        Goal=goal(_,_,S),
        S=<T,
        new_action_sell(Goal,beliefs(at(X,Y),stock(T)),New_action),
        %first_action([Goal, New_action], Goal, [Action|_]),
        new_first_action(New_action,New_rest_action1,Action).


% If not enough stock to sell, throw it.
get_action(beliefs(at(X,Y),stock(T)),intents([[Goal,Plan]|Int_sell],[]),intents([[Goal,Plan]|Int_sell],[]),move(X,Y)) :-
        Goal=goal(_,_,S),
        S>T.


% If Int_pick is not empty. Select this intention.
% If first action in this plan is applicable, select this action, update intention.
get_action(beliefs(at(_,_),stock(_)),intents(Int_sell,[Int_pick|Int_pick_rest]),intents(Int_sell,[[Goal,RestofActions]|Int_pick_rest]),Action) :-
        first_action(Int_pick,Goal,[Action|RestofActions]),
        applicable(Action).


% If first action is not applicable
% Construct a new plan
% Select the first action, update intention.
get_action(beliefs(at(X,Y),stock(T)),intents(Int_sell,[Int_pick|Int_pick_rest]),intents(Int_sell,[[Goal,New_action1]|Int_pick_rest]),Action) :-
        first_action(Int_pick, Goal,[Wrong_Action|_]),
        not(applicable(Wrong_Action)),
        new_action_pick(Goal,beliefs(at(X,Y),stock(T)),New_action),
        new_first_action(New_action,New_action1,Action).


% If there is no plan for the goal
% Construct a new plan
% Select the first action, update intention.
get_action(beliefs(at(X,Y),stock(T)),intents(Int_sell,[[Goal,[]]|Int_pick_rest]),intents(Int_sell,[[Goal, New_action1]|Int_pick_rest]),Action) :-
        new_action_pick(Goal,beliefs(at(X,Y),stock(T)),New_action),
        %first_action([Goal, New_action], Goal, [Action|_]),
        new_first_action(New_action,New_action1,Action).


% Distinguish goals and actions in a list to select the first action.
first_action([Goal|Actions],Goal,Actions).


% Select a new first action from a new actions list.
new_first_action([Action|New_action1],New_action1,Action).


% Construct new plan for Int_sell.
new_action_sell(Goal,Beliefs,Actions) :-
        new_action_sell(Goal,Beliefs,[],Actions).
new_action_sell(goal(X,Y,_),beliefs(at(X,Y),stock(_)),Partial_action,Actions) :-
        reverse([sell(X,Y)|Partial_action],Actions).
new_action_sell(Goal,beliefs(at(X,Y),stock(_)),Partial_action,Actions) :-
        right_move(X,Y,move(X2,Y2)),
        right_direction(move(X2,Y2),Goal,at(X,Y)),
        new_action_sell(Goal,beliefs(at(X2,Y2),stock(_)),[move(X2,Y2)|Partial_action],Actions).


% Construct new plan for Int_pick.
new_action_pick(Goal,Beliefs,Actions) :-
        new_action_pick(Goal,Beliefs,[],Actions).
new_action_pick(goal(X,Y,_),beliefs(at(X,Y),stock(_)),Partial_action,Actions) :-
        reverse([pick(X,Y)|Partial_action],Actions).
new_action_pick(Goal,beliefs(at(X,Y),stock(_)),Partial_action,Actions) :-
        right_move(X,Y,move(X2,Y2)),
        right_direction(move(X2,Y2),Goal,at(X,Y)),
        new_action_pick(Goal,beliefs(at(X2,Y2),stock(_)),[move(X2,Y2)|Partial_action],Actions).
/*
% Reverse a list.
reverse(List,Reverse) :-
        reverse(List,[],Reverse).
reverse([],Reverse,Reverse).
reverse([Head|Tail],Rest_Reverse,Reverse) :-
        reverse(Tail,[Head|Rest_Reverse],Reverse).
*/

% Construct a correct move.
right_move(X,Y,Move) :-
        X1 is X+1,Move=move(X1,Y);
        X2 is X-1,Move=move(X2,Y);
        Y1 is Y+1,Move=move(X,Y1);
        Y2 is Y-1,Move=move(X,Y2).

% Determine whether the direction is towards goal.
right_direction(move(X1,Y1),goal(X2,Y2,_),at(X,Y)) :-
        distance((X1,Y1),(X2,Y2),Current_dis),
        distance((X,Y),(X2,Y2),Plan_dis),
        Current_dis<Plan_dis.
		
		
		
% %--Q5
update_intentions(at(_,_),Intentions,Intentions).
update_intentions(dropped(_,_),Intents([_|Int_drop],Int_pick),Intents(TInt_drop,Int_pick]).
update_intentions(picked(_,_),Intents(Int_drop,[_|Int_pick]),Intents(Int_drop,TInt_pick]).
