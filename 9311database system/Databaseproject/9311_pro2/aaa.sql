


create or replace function Q1(course_id integer)
    returns RoomRecord
as $$
declare co_id integer;
declare result RoomRecord;
begin
	select c.id into co_id from courses as c join course_enrolments as c_e on (c.id=c_e.course);
	exception
	when $1 not in (co_id) then
		raise exception 'INVALIDCOURSEID';
	if  $1 in (co_id) then
		select num_rooms into result from Q1_output1;
		select * into result from Q1_2output($1);
		return result;
	end if;
end;
$$ language plpgsql;


----
drop type if exists RoomRecord cascade;
create type RoomRecord as (valid_room_number integer, bigger_room_number integer);

create or replace function Q1(course_id integer)
    returns RoomRecord
as $$
declare co_id integer;
declare result RoomRecord;
begin
if(not found)
raise exception "";
end if;
	select c.id into co_id from courses as c join course_enrolments as c_e on (c.id=c_e.course);
	exception

	
		select num_rooms into result from Q1_output1;
		select * into result from Q1_2output($1);
		return result;
	end;
$$ language plpgsql;
----


--success but no exception
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


drop type if exists TeachingRecord cascade;
create type TeachingRecord as (cid integer, term char(4), code char(8), name text, uoc integer, average_mark integer, highest_mark integer, median_mark integer, totalEnrols integer);

create or replace function Q2(staff_id integer)
	returns setof TeachingRecord
as $$
declare result TeachingRecord;
begin
	select Q2_cid.course, Q2_term.term,Q2_code.code,Q2_code.name,Q2_code.uoc,Q2_mark.avg_mark,
	Q2_mark.max_mark,Q2_medium(Q2_cid.course),Q2_mark.total_num into result
	from Q2_cid
	inner join Q2_term on (Q2_cid.course=Q2_term.course)
	inner join Q2_code on (Q2_code.id=Q2_cid.course)
	inner join Q2_mark on (Q2_cid.course=Q2_mark.course)
	where Q2_cid.id=$1;
	if (not found) then
		raise exception 'INVALID STAFFID';
	end if;
	return result;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;



--2
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
	where Q2_cid.id=5035382
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
--1
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








select a.student,a.course,people.unswid,people.name
from 
	(select course_enrolments.student,course_enrolments.course
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

---
drop type if exists sAtext cascade;
create type sAtext as(student integer,course integer,mark integer,record text);
create or replace function Q3_record_t(studentid integer)
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
where students.id=$1
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id desc
limit 5
)
loop 
if x.mark is null 
then x.record='null';
return next x;
else
return next x;
end if;
end loop;
end;
$$ language plpgsql;


drop type if exists CourseRecord cascade;
create type CourseRecord as (unswid integer, student_name text, course_records text);

create or replace function Q3(org_id integer, num_courses integer, min_score integer)
  returns setof CourseRecord
as $$
declare x CourseRecord;
begin
for x in 
(select Q3_orgid_f.unswid,Q3_orgid_f.name,Q3_record_t.record
from Q3_orgid_f($1,$2,$3),Q3_record_t(Q3_orgid_f.student))
--inner join Q3_record on (Q3_record.student=Q3_orgid_f.student))
loop
return next x;
end loop;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;


1129218
1139998
63161
select * from Q3_record_t(1129218);





select students.id as student,courses.id as course,course_enrolments.mark,subjects.code||','||subjects.name||','||semesters.name||','||orgunits.name||','||course_enrolments.mark as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join orgunits on (orgunits.id=subjects.offeredby)
where students.id=1139998 
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id desc
limit 5


select * from Q3_num_in_orgid(52);
PHAR3306
select courses.id,subjects.name from subjects 
inner join courses on (subjects.id=courses.subject) where subjects.code='PHAR3306'
----

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
----
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
----
select distinct(k2.student),array_to_string(array(select k1.record from Q3_record_t(1139998,52) k1 where k1.student=k2.student),E'\n')
from Q3_record_t(1139998,52) k2
---??

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
limit 5
)
loop 
if x.mark is null 
then x.record='null';
return next x;
else
return next x;
end if;
end loop;
end;
$$ language plpgsql;



select students.id as student,
array_to_string(array(select subjects.code||','||subjects.name||','||semesters.name||','||orgunits.name||','||course_enrolments.mark
from 
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join orgunits on (orgunits.id=subjects.offeredby)
inner join Q3_num_in_orgid(52) on (course_enrolments.course=Q3_num_in_orgid.course)
where students.id=1139998
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id asc
limit 5
),'\n') as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join orgunits on (orgunits.id=subjects.offeredby)
inner join Q3_num_in_orgid(52) on (course_enrolments.course=Q3_num_in_orgid.course)
where students.id=1139998
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id asc
limit 5
;

create or replace view k
as 
select students.id as student,courses.id as course,course_enrolments.mark,subjects.code||','||subjects.name||','||semesters.name||','||orgunits.name||','||course_enrolments.mark as record
from people
inner join students on (people.id=students.id)
inner join course_enrolments on (course_enrolments.student=students.id)
inner join courses on (course_enrolments.course=courses.id)
inner join subjects on (courses.subject=subjects.id)
inner join semesters on (courses.semester=semesters.id)
inner join orgunits on (orgunits.id=subjects.offeredby)
inner join Q3_num_in_orgid(52) on (course_enrolments.course=Q3_num_in_orgid.course)
where students.id=1139998
order by case when course_enrolments.mark is null then 0 else 1 end desc,course_enrolments.mark desc,courses.id asc
limit 5;



select distinct(k1.student),array_to_string(array(select k2.record from k k2 where k1.student=k2.student),E'\n')
from k k1

select distinct(k2.student),array_to_string(array(select k1.record from Q3_record_t(1139998,52) k1 where k1.student=k2.student),E'\n')
from Q3_record_t(1139998,52) k2

----Q3
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

drop type if exists CourseRecord cascade;
create type CourseRecord as (unswid integer, student_name text, course_records text);

create or replace function Q3(org_id integer, num_courses integer, min_score integer)
  returns setof CourseRecord
as $$
declare x CourseRecord;
begin
for x in 
(select Q3_orgid_f.unswid,Q3_orgid_f.name,Q3_record_t.record
from Q3_orgid_f($1,$2,$3)
inner join Q3_record_t(Q3_orgid_f.student,$1) on (Q3_record_t.student=Q3_orgid_f.student))
loop
return next x;
end loop;
end;
--... SQL statements, possibly using other views/functions defined by you ...
$$ language plpgsql;
