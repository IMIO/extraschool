select c.schoolimplantation as schoolimplantation, ept.parent_id as parent_id, childid, min(activity_occurrence_id) activity_occurrence_id,
                                    sum(case when es = 'S' then prestation_time else 0 end) - sum(case when es = 'E' then prestation_time else 0 end) as duration
                                    
                                from extraschool_prestationtimes ept
                                left join extraschool_child c on ept.childid = c.id
                                left join extraschool_parent p on p.id = c.parentid
                                left join extraschool_activityoccurrence ao on ao.id = ept.activity_occurrence_id
                                left join extraschool_activity a on a.id = ao.activityid
                                where ept.prestation_date between '2018-05-01' and '2018-05-31'
                                        and verified = True
                                        and ept.activity_category_id = 1
                                        and invoiced_prestation_id is NULL
                                group by ept.parent_id,c.schoolimplantation,childid, p.streetcode,case when tarif_group_name = '' or tarif_group_name is NULL then a.name else tarif_group_name  end, ept.prestation_date
                                order by parent_id, c.schoolimplantation, min(activity_occurrence_id)
-- Do in HANNUT

SELECT *
FROM extraschool_prestationtimes
WHERE prestation_times_of_the_day_id = 171388

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 471903
WHERE id = 491862;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 469954
WHERE id = 491863;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 469034
WHERE id = 516426;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468930
WHERE id = 491860;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468933
WHERE id = 505279;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468936
WHERE id = 516429;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468929
WHERE id = 491861;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 466368
WHERE id = 516419;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 465786
WHERE id = 516428;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 465785
WHERE id = 505280;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 465785
WHERE id = 505280;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 466369
WHERE id = 516424;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468933
WHERE id = 510579;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 468934
WHERE id = 505282;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 469033
WHERE id = 516431;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 469957
WHERE id = 516422;

UPDATE extraschool_prestationtimes
SET invoiced_prestation_id = 471905
WHERE id = 516421;

