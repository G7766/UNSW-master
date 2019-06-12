% Library database for COMP9414/9814/3411

% Author: Bill Wilson

%-------- database ---------------------------

% book(CatalogNo, Title, author(Family, Given))
% Each fact is a record of a book in the library.
% This library only has books with a single author :-(
% How would you go about changing the "book" terms to fix this?

book(1, 'Prolog Programming for Artificial Intelligence',
	author(bratko, ivan)).
book(2, 'Tehanu',
	author(leguin, ursula)).
book(3, 'Frog and Reptiles of the Sydney Region',
	author(griffiths, ken)).

% I'm cheating here - Harrison & Minsky are two separate people.
book(4, 'The Turing Option',
	author(minsky, harrison)).

book(5, 'Likely Lads and Lasses',
	author(gill, alan)).
book(6, 'The Left Hand of Darkness',
	author(leguin, ursula)).
book(7, 'September 11',
	author(chomsky, noam)).
book(8, 'La Peste',
	author(camus, albert)).
book(9, 'Harry Potter and the Deathly Hallows',
	author(rowling, jk)).



% member(MemberNo, name(Family, Given), Address)
% Each fact is a record of a registered member/borrower
% in the library.

member(1, name(bloggs, joe), '23 The Irons, Cleethorpe').
member(2, name(bloggs, jane), '23 The Irons, Cleethorpe').
member(3, name(nguyen, john), '2776 Belmore Rd Randwick').
member(4, name(namatjira, stan), '33 Todd Rd, Alice Springs').
member(5, name(windsor, liz), 'The Castle, Windsor').
member(6, name(windsor, phil), 'The Doghouse, The Castle, Windsor').
member(7, name(wong, jerry), '599 Todman Ave Kensington').
member(8, name(ivanova, eva), '598 Todman Ave Kensington').
member(9, name(papadopoulos, jim), '985 Snape St Kingsford').


% loan(CatalogNo, MemberNo, BorrowDate, DueDate)
% Each fact is a record of a loan.

loan(1, 3, date(2015, 3, 13), date(2015, 4, 13)).
loan(9, 8, date(2015, 7, 21), date(2015, 8, 21)).
loan(4, 1, date(2015, 3, 12), date(2015, 4, 12)).
loan(6, 1, date(2015, 3, 12), date(2015, 4, 12)).

%------- bits of code -----------------------

%later(Date1, Date2) if Date1 is after Date2:
later(date(Y, M, Day1), date(Y, M, Day2)) :-
		Day1 > Day2.
later(date(Y, Month1, _), date(Y, Month2, _)) :-
		Month1 > Month2.
later(date(Year1, _, _), date(Year2, _, _)) :-
		Year1 > Year2.

% borrowed(MemFamily, Title, CatalogNo)
% succeeds if a borrower with MemFamily name has borrowed
% a book with this Title and CatalogNo.
borrowed(MemFamily, Title, CatalogNo) :-
   member(MemberNo, name(MemFamily, _), _),
   loan(CatalogNo, MemberNo, _, _),
   book(CatalogNo, Title, _).

% overdue(+DateToday, -Title, -CatalogNo, -MemFamily):
%   given the date Today, produces the Title, CatalogNo,
%   and MemFamily of all overdue books.
overdue(Today, Title, CatalogNo, MemFamily) :-
  loan(CatalogNo, MemberNo, _, DueDate),
  later(Today, DueDate),
  book(CatalogNo, Title, _),
  libmember(MemberNo, name(MemFamily, _), _).

% due_date(+Date_Today, -Due_Date)
% Binds Due_Date to the date one month in the future,
% given today's date, which must be supplied as the
% first argument, e.g. if today is 14 Feb 1966, then
% ?- due_date(date(1966, 2, 14), DueDate).
due_date(date(Y, Month1, D),
         date(Y, Month2, D)) :-
           Month1 < 12,
	   Month2 is Month1 + 1.
due_date(date(Year1, 12, D),
         date(Year2, 1, D)) :-
           Year2 is Year1 + 1.
