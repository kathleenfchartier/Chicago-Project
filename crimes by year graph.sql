

select `Year`, count(`Year`) as numb_crimes,  REPEAT('*', count(`Year`)/10000) as 'Graph'
from `chicago_crime_data`
group by `Year`
order by `Year`;