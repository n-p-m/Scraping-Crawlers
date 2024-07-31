from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pandas as pd
from ContentExtractorModule import WebsiteDataExtractor
from CleaningModule import *
import json
from logging_config import logger

def run(playwright, query):
    logger.info("Inside Run Function")
    browser = playwright.chromium.launch(headless=False)  # Set headless to False
    logger.info("Browser Launched")
    context = browser.new_context()
    logger.info("New Context Created")

    # Open new page
    page = context.new_page()
    logger.info("New Page Created")

    # Go to Google
    page.goto("https://www.google.com")
    logger.info("Navigated to Google")

    # Check if the search box exists
    search_box = page.get_by_role("combobox", name="Search")
    logger.info("Trying to get search box")

    # search_box = page.query_selector('input[type="text"], textarea')
    # search_box = page.query_selector('textarea.gLFyf')
    
    #Below not working.
    # search_box = page.get_by_placeholder("Search")
    # search_box = page.locator('input[type="text"], textarea')
    # search_box = page.get_by_label("Search")

    # Perform search
    # person_name = "Sam Altman"
    # company_name = "OpenAI"

    if search_box:
        # Fill the search box
        logger.info("Search box found")
        # search_box.fill(f"{person_name} {company_name}")
        search_box.fill(query)  
        page.press('textarea.gLFyf', "Enter")
    else:
        logger.error("Search box not found")
        # print("Search box not found")

    # Wait for search results to load
    page.wait_for_load_state("networkidle", timeout=60000)
    logger.info("Search results loaded")

    # Check if the News tab exists
    news_tab = page.query_selector('text=News')
    logger.info("Trying to get News tab")

    if news_tab:
        # Click on the News tab
        logger.info("News tab found")
        news_tab.click()
    else:
        logger.error("News tab not found")
        # print("News tab not found")

    # Wait for news results to load
    page.wait_for_load_state("networkidle", timeout=60000)
    logger.info("News results loaded")
    # Extract all 'a' tags
    all_a_tags = page.eval_on_selector_all("a", "elements => elements.map(a => a.href)")
    logger.info("Extracted all 'a' tags")
    final_list=[]

    for url in all_a_tags:
        logger.info(f"Checking if URL is not google domain: {url}")
        if is_not_google_domain(url, 'google.com'):
            logger.info(f"URL is not google domain: {url}") 
            final_list.append(url)
    logger.info("Final List of URLs Created")
    # df=pd.DataFrame(final_list, columns=['URL'])
    
    # df.to_csv('GoogleNews.csv', index=False)
    # Close browser
    browser.close()
    logger.info("Browser Closed and returning final_list")
    return final_list

def is_not_google_domain(url,domain):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain != 'google.com' and not domain.endswith('.google.com')

if __name__ == "__main__":
    start_time=time.time()
    final_df  = pd.DataFrame(columns=['URL','Title', 'Main Text', 'Date In Article'])

    forbes_df=pd.read_csv('ForbesList2.csv')

    POI_articles_JSON = {
        }

    logger.info("Iterating Over the Forbes List")
    for index, row in forbes_df[:3].iterrows():
        #only execute below lines of code if there is a first name
        # if pd.isna(row['First Name']):
        #     continue
        logger.info(f"Processing index {index}")
        fn = '' if pd.isna(row['First Name']) else str(row['First Name'])
        ln = '' if pd.isna(row['Last Name']) else str(row['Last Name'])
        org = '' if pd.isna(row['Employment Organization']) else str(row['Employment Organization'])
        logger.info(f"First Name: {fn}, Last Name: {ln}, Organization: {org}")
        # print(type(row['Last Name']))
        # print(type(row['Employment Organization']))
        query = fn + ' ' + ln + ' ' + org
        # print("query is-> "+ query)
        # print("entering scrapping section")
        
        logger.info("EnteringGoogle Extraction")
        with sync_playwright() as playwright:
            logger.info("Starting Google Extraction")
            google_articles = run(playwright,query)
            logger.info("Google Extraction Completed")

        
        
        hcd_cleaner = GenericCleaner("", "")
        hcd_cleaner.logger.info("Starting Cleaning")
        URL_array_df = hcd_cleaner.clean(google_articles)
        hcd_cleaner.logger.info("Cleaning Completed")

       
        logger.info("Creating JSON Object for articles")
        individual_poi_json = {
            'id': index,
            'Name': fn + '|' + ln,
            'Organization': org,
            'articles' : []

        }

        logger.info("JSON Article Object Created")

        # print("!!!!!!!!!!! Starting STEP 3 !!!!!!!!!!!!!!!!!!")

        extractor = WebsiteDataExtractor(URL_array_df)
        extractor.logger.info("Starting Extracting Main Content of Article")
        new_df, status_df = extractor.process_df()
        extractor.logger.info("Completed Extracting Main Content of Article")
        
        ######### Adding articles to the parent JSON #############
        for _, row in new_df.iterrows():
            article = {
                'title': row['Title'],
                'article': row['Main Text'],
                'date': row['Date In Article'],
                'URL': row['URL']
            }
            logger.info(f"Adding articles to the JSON")
            individual_poi_json['articles'].append(article)
            
        # logger.info(f"Added articles to the JSON")
        key_for_json = str(index)
        # print("key_for_json is-> "+ key_for_json)
        logger.info(f"Adding JSON article Object to POI_articles_JSON")
        POI_articles_JSON[key_for_json] = individual_poi_json

    json_string = json.dumps(POI_articles_JSON, indent=2)
        
    # print(json_string)
    with open('temp_POI.json', 'w') as json_file:
        json_file.write(json_string)
    logger.info("Writing the JSON object to JSON file")
        # json_string = json.dumps(articles_json, indent=2)
        # print(json_string)
        # logger.info("Writing the JSON object to JSON file")
        # # file_path=
        # os.makedirs(folder, exist_ok=True)
        # file_path = os.path.join(folder, f'{domainName}_articles.json')


        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(json_string)

        # logger.info("JSON object written to JSON file")
        
    end_time=time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Execution time: {elapsed_time:.2f} seconds")
        # Print the result
        # print(f"Execution time: {elapsed_time:.2f} seconds")

    logger.info("Process completed successfully")
