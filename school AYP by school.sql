/* 
How many schools made AYP by area?
*/
select `Elementary, Middle, or High School`, 
        sum(case when `Adequate Yearly Progress Made?`='Yes' then 1 else 0 end) as AYP_met,
        sum(case when `Adequate Yearly Progress Made?`='No' then 1 else 0 end) as AYP_not_met
from chicago_public_schools
group by `Elementary, Middle, or High School`
;


select `Elementary, Middle, or High School`, `Adequate Yearly Progress Made?`, count(`Adequate Yearly Progress Made?`) as ayp_count
from chicago_public_schools
group by `Adequate Yearly Progress Made?`, `Elementary, Middle, or High School`;