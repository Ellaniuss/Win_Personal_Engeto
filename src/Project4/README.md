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
    5. Má výška HDP vliv na změny ve mzdách a cenách potravin ? 
       Neboli, pokud HDP vzroste výrazněji v jednom  roce, projeví se to na cenách potravin či mzdách ve stejném nebo následujícím roce výraznějším růstem ?


### Seznam výstupvých scriptů
**Scripty jsou ve složce Scripts v repositáři**
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

4.	**Script project4_SQL_question_4** -
V prvním kroku jsem vytvořil pohled pay_comparation, kde ve sloupci pervious_avg_pay je možné vidět hodnotu průměrné mzdy předchozího období pro dané odvětví.
Ve druhém kroku jsem vytvořil pohled pay_percentage_trend, který zobrazuje procentuální rozdíl mezd oproti předchozímu období.
Ve třetím kroku jsem vytvořil pohled overall_price_pay_trend, který spojuje průměrné hodnoty z pohledu pay_percentage_trend (v tomto scriptu),
průmerné hodnoty z pohledu price_precentage_trend (pohled vytvořen ve scriptu project4_SQL_question_3). Data jsou seskupena skrze roky, ve kterých byly hodnoty počítány.
Vytvořením 4. pohledu price_pay_growth_comparation jsem dosáhl zobrazení tabulky, která obsahuje porovnání výsledných hodnot.

5.	**Script project4_SQL_question_5** -
Nejprve jsem vytvořil pohled cz_hdp z tabulky t_david_heczko_project_sql_secondary_final, ve kterém jsem zobrazil data o HDP v Česku v letech 2006 až 2018. Následně jsem musel vytvořit další dva pohledy k průměrným platům (avg_pay_percentage_trend)  a cenám potravin (avg_price_percentage_trend), jelikož v předchozích vytvořených pohledech byly data rozděleny do jednotlivých kategorií, a chyběly výsledky na celkové průměrné hodnoty za daný rok.
Nakonec jsem vytvořil pohled hdp_price_pay_yoy spojením všech pohledů na scriptu,  kde je možno vidět veškerá data ohledně HDP růstu, růstu platů a cen potravin.
Script na konci obsahuje klauzuli SELECT, ve které jsem hledal odpověď na 5. otázku.



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

### 3. Která kategorie potravin zdražuje nejpomaleji (je u ní nejnižší percentuální meziroční nárůst)?
V datech v pohledu price_precentage_trend_final je zřejmé, že nejpomalejší zdražování probíhalo u Žlutých banánů, kde průměrné meziroční zdražení bylo 0,75%.
Další zajímavou informací, která je z tabulky jasně viditelná je, že né všechny potraviny průměrně zdražovaly. Krystalový cukr a rajská jablka měly zlevňující tendenci, a to u ckuru o 1,77% a u rajských jablek o 0,68%.

### 4. Existuje rok, ve kterém byl meziroční nárůst cen potravin výrazně vyšší než růst mezd (větší než 10 %)?
Po srovnání meziročního průměrného nárůstu (year on year, yoy) mezd všech odvětví, a průměrného yoy nárůstu cen všech potravin vyplývá,
že všeobecně potraviny nezdrahly v daném roce o více než 10%.
Největší rozdíl mezi růstem průmerné mzdy a průměrné ceny potravin nastal v roce 2013, kdy ceny potravin vzrostly o 6,79% oproti růstu průměrné mzdy.

### 5.	Má výška HDP vliv na změny ve mzdách a cenách potravin? Neboli, pokud HDP vzroste výrazněji v jednom roce, projeví se to na cenách potravin či mzdách ve stejném nebo násdujícím roce výraznějším růstem?
Z dostupných dat reflektujících změny HDP, průměrných platů a průměrné ceny potravin, nelze jasně vyvodit závěr, že růst HDP má vliv na růst platů a cen potravin.
Toto tvrzení vyplývá z následujících poznatků:
-	V roce 2007 vzrostlo HDP o 5.57 % oproti předchozímu roku.
    Ve stejném roce vzrostly platy o 6.91 % a potraviny zdražily o 9.25 %.
 	Všechny kategorie tedy rostly. V následujícím roce platy a ceny potravin dále prudce rostly, a to u platů o 7.08 % a u cen potravin o 8.91 %.

-	V roce 2009 HDP kleslo o 4.66 %. Platy avšak vzrostly o 2.84 %, kdežto potraviny zlevnily o 6.58%.
    Zde vidíme, že i když HDP klesalo a potraviny zlevňovaly, hodnota průměrných platů rostla.
 	V následujícím roce platy dále rostly o 2.15 % ale potraviny zdražily o 1.52 %.

-	V roce 2015 HDP opět vzrostlo o 5.39%. Platy nicméně vzrostly jen o 2.9 % a potraviny zlevnily o 0.67 %.
    Zde zase naopak vidíme, že oproti roku 2007, kdy HDP také rostlo o více než 5 %, platy ani ceny potravin nerostly o podobná procenta jako v roce 2007, ba dokonce ceny potravin šly opačnou tendencí.
 	V následujícím roce platy nadále rostly, a to o 3.94 %, kdežto ceny potravin znova klesaly o -1.40 %.

-	V roce 2017 došlo opět o nárůst HDP o více než 5 % a platy a ceny potravin vzrostly také o více než 5 %, konkrétně platy o 6.40 % a ceny potravin o 7.06 %.
    V následujícím roce platy prudce rostly a to až o 7.88 % kdežto potraviny vzrostly jen 2.41 %.

Z výpisu vyplývá, že nelze sledovat opakující se trend ani u platů ani u cen potravin. 
Data jsou různorodá a souvislosti nejsou přímě úměrné.


