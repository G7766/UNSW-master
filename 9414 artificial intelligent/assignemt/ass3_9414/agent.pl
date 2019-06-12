% % % % % % % % % % % % % % % % % % % % % % % %
%
%        COMP9414 Assignment3  sem1 2018 
%        Done by: PEIGUO GUAN (z5143964)
%                 TAORAN SUN  (z5150998)                
%        hw3group Number: 426
%        Assignment Name: Option 2 Prolog (BDI Agent)
% % % % % % % % % % % % % % % % % % % % % % % %



% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 1 Write a Prolog procedure
% -initial_intentions(Intentions):
% -binds Intentions to intents(L,[])
% -L in the form [[goal(X1,Y1),[]], ... , [goal(Xn,Yn),[]]]
% -(Xt,Yt) is the location of the monster
% -(X0,Y0) is the location of the current agent
% -(X1,Y1), ... , (Xn-1,Yn-1) are places stones need to be dropped  
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %


% % ----- Q1:

% the current position of the agent is dynmaically change, 
% using assert and retract to follow the position
% use path search and disj (solve function) to get the total path include land_path + water_path
% and filter the land_path to get the water_path

% base case
intents([],[]).
initial_intentions(intents(L,[])):-
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    monster(Xt,Yt),
    solve(goal(Xt,Yt),Path,_,_),
    findall(X,(member(goal(X1,Y1),Path), not(land(X1,Y1)), X = [goal(X1,Y1),[]]), L),
    retract(goal(goal(X1,Y1))).



% s(+state(start),-state(trans),-cost)
% to find the best way, setting  
% cost land = 1 ,sea = 1000
% as well as to consider the water_path that has been dropped 

s(goal(X1,Y1),goal(X2,Y2),1):-
    land_or_dropped(X2,Y2),
    mandist(X1/Y1,X2/Y2,1).

s(goal(X1,Y1),goal(X2,Y2),1000):-
    between(1, 100, X2),
    between(1, 100, Y2),
    not(land(X2,Y2)),
    mandist(X1/Y1,X2/Y2,1).


% D is Manhattan Dist between two positions
mandist(X/Y,X1/Y1,D):-
    dif(X,X1,Dx),
    dif(Y,Y1,Dy),
    D is Dx+Dy.




% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 2
% -trigger(Percepts, Goals):
% -Percepts to recept stone path Goals is output form
% -change stone(X,Y) to the form of goal(X,Y)
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %

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

% change state(X,Y) to goal(X,Y)
trigger_state_to_goal([],[]).
trigger_state_to_goal([state(X,Y)|Tail],[goal(X,Y)|Goals]):-
    trigger_state_to_goal(Tail,Goals).
	
	
% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 3
% -return the updated Intentions of the agent after inserting the new goals into Int_pick
% -A valid path is one which passes through only locations (X,Y) 
% -for which land_or_dropped(X,Y) is true 
% -If no such valid path exists, then the new goal should be abondoned
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %	

% % -- Q3

% incorporate_goals(Goals, Intentions, Intentions1)
% Base case : In case no new goals for stone, Intentions
% stay
incorporate_goals([], Intentions, Intentions1):-
		Intentions1 = Intentions.

% In case new goal
% In case existed goal, loop to next stone goal
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
		member([goal(X,Y),_],Int_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,Int_pick), Intentions1).


		
% Insert new stone goal to correct position in Int_pick
incorporate_goals([goal(X,Y)|Goal_stone], intents(Int_drop,Int_pick), Intentions1) :-
		comp(X,Y),
        update_intents_goal(goal(X,Y), Int_pick, NewInt_pick),
        incorporate_goals(Goal_stone, intents(Int_drop,NewInt_pick), Intentions1).
% If agent can not move to new stone, loop to next stone goal.
incorporate_goals([goal(X,Y)|Goal_stone], Intentions, Intentions1):-
		comp1(X,Y),
		incorporate_goals(Goal_stone, Intentions, Intentions1).
		
		
		
% Insert first new goal to list as intention in the form of [goal(X,Y),[]]
update_intents_goal(goal(X,Y), [], [[goal(X,Y),[]]]).


% new goal has lower distance, insert the intention of new goal at first.
% compare distance D =< D1
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail1], [[goal(X,Y),Plan]|Tail]):-
		agent_at(X0,Y0),
	    distance((X,Y), (X0,Y0), D),
		distance((X1,Y1), (X0,Y0), D1),
		D =< D1,
		Tail = [[goal(X1,Y1),Plan]|Tail1].
		
% compare distance D > D1
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail1], [[goal(X1,Y1),Plan]|Tail]):-
		agent_at(X0,Y0),
	    distance((X,Y), (X0,Y0), D),
		distance((X1,Y1), (X0,Y0), D1),
		D > D1,
		update_intents_goal(goal(X,Y), Tail1, Tail).
		

% find a path between agent and stone.


% find points which is not exist.

initial_intentions2(X,Y,intents(L)):-
    assert(goal(goal(1,1))),
    solve(goal(X,Y),Path,_,_),
    findall(A,(member(goal(X1,Y1),Path), not(land_or_dropped(X1,Y1)), A = [goal(X1,Y1),[]]), L),
	retract(goal(goal(X1,Y1))),!.
% Judge valid of path.
distingish(L):-
	L = [].
distingish2(L):-
	L = [[goal(_,_),_]|_].
comp(X,Y):-
	initial_intentions2(X,Y,intents(L)),
	L = [].
comp1(X,Y):-
	initial_intentions2(X,Y,intents(L)),
	distingish2(L).


% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 4
% -get_action(Intentions1, Intentions2, Action):
% -get the Intentions from Q3 as Intentions1
% -if find a stone we can get and we do not have a stone in hand,
% -make a strategy to get the stone ,the from (goal(X,Y),Plan)
% -Plan is the path to the goal(X,Y) and pick the stone
% -if hold stone in hand, gat action to drop, drop the stone in water_path position
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %


% incorporate_goals(Goals, Intentions, Intentions1), 
%  writeln(Intentions1),

 % ----- Q4:

% get_action(Intentions1, Intentions2, Action)
% writeln(Intentions2)

% case : if we hold a stone, get the current pos and do go_to_drop function
get_action(intents(Int_drop,Int_pick),intents(Int_drop1,Int_pick),Action):-
    agent_stones(1),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    go_to_drop(Int_drop,Int_drop1,Action),
    retract(goal(goal(X0,Y0))),!.

% case : if we do not hold a stone, get the current pos and do go_to_pick function
get_action(intents(Int_drop,Int_pick),intents(Int_drop,Int_pick1),Action):-
    agent_stones(0),
    %writeln('aaaaaaaa'),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    go_to_pick(Int_pick,Int_pick1,Action),
    retract(goal(goal(X0,Y0))),!.

% --drop
% base case if empty list , stand there
go_to_drop([],[],move(X0,Y0)):-
        agent_at(X0,Y0),!.

% case if plan list is not empty ,the next step is to next action in list
go_to_drop([[goal(X,Y),[HPlan|TPlan]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan.

% case if plan list is empty and the point is applicable, find the plan to drop
go_to_drop([[goal(X,Y),[]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    solve(state(X,Y),Path1,_,_),
    trigger_state_to_goal(Path1,Path),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

% case if plan list is empty and unapplicable
go_to_drop([[goal(X,Y),[HPlan|_]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    not(applicable(HPlan)),
    solve(state(X,Y),Path1,_,_),
    trigger_state_to_goal(Path1,Path),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

% --pick
% base case if empty list , stand there
go_to_pick([],[],move(X0,Y0)):-
        agent_at(X0,Y0).

% case if plan list is not empty ,the next step is to next action in list
go_to_pick([[goal(X,Y),[HPlan|TPlan]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    %writeln('kkk'),
    Action = HPlan,
    Plan1 = TPlan.

% case if plan list is empty and the goal is applicable,find the plan to pick the stone
go_to_pick([[goal(X,Y),[]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    solve(state(X,Y),Path1,_,_),
    trigger_state_to_goal(Path1,Path),
    %writeln('bbb'),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

% case if plan list is empty and the goal is not applicable
go_to_pick([[goal(X,Y),[HPlan|_]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    not(applicable(HPlan)),
    %writeln('ccc'),
    solve(state(X,Y),Path1,_,_),
    trigger_state_to_goal(Path1,Path),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].
		


% % % % % % % % % % % % % % % % % % % % % % % % % % % %
%
% Part 5
% -update the agents intentions, based on observation
% -In the case of a picked() or dropped() observation
% -remove the corresponding plan from its list of intentions
% % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% % -- Q5

% when move(X,Y) finish, intentions stay there
update_intentions(at(_,_),Intentions,Intentions).
% when drop(X,Y) finish, update intentions from list
update_intentions(dropped(_,_),intents([_|Int_drop],Int_pick),intents(Int_drop,Int_pick)).
% when pick(X,Y) finish, update intentions from list
update_intentions(picked(_,_),intents(Int_drop,[_|Int_pick]),intents(Int_drop,Int_pick)).









% % % % % % % % % % % % % % % % % % % % % % % %
%
%        pathsearch & ucsdijkstra
%
% % % % % % % % % % % % % % % % % % % % % % % %


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