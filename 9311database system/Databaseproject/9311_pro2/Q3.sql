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
--limit 5
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