
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

initial_intentions(intents(L,[])):-
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    target_monster(Xt,Yt),
    solve(goal(Xt,Yt),Path,_,_),
    findall(X,(member(goal(X1,Y1),Path), not(land(X1,Y1)), X = [goal(X1,Y1),[]]), L),
    retract(goal(goal(X1,Y1))),
    retractall(s(_,_,1000)).

%iniii(intents(L,[])):-
%    assert(goal(goal(1,1))),
%    solve(goal(9,9),Path,_,_),
%    finall(X,(member(goal(G1,G2),Path) , not(land(G1,G2)),X=[goal(G1,G2),[]]),L),
%    retract(goal(goal(1,1))),
%    retractall(s(_,_,1000)).




% s(+state(start),-state(trans),-cost)
% cost land = 1 ,sea = 1000

s(goal(X1,Y1),goal(X2,Y2),1):-
    land(X2,Y2),
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
        
% D > D1
update_intents_goal(goal(X,Y),[[goal(X1,Y1),Plan]|Tail1], [[goal(X1,Y1),Plan]|Tail]):-
        agent_at(X0,Y0),
        distance((X,Y), (X0,Y0), D),
        distance((X1,Y1), (X0,Y0), D1),
        D > D1,
        update_intents_goal(goal(X,Y), Tail1, Tail).
        

        
find_path1(X,Y,Road):-
    Start = goal(X,Y),
    solve(Start,Path,_,_),
    reverse(Path,Road).

        
initial_intentions2(X,Y,intents2(Intentions)):-
    find_path1(X,Y,Path),
    find_repath(Path,Intentions),!.

distingish(Intents):-
    Intents = [].


distingish2(Intents):-
    Intents = [[goal(_,_),_]|_].
    

comp(X,Y):-
    initial_intentions2(X,Y,intents2(Intents)),
    distingish(Intents).
    
comp1(X,Y):-
    initial_intentions2(X,Y,intents2(Intents)),
    distingish2(Intents).
		
		
		

		
% % Q4
% % ----- Q4:
get_action(intents(Int_drop,Int_pick),intents(Int_drop1,Int_pick),Action):-
    agent_stones(1),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    get_action_drop(Int_drop,Int_drop1,Action),
    retract(goal(goal(X0,Y0))),!.

get_action(intents(Int_drop,Int_pick),intents(Int_drop,Int_pick1),Action):-
    agent_stones(0),
    agent_at(X0,Y0),
    assert(goal(goal(X0,Y0))),
    get_action_drop(Int_pick,Int_pick1,Action),
    retract(goal(goal(X0,Y0))),!.

% --drop
get_action_drop([],[],move(X0,Y0)):-
    agent_at(X0,Y0),!.
get_action_drop([[goal(X,Y),[HPlan|TPlan]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan.
get_action_drop([[goal(X,Y),[]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    solve(goal(X,Y),Path,_,_),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

get_action_drop([[goal(X,Y),[HPlan|_]]|Tdrop],[[goal(X,Y),Plan1]|Tdrop],Action):-
    not(applicable(HPlan)),
    solve(goal(X,Y),Path,_,_),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[drop(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].

% --pick
get_action_pick([],[],move(X0,Y0)):-
        agent_at(X0,Y0).
get_action_pick([[goal(X,Y),[HPlan|TPlan]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan.
get_action_pick([[goal(X,Y),[]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    solve(goal(X,Y),Path,_,_),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].
get_action_pick([[goal(X,Y),[HPlan|_]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    not(applicable(HPlan)),
    solve(goal(X,Y),Path,_,_),
    append([_|Move_Path],[_],Path),
    trigger_goal_to_move(Move_Path,Move_move_Path),
    append(Move_move_Path,[pick(X,Y)],FinalPlan),
    FinalPlan = [Action|Plan1].



	
% % -- Q5

% After move(X,Y), intentions stay there
update_intentions(at(_,_),Intentions,Intentions).
% After drop(X,Y), update intentions by drop that intention from list
update_intentions(dropped(_,_),intents([_|Int_drop],Int_pick),intents(Int_drop,Int_pick)).
% After pick(X,Y), update intentions by drop that intention from list
update_intentions(picked(_,_),intents(Int_drop,[_|Int_pick]),intents(Int_drop,Int_pick)).


