/*
 * 1. creation of view and selection for czechia_price with relevant colums, calculated year and average value of prices
 */
CREATE VIEW IF NOT EXISTS cz_price_by_years AS 		
	SELECT
		YEAR(date_from) AS calculated_year,
		cpc.name AS calculated_item,
		concat(cpc.price_value, ' ', cpc.price_unit) AS amount_value,
		round(avg(value), 2) AS avg_value,
		cr.name AS calculated_region
	FROM czechia_price c_price
	JOIN czechia_price_category cpc
		ON c_price.category_code = cpc.code
	JOIN czechia_region cr
		ON c_price.region_code = cr.code
	WHERE
		region_code IS NOT NULL
	GROUP BY
		category_code,
		region_code,
		YEAR(date_from)
	ORDER BY
		year(date_from)
			

-- check of the created view
SELECT *
FROM cz_price_by_years cpby;


/*
 * 2. create selection for czechia_payroll
 */
CREATE VIEW IF NOT EXISTS cz_avg_pay AS 
	SELECT
		c_pay.payroll_year,
		avg(c_pay.value) AS avg_pay,
		c_pay.industry_branch_code,
		cpib.name
	FROM czechia_payroll c_pay
	JOIN czechia_payroll_calculation cpc
		ON c_pay.calculation_code = cpc.code
	JOIN czechia_payroll_value_type p_type
		ON c_pay.value_type_code = p_type.code
	JOIN czechia_payroll_industry_branch cpib
		ON c_pay.industry_branch_code = cpib.code
	WHERE 
		p_type.code = 5958
		AND 
		c_pay.calculation_code = 200
	GROUP BY
		payroll_year,
		industry_branch_code,
		cpib.name 
	ORDER BY
		payroll_year,
		industry_branch_code
		
DROP VIEW cz_avg_pay

/*
 * 3. Join of cz_avg_pay and cz_price_by_years and create table
 */


CREATE OR REPLACE TABLE t_david_heczko_project_SQL_primary_final AS 
	SELECT
		cap.payroll_year AS calculated_year,
		round(cap.avg_pay) AS avg_pay,
		cap.name,
		cpby.calculated_item,
		cpby.amount_value,
		cpby.avg_value	
	FROM cz_avg_pay cap
	LEFT JOIN cz_price_by_years cpby
		ON cap.payroll_year = cpby.calculated_year
	WHERE cpby.calculated_item IS NOT NULL
	GROUP BY 
		cpby.calculated_year,
		cap.avg_pay,
		cap.name,
		cpby.calculated_item,
		cpby.amount_value,
		cpby.avg_value
		
SELECT *
FROM t_david_heczko_project_sql_primary_final dtable
