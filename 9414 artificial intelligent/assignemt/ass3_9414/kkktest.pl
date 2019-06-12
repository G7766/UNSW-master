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






% % Q4
% % ----- Q4:

%get_action(Intentions,Intentions1,Action)

% agent_stones(1) if already have a stone, go to drop
get_action(intents([HInt_drop|TInt_drop],Int_pick),intents([HInt_drop1|TInt_drop],Int_pick),Action):-
    agent_stones(1),
    get_action_drop(HInt_drop,HInt_drop1,Action),!.


% agent_stones(0) if do not have a stone, go to pick 
get_action(intents(Int_drop,[HInt_pick|TInt_pick]),intents(Int_drop,[HInt_pick1|TInt_pick]),Action):-
    agent_stones(0),
    get_action_pick(HInt_pick,HInt_pick1,Action),!.

get_action(intens(Int_drop,[]),intents(Int_drop,[HInt_pick1|TInt_pick]),Action):-
    agent_at(X0,Y0),
    move(X0,Y0),!.

% -----------------   
% get_action_drop(goal, plan, plan1, action)

get_action_drop([],[],move(X0,Y0)):-
        agent_at(X0,Y0),!.

get_action_drop([goal(X,Y),[HPlan|TPlan]],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan,!.

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
    agent_at(X0,Y0),!.

get_action_pick([[goal(X,Y),[HPlan|TPlan]]|Tpick],[[goal(X,Y),Plan1]|Tpick],Action):-
    applicable(HPlan),
    Action = HPlan,
    Plan1 = TPlan,!.

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







s(state(X1,Y1),state(X2,Y2),1):-
    land(X2,Y2),
    mandist(X1/Y1,X2/Y2,1).

s(state(X1,Y1),state(X2,Y2),1000):-
    between(1, 100, X2),
    between(1, 100, Y2),
    not(land(X2,Y2)),
    mandist(X1/Y1,X2/Y2,1).


s(goal(X1,Y1),goal(X2,Y2),1):-
    land_or_dropped(X2,Y2),
    distance((X1,Y1),(X2,Y2),1).

s(goal(X1,Y1),goal(X2,Y2),1000):-
    UX1 is X1 + 1,
    DX1 is X1 - 1,
    UY1 is Y1 + 1,
    DY1 is Y1 - 1,
    between(DY1,UY1,Y2),
    between(DX1,UX1,X2),
    distance((X1,Y1),(X2,Y2),1).
goal(state(1,1)).

s(state(X1,Y1),state(X2,Y2),1):-
    land_or_dropped(X2,Y2),
    distance((X1,Y1),(X2,Y2),1).

s(state(X1,Y1),state(X2,Y2),1000):-
    UX1 is X1 + 1,
    DX1 is X1 - 1,
    UY1 is Y1 + 1,
    DY1 is Y1 - 1,
    between(DY1,UY1,Y2),
    between(DX1,UX1,X2),
    distance((X1,Y1),(X2,Y2),1).
goal(state(1,1)).