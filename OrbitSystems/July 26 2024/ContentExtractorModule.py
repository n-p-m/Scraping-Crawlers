
import sys
from trafilatura import fetch_url, extract
import pandas as pd
import requests
from htmldate import find_date
import extraction
import time
import logging


class TextExtractor:
    @staticmethod
    def extract_main_text(page,url):
        try:
            # downloaded = fetch_url(url)
            # print("The downloaded stuff is->>>"+downloaded)
            if page is None:
                print(f"Failed to fetch content from {url}")
                return None
            main_text = extract(page, include_comments=False, include_tables=False, no_fallback=True)
            if main_text:
                return main_text.strip()
            else:
                print(f"No main text could be extracted from {url}")
                return None
        except Exception as e:
            print(f"An error occurred while processing {url}: {str(e)}")
            return None

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
            # First, launch the URL
            response = requests.get(url, headers=self.headers)
            self.logger.info(f"Processing Finished for URL: {url}")
            # Wait for 1 second
            self.logger.info("Waiting 1 second for the page to")
            time.sleep(1)
            
            # Now grab the HTML content
            self.logger.info("Extracting HTML after waiting")
            page = response.text
            # print("The response is->>>"+response.text+"END OF RESPONSE")

            
            # page = requests.get(url, headers=self.headers).text
            # print("Before extracting main text")

            self.logger.info("Extracting main text")
            extracted_text = TextExtractor.extract_main_text(page,url)
            self.logger.info("Extracting main text completed")
            # print("After extracting main text")
            # if extracted_text:
                # print("Inside if statement")
                
                # print()
            self.logger.info("Getting title")
            title=extraction.Extractor().extract(page, source_url=url).title
            self.logger.info("Finished Extracting title")    
                # print("Title completed")

                # print("DIA")
            self.logger.info("Getting Date Of Article")
            dia=find_date(page)
            self.logger.info("Extracted Date Of Article")
                # print("DIA completed")
            new_row = pd.DataFrame({
                    'Title': [title],
                    'Date In Article': [dia],
                    'Main Text': [extracted_text],
                    'URL': [url]
                })
            
            self.logger.info("Adding New Row To The Dataframe")
            self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
            self.URL_df.loc[index,'Status']="Success"
            self.logger.info("Added New Row To The DataFrame")

        except Exception as e:
            self.URL_df.loc[index,'Status']="Failed"
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
            # self.logger.error(f"An error occurred while processing {url}: {str(e)}")
            # self._handle_extraction_error(url, e)

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
