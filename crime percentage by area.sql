
SELECT sc.`Community Area`
     , COUNT(`ID`) AS total                     /* Counts the total by community area with group by */
     , COUNT(`ID`) / t.cnt* 100 AS `percentage` /* Calculates the percentage of total by community area to overall crime total from cross join*/
FROM chicago_crime_data as sc
CROSS JOIN(SELECT COUNT(`ID`) AS cnt FROM chicago_crime_data) t  /* Counts total crimes */
GROUP BY sc.`Community Area`, t.cnt  
order by `percentage` desc;
 
