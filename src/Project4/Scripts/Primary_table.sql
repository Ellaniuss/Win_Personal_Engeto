/*
 * 1. creation of view and selection for czechia_price with relevant colums, calculated year and average value of prices
 */
CREATE VIEW cz_price_by_years AS 		
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
CREATE VIEW cz_avg_pay AS 
	SELECT
		c_price.payroll_year,
		avg(c_price.value) AS avg_pay,
		c_price.industry_branch_code,
		cpib.name
	FROM czechia_payroll c_price
	JOIN czechia_payroll_calculation cpc
		ON c_price.calculation_code = cpc.code
	JOIN czechia_payroll_unit cpu
		ON c_price.unit_code = cpu.code
	JOIN czechia_payroll_value_type p_type
		ON c_price.value_type_code = p_type.code
	JOIN czechia_payroll_industry_branch cpib
		ON c_price.industry_branch_code = cpib.code
	WHERE 
		p_type.code = 5958
		AND 
		c_price.calculation_code = 200
	GROUP BY
		payroll_year,
		industry_branch_code,
		cpib.name 
	ORDER BY
		payroll_year,
		industry_branch_code

/*
 * 3. Join of cz_avg_pay and cz_price_by_years and create table
 */
CREATE TABLE t_david_heczko_project_SQL_primary_final AS 
	SELECT
		cap.payroll_year,
		cap.avg_pay,
		cap.industry_branch_code AS industry_code,
		cap.name AS industry,
		cpby.*
	FROM cz_avg_pay cap
	LEFT JOIN cz_price_by_years cpby
		ON cap.payroll_year = cpby.calculated_year
	WHERE cpby.calculated_item IS NOT NULL
	GROUP BY 
		cpby.calculated_year,
		cap.industry_branch_code,
		cpby.calculated_item

SELECT *
FROM t_david_heczko_project_sql_primary_final dtable