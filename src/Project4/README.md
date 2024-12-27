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
    3. project4_SQL_question_1.sql 
    4. project4_SQL_question_2.sql 	
    5. project4_SQL_question_3.sql 
    6. project4_SQL_question_4.sql
    7. project4_SQL_question_5.sql
 
## Průběh

### 1. Tvorba t_david_heczko_SQL_primary_final
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

### 2. Tvorba t_david_heczko_SQL_secondary_final
Nejprve jsem vytvořil pohled spojující metodou LEFT JOIN tabulky economies a countries, a zobrazující data ohledně roku,
zemí, populace, GDP a GINI hodnot. Pomocí klauzule WHERE jsem vyfiltroval pouze země Evropy a období mezi lety 2006 a 2018.
Následně jsem klauzulí CREATE TABLE vytvořil z tohoto pohledu tabulku t_david_heczko_project_SQL_secondary_final.sql.

### 3. Tvorba pohledů
Pohledy jsem vytvářel do separátních scriptů, pro každou otázku zvlášť. Při psaní druhého scriptu jsem zjistil,
že tablukla Primary obsahuje hodnoty value pro období po 8 měsících namísto celého roku.
Problém jsem opravil funkcí avg na value a klauzulí GROUP BY.

1.	**Script project4_SQL_question_1** - 
Vytvořil jsem VIEW skrze kombinaci SELECT a CASE, kde jsem použil klauzuli ‘lag() OVER‘  a partition by branch_code a zadal podmínku, kde pokud je předchozí hodnota menší, označí se řádek jako ´yes´ v novém sloupci is_lower.
Na základě vytvořeného VIEW, jsem pracoval se dvěma klauzulemi SELECT.  V prvním SELECTu vidíme odvětví a roky, ve kterých klesala průměrná mzda. Ve druhém SELECTu vidíme jen informace, jestli průměrná mzda klesala či nikoliv.

2.	**Script project4_SQL_question_2** - 
Použil jsem klauzuli SELECT a funkce avg() na avg_pay, pro zobrazení průměrných platů skrze všechna odvětví. Dále jsem podělil průměrný plat na daný rok s průměrnou cenou potraviny abychom získali množství potraviny, kterou lze koupit za průměrný plat.
Na základě klauzule CASE jsem doplnil jednotky do sloupce unit_per_pay na základě vyhledání str ve sloupci provision_unit.
Dále jsem do klauzule WHERE zadal takové podmínky, aby se zobrazily jenom hodnoty v letech 2006 a 2018, a jen hodnoty které obsahují slova mléko a chléb.

3.	**Script project4_SQL_question_3** - 
V prvním kroku jsem vytvořil za použití funkce SELECT pohled, který zobrazoval jen roky, kategorii potravin, počítanou jednotku a průměrnou cenu za jednotlivé roky.
Bylo potřeba použít GROUP BY na kategorii potravin aby se zobrazovaly data bez duplicit, které vznikly díky spojení tabulek price a payroll.
V druhém kroku jsem ze selekce vytvořil pohled a použil funkci lag() OVER, která má za úkol vytvořit sloupec pervious_price vedle počítaných let. Tedy postupuje po jednotlivých letech a připisuje hodnotu předchozího roku. Pro zobrazení prvních hodnot v nezměněné a “nenullové“ hodnotě bylo zapotřebí použít klauzuli ifnull().
Ve třetím kroku jsem vytvořil pohled počítající precentuální hodnotu rozdílu ceny a předchozí ceny na daném roku.
Čtvrtý pohled zobrazuje data ohledně průměrného nárůstu či poklesu cen napříč počítanými lety pro každou potravinu zvlášť.


## Odpovědi na výzkumné otázky
### 1. Rostou v průběhu let mzdy ve všech odvětvích, nebo v některých klesají?
Podle dostupných dat je viditelé, že mzy né vždy rostly.
Ve specifických odvětvích (viz. detail níže) nastal pokles průměrných mezd oproti předchozímu roku v letech 2009, 2010, 2011, 2013, 2014, 2015 a 2016.
Z dat je také zřejmé, že v roce 2013 došlo k hromadnému poklesu průměrných mezd v mnoha odvětvích.
Detail pro jednotlivé zasažené obory:

 a) **2009:**
 - Zemědělství, lesnictví, rybářství
 - Těžba a dobývání
 - Ubytování, stravování a pohostinství
 - Činnosti v oblasti nemovitostí
   
 b) **2010:**
- Profesní, vědecké a technické činnosti
- Veřejná správa a obrana; povinné sociální zabezpečení
- Vzdělávání
  
 c) **2011:**
- Výroba a rozvod elektřiny, plynu, tepla a klimatiz. vzduchu
- Doprava a skladování
- Ubytování, stravování a pohostinství
- Veřejná správa a obrana; povinné sociální zabezpečení
  
 d) **2013:**
- Těžba a dobývání
- Výroba a rozvod elektřiny, plynu, tepla a klimatiz. vzduchu
- Zásobování vodou; činnosti související s odpady a sanacemi
- Stavebnictví
- Velkoobchod a maloobchod; opravy a údržba motorových vozidel
- Informační a komunikační činnosti
- Peněžnictví a pojišťovnictví
- Činnosti v oblasti nemovitostí
- Profesní, vědecké a technické činnosti
- Administrativní a podpůrné činnosti
- Kulturní, zábavní a rekreační činnosti
  
 e) **2014:**
- Těžba a dobývání
  
 f) **2015:**
- Výroba a rozvod elektřiny, plynu, tepla a klimatiz. vzduchu
  
 g) **2016:**
- Těžba a dobývání

### 2. Kolik je možné si koupit litrů mléka a kilogramů chleba za první a poslední srovnatelné období v dostupných datech cen a mezd?
  Z dostupných dat vyplývá, že v roce 2006 bylo možné, za průmernou mzdu napříč odvětvími, koupit:
      a) 919 kilogramů chleba
      b) 1026 litrů mléka
  Zato v roce 2018 bylo možné, za průmernou mzdu napříč odvětvími, koupit:
      a) 1051 kilogramů chleba, což je o 132 kilogramů více než v roce 2006
      b) 1285 litrů mléka, což je o 256 litrů více než v roce 2006



