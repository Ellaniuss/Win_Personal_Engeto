/*
 * 1. Creating view with 'yes' in is_lower column when pervious avg_pay was bigger
 */
CREATE VIEW IF NOT EXISTS increase_pay_check AS 
	SELECT
		calculated_year,
		avg_pay,
		branch_code,
		branch_name,
		CASE
			WHEN avg_pay < lag(avg_pay) OVER (PARTITION BY branch_code ORDER BY calculated_year)
			THEN 'yes'
			ELSE 'no'
		END AS is_lower
	FROM t_david_heczko_project_sql_primary_final t_primary
	GROUP BY
		calculated_year,
		avg_pay,
		branch_code,
		branch_name
	ORDER BY
		branch_code,
		calculated_year;



/*
 * 2. selecting only industries wich had decrease of avg_pay during specific years
 */

-- following shows all branches and calculated years in which there was decrease of average pay against pervious year.
SELECT
	branch_code,
	branch_name,
	calculated_year
FROM increase_pay_check ipc
WHERE is_lower = 'yes'
GROUP BY
	branch_code,
	branch_name,
	calculated_year,
	is_lower
ORDER BY
	branch_code,
	calculated_year

-- following shows only branches that had decreaase of average_pay during all time
SELECT
	branch_name,
	is_lower
FROM increase_pay_check ipc
WHERE is_lower = 'yes'
GROUP BY
	branch_name,
	is_lower


