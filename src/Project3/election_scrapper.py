"""
election_scrapper.py: třetí projekt do Engeto Online Python Akademie
author: David Heczko
email: heczko.david@gmail.com
discord: David H ellaniuss
"""

import sys

import pandas
from bs4 import BeautifulSoup as bs
import requests

from url_collector import collect_urls

def validate_url(url):
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

def validate_output(output_filename):
    '''
    Simple function validating second argument.
    Second argument is needed to be string ending with .csv.
    '''
    return output_filename.endswith(".csv")

errors = []

def main():
    '''
    Main function for scrapping election results from provided URL and saving it to the csv file.
    Function performs following steps:
        1. Checks command-line arguments to ensure that there are exactly two given.
        2. Validates both arguments using functions validate_url and validate_output.
        3. Fetches HTML content from provided URL by using 'request' library as Main URL for the code.
        4. Creates list of links from Main URL by using imported function collect_urls.
        5. Gets data from each link stored in the list of links and saves them to the lists for each cathegory.
        6. Creates Data dictionary from each cathegory and coresponding data.
        7. Creates dataframe using Pandas and Data dictionary.
        8. Creates csv file from dataframe, named by second argument.

    '''
    if len(sys.argv) < 3:
        print(f"Expected are two arguments: <URL from volby.cz> <output_filename.csv. \n Program will be terminated!")
        sys.exit(1)

    url = sys.argv[1]
    output_filename = sys.argv[2]


    if not validate_url(url):
        print(' '.join(str(e) for e in errors))
        print(f"Terminating program.")
        sys.exit(1)
    elif not validate_output(output_filename):
        print(f"Error: Second argument should be name of the csv file, input was {output_filename}. Terminating program.")
        sys.exit(1)

    try:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error: Failed to getting data from prvided URL. {e}")


    links = collect_urls(url)


    locations = []
    registered_final = []
    envelopes_final = []
    valid_votes_final = []
    parties_final = []
    party_votes_final = []

    codes = [city.text for city in soup.find_all("td", class_="cislo")]
    cities = [city.text for city in soup.find_all("td", class_="overflow_name")]

    for link in links:
        try:
            local_url = requests.get(link)
            local_soup = bs(local_url.content, 'html.parser')

            registered = int(local_soup.find("td", headers="sa2").text.replace("\xa0",""))
            registered_final.append(registered)

            envelopes = int(local_soup.find("td", headers="sa5").text.replace("\xa0",""))
            envelopes_final.append(envelopes)

            valid_votes = int(local_soup.find("td", headers="sa6").text.replace("\xa0",""))
            valid_votes_final.append(valid_votes)

            parties_t1 = [party.text for party in local_soup.find_all("td", headers="t1sa1 t1sb2")]
            parties_t2 = [party.text for party in local_soup.find_all("td", headers="t2sa1 t2sb2")]

            parties_final.append(parties_t1 +  parties_t2)

            party_votes_t1 = [int(vote.text.replace('\xa0','').replace('-', '0')) for vote in local_soup.find_all("td", headers="t1sa2 t1sb3")]
            party_votes_t2 = [int(vote.text.replace('\xa0','').replace('-', '0')) for vote in local_soup.find_all("td", headers="t2sa2 t2sb3")]
            party_votes_final.append(party_votes_t1 + party_votes_t2)

        except requests.RequestException as e:
            print(f"Error: Failed to getting data from link {link}. {e}")
            continue


    data = {
        "Codes" : codes,
        "Location" : cities,
        "Registered" : registered_final,
        "Envelopes" : envelopes_final,
        "Valid" : valid_votes_final
    }

    for index, party in enumerate(parties_final[0]):
        party_votes_data = [votes[index] for votes in party_votes_final]
        data[party] = party_votes_data

    df = pandas.DataFrame(data)
    try:
        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"Data succefully saved to {output_filename}")
    except IOError as e:
        print(f"Error: Failed to write data to {output_filename}. {e}")

if __name__ == '__main__':
    main()
