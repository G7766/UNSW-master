-- COMP9311 18s1 Project 1
--
-- MyMyUNSW Solution Template


-- Q1: 
create or replace view Q1(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select people.unswid, people.name
from people
inner join students
on people.id = students.id
inner join course_enrolments
on students.id = course_enrolments.student
where students.stype = 'intl'
and course_enrolments.mark >= 85
group by people.unswid, people.name
HAVING count(*) > 20;



-- Q2: 
create or replace view Q2(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select r.unswid, r.longname
from rooms r
inner join room_types rt
on r.rtype = rt.id
inner join buildings b
on r.building = b.id
where b.name = 'Computer Science Building'
and rt.description = 'Meeting Room'
and r.capacity >= 20;



-- Q3: 
create or replace view Q3(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.unswid, p.name
from people p
inner join staff s
on p.id = s.id
inner join course_staff cs
on s.id = cs.staff
inner join course_enrolments ce
on cs.course = ce.course
inner join students st
on ce.student = st.id
inner join people pp
on pp.id = st.id
where pp.name = 'Stefan Bilek'
group by p.unswid, p.name;



-- Q4:
--reate or replace view Q4(unswid, name)
--as
--select p.unswid, p.name
--from people p 
--inner join view04a
--inner join
--... SQL statements, possibly using other views/functions defined by you ...
create or replace view Q4a(unswid, name)
as
select p.unswid, p.name
from people p
inner join students s
on p.id = s.id
inner join course_enrolments ce
on s.id = ce.student
inner join courses c
on ce.course = c.id
inner join subjects sb
on c.subject = sb.id
where sb.code in (select sub.code from subjects sub where sub.code = 'COMP3331')
--and sb.code <> 'COMP3231'
;
create or replace view Q4b(unswid, name)
as
select distinct p.unswid, p.name
from people p
inner join students s
on p.id = s.id
inner join course_enrolments ce
on s.id = ce.student
inner join courses c
on ce.course = c.id
inner join subjects sb
on c.subject = sb.id
where sb.code in (select sub.code from subjects sub where sub.code = 'COMP3231')
;
create or replace view Q4(unswid, name)
	as
select distinct Q4a.unswid, Q4a.name
from Q4a
inner join Q4b
on Q4a.unswid not in (select Q4b.unswid from Q4b);


-- Q5: 
create or replace view Q5a(num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select count(distinct pe.student)
from students s
inner join program_enrolments pe
on s.id = pe.student
inner join semesters sem
on pe.semester = sem.id
inner join stream_enrolments stre
on pe.id = stre.partof
inner join streams str
on str.id = stre.stream
where str.name = 'Chemistry' and sem.name = 'Sem1 2011' and s.stype = 'local'
;

-- Q5: 
create or replace view Q5b(num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select count(distinct pe.student)
from students s
inner join program_enrolments pe
on s.id = pe.student
inner join programs pro
on pe.program = pro.id
inner join semesters sem
on pe.semester = sem.id
inner join stream_enrolments stre
on pe.id = stre.partof
inner join streams str
on str.id = stre.stream
inner join orgunits o
on pro.offeredby = o.id
where s.stype = 'intl' and sem.name = 'Sem1 2011' and (o.name like '%Computer Science and Engineering%');


-- Q6:
create or replace function
	Q6(courseid text) returns text
as $$
declare setof1 text;
begin
	select sub.name, sub.uoc into setof1
	from subjects sub, courses c
	where sub.id = c.subject and sub.code = courseid;
	return setof1;
end;
$$ language sql;



-- Q7: 
create or replace view Q7a(code, name)
	as

select Q7a.code, count(Q7a.code)
from (select pr.code, st.stype
	from programs pr
	inner join program_enrolments pre
	on pr.id = pre.program
	inner join students st
	on pre.student = st.id) as Q7a
	where Q7a.stype = 'intl'
group by Q7a.code;


create or replace view Q7b(code, name)
as
select Q7a.code, count(Q7a.code)
from (select pr.code, st.stype
	from programs pr
	inner join program_enrolments pre
	on pr.id = pre.program
	inner join students st
	on pre.student = st.id) as Q7a
group by Q7a.code;


create or replace view Q7(code, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select Q7aa.code
from (select Q7a.code, count(Q7a.code)
	from (select pr.code, st.stype
		from programs pr
		inner join program_enrolments pre
		on pr.id = pre.program
		inner join students st
		on pre.student = st.id) as Q7a
	where Q7a.stype = 'intl'
	group by Q7a.code) as Q7aa
inner join (select Q7b.code, count(Q7b.code)
	from (select pr.code, st.stype
		from programs pr
		inner join program_enrolments pre
		on pr.id = pre.program
		inner join students st
		on pre.student = st.id) as Q7b
	group by Q7b.code) as Q7bb
on Q7aa.code = Q7bb.code
where (Q7aa.count / Q7bb.count * 100) > 50;


--where Q7a.name > Q7b.name 
--and p.id = Q7a.code
--and p.id = Q7b.code
--and Q7a.code = Q7b.code
;

-- Q8:
create or replace view Q8(code, name, semester)
as
--... SQL statements, possibly using other views/functions defined by you ...
select s.code, s.name, sem.name
from subject s, semesters sem, course_enrolment ce, courses c
where s.id = c.subject
and c.id = ce.coures
and sem.id = c.semester
and (select count(*) from course_enrolments ce where ce.mark = null) > 15
;



-- Q9:
create or replace view Q9(name, school, email, starting, num_subjects)
as
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q10:
create or replace view Q10(code, name, year, s1_HD_rate, s2_HD_rate)
as
--... SQL statements, possibly using other views/functions defined by you ...
;