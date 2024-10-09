import sys

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv

def validate_url(url,errors):
    '''
    Function validates validity of URL for scrapping.
    Expected URL: https://volby.cz - Výsledky hlasování za územní celky, rok 2017
    Function returns list of errors.
    '''
    try:
        if type(url) != str:
            errors.append(f"Incorrect input. Expecting string, input is {type(url)}.")
            return False
        elif not url.startswith("https://volby.cz/pls/ps2017nss/ps3"):
            errors.append(f"URL not in valid. Expected URL for: 'Výsledky hlasování pro územní celky / Výběr Obce (2017)'")
            return False
        response = requests.get(url)

        if response.status_code != 200:
            errors.append(f"URL not valid, status code: {response.status_code}")
            return False

        soup = bs(response.content, "html.parser")
        if soup.find("td") is None:
            errors.append(f"URL not valid: Data not found.")
            return False

        return True
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
def validate_output(output_filename, errors):
    '''
    Simple function validating second argument.
    Second argument is needed to be string ending with .csv.
    '''
    if not output_filename.endswith(".csv"):
        errors.append(f"Second argument should be name of the csv file, input was {output_filename}. Terminating program.")
    return False
def collect_links(soup):
    base_url = "https://volby.cz/pls/ps2017nss/"
    links = list()

    relative_urls = soup.find_all('a',href=True)
    for url in relative_urls:
      if url['href'].startswith('ps311'):
          full_url = base_url + url['href']
          if full_url not in links:
              links.append(full_url)

    return links
def create_soup(url):
    try:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
def scrape_page(soup, attrs):
    try:
        pre_scraps = soup.find_all('td', attrs=attrs)
        scraps = [i.text.replace('\xa0', '').strip() for i in pre_scraps]
        return scraps
    except AttributeError as e:
        raise SystemExit(f'Error: {e}. Program will be terminated.')

def main():
    errors = []

    if len(sys.argv) < 2:
        raise SystemExit(f"Error: Please provide the URL as a command-line argument. Program will be terminated.")
    main_url = sys.argv[1]
    output_filename = sys.argv[2]

    if not validate_url(main_url,errors) and validate_output(output_filename,errors):
        print(' '.join(str(e) for e in errors))
        print(f"Terminating program.")
        sys.exit(1)

    soup1 = create_soup(main_url)
    links = collect_links(soup1)

    attrs = [
            {'class': 'cislo'},  # 0 codes
            {'class': 'overflow_name'},  # 1 cities
            {'class': 'cislo', 'headers': 'sa2'},  # 2 voters
            {'class': 'cislo', 'headers': 'sa3'},  # 3 envelopes
            {'class': 'cislo', 'headers': 'sa6'},  # 4 valid
            {'class': 'overflow_name'},  # 5 parties
            {'headers': 't1sa2 t1sb3'},  # 6 party votes table 1
            {'headers': 't2sa2 t2sb3'}   # 7 party votes table 2
        ]

    results = []

    codes = scrape_page(soup1, attrs[0])
    cities = scrape_page(soup1, attrs[1])

    for link in links:
        try:
            soup2 = create_soup(link)
            parties = scrape_page(soup2, attrs[5])

            data = {
                'Code': None,
                'Location': None,
                'Registered': None,
                'Envelopes': None,
                'Valid': None,
            }

            party_votes = scrape_page(soup2, attrs[6]) + scrape_page(soup2, attrs[7])

            data['Code'] = codes[len(results)]
            data['Location'] = cities[len(results)]
            data['Registered'] = int(scrape_page(soup2, attrs[2])[0])
            data['Envelopes'] = int(scrape_page(soup2, attrs[3])[0])
            data['Valid'] = int(scrape_page(soup2, attrs[4])[0])

            for i, party in enumerate(parties):
                data[party] = int(party_votes[i])

            results.append(data)
        except requests.RequestException as e:
            print(f"Error: Failed to getting data from link {link}. {e}")
            continue

    df = pd.DataFrame(results)
    try:
        df.to_csv(output_filename, encoding='utf-8-sig', index=False)
        print(f"Data succefully saved to {output_filename}")
    except IOError as e:
        print(f"Error: Failed to write data to {output_filename}. {e}")



if __name__ == '__main__':
    main()