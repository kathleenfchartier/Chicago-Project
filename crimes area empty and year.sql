/*  Query crime count by Year for crimes without Comminity area  */

select `Community Area`, `Year`, count(`ID`) as crime_count
from chicago_crime_data
where `Community Area` is null or `Community Area`=0
group by `Community Area`, `Year`;
