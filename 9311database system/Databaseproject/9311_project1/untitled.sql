create or replace view Q9(name, school, email, starting, num_subjects)
as select distinct people.name, orgunits.longname, people.email,affiliations.starting,count(distinct subjects.code) as num_subjects
from people, staff, orgunits, orgunit_types, affiliations, staff_roles,courses,course_staff,subjects
where people.id=staff.id and courses.subject=subjects.id
and courses.id=course_staff.course and course_staff.staff=staff.id 
and orgunits.utype=orgunit_types.id
and affiliations.staff=staff.id and affiliations.orgunit=orgunits.id and affiliations.role=staff_roles.id
and affiliations.isprimary='t' and affiliations.ending is null and staff_roles.name='Head of School'
and orgunit_types.id=2 group by people.name,orgunits.longname, people.email,affiliations.starting

 1884 | COMP3311 | Database Systems
 4897 | COMP9311 | Database Systems

 select * from Q10d_s1 where subject=1884 or subject=4897;


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