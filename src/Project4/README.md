# Průvodní listina SQL projektu Engeto

## Úvod
Úkolem projektu bylo zodpovědět 5 analytických otázek za použití dat ze dvou tabulek, které jsme měli vytvořit z dostupných dat.
Výstupem jsou tedy SQL scripty, které:
    a) vytvářejí dvě tabulky s relevantními daty
    b) odpovídají na všech 5 otázek

### Analytické otázky
    1. Rostou v průběhu let mzdy ve všech odvětvích, nebo v některých klesají ?
    2. Kolik je možné si koupit litrů mléka a kilogramů chleba za první a poslední srovnatelné období v dostupných datech cen a mezd ?
    3. Která kategorie potravin zdražuje nejpomaleji (je u ní nejmenší procentuální roční nárust)?
    4. Existuje rok, ve kterém byl meziroční nárust cen potravin výrazně vyšší než růst cen (větší než 10%)?
    5. Má výška HDP vliv na změny ve mzdách a cenách potravin ? Neboli, pokud HDP vzroste výrazněji v jednom  roce, projeví se to na cenách potravin či mzdách ve stejném nebo následujícím roce výraznějším růstem ?


### Seznam výstupvých scriptů
    1. Primary_table.sql -- script který vytváří tabulku s relevantními daty ohledně mezd a cen potravin ve společných letech.
    2. Secondary_table.sql -- script který vytváří doplňkovou tabulku s daty ohledně HDP, GINI a populace v evropských státech.


## Průběh

### Tvorba t_david_heczko_SQL_primary_final
Nejprve jsem zobrazil pohled pro mzdy na základě czechia-payroll použitím SELECT *.
K tomu jsem navázal použitím JOIN data ohledně názvů odvětví, typu počítání, typu hodnoty.
Poté jsem vytvořil pohled pro ceny potravin. K tomu jsem navázal použitím join data ohledně názvu potravin, měny a jednotek.
Jelikož chyběl pohledu u cen potravin kalkulovaný rok, za použití klauzule year() jsem přepočtal data z date_from na roky a vytrořil tak sloupec vhodný pro spojení s pohledem pro mzdy .
Tyto dvě zobrazení jsem se poté pokusil spojit vnořením SELECTu pro ceny do SELECTu pro mzdy a vytvořit použizím CREATE TABLE výslednou tabulku.
Zjistil jsem, že toto řešení není vhodné, jelikož má tabulka přiloš mnoho dat a její vytvoření by zabralo obrovské množství času.
Na základě tohoto problému, jsem předělal původní script následovně:
  1.Puvodní SELECTy jsem předělal za použití GROUP BY a WHERE, kde jsem se zaměřil jen na relevantí data
  2.Použil jsem klauzuli avg() u hodnot pro mzdy abych dostal průměrné mzdy za rok
  3.použil jsem avg() u hodnot pro ceny potravin, abych dostal průmerné ceny za rok
  4.z každého SELECu jsem vytvořil VIEW
  5.Obě VIEW jsem následné spojil skrze LEFT JOIN, kde jsem jednotlivá data spojoval za použití GROUP BY na počítaných letech, průměrných mzdách, názvu odvětví, názvu položek potravin, množství potravin, průměrnou cenu potravin.

 
