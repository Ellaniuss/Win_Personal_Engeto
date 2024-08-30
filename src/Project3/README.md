# Engeto Project 3 - Election Scrapper

Usage Instructions for the Election Data Scraper

This script scrapes election data from a specified URL and saves it to a CSV file.
URL that are suited for this program are specifically:
  - On URL https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ 
  - Choose link from X assigned to Výběr obce.

Script should be run via command-line using two arguments:
  1. URL of requrired territorial unit (str) 
  2. Name of output CSV file (str)

Sript will scrappe tables with data from the link and save it to the csv file.

## Example Usage:
1. Ensure you have the required packages installed that are listed in requirements.txt
2. Ensure that both election_scrapper.py and url_collector.py are in same folder.
3. Run the script from command line:
   example:
   py election_scrapper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "Vysledky_Praha.csv"
4. Sript will:
   a. validate both arguments
   b. fetch and parse data from provided URL
   c. collect and process all URLs connected to the input URL
   d. extract relevant election data
   e. create dataframe using Pandas library using extracted data
   f. export dataframe to specified csv file.

## Error Handling:
- The script will terminate and provide an error message if:
  - The number of arguments is incorrect.
  - The provided URL is not valid.
  - The output filename does not end with ".csv".
  - There is a problem fetching data from the URL or writing to the CSV file.

