
-- Following shows how many litres of milk and kilograms of bread could be bought for average pay in years 2006 and 2018

SELECT
	calculated_year,
	round(avg(avg_pay), 2) AS avg_pay,
	provision_name,
	provision_unit,
	avg_price,
	round((avg_pay/avg_price)) AS item_amount_per_pay,
	CASE
		WHEN provision_unit LIKE '%kg%' THEN 'kg'
		WHEN provision_unit LIKE '%ks%' THEN 'ks'
		WHEN provision_unit LIKE '%l%' THEN 'l'
		ELSE 'g'
	END AS unit_per_pay
FROM t_david_heczko_project_sql_primary_final t_primary
WHERE 
	calculated_year IN (2006, 2018)
	AND (provision_name LIKE '%mleko%' OR provision_name LIKE '%chleb%')
GROUP BY
	calculated_year,
	provision_name,
	provision_unit,
	avg_price