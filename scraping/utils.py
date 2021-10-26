import requests
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

def search_opotunities(keywords):
    # Header definition
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7',
        'Referer': 'https://google.com',
        'DNT': '1'
    }
    # Main page
    main_str = "https://euraxess.ec.europa.eu/jobs/search"
    # Keywords (i.e. job field: data science, data analyst etc...)
    keywords = str(keywords)
    # Join keywords and main page: web to scrape
    search_str = "?keywords=" + keywords.replace(" ", "%20")
    subdomain_str = main_str + search_str
    # Subdomain request
    subdomain_rq = requests.get(subdomain_str, headers=headers)
    # If web is available, it will return 200 (i.e. Ok for scraping)
    if subdomain_rq.status_code == 200:
        print("Web is available for scraping")
    else:
        print("Something is wrong. Status code:", subdomain_rq.status_code)
    # Extract useful from subdomain (keyword) page
    soup_subdomain = BS(subdomain_rq.content, "html.parser")
    # Extract number of offers/pages for subdomain_page (keywords):
    offers_subdomain = soup_subdomain.find_all("h2", {"class": "text-center"})
    # Number of offers
    offers_count = re.findall(r'[0-9]+', str(offers_subdomain))[1]
    # Number of pages
    pager_subdomain = soup_subdomain.find_all("li", {"class": "pager-current"})
    if offers_count == '0':  # If = 0, a message indicating the issue is showed.
        print("There are no offers with these keywords. Please, type other keywords")
    else:
        if len(pager_subdomain) > 0:  # if pages > 0, the function iterates, scraping each page to obtain info.
            pages_count_subdomain = re.findall(r'[0-9]+', str(pager_subdomain))[1]  # Number of pages (iterate purpose)
            print('Number of offers using the keyword "{}":'.format(keywords), offers_count, "in {} pages".format(pages_count_subdomain))
            # for loop to obtain job offer titles
            raw_titles_sub = []
            for i in range(int(pages_count_subdomain)):
                subdomain_pages_str = subdomain_str + "&page={}".format(i)  # String of keyword webpage i
                subdomain_pages_rq = requests.get(subdomain_pages_str, headers=headers)  # Request of this page
                soup_subdomain_pages = BS(subdomain_pages_rq.content, "html.parser")  # page BeautifulSoup
                titles_subdomain = soup_subdomain_pages.find_all("div", {"class": "col-sm-12 col-md-6"})  # Obtain html line of titles
                for j in range(len(titles_subdomain)):
                    raw_titles_sub.append(titles_subdomain[j].get_text())  # Get offer titles
                titles_sub = []
                for title in raw_titles_sub:    # for loop to correct the titles (replace final \n)
                    replaced_n = title.replace("\n","")
                    titles_sub.append(replaced_n)
                empty_table = pd.DataFrame()
                empty_table["Job Offer Title"] = titles_sub
                empty_table.to_csv(r"{}.csv".format(keywords))