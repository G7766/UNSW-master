create or replace view Q1(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.unswid,p.name 
from people p join Students s on (p.id=s.id) join course_enrolments c on (c.student=s.id) 
where s.stype='intl' and c.mark >= 85                 
group by p.unswid,p.name having count(c.student)>20;
;


--(pass)
-- Q2: 
create or replace view Q2(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select r.unswid,r.longname
from Rooms r join room_types r_t on (r.rtype=r_t.id) join buildings b on (r.building=b.id) 
where b.name='Computer Science Building' and r_t.description='Meeting Room' and r.capacity>=20
;


--(pass)
-- Q3: 
create or replace view Q3(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.unswid,p.name from (select c_s.staff from (select c_e.course from (select s.id from Students s join People p on (s.id=p.id) where p.name='Stefan Bilek')  stu join course_enrolments c_e on (stu.id=c_e.student)) cour join course_staff c_s on (cour.course=c_s.course)) satf join People p on (satf.staff=p.id)
;


--Q4(pass)
create or replace view Q4a(unswid,name) as
select p.unswid,p.name
from people p
inner join course_enrolments c_e on (c_e.student=p.id)
inner join courses c on (c.id=c_e.course)
inner join subjects s on (s.id=c.subject)
where s.code='COMP3331';
--Q4b:
create or replace view Q4b(unswid,name) as
select p.unswid,p.name
from people p
inner join course_enrolments c_e on (c_e.student=p.id)
inner join courses c on (c.id=c_e.course)
inner join subjects s on (s.id=c.subject)
where s.code='COMP3231';

create or replace view Q4(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct Q4a.* from Q4a
inner join Q4b on (Q4a.unswid not in(select unswid from Q4b));
;




--(pass)
-- Q6:
create or replace function
	Q6(text) returns text
as
$$ select code||' '||name||' '||uoc from subjects  where code=$1;
$$ language sql;


--(pass)
-- Q7: 
--count num of all program
create or replace view Q7a(count, program)
as
select count(student),program from program_enrolments group by (program)
;
--intl student
create or replace view Q7b(count, program)
as
select count(intl_s.student),intl_s.program
from
	(select p_e.student,p_e.program 
	from students s join program_enrolments p_e on(s.id=p_e.student)where s.stype='intl') 
	as intl_s group by (intl_s.program)
;
create or replace view Q7(code, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.code,p.name from
(select pro.program from(select cast(Q7b.count::float/Q7a.count as numeric(3,2)) as percent, Q7b.program from Q7a join Q7b on (Q7a.program=Q7b.program)) as pro where pro.percent>0.5) as f join programs p on(f.program=p.id)
;



--Q8(pass)
create or replace view Q8a
as
select avg(c_e.mark) as mark ,c_e.course,c.subject,c.semester 
from course_enrolments c_e 
join courses c on(c_e.course=c.id)
where c_e.mark is not null 
group by c_e.course , c.subject ,c.semester having count(c_e.mark)>=15
;

create or replace view Q8b
as
select Q8a.*
from
	(select max(mark) from Q8a) as l join Q8a on (l.max=Q8a.mark)
;

create or replace view Q8(code, name, semester)
as
select s.code,s.name,sem.name
from Q8b
inner join subjects s on s.id=Q8b.subject
inner join semesters sem on (sem.id=Q8b.semester)
;


-- Q9:(pass)
--find people
create or replace view Q9a as
select p.name,o.longname,p.email,a.starting,a.staff
from People p
inner join affiliations a on (a.staff=p.id)
inner join orgunits o on (o.id=a.orgunit)
inner join staff_roles s_r on(s_r.id=a.role)
inner join orgunit_types o_t on (o_t.id=o.utype)
where s_r.name='Head of School' and a.ending is null and a.isprimary='t' and o_t.name='School'
;




--find staff and num_subject
create or replace view Q9c as
select count( distinct m.code) as num_subjects, m.staff
from 
	(select c_s.course,c.subject,s.code,c_s.staff
	from course_staff c_s
	inner join courses c on (c.id=c_s.course)
	inner join subjects s on (s.id=c.subject)
	) as m group by m.staff having count(m.code)>0
;

create or replace view Q9(name, school, email, starting, num_subjects)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct Q9a.name,Q9a.longname,Q9a.email,Q9a.starting,Q9c.num_subjects
from Q9a join Q9c on (Q9a.staff=Q9c.staff)
;












-- Q10:(pass)
--copm93 student mark on 03-12 sem
create or replace view Q10a
as
select c_e.course,c.subject,c.semester,c_e.student,c_e.mark,sem.term,sem.year
from courses c
inner join course_enrolments c_e on (c_e.course=c.id)
inner join (select id,code,name,offeredby from subjects where code like 'COMP93%') as cc on (cc.id=c.subject)
inner join (select id,substring(cast(year as char(4)),3) as year,term,name from semesters where term like 'S%' and year between 2003 and 2012) as sem on (sem.id=c.semester)
;

create or replace view Q10b
as
select count(student),subject,semester,year from Q10a where mark>=0 group by subject,semester,year order by semester;

--number of student in subject mark<85
create or replace view Q10c
as
select count(student),subject,semester,year from Q10a where mark<85 group by subject,semester,year order by semester;


--hd_rate
create or replace view Q10d
as
select cast((1-Q10c.count::float/Q10b.count) as numeric(4,2)) as rate, Q10c.subject, Q10c.semester, Q10b.year
from Q10b,Q10c 
where  Q10b.subject=Q10c.subject and Q10b.semester= Q10c.semester
;

--s1 hd_rate
create or replace view Q10d_s1
as
select Q10d.*,semesters.term
from Q10d join semesters on(Q10d.semester=semesters.id)
where semesters.term='S1'
;
--s2 hd_rate
create or replace view Q10d_s2
as
select Q10d.*,semesters.term
from Q10d join semesters on(Q10d.semester=semesters.id)
where semesters.term='S2'
;



create or replace view Q10x(code, name, year, s1_HD_rate, s2_HD_rate)
as
select distinct s.code,s.name,Q10d_s1.year,Q10d_s1.rate as rate1 ,Q10d_s2.rate as rate2
from Q10d_s1 , Q10d_s2 , subjects as s
where Q10d_s1.subject=s.id and Q10d_s2.subject=s.id and Q10d_s1.subject=Q10d_s2.subject and Q10d_s1.year=Q10d_s2.year
order by s.name
;

create or replace view Q10(code, name, year, s1_HD_rate, s2_HD_rate)
as
select Q10x.code,Q10x.name,Q10x.year,Q10x.s1_HD_rate,Q10x.s2_HD_rate
from
(select name
from Q10x
group by name having count(year)=10) as z join Q10x on (z.name=Q10x.name);

