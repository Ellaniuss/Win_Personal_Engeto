import sys

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_input():
    """
    Retrieves command-line arguments for the URL and output filename.

    This function expects two command-line arguments:
    - A URL from https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.
    - An output filename (with a .csv extension).

    If either argument is missing, the function prints an error message and exits the program.

    Returns:
        main_url variable (str)
        output_filename variable (str)
    """
    if len(sys.argv) < 3:
        print(f"Expected are two arguments: <URL from volby.cz> <output_filename.csv. \n Program will be terminated!")
        sys.exit(1)
    
    main_url = sys.argv[1]
    output_filename = sys.argv[2]
    
    return main_url, output_filename


def validate_input(url, output_filename):
    """
    Validate given input for both arguments.

    This function checks if the provided arguments are valid.
    It checks URL validity for election scrapping of Czech 2017 communal elections,
    where it validates the response status code and checks if the page contains
    the expected table data (`<td>` tags).
    It checks if the provided output filename ends with the '.csv' suffix.
    Errors are appended to the `errors` list if any validation checks fail.

    Args:
        url (str):
            The URL to be validated.
        output_filename (str):
            String containing name of the csv file to which will be stored data.
    Returns:
        valid (boolean):
            Variable containing boolean.
        errors(list):
            List containing errors
    """
    errors = []
    valid = True
    try:
        if not url.startswith("https://www.volby.cz/pls/ps2017nss/ps3"):
            errors.append(f"Input error. Expected URL for: 'Výsledky hlasování pro územní celky / Výběr Obce (2017)'")
            valid = False

        response = requests.get(url)

        if response.status_code != 200:
            errors.append(f"URL not valid, status code: {response.status_code}")
            valid = False

        soup = bs(response.content, "html.parser")

        if soup.find("td") is None:
            errors.append(f"URL not valid: Data not found.")
            valid = False

    except requests.RequestException as e:
        errors.append(f"Request failed: {e}")
        valid = False

    if not output_filename.endswith(".csv"):
        errors.append(f"Second argument should be name of the csv file, input was {output_filename}.")
        valid = False

    return valid, errors


def check_for_messages(valid, errors):
    """
    Checks for input validity and prints errors if any.

    This function takes the validation status of input and list of errors, printing each error
    if validation has failed. If errors are present, it terminates the program.

    Args:
        valid (bool): The validation status; should be False if any errors occurred.
        errors (list): A list of error messages generated during validation.

    Raises:
        SystemExit: Exits the program if validation fails.
    """

    if not valid:
        print('Errors appeared when running code: ')
        for error in errors:
            print('\t', error)
        print('\nTerminating program!')
        sys.exit(1)


def collect_links(soup):
    """
    Collect links from a BeautifulSoup object.

    This function searches for tags (`<a>`) in the provided BeautifulSoup object
    and collects the full URLs where the `href` attribute starts with 'ps311'.
    The base URL 'https://volby.cz/pls/ps2017nss/' is appended to these relative URLs
    to form complete links. Only unique links are included in the resulting list.

    Args:
        soup (BeautifulSoup):
            A BeautifulSoup object.

    Returns:
        list:
            A list of all urls scrapped from main url.
    """

    base_url = "https://volby.cz/pls/ps2017nss/"
    links = list()

    relative_urls = soup.find_all('a', href=True)

    for url in relative_urls:
        if url['href'].startswith('ps311'):
            full_url = base_url + url['href']

        if full_url not in links:
            links.append(full_url)

    return links


def create_soup(url):
    """
    Fetch the content of the URL and parse it into BeautifulSoup object.

    This function sends a GET request to the specified URL and parses the HTML
    content into a BeautifulSoup object. If a request exception occurs, it raises
    a SystemExit with the exception message, terminating the program.

     Args:
        url (str): The URL to fetch and parse.

    Returns:
        BeautifulSoup:
            A BeautifulSoup object containing the parsed HTML content.

    Raises:
        SystemExit:
            If a request exception occurs while fetching the URL.
    """
    try:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def scrape_page(soup, attrs):
    """
    Scrape text data from a BeautifulSoup objects based on given HTML attribute.

    Function searches through given soup object and looks of all elements with given
    HTML attribute. It extracts and cleans the text content and returns valid data.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object
        attrs (dict): A dictionary of HTML attributes

    Returns:
        list: A list of cleaned text extracted from the matching elements.

    Raises:
        SystemExit: If an AttributeError occurs during scraping, the program is terminated
                   with an error message.
    """
    try:
        pre_scraps = soup.find_all('td', attrs=attrs)
        scraps = [i.text.replace('\xa0', '').strip() for i in pre_scraps]
        return scraps
    except AttributeError as e:
        raise SystemExit(f'Error: {e}. Program will be terminated.')


def create_data_structures():
    """
    Creates two structures for storing scrapped data.

    This function creates dictionary of HTML attributes that are used to identify specific data elements
    for scrapping from HTML page.
    Then it creates a dictionary for each data category scrapped from HTML page.

    Returns:
        attrs (list): A list named attrs of dictionaries.
        data (dict): A dictionary for each
    """
    attrs = [
        {'class': 'cislo'},  # 0 codes
        {'class': 'overflow_name'},  # 1 cities
        {'class': 'cislo', 'headers': 'sa2'},  # 2 voters
        {'class': 'cislo', 'headers': 'sa3'},  # 3 envelopes
        {'class': 'cislo', 'headers': 'sa6'},  # 4 valid
        {'class': 'overflow_name'},  # 5 parties
        {'headers': 't1sa2 t1sb3'},  # 6 party votes table 1
        {'headers': 't2sa2 t2sb3'}  # 7 party votes table 2
    ]

    data = {
        'Code': None,
        'Location': None,
        'Registered': None,
        'Envelopes': None,
        'Valid': None,
    }

    return attrs, data


def collect_data(links, attrs, codes, cities):
    """
    Scrapes and collects data for each city in chosen territorial unit.

    Function created blank list named results and receives list of links that are collected from main_url.
    For each link it creates BeautifulSoup object and data structure containing main categories.
    Then it scrapes data for each requested category listed in attrs and stores them on corresponding keys in dictionary
    data. Finally, it appends each dictionary to the list results.

    Args:
        links (list): A list of URLs to be scraped.
        attrs (list): A list of attribute dictionaries used to locate specific data in HTML (e.g., codes, voters).
        codes (list): A list of unique codes corresponding to each location.
        cities (list): A list of city names or locations matching each code.

    Returns:
        results (list): A list of dictionaries, each containing the scraped data.

    Raises:
        requests.RequestException: If a request fails for a URL, an error message is printed,
                                   and the function continues to the next link.
    """

    print('Beginning fetching sequence.')
    results = []

    for link in links:
        try:
            soup2 = create_soup(link)
            _, data = create_data_structures()

            parties = scrape_page(soup2, attrs[5])
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
    print('Data collected.')
    return results


def create_csv(results, output_filename):
    """
    Creates a CSV file from a collected data in results and saves it to the specified output filename.

    This function converts the created data structure stored in results into a Pandas DataFrame.
    It then creates CSV file with UTF-8 encoding and writes the DataFrame to it.

    Args:
        results (list): A list created by function collect_data().
        output_filename (str): The name of the output CSV file.

    Raises:
        IOError: If there is an error writing the DataFrame to the CSV file, an error message is printed.
    """
    df = pd.DataFrame(results)
    print('Dataframe created.')
    try:
        df.to_csv(output_filename, encoding='utf-8-sig', index=False)
        print(f"Data successfully saved to {output_filename}")
    except IOError as e:
        print(f"Error: Failed to write data to {output_filename}. {e}")


def main():
    """
    Main function of the script, initiating and running scrapping process.

    This function coordinates the execution of the script by performing following steps:
        1. Retrieves command-line arguments for the URL and output filename using `get_input()`.
        2. Validates the input URL and output filename using `validate_input()`.
        3. Creates a BeautifulSoup object from the main URL to scrape initial data.
        4. Collects links to detailed pages for each city using `collect_links()`.
        5. Scrapes data for codes and city names from the initial page.
        6. Collects data for each city using `collect_data()`,
        7. Creates a CSV file from the collected data using `create_csv()`.

    """

    main_url, output_filename = get_input()
    valid, errors = validate_input(main_url, output_filename)
    check_for_messages(valid, errors)

    soup1 = create_soup(main_url)
    links = collect_links(soup1)

    attrs, _ = create_data_structures()

    codes = scrape_page(soup1, attrs[0])
    cities = scrape_page(soup1, attrs[1])

    results = collect_data(links, attrs, codes, cities)

    create_csv(results, output_filename)


if __name__ == '__main__':
    main()
