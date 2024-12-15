-- creation of view for all needed data from czechia_payroll

SELECT
	id AS payroll_id,
	value AS pay,
	cpu.name AS entity,
	cpvt.name AS type,
	cpc.name AS calculation,
	cpib.name AS branch,
	payroll_quarter,
	payroll_year		
FROM czechia_payroll cp
JOIN czechia_payroll_value_type cpvt
	ON cp.value_type_code = cpvt.code
JOIN czechia_payroll_unit cpu
	ON cp.unit_code = cpu.code
JOIN czechia_payroll_industry_branch cpib
	ON cp.industry_branch_code = cpib.code
JOIN czechia_payroll_calculation cpc
	ON cp.calculation_code = cpc.code

 
		


	







