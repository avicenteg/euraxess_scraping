from bs4 import BeautifulSoup as BS
import csv
import pandas as pd
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm 
from webdriver_manager.chrome import ChromeDriverManager

def search_oportunities(keywords):
    # Header definition
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7',
        'Referer': 'https://google.com',
        'DNT': '1'
    }
    # Main page
    main_str = "https://euraxess.ec.europa.eu"
    # Keywords (i.e. job field: data science, data analyst etc...)
    keywords = str(keywords)
    # Join keywords and main page: web to scrape
    search_str = "?keywords=" + keywords.replace(" ", "%20")
    subdomain_str = main_str + "/jobs/search" + search_str
    # Subdomain request
    subdomain_rq = requests.get(subdomain_str, headers=headers)
    subdomain_rq.close()
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
            # for loop to obtain job offer titles & URLs
            raw_titles_sub = []
            raw_href_sub = []
            countries = []
            cities = []
            profiles = []
            companies = []
            hours = []
            apply_url =[]
            for i in tqdm(range(int(pages_count_subdomain))):
                subdomain_pages_str = subdomain_str + "&page={}".format(i)  # String of keyword webpage i
                subdomain_pages_rq = requests.get(subdomain_pages_str, headers=headers, timeout=120)  # Request of this page
                subdomain_pages_rq.close()
                soup_subdomain_pages = BS(subdomain_pages_rq.content, "html.parser")  # page BeautifulSoup
                titles_subdomain = soup_subdomain_pages.find_all("div", {"class": "col-sm-12 col-md-6"})  # Obtain html line of titles
                for title in titles_subdomain:
                    suffix_href = "".join(re.findall(r'/jobs/\d+',str(title)))
                    href = main_str + suffix_href
                    raw_href_sub.append(href)   # Get offer URLs
                    raw_titles_sub.append(title.get_text().replace("\n",""))  # Get offer titles
            for url in tqdm(raw_href_sub):
                job_rq = requests.get(url, headers=headers, timeout=120)
                job_rq.close()
                job_soup = BS(job_rq.content, "html.parser")
                job_country = job_soup.find_all("div", {"class": "value field-country"})
                job_city = job_soup.find_all("div", {"class": "value field-city"})
                job_company = job_soup.find_all("div", {"class": "col-xs-12 col-sm-7 value field-company-institute inline"})
                hours_week = job_soup.find_all("div", {"class": "col-xs-12 col-sm-7 value field-hours-per-week inline"})
                researcher_profile = job_soup.find_all("div", {"class": "col-xs-12 col-sm-7 value field-research-profile inline"})
                if len(job_country) > 0:
                    countries.append(job_country[0].get_text().strip())
                else:
                    countries.append("")
                if len(job_city) > 0:
                    cities.append(job_city[0].get_text().strip())
                else:
                    cities.append("")
                if len(job_company) > 0:
                    companies.append(job_company[0].get_text().strip())
                else:
                    companies.append("")
                if len(hours_week) > 0:
                    hours.append(hours_week[0].get_text().strip())
                else:
                    hours.append("")
                if len(researcher_profile) > 0:
                    profiles.append(" ".join(researcher_profile[0].get_text().strip().replace("\n\n",",").split()))
                else:
                    profiles.append("")
                apply_url.append(_get_contacts(url)) 
                

    empty_table = pd.DataFrame()
    empty_table["Job Offer Title"] = raw_titles_sub
    empty_table["Researcher Profile"] = profiles
    empty_table["Company"] = companies
    empty_table["Hours/Week"] = hours
    empty_table["Country"] = countries
    empty_table["City"] = cities
    empty_table["Where to Apply"] = apply_url
    empty_table["More Info"] = raw_href_sub

    empty_table.to_csv(r"{}.csv".format(keywords),quoting=csv.QUOTE_NONNUMERIC, sep=";" ,index=False)

def _get_contacts(url):
    # headless browser
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    # install chromedriver and open new browser
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # open url in browser
    driver.get(url)
    # find 'WHERE TO APPLY' buttom 
    apply_element = driver.find_element(By.ID,'apply_id')
    # click the buttom
    apply_element.click()
    # get new window
    application_web = driver.find_element(By.ID,'applyModal') 
    # get application url   
    url_element = application_web.find_element(By.TAG_NAME,'a')
    application_url = url_element.get_attribute('href')
    driver.quit()
    return application_url
