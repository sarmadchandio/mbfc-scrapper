from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from tqdm import tqdm
import json


def load_webdriver():
    # headless driver
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    return driver

# scrapes through the category pages and extracts all the links present there
# TODO
def get_sources_from_category_page(driver):
    categories = ['left', 'leftcenter', 'center', 'right-center', 'right', 'conspiracy', 'fake-news', 'pro-science', 'satire']
    all_links = set()
    for cat in categories:
        driver.get(f'https://mediabiasfactcheck.com/{cat}/')

        # for all the links in the table below extract the hrefs and their text
        xpath = '//*[@id="post-48"]/div' if cat=='satire' else '//*[@id="mbfc-table"]'
        links_table = driver.find_element(By.XPATH, xpath)
        links = set(links_table.find_elements(By.TAG_NAME, 'a'))
        for link in links:
            all_links.add(link.get_attribute('href'))
        print(f'{cat}_a_tags: {len(links)}')
        print(f'cummlative_hrefs: {len(all_links)}')

    print(len(all_links))

# scrapes through the filtered search and extracts all the links present there
def get_sources_from_filter_page(driver):
    sources = []
    
    driver.get('https://mediabiasfactcheck.com/filtered-search/')
    total_pages = driver.find_element(By.XPATH, '//*[@id="post-32822"]/div/span/a[6]').get_attribute('href').split('pg=')[-1]
    print(f"Total pages: {total_pages}")
    

    for page in tqdm(range(1, int(total_pages))):
        driver.get('https://mediabiasfactcheck.com/filtered-search/?pg='+str(page))
        table_body = driver.find_element(By.XPATH, '//*[@id="mbfc-table"]/tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')
        # print all the row data
        for row in rows:
            entries = row.find_elements(By.TAG_NAME, 'td')
            entry_dict = {
                "bias": entries[1].text,
                "credibility": entries[4].text,
                "domain": "",
                "name": entries[0].text,
                "questionable": [],
                "reporting": entries[2].text,
                "url": entries[0].find_element(By.TAG_NAME, 'a').get_attribute('href'),
                "media-type": entries[5].text
            }
            sources.append(entry_dict)
    # dump sources to a json file in a pretty format
    with open('filter-sources.json', 'w') as f:
        json.dump(sources, f, indent=4)

# TODO
def get_data_for_missing_sources(driver):
    with open('missing-sources.json', 'r') as f:
        missing_sources = json.load(f)
    for url in tqdm(missing_sources):
        try:
            driver.get(url)
            drive

        except Exception as e:
            # error in loading the page
            print(f"Error in page: {url} : {e}")

        break



def main():
    # there are more or less 5600 news sources on mbfc. Tried searching through the filtered search and category wise.
    driver = load_webdriver()
    print("driver loaded")
    # get_sources_from_category_page(driver)
    # get_sources_from_filter_page(driver)
    get_data_for_missing_sources(driver)


    driver.quit()

if __name__ == '__main__':
    main()