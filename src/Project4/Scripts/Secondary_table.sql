/*
 * 1. Created select for relevant data.
 */
SELECT
	e.`year`,
	e.country,
	e.population,
	round(e.GDP) AS GDP,
	e.gini
FROM economies e
LEFT JOIN countries c
	ON e.country = c.country
WHERE
	c.continent = 'Europe'
	AND
	e.`year` BETWEEN 2006 AND 2018
ORDER BY 
	e.country,
	e.`year`

/*
 * 2. Created table from the selection
 */
CREATE TABLE t_david_heczko_project_SQL_secondary_final AS 
	SELECT
		e.`year`,
		e.country,
		e.population,
		round(e.GDP) AS GDP,
		e.gini
	FROM economies e
	LEFT JOIN countries c
		ON e.country = c.country
	WHERE
		c.continent = 'Europe'
		AND
		e.`year` BETWEEN 2006 AND 2018
	ORDER BY 
		e.country,
		e.`year`