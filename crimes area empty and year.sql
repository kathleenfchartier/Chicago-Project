
select `Community Area`, `Year`, count(`ID`) as crime_count
from chicago_crime_data
where `Community Area` is null or `Community Area`=0
group by `Community Area`, `Year`;

select `Community Area`, `Year`, `Updated On`, count(`ID`)
from chicago_crime_data
where `Community Area` is null and `Year`=2001
group by `Community Area`, `Year`, `Updated On`;