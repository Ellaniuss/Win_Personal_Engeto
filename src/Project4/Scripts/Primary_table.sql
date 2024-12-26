/*
 * 1. creation of view and selection for czechia_price with relevant colums, calculated year and average value of prices
 */
CREATE VIEW IF NOT EXISTS cz_price_by_years AS 
	SELECT
		year(date_from) AS price_year,
		cpc.name AS provision_name,
		concat(cpc.price_value,' ', cpc.price_unit) AS provision_unit,
		round(avg(value),2) AS avg_price
	FROM czechia_price c_price
	LEFT JOIN czechia_price_category cpc
		ON c_price.category_code = cpc.code
	WHERE
		region_code IS NULL
	GROUP BY 
		year(date_from),
		cpc.name,
		concat(cpc.price_value,' ', cpc.price_unit)
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
		

/*
 * 3. Join of cz_avg_pay and cz_price_by_years and create table
 */
		
CREATE OR REPLACE TABLE t_david_heczko_project_SQL_primary_final AS 
	SELECT
		cap.payroll_year AS calculated_year,
		round(cap.avg_pay,2) AS avg_pay,
		cap.industry_branch_code AS branch_code,
		cap.name AS branch_name,
		cpby.provision_name AS parovision_name,
		cpby.provision_unit AS provision_unit,
		cpby.avg_price AS avg_price
	FROM cz_avg_pay cap
	JOIN cz_price_by_years cpby
		ON cap.payroll_year = cpby.price_year
	GROUP BY
		cap.payroll_year,
		cap.avg_pay,
		cap.industry_branch_code,
		cpby.provision_name,
		cpby.provision_unit,
		cpby.avg_price
	ORDER BY
		cap.payroll_year,
		cap.industry_branch_code,
		cpby.provision_name 
	
		
SELECT *
FROM t_david_heczko_project_sql_primary_final dtable
