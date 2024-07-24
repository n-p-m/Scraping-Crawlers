

from bs4 import BeautifulSoup
import requests
import csv 
import os
import pandas as pd
from abc import ABC, abstractmethod

# Below portion is for NYTimes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import random
import traceback
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup, Tag
import time


#End of NYtimes requirements
# Importing files

from CleaningModule import *
from ContentExtractorModule import WebsiteDataExtractor



class ArticleExtractor(ABC):
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        
        # self.session = requests.Session()
#         self.headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1'
# }
#         self.session.headers.update={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1'
# }
    def extract_article_urls(self):
        response = self.get_response()
        time.sleep(1)
        # print("Response received, and response is->"+str(response.status_code))
        if response.status_code == 200:
            # print("Inside 200")
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = self.parse_articles(soup)
            # self.write_to_csv(self.URL_array)
            print(f"URLS have been added to the list")
            return articles

    def get_response(self):
        return requests.get(self.url, headers=self.headers)
        # return self.session.get(self.url)

    @abstractmethod
    def parse_articles(self, soup):
        pass

    # def write_to_csv(self, articles):
    #     os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
    #     file_exists = os.path.isfile(self.csv_path)

    #     with open(self.csv_path, 'a', newline='', encoding='utf-8') as file:
    #         fieldnames = ["Title", "URL"]
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
            
    #         if not file_exists:
    #             writer.writeheader()

    #         for article in articles:
    #             writer.writerow(article)


class GenericArticleExtractor(ArticleExtractor):
    def parse_articles(self, soup):
        articles = []
        anchor_tags = soup.find_all('a')
        for tag in anchor_tags:
            if tag.get('href'):
                articles.append(tag.get('href'))
        return articles


class FoxNewsArticleExtractor(ArticleExtractor):
    def parse_articles(self, soup):
        articles = []
        anchor_tags = soup.find_all('a')
        for tag in anchor_tags:
            if tag.get('href'):
                articles.append({"Title": tag.text, "URL": tag.get('href')})
        return articles

class CNNArticleExtractor(ArticleExtractor):
    def parse_articles(self, soup):
        articles = []
        # Find all article containers
        article_containers = soup.find_all('div', class_='container__item')
        
        for container in article_containers:
            # Find the anchor tag for the URL
            anchor = container.find('a')
            if anchor and anchor.get('href'):
                url = anchor.get('href')
                # If the URL is relative, make it absolute
                if url.startswith('/'):
                    url = f"https://www.cnn.com{url}"
                
                # Find the title within the span tag
                title_span = container.find('span', class_='container__headline-text')
                title = title_span.text.strip() if title_span else "No title found"
                
                articles.append({"Title": title, "URL": url})
        
        return articles
    

class NYTimesArticleExtractor(ArticleExtractor):
    def __init__(self, url, csv_path,duration):
        self.duration=duration
        self.url = url
        self.csv_path = csv_path
        self.driver = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        ]
        print(f"Initialized NYTimesArticleExtractor with URL: {url}")

    def setup_driver(self):
        # --------------------Below Code with Head-----------------
        print("Setting up Chrome driver...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome driver set up successfully.")
            return True
        except WebDriverException as e:
            print(f"Failed to start Chrome: {e}")
            return False 
       

    def human_like_delay(self, min_seconds=2, max_seconds=7):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def human_like_scroll(self, duration):
        print(f"Starting continuous downward scroll for {duration} sec...")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            current_position = self.driver.execute_script("return window.pageYOffset;")
            scroll_amount = random.randint(100, 800)
            self.driver.execute_script(f"window.scrollTo(0, {current_position + scroll_amount});")
            time.sleep(random.uniform(0.5, 2))
        
        print("Finished scrolling.")

    def extract_article_urls(self):
        print("Starting article URL extraction...")
        if not self.setup_driver():
            print("Unable to set up Chrome driver.")
            return

        try:
            print(f"Navigating to URL: {self.url}")
            self.human_like_delay(5, 10)
            self.driver.get(self.url)
            
            print("Waiting for page to load...")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.human_like_delay()
            
            print("Performing pre-parse action...")
            self.pre_parse_action()
            
            self.human_like_delay()

            print("Getting page source...")
            page_source = self.driver.page_source
            print(f"Page source length: {len(page_source)}")
            
            print("Capturing screenshot...")
            self.driver.save_screenshot("nytimes_screenshot.png")
            
            with open('nytimes_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            
            # soup = BeautifulSoup(page_source, 'html.parser')
            print("Parsing articles...")
            articles = self.parse_articles(page_source)
            # print(f"Found {len(articles)} articles.")
            self.write_to_csv(articles)
            print(f"Data has been written to {self.csv_path}")
        except Exception as e:
            print(f"An error occurred during extraction: {e}")
            traceback.print_exc()
        finally:
            if self.driver:
                print("Quitting Chrome driver...")
                self.driver.quit()

    def pre_parse_action(self):
        try:
            print("Waiting for search tab...")
            wait = WebDriverWait(self.driver, 15)
            search_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[role="tab"][href="#stream-panel"][data-id="search"]')))
            print("Moving to search tab...")
            
            actions = ActionChains(self.driver)
            actions.move_to_element(search_tab).perform()
            self.human_like_delay(1, 3)
            
            print("Clicking search tab...")
            search_tab.click()
            self.human_like_delay()

            print("Starting continuous downward scroll...")
            self.human_like_scroll(self.duration)  # Scroll for 1 minute
        except Exception as e:
            print(f"Error during pre-parse action: {e}")
            traceback.print_exc()
        
    def parse_articles(self, html_content):
        # print("Inside TestParse")
        articles=[]
        soup = BeautifulSoup(html_content, 'html.parser')
        # all_a_tags = soup.find_all('a')
        target_a_tags = soup.find_all('a', class_='css-8hzhxf')

        # print(f"Total <a> tags found: {len(all_a_tags)}")
        print(f"!!!!!!!!<a> tags with class 'css-8hzhxf' found: {len(target_a_tags)}")
        

        # containers = soup.find_all('a', class_='css-8hzhxf')

        for container in target_a_tags:
            # print("Inside for loop for test_parse")
            url = container.get('href')
            if url and url.startswith('/'):
                url = f"https://www.nytimes.com{url}"
            
            title = container.text.strip()
            
            if url and title:
                articles.append({"Title": title, "URL": url})
                # print(f"Added article: {title[:30]}... - {url}")
        # print("Printing articles")
        # print(articles)
        # print(f"!!!!!!!!With length of articles->{len(articles)}")
        # print('end of test_parse_articles')
        return articles
        

# nytimes_extractor = NYTimesArticleExtractor("https://www.nytimes.com/section/business", './csvs/NYTimes/InitialHrefNYTimesBusinessArticles.csv',300)
# # nytimes_extractor.extract_article_urls()
# folder = './csvs/FoxNews/'

# start_time = time.time()

# genericExtraction= GenericArticleExtractor("https://www.foxbusiness.com/", './csvs/FoxNews/InitialFoxBusinessArticles.csv')
# genericExtraction.extract_article_urls()


# fox_cleaner = FoxNewsCleaner(folder,"https://www.foxbusiness.com")
# fox_cleaner.clean("InitialFoxBusinessArticles")


# csv_path = folder + 'InitialFoxBusinessArticles_Extraction_of_Info.csv'
# start=time.time()
# extractor = WebsiteDataExtractor(csv_path, folder)
# extractor.process_csv()

# end_time=time.time()

# elapsed_time = end_time - start_time

# # Print the result
# print(f"Execution time: {elapsed_time:.2f} seconds")