delete  
from extraschool_prestationtimes
where prestation_times_of_the_day_id in (
select max(ptddd.id)
from (select ptdd.id z_id, activity_category_id, child_id, date_of_the_day
from extraschool_prestation_times_of_the_day ptdd
left join extraschool_child ecc on ptdd.child_id = ecc.id
where ptdd.id in (select zz_id
from (select min(ptd.id) as zz_id,date_of_the_day,child_id, count(*)
from extraschool_prestation_times_of_the_day ptd
left join extraschool_child ec on ptd.child_id = ec.id
group by activity_category_id,date_of_the_day,child_id
having count(*) > 1
) as subq)) as subqq
left join extraschool_prestation_times_of_the_day ptddd on subqq.child_id = ptddd.child_id and subqq.date_of_the_day = ptddd.date_of_the_day
left join extraschool_prestationtimes ept on ept.prestation_times_of_the_day_id = ptddd.id
group by subqq.activity_category_id, subqq.child_id, subqq.date_of_the_day
);