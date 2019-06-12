-- Q1: 
create or replace view Q1(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.unswid,p.name 
from people p join Students s on (p.id=s.id) join course_enrolments c on (c.student=s.id) 
where s.stype='intl' and c.grade >= 85                 --this '85' is no sure
group by p.unswid,p.name having count(c.student)>20;
;



-- Q2: 
create or replace view Q2(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select r.unswid,r.longname
from Rooms r join room_types r_t on (r.rtype=r_t.id) join buildings b on (r.building=b.id) 
where b.name='Computer Science Building' and r_t.description='Meeting Room' and r.capacity>=20
;



-- Q3: 
create or replace view Q3(unswid, name)
as
--... SQL statements, possibly using other views/functions defined by you ...
select p.unswid,p.name from (select c_s.staff from (select c_e.course from (select s.id from Students s join People p on (s.id=p.id) where p.name='Stefan Bilek')  stu join course_enrolments c_e on (stu.id=c_e.student)) cour join course_staff c_s on (cour.course=c_s.course)) satf join People p on (satf.staff=p.id)
;	


-- Q4:

---Q4a:
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
select distinct Q4a.* from Q4a,Q4b where Q4a.unswid not in(Q4b.unswid);
;




-- Q5: 
create or replace view Q5a(num)
as

--... SQL statements, possibly using other views/functions defined by you ...
select count(*) from Q5ab join Q5ac on (Q5ab.id=Q5ac.student)
;

create or replace view Q5ab(id,stype,semester) as
select s.id,s.stype ,semm.semester from (select p_e.id, p_e.student, p_e.semester from ( select id,unswid,year,term from semesters where year=2011 and term='S1') sem join program_enrolments p_e on(sem.id=p_e.semester)) as semm join students s on (s.id=semm.student) where s.stype='local' ;
-----------------------------------
select id,code,name from subjects ;
select id, code, name from streams where name='Chemistry';

create or replace view Q5ac as
select c_e.student from (select c.id from (select subjects.id from streams join subjects on (streams.id=subjects.id) where streams.name='Chemistry') as subj join courses c on (c.subject=subj.id)) as sj_c join course_enrolments c_e on (sj_c.id=c_e.course);
----------
-- Q5: 
create or replace view Q5b(num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select distinct * from Q5ba join Q5bb on(Q5ba.student=Q5bb.id)
;

create or replace view Q5ba as
select pe.id ,pe.student,pe.semester,pe.program from program_enrolments pe join programs p on (p.id=pe.program) where p.name like '%Computer Science%' and p.name like '%Engineering%';
create or replace view Q5bb as
select students.id,students.stype,semesters.year,semesters.term,program_enrolments.program,program_enrolments.semester
from students
inner join program_enrolments on (program_enrolments.student=students.id)
inner join semesters on (semesters.id=program_enrolments.semester)
where students.stype='intl' and semesters.year=2011 and semesters.term='S1';