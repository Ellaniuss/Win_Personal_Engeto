/*
 * 1. creating view to display only provisions and their prices for calculated year
 */
CREATE VIEW provision_prices_by_year AS
	SELECT
		calculated_year,
		provision_name,
		provision_unit,
		avg_price
	FROM t_david_heczko_project_sql_primary_final t_prim
	GROUP BY
		provision_name,
		calculated_year,
		provision_unit,
		avg_price
	ORDER BY
		provision_name,
		calculated_year,
		branch_code
/*
 * 2. creating view that shows prices by year and prices from pervious year to compare
 */
		
CREATE VIEW provision_prices_comparation AS 		
	SELECT
		calculated_year,
		provision_name,
		avg_price,
		ifnull(lag(avg_price) OVER (PARTITION BY provision_name ORDER BY calculated_year), avg_price) AS pervious_price
	FROM provision_prices_by_year ppby

	
/*
 * 3. creating view that shows precentage increase/decrease between years per provision type
 */	
CREATE VIEW price_precentage_trend AS 
	SELECT
		calculated_year,
		provision_name,
		avg_price,
		pervious_price,
		round(((avg_price - pervious_price) / pervious_price) * 100,2) AS increase_percentage
	FROM provision_prices_comparation ppc
	

/*
 * 4. creating view that shows overall precentage increase/decrease of provision prices 
 */	
CREATE VIEW price_precentage_trend_final AS
	SELECT
		provision_name,
		concat(round(avg(increase_percentage),2), ' %') AS percentage_trend
	FROM price_precentage_trend ppt
	GROUP BY
		provision_name
	ORDER BY
		round(avg(increase_percentage),2)
		
SELECT *
FROM price_precentage_trend_final pptf