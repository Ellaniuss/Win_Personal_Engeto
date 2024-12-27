/*
 * 1. creating view to compare avg pay year on year difference for each industry during years 2006 and 2018
 */
CREATE VIEW pay_comparation AS 
	SELECT
		calculated_year,
		branch_code,
		branch_name,
		avg_pay,
		ifnull(lag(avg_pay) OVER (PARTITION BY branch_code ORDER BY calculated_year),avg_pay) AS pervious_avg_pay 
	FROM t_david_heczko_project_sql_primary_final t_prim
	GROUP BY
		calculated_year,
		branch_code,
		branch_name,
		avg_pay
	ORDER BY
		branch_code,
		calculated_year
	
	
/*
 * 2. calculation of percentage value of the yoy pay difference of each indrustry
 */
CREATE VIEW pay_percentage_trend AS 
	SELECT
		calculated_year,
		branch_code,
		branch_name,
		avg_pay,
		pervious_avg_pay,
		round(((avg_pay - pervious_avg_pay)/pervious_avg_pay)* 100, 2) AS increase_pay
	FROM pay_comparation pc
	
	

/*
 * 3. calculation of overall yoy average pay difference of all industries and overall yoy average price difference of all provisions.
 *    Price yoy difference for each provision type in percentage is in view price_precentage_trend, created by script project4_SQL_question_3.sql.
 */
CREATE VIEW overall_price_pay_trend AS 
	SELECT
		ppt.calculated_year,
		round(avg(ppt.increase_pay),2) AS overall_pay_avg_increase,
		round(avg(ppt2.increase_percentage),2) AS overall_price_avg_increase
	FROM pay_percentage_trend ppt
	JOIN price_precentage_trend ppt2
		ON ppt.calculated_year = ppt2.calculated_year
	GROUP BY
		calculated_year


/*
 * 4. comparation of overal yoy average percentage growth of wages and prices between 2006 and 2018
 */
CREATE VIEW price_pay_growth_comparation AS 
	SELECT
		calculated_year,
		concat(overall_pay_avg_increase, ' %') AS overall_pay_avg_increase,
		concat(overall_price_avg_increase, ' %') AS overall_price_avg_increase,
		concat(overall_price_avg_increase - overall_pay_avg_increase, ' %') AS price_pay_growth_difference
	FROM overall_price_pay_trend oppt
	ORDER BY
		overall_price_avg_increase - overall_pay_avg_increase DESC

/*
 * 5. display of results
 */
SELECT *		
FROM price_pay_growth_comparation ppgc 