
import sys
from trafilatura import fetch_url, extract
import pandas as pd
import requests
from htmldate import find_date
import extraction
import time
import logging
import signal
from bs4 import BeautifulSoup


class TextExtractor:
    @staticmethod
    def extract_main_text(page,url):
        
        if page is None:
            print(f"Failed to fetch content from {url}")
            return None
        
        try:
            # downloaded = fetch_url(url)
            # print("The downloaded stuff is->>>"+downloaded)    
            main_text = extract(page, include_comments=False, include_tables=False, no_fallback=True)
            if main_text:
                return main_text.strip()
            else:
                logging.info(f"No main text could be extracted from {url}")
                return None
        except Exception as e:
            logging.info(f"An error occurred while processing {url}: {str(e)}")
            return None

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function call timed out")


class WebsiteDataExtractor:
    def __init__(self, URL_df):
        self.URL_df = URL_df
        # self.output_folder = output_folder
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        self.new_df = pd.DataFrame(columns=['Title', 'Main Text', 'Date In Article', 'URL'])
        self.logger = logging.getLogger(self.__class__.__name__)


    def process_df(self):
        # csv_file = pd.read_csv(self.csv_path)
        for index, row in self.URL_df.iterrows():
            # url = self._prepare_url(row['URL'])
            self.logger.info(f"processing index {index}-> {row['URL']}")
            url = row['URL']
            self._process_url(index, url)
        return (self.new_df, self.URL_df)

    def _process_url(self, index, url):
        try:
            self.logger.info(f"Processing URL: {url}")
            response = requests.get(url, headers=self.headers)
            self.logger.info(f"Processing Finished for URL: {url}")
            self.logger.info("Waiting 1 second for the page to load")
            time.sleep(1)
            
            self.logger.info("Extracting HTML after waiting")
            page = response.text

            # Set the signal handler and a 60-second alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            
            # Extract main text
            self.logger.info("Extracting main text")
            signal.alarm(60)
            try:
                extracted_text = TextExtractor.extract_main_text(page, url)
            except TimeoutException:
                self.logger.error("Main text extraction timed out after 60 seconds")
                extracted_text = "TIMED OUT"
            finally:
                signal.alarm(0)
            self.logger.info("Extracting main text completed")

            # Extract title
            self.logger.info("Getting title")
            signal.alarm(60)
            try:
                # title = extraction.Extractor().extract(page, source_url=url).title
                title = BeautifulSoup(page, 'html.parser').title.get_text()
            except TimeoutException:
                self.logger.error("Title extraction timed out after 60 seconds")
                title = "TIMED OUT"
            finally:
                signal.alarm(0)
            self.logger.info("Finished Extracting title")

            # Extract date
            self.logger.info("Getting Date Of Article")
            signal.alarm(60)
            try:
                dia = find_date(page)
            except TimeoutException:
                self.logger.error("Date extraction timed out after 60 seconds")
                dia = "TIMED OUT"
            finally:
                signal.alarm(0)
            self.logger.info("Extracted Date Of Article")

            new_row = pd.DataFrame({
                'Title': [title],
                'Date In Article': [dia],
                'Main Text': [extracted_text],
                'URL': [url]
            })
            
            self.logger.info("Adding New Row To The Dataframe")
            self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
            self.URL_df.loc[index, 'Status'] = "Success"
            self.logger.info("Added New Row To The DataFrame")

        except Exception as e:
            self.URL_df.loc[index, 'Status'] = "Failed"
            self.logger.error(f"An error occurred while processing {url}: {str(e)}")
            new_row = pd.DataFrame({
                'Title': ['FAILED'],
                'Date In Article': ['FAILED'],
                'Main Text': ['FAILED'],
                'URL': [url]
            })
            self.logger.info("Adding FAILED Row To The Dataframe")
            self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
            self.logger.info("Added FAILED Row To The DataFrame")

    # def _handle_extraction_error(self, url, error):
    #     new_row = pd.DataFrame({
    #         'Title': ['FAILED'],
    #         'Date In Article': ['FAILED'],
    #         'Main Text': ['FAILED'],
    #         'URL': [url]
    #     })
    #     self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
    #     print(f"An error occurred while processing {url}: {str(error)}")

    # def _save_results(self):
    #     self.new_dfB.to_csv(f"{self.output_folder}OutputFile.csv", index=False, encoding='utf-8-sig')
