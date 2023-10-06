
select `Elementary, Middle, or High School`, count(`Elementary, Middle, or High School`) as school_count
from chicago_public_schools_perc
group by `Elementary, Middle, or High School`;