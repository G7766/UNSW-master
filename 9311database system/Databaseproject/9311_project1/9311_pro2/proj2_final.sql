-------------Q1

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


-------------Q2

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
---Q2
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

---Q3
--------------------Q3:
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
-----Q3_num_in_orgid
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
----Q3_record
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
-----Q3_orgid_f
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
----Q3_record_t
drop type if exists sAtext cascade;
create type sAtext as(student integer,course integer,mark integer,record text);
create or replace function Q3_record_t(studentid integer,orgid integer)
        returns setof sAtext
as $$
declare
x sAtext;
n integer:=1;
begin
for x in (
select students.id as student,courses.id as course,course_enrolments.mark,subjects.code||', '||subjects.name||', '||semesters.name||', '||orgunits.name||', '||course_enrolments.mark as record
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
---Q3_record_t_t
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
-------
drop type if exists CourseRecord cascade;
create type CourseRecord as (unswid integer, student_name text, course_records text);

create or replace function Q3(org_id integer, num_courses integer, min_score integer)
  returns setof CourseRecord
as $$
declare x CourseRecord;
begin
for x in
(select Q3_orgid_f.unswid,Q3_orgid_f.name,concat(Q3_record_t_t.record,'
')
from Q3_orgid_f($1,$2,$3)
inner join Q3_record_t_t(Q3_orgid_f.student,$1) on (Q3_orgid_f.student=Q3_record_t_t.student)
order by Q3_orgid_f.unswid
)
loop
return next x;
end loop;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;







