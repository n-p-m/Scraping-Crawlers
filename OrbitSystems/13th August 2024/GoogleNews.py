from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import pandas as pd
from ContentExtractorModule import WebsiteDataExtractor
from CleaningModule import *
import json
from logging_config import logger


def URL_JSON_Creation(url, status):
    return {"URL": url, "Status": status}

# class CustomEncoder(json.JSONEncoder):
#     def encode(self, obj):
#         if isinstance(obj, dict):
#             return "{\n\n" + ",\n   ".join(f'{{     "URL": "{k}",     "Status": "{v}"   }}' for k, v in obj.items()) + "\n\n}"
#         return super().encode(obj)

# def format_json(data):
#     items = [f'{{ "URL": "{url}", "Status": "{status}" }}' for url, status in data.items()]
#     formatted_items = ',\n'.join(items)
#     return f'{{\n{formatted_items}\n}}'


# import time

# def run(playwright, query):
#     try:
#         logger.info("Inside Run Function")
#         browser = playwright.chromium.launch(headless=False)
#         logger.info("Browser Launched")
#         context = browser.new_context()
#         logger.info("New Context Created")

#         # Open new page
#         page = context.new_page()
#         logger.info("New Page Created")

#         # Go to Google
#         page.goto("https://www.google.com")
#         logger.info("Navigated to Google")

#         # Check if the search box exists
#         search_box = page.get_by_role("combobox", name="Search")
#         logger.info("Trying to get search box")

#         if search_box:
#             # Fill the search box
#             logger.info("Search box found")
#             search_box.fill(query)  
#             page.press('textarea.gLFyf', "Enter")
#         else:
#             logger.error("Search box not found")

#         # Wait for search results to load
#         page.wait_for_load_state("networkidle", timeout=60000)
#         logger.info("Search results loaded")

#          # Wait for 5 seconds to allow popup to appear
#         logger.info("Waiting for 2 seconds for potential popup")
#         time.sleep(2)

#         # Check for and handle the location popup
#         if page.is_visible("text='See results closer to you?'"):
#             logger.info("Location popup detected")
#             page.click("text='Not now'")
#             logger.info("Clicked 'Not now' on location popup")
#         else:
#             logger.info("No location popup detected")


#         # Check if the News tab exists
#         news_tab = page.query_selector('text=News')
#         logger.info("Trying to get News tab")

#         if news_tab:
#             # Click on the News tab
#             logger.info("News tab found")
#             news_tab.click()
#             # Wait for news results to load
#             page.wait_for_load_state("networkidle", timeout=60000)
#             logger.info("News results loaded")
#         else:
#             logger.error("News tab not found")

#         # Extract all 'a' tags
#         all_a_tags = page.eval_on_selector_all("a", "elements => elements.map(a => a.href)")
#         logger.info("Extracted all 'a' tags")
#         final_list = []

#         for url in all_a_tags:
#             logger.info(f"Checking if URL is not google domain: {url}")
#             if is_not_google_domain(url, 'google.com'):
#                 logger.info(f"URL is not google domain: {url}") 
#                 final_list.append(url)
#         logger.info("Final List of URLs Created")

#         # Close browser
#         browser.close()
#         logger.info("Browser Closed and returning final_list")
#         return final_list
#     except Exception as e:
#         logger.error(f"Error in run function: {e}")
#         return []

import time

def run(playwright, query):
    try:
        logger.info("Inside Run Function")
        browser = playwright.chromium.launch(headless=False)
        logger.info("Browser Launched")
        context = browser.new_context()
        logger.info("New Context Created")

        page = context.new_page()
        logger.info("New Page Created")

        page.goto("https://www.google.com")
        logger.info("Navigated to Google")

        # Wait for 5 seconds to allow popup to appear
        logger.info("Waiting for 5 seconds for potential popup")
        time.sleep(5)

        # Check for and handle the location popup
        if page.is_visible("text='See Results closer to you?'"):
            logger.info("Location popup detected")
            page.click("text='Not now'")
            logger.info("Clicked 'Not now' on location popup")
        else:
            logger.info("No location popup detected")

        # Check if the search box exists
        search_box = page.get_by_role("combobox", name="Search")
        logger.info("Trying to get search box")

        if search_box:
            logger.info("Search box found")
            search_box.fill(query)  
            page.press('textarea.gLFyf', "Enter")
        else:
            logger.error("Search box not found")

        # Wait for search results to load
        page.wait_for_load_state("networkidle", timeout=60000)
        logger.info("Search results loaded")

        # Check for the presence of the News tab in the HTML
        news_tab_exists = page.query_selector('a:has-text("News")')
        
        if news_tab_exists:
            logger.info("News tab found in HTML")
            
            # Check if the News tab is directly visible
            if page.is_visible('a:has-text("News")'):
                logger.info("News tab is directly visible")
                page.click('a:has-text("News")')
            else:
                logger.info("News tab is not directly visible, checking More section")
                more_button = page.query_selector('text = More')
                if more_button:
                    more_button.click()
                    logger.info("Clicked More button")
                    # Wait for the News option to be visible in the expanded menu
                    page.wait_for_selector('a:has-text("News")', state="visible", timeout=5000)
                    page.click('a:has-text("News")')
                    logger.info("Clicked News in More section")
                else:
                    logger.error("More button not found")
        else:
            logger.error("News tab not found in HTML")

        # Wait for news results to load
        page.wait_for_load_state("networkidle", timeout=60000)
        logger.info("News results loaded")

        # Extract all 'a' tags
        all_a_tags = page.eval_on_selector_all("a", "elements => elements.map(a => a.href)")
        logger.info("Extracted all 'a' tags")
        final_list = []

        for url in all_a_tags:
            logger.info(f"Checking if URL is not google domain: {url}")
            if is_not_google_domain(url, 'google.com'):
                logger.info(f"URL is not google domain: {url}") 
                final_list.append(url)
        logger.info("Final List of URLs Created")

        # Close browser
        browser.close()
        logger.info("Browser Closed and returning final_list")
        return final_list
    except Exception as e:
        logger.error(f"Error in run function: {e}")
        return []
    
def is_not_google_domain(url,domain):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain != 'google.com' and not domain.endswith('.google.com')

if __name__ == "__main__":
    start_time=time.time()

    URL_status = []

    final_df  = pd.DataFrame(columns=['URL','Title', 'Main Text', 'Date In Article'])

    forbes_df=pd.read_csv('ForbesList2.csv')

    POI_articles_JSON = {}

    logger.info("Iterating Over the Forbes List")
    for index, row in forbes_df[15:17].iterrows():
        #only execute below lines of code if there is a first name
        # if pd.isna(row['First Name']):
        #     continue
        logger.info(f"Processing index {index}")
        fn = '' if pd.isna(row['First name']) else str(row['First name'])
        ln = '' if pd.isna(row['Last name']) else str(row['Last name'])
        org = '' if pd.isna(row['Organization']) else str(row['Organization'])
        logger.info(f"First name: {fn}, Last name: {ln}, Organization: {org}")
        # print(type(row['Last name']))
        # print(type(row['Organization']))
        query = fn + ' ' + ln + ' ' + org
        # print("query is-> "+ query)
        # print("entering scrapping section")
        
        logger.info("EnteringGoogle Extraction")
        with sync_playwright() as playwright:
            logger.info("Starting Google Extraction")
            google_articles = run(playwright,query)
            logger.info("Google Extraction Completed")

        
        if not google_articles:
            logger.error("No articles found")
            continue
        
        hcd_cleaner = GenericCleaner("", "")
        hcd_cleaner.logger.info("Starting Cleaning")
        URL_array_df = hcd_cleaner.clean(google_articles)
        hcd_cleaner.logger.info("Cleaning Completed")

       
        logger.info("Creating JSON Object for articles")
        individual_poi_json = {
            'id': index+1,
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
        
        # Saving the json for URL status

        for _, row in status_df.iterrows():
            # Create a JSON record for each row
            record = URL_JSON_Creation(row['URL'], row['Status'])
            
            # Add the record to our list
            URL_status.append(record)

        json_data = json.dumps(URL_status, indent=2)

        with open('url_status.json', 'w') as f:
            f.write(json_data)
    
        logger.info("JSON file 'url_status.json' has been created with all records.")


        # data = status_df.set_index('URL')['Status'].to_dict()
    
        # # Format the data
        # formatted_json = format_json(data)
    
        # # Write the formatted data to a JSON file
        # with open('url_status.json', 'w') as f:
        #     f.write(formatted_json)
        
        # print("JSON file 'url_status.json' has been created with all records.")


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
        key_for_json = str(index+1)
        # print("key_for_json is-> "+ key_for_json)
        # logger.info(f"Adding JSON article Object to POI_articles_JSON")
        POI_articles_JSON[key_for_json] = individual_poi_json

    json_string = json.dumps(POI_articles_JSON, indent=2)
        
    # print(json_string)
    with open('Forbes_POI.json', 'w') as json_file:
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
