/*
 * 5.	
 * Má výška HDP vliv na změny ve mzdách a cenách potravin?
 * Neboli, pokud HDP vzroste výrazněji v jednom roce, projeví se to na cenách potravin či mzdách ve stejném nebo násdujícím roce výraznějším růstem?
 */

/*
 * 1. creating view for CZ GDP detail
 */
CREATE VIEW cz_yoy_hdp AS 	
	SELECT
			year_eu,
			country,
			gdp AS HDP,
			ifnull(lag(GDP) OVER (PARTITION BY country ORDER BY year_eu), GDP) AS previous_HDP
		FROM t_david_heczko_project_sql_secondary_final t_sec
		WHERE country LIKE '%cze%'

/*
 * 2. creating view for average payroll trend
 */	
CREATE VIEW avg_pay_percentage_trend AS 
	SELECT
		calculated_year,
		round(avg(avg_pay)) AS avg_pay,
		round(avg(previous_avg_pay)) AS previous_avg_pay,
		round((avg(avg_pay) - avg(previous_avg_pay))) AS avg_pay_diff,
		concat(round(avg(increase_pay),2), ' %') AS avg_pay_growth
	FROM pay_percentage_trend ppt
	GROUP BY calculated_year

/*
 * 3. creating view for average provision prices trend
 */
CREATE VIEW avg_price_percentage_trend AS 	
	SELECT
		calculated_year,
		round(avg(avg_price),2) AS avg_price,
		round(avg(previous_price),2) AS previous_price,
		round((avg(avg_price) - avg(previous_price)),2) AS avg_price_diff,
		concat(round(avg(increase_percentage),2), ' %') AS avg_price_growth
	FROM price_percentage_trend ppt 
	GROUP BY calculated_year 
/*
 * 4. creating view for overall hdp, average payroll and price values and trends
 */
CREATE VIEW hdp_price_pay_yoy AS 
	SELECT
		year_eu,
		HDP,
		HDP - previous_HDP AS HDP_yoy_diff,
		concat(round(((HDP - previous_HDP)/ previous_HDP)*100,2), ' %') AS HDP_yoy_growth,
		pay_tr.avg_pay AS avg_pay,
		pay_tr.previous_avg_pay AS previous_avg_pay,
		pay_tr.avg_pay_diff AS pay_diff,
		pay_tr.avg_pay_growth AS pay_growth,
		price_tr.avg_price AS avg_price,
		price_tr.previous_price AS previous_price,
		price_tr.avg_price_diff AS price_diff,
		price_tr.avg_price_growth AS price_growth
	FROM cz_yoy_hdp cyh
	JOIN avg_pay_percentage_trend pay_tr
		ON cyh.year_eu = pay_tr.calculated_year
	JOIN avg_price_percentage_trend price_tr 
		ON cyh.year_eu = price_tr.calculated_year

/*
 * 5. creating selection to see connection between growth of HDP and growth of pay and prices.
 */	
SELECT
	year_eu,
	HDP,
	HDP_yoy_growth,
	avg_pay,
	pay_growth,
	avg_price,
	price_growth
FROM hdp_price_pay_yoy hppy

