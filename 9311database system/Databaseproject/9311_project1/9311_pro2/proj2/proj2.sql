
//
-- Q6:
create or replace function
        Q6(text) returns text
as
$$ select code||' '||name||' '||uoc from subjects  where code=$1;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language sql;
//





--Q1:

drop type if exists RoomRecord cascade;
create type RoomRecord as (valid_room_number integer, bigger_room_number integer);

create or replace function Q1(course_id integer)
    returns RoomRecord
as $$
declare co_id integer;
declare result RoomRecord;
begin
	select c.id into co_id from courses as c join course_enrolments as c_e on (c.id=c_e.course);
	select a.num_rooms, b.* into result from Q1_output1 as a,Q1_2output($1) as b where a.course=$1;
	--return result;
	if(not found) then
	      raise exception 'INVALID COURSEID';
	end if;
	return result;
	--select c.id into co_id from courses as c join course_enrolments as c_e on (c.id=c_e.course);
	--select a.num_rooms, b.* into result from Q1_output1 as a,Q1_2output($1) as b where a.course=$1;
	--return result;
end;
$$ language plpgsql;




--
select c.id from courses as c join course_enrolments as c_e on (c.id=c_e.course)
--number of students in each course
select count(student) as student_num ,course from course_enrolments group by course;
--number of capacity in each rooms
select id,name,capacity from rooms;



--(output 1 )--course/student_num/num_rooms
create or replace view Q1_output1
as
select num_of_s.course, num_of_s.student_num, count(r.id) as num_rooms
from (select count(student) as student_num ,course from course_enrolments group by course)
as num_of_s, rooms as r where r.capacity>=student_num 
group by num_of_s.course,num_of_s.student_num
;


--(output 2 )--course/student_num/num_rooms
create or replace view Q1_output2
as
select n_of_s.course, n_of_s.num_of_s, count(r.id) as num_rooms
from
(select student_s.course,(waitlist_s.waitlist_student_num+student_s.student_num) as num_of_s
from
	(select count(student) as waitlist_student_num, course from course_enrolment_waitlist group by course)
	as waitlist_s
	inner join 
	(select count(student) as student_num ,course from course_enrolments group by course) 
	as student_s
	on (waitlist_s.course=student_s.course)
) as n_of_s, rooms as r 
where r.capacity>=n_of_s.num_of_s
group by n_of_s.course, n_of_s.num_of_s;

--function Q1--2
create or replace function Q1_2output(course_id int)
	returns int
as $$
declare co_id integer;
begin
	select course into co_id from course_enrolment_waitlist;
	if co_id is null or $1 not in (co_id) then
		return (select num_rooms from Q1_output1 where course=$1);
	else
		return (select num_rooms from Q1_output2 where course=$1);
	end if;
	end;
$$ language plpgsql;














--Q2:

drop type if exists TeachingRecord cascade;
create type TeachingRecord as (cid integer, term char(4), code char(8), name text, uoc integer, average_mark integer, highest_mark integer,median_mark integer, totalEnrols integer);

create or replace function Q2(staff_id integer)
        returns setof TeachingRecord
as $$
declare
result TeachingRecord;
x TeachingRecord;
begin
        for x in
        select Q2_cid.course, Q2_term.term,Q2_code.code,Q2_code.name,case when Q2_code.uoc=0 then null else Q2_code.uoc end as uoc,Q2_mark.avg_mark,
        Q2_mark.max_mark,Q2_medium(Q2_cid.course),Q2_mark.total_num
        from Q2_cid
        inner join Q2_term on (Q2_cid.course=Q2_term.course)
        inner join Q2_code on (Q2_code.id=Q2_cid.course)
        inner join Q2_mark on (Q2_cid.course=Q2_mark.course)
        where Q2_cid.id=$1
        loop
        if x.totalEnrols!=0
        then
        return next x;
        end if;
        end loop;
        if (not found) then
                raise exception 'INVALID STAFFID';
        end if;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;


--course_staff(course,staff),courses(course_id,semester)

---/course/staff_id--cid
create or replace view Q2_cid
as
select course_staff.course,staff.id
from course_staff
inner join staff on (course_staff.staff=staff.id);

--course/semester/term--term
create or replace view Q2_term
as
select courses.id as course,semesters.id as semester,(substring(cast(semesters.year as char(4)),3)||lower(semesters.term)) as term 
from semesters
inner join courses on (semesters.id=courses.semester);
--course,subject--code,subject_name,uoc
create or replace view Q2_code
as
select courses.id,courses.subject,subjects.code,subjects.name,subjects.uoc
from courses join subjects on (courses.subject=subjects.id);
---not null mark
create or replace view Q2_course_enrolments
as
select * from course_enrolments where mark is not null;
--course/avg(mark)--avg(mark)
create or replace view Q2_mark
as
select course,round(avg(mark),0) as avg_mark, max(mark) as max_mark,count(*) as total_num from Q2_course_enrolments group by course;



--medium number(final)
create or replace function Q2_medium(course_id integer)
	returns integer
as $$
declare medium integer;
begin 
	select round(avg(z.mark),0) into medium
		from(select aa.* from 
				(select row_number() over(order by mark) as id, course,mark 
				from (select student,course,mark from Q2_course_enrolments where course=$1 order by mark) as a) as aa, 
				(select count(*) 
				from (select student,course,mark from Q2_course_enrolments where course=$1 order by mark) as b) as bb
				where aa.id=bb.count/2+1 or aa.id=(bb.count+1)/2
			)as z;
	return medium;
end;
$$ language plpgsql;

---!!!!!
select Q2_cid.id as stffid, Q2_cid.course, Q2_term.term,Q2_code.code,Q2_code.name,case when Q2_code.uoc=0 then null end as uoc,Q2_mark.avg_mark,Q2_mark.max_mark,Q2_medium(Q2_cid.course),Q2_mark.total_num
from Q2_cid
inner join Q2_term on (Q2_cid.course=Q2_term.course)
inner join Q2_code on (Q2_code.id=Q2_cid.course)
inner join Q2_mark on (Q2_cid.course=Q2_mark.course)
where Q2_cid.id=5035382;

select Q2_cid.id as stffid, Q2_cid.course, Q2_term.term,Q2_code.code,Q2_code.name,Q2_code.uoc,Q2_mark.avg_mark,Q2_mark.max_mark,Q2_medium(Q2_cid.course),Q2_mark.total_num
from Q2_cid
inner join Q2_term on (Q2_cid.course=Q2_term.course)
inner join Q2_code on (Q2_code.id=Q2_cid.course)
inner join Q2_mark on (Q2_cid.course=Q2_mark.course)
where Q2_cid.id=5035382;

select Q2_cid.course, Q2_term.term,Q2_code.code,Q2_code.name,Q2_code.uoc,Q2_mark.avg_mark,Q2_mark.max_mark,Q2_mark.total_num
from Q2_cid
inner join Q2_term on (Q2_cid.course=Q2_term.course)
inner join Q2_code on (Q2_code.id=Q2_cid.course)
inner join Q2_mark on (Q2_cid.course=Q2_mark.course)
where Q2_mark.total_num=0
;



---中位数test
create or replace view Q2_medium
as
select student,course,mark from Q2_course_enrolments where course=5270 order by mark;


select round(avg(z.mark),0)
from(select a.* from 
		---row_number() 用来给排序 自动添加序号
		(select row_number() over(order by mark) as id, course,mark 
		from Q2_medium) as a, 
		(select count(*) 
		from Q2_medium) as b
		where a.id=b.count/2+1 or a.id=(b.count+1)/2
	) as z;
--------------

--medium number(final)
create or replace function Q2_medium(course_id integer)
	returns integer
as $$
declare medium integer;
begin 
	select round(avg(z.mark),0) into medium
		from(select aa.* from 
				(select row_number() over(order by mark) as id, course,mark 
				from (select student,course,mark from Q2_course_enrolments where course=$1 order by mark) as a) as aa, 
				(select count(*) 
				from (select student,course,mark from Q2_course_enrolments where course=$1 order by mark) as b) as bb
				where aa.id=bb.count/2+1 or aa.id=(bb.count+1)/2
			)as z;
	return medium;
end;
$$ language plpgsql;





--Q3:

drop type if exists CourseRecord cascade;
create type CourseRecord as (unswid integer, student_name text, course_records text);

create or replace function Q3(org_id integer, num_courses integer, min_score integer)
  returns setof CourseRecord
as $$
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;




select students.id as student,people.name,course_enrolments.course,course_enrolments.mark,subjects.code,
subjects.name as subject,semesters.name as semester,orgunits.name as orgunit
from people 
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join course_staff on (course_staff.course=courses.id)
inner join affiliations on (affiliations.staff=course_staff.staff)
inner join orgunits on (orgunits.id=affiliations.orgunit)


---org_num
create or replace function Q3_orgnum(org_id integer)
  returns integer
as $$
declare a integer;
begin
with recursive result as(
select member from orgunit_groups where owner=$1
union 
select orgunit_groups.member
from result join orgunit_groups on (result.member=orgunit_groups.owner))
--select member from result;
select count(member) into a from result;
return a;
end;
$$ language plpgsql;
----student/count(course)
create or replace view Q3_num_course
as
select course_enrolments.student,count(course_enrolments.course)
from course_enrolments
group by course_enrolments.student;
----student/course/mark
create or replace view Q3_course_mark
as
select course_enrolments.student,course_enrolments.course,course_enrolments.mark
from course_enrolments;
-----org_id/member
create or replace function Q3_orgid(org_id integer)
  returns setof integer
as $$
declare x integer;
begin
for x in
(with recursive result as(
select member from orgunit_groups where owner=$1
union 
select orgunit_groups.member
from result join orgunit_groups on (result.member=orgunit_groups.owner))
select member from result)
loop
return next x;
end loop;
end;
$$ language plpgsql;
-----
drop type if exists oAcid cascade;
create type oAcid as (orgid integer, course integer);
create or replace function Q3_num_in_orgid(org_id integer)
  returns setof oAcid
as $$
declare x oAcid;
begin 
for x in
(select Q3_orgid.q3_orgid as orgid,courses.id as course
from Q3_orgid($1) 
inner join subjects on (subjects.offeredby=Q3_orgid.q3_orgid)
inner join courses on (courses.subject=subjects.id))
loop
return next x;
end loop;
end;
$$ language plpgsql;
----
create or replace view Q3_record
as
select students.id as student,course_enrolments.course,subjects.code||', '||subjects.name||', '||semesters.name||', '||orgunits.name||', '||course_enrolments.mark as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join course_staff on (course_staff.course=courses.id)
inner join affiliations on (affiliations.staff=course_staff.staff)
inner join orgunits on (orgunits.id=affiliations.orgunit);
-----
drop type if exists stAidAname cascade;
create type stAidAname as (student integer,unswid integer, name text);
create or replace function Q3_orgid_f(org_id integer, num_courses integer, min_score integer)
  returns setof stAidAname
as $$
declare x stAidAname;
begin 
for x in 
(select distinct(a.student),people.unswid,people.name
from 
	(select course_enrolments.student,course_enrolments.course
	from Q3_num_in_orgid($1)
	inner join course_enrolments on (course_enrolments.course=Q3_num_in_orgid.course)
	where course_enrolments.mark>=$3) 
	as a inner join 
	(select course_enrolments.student,count(Q3_num_in_orgid.course)
	from Q3_num_in_orgid($1)
	inner join course_enrolments on (course_enrolments.course=Q3_num_in_orgid.course)
	group by course_enrolments.student
	having count(Q3_num_in_orgid.course)>$2
	) as b on (a.student=b.student)
	inner join people on (a.student=people.id))
loop
return next x;
end loop;
end;
$$ language plpgsql;

----
drop type if exists sAtext cascade;
create type sAtext as(student integer,course integer,mark integer,record text);
create or replace function Q3_record_t(studentid integer,orgid integer)
	returns setof sAtext
as $$
declare x sAtext;
begin
for x in (
select students.id as student,courses.id as course,course_enrolments.mark,subjects.code||','||subjects.name||','||semesters.name||','||orgunits.name||','||course_enrolments.mark as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join orgunits on (orgunits.id=subjects.offeredby)
inner join Q3_num_in_orgid($2) on (course_enrolments.course=Q3_num_in_orgid.course)
where students.id=$1 
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id asc
)
loop
if n<=5 then 
	if x.mark is null 
	then x.record='null';
		n=n+1;
	return next x;
	else
		n=n+1;
	return next x;
	end if;
else
end if;
end loop;
end;
$$ language plpgsql;
---
drop type if exists sAt cascade;
create type sAt as(student integer,record text);
create or replace function Q3_record_t_t(studentid integer,orgid integer)
	returns setof sAt
as $$
declare 
x sAt;
begin
for x in(
select distinct(k2.student),array_to_string(array(select k1.record from Q3_record_t($1,$2) as k1 where k1.student=k2.student),E'\n')
from Q3_record_t($1,$2) as k2
)
loop
return next x;
end loop;
end;
$$ language plpgsql;
---
drop type if exists CourseRecord cascade;
create type CourseRecord as (unswid integer, student_name text, course_records text);

create or replace function Q3(org_id integer, num_courses integer, min_score integer)
  returns setof CourseRecord
as $$
declare x CourseRecord;
begin
for x in 
(select Q3_orgid_f.unswid,Q3_orgid_f.name,Q3_record_t_t.record
from Q3_orgid_f($1,$2,$3)
inner join Q3_record_t_t(Q3_orgid_f.student,$1) on (Q3_orgid_f.student=Q3_record_t_t.student)
)
loop
return next x;
end loop;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;

/* 
select  Q3_orgid_f.unswid,Q3_orgid_f.name,Q3_record.record
from Q3_orgid_f(52,35,100)
inner join Q3_record on (Q3_record.student=Q3_orgid_f.student)
*/
Q3_orgid_f

create or replace view Q3_record
as
select students.id as student,course_enrolments.course,subjects.code||','||subjects.name||','||semesters.name||','||orgunits.name||','||course_enrolments.mark as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join course_staff on (course_staff.course=courses.id)
inner join affiliations on (affiliations.staff=course_staff.staff)
inner join orgunits on (orgunits.id=affiliations.orgunit)
group by ;








---test 35,100
select Q3_course_mark.student
from Q3_num_course
inner join Q3_course_mark on (Q3_num_course.student=Q3_course_mark.student)
where Q3_num_course.count>=35 and Q3_course_mark.mark>=100;


create or replace view Q3_num_course
as
select students.id,people.name, count(course_enrolments.course)
from students
inner join people on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join course_staff on (course_staff.course=courses.id)
inner join affiliations on (affiliations.staff=course_staff.staff)
inner join orgunits on (orgunits.id=affiliations.orgunit)
group by students.id,people.name

---staff,orgid,course
create or replace view Q3_num_in_orgid
as
select Q3_orgid.q3_orgid as orgid,courses.id as course
from Q3_orgid(52) 
inner join subjects on (subjects.offeredby=Q3_orgid.q3_orgid)
inner join courses on (courses.subject=subjects.id);

---学生最少选了35门课，并且至少有一门是在100分及以上  的 学生学号和课，成绩
--大于100分的学生
create or replace view Q3_student_limit_mark
as
select a.student,Q3_num_in_orgid.course,a.mark
from Q3_num_in_orgid
inner join (select student,course,mark from course_enrolments) as a on (Q3_num_in_orgid.course=a.course)
where a.mark>=100
;
select a.student,people.name
from 
	(select distinct(course_enrolments.student)
	from Q3_num_in_orgid
	inner join course_enrolments on (course_enrolments.course=Q3_num_in_orgid.course)
	where course_enrolments.mark>=100) 
	as a inner join 
	(select course_enrolments.student,count(Q3_num_in_orgid.course)
	from Q3_num_in_orgid
	inner join course_enrolments on (course_enrolments.course=Q3_num_in_orgid.course)
	group by course_enrolments.student
	having count(Q3_num_in_orgid.course)>35
	) as b on (a.student=b.student)
	inner join people on (a.student=people.id);


select course_enrolments.student,count(Q3_num_in_orgid.course)
from Q3_num_in_orgid
inner join course_enrolments on (course_enrolments.course=Q3_num_in_orgid.course)
group by course_enrolments.student
having count(Q3_num_in_orgid.course)>=35;





having count(course_enrolments.student)>=35;

--  >=35的学生
create or replace view Q3_student_course
as
select a.student,count(Q3_num_in_orgid.course)
from Q3_num_in_orgid
inner join (select student,course,mark from course_enrolments) as a on (Q3_num_in_orgid.course=a.course)
group by a.student
having count(Q3_num_in_orgid.course)>=35;

Q3_student_course.student,
select distinct(people.name)
from Q3_student_course
inner join Q3_student_limit_mark on (Q3_student_course.student=Q3_student_limit_mark.student)
inner join people on (Q3_student_course.student=people.id)
;

