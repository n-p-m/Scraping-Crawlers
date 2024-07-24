
import sys
from trafilatura import fetch_url, extract
import pandas as pd
import requests
from htmldate import find_date
import extraction
import time
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
   
   
   
    # def extract_main_text(url):
    #     try:
    #         downloaded = fetch_url(url)
    #         print("The downloaded stuff is->>>"+downloaded)
    #         if downloaded is None:
    #             print(f"Failed to fetch content from {url}")
    #             return None
    #         main_text = extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)
    #         if main_text:
    #             return main_text.strip()
    #         else:
    #             print(f"No main text could be extracted from {url}")
    #             return None
    #     except Exception as e:
    #         print(f"An error occurred while processing {url}: {str(e)}")
    #         return None

class WebsiteDataExtractor:
    def __init__(self, URL_df):
        self.URL_df = URL_df
        # self.output_folder = output_folder
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        self.new_df = pd.DataFrame(columns=['Title', 'Main Text', 'Date In Article', 'URL'])

    def process_df(self):
        # csv_file = pd.read_csv(self.csv_path)
        for index, row in self.URL_df.iterrows():
            # url = self._prepare_url(row['URL'])
            print(f"processing index {index}-> {row['URL']}")
            url = row['URL']
            self._process_url(url)
        return self.new_df
        # self._save_results()

    # def _prepare_url(self, url):
    #     if url.startswith('//'):
    #         return "https:" + url
    #     return url

    def _process_url(self, url):
        print()
        try:
            # First, launch the URL
            response = requests.get(url, headers=self.headers)
            
            # Wait for 1 second
            time.sleep(1)
            
            # Now grab the HTML content
            page = response.text
            # print("The response is->>>"+response.text+"END OF RESPONSE")

            
            # page = requests.get(url, headers=self.headers).text
            # print("Before extracting main text")
            extracted_text = TextExtractor.extract_main_text(page,url)
            # print("After extracting main text")
            if extracted_text:
                # print("Inside if statement")
                
                # print("Getting title")
                title=extraction.Extractor().extract(page, source_url=url).title
                # print("Title completed")

                # print("DIA")
                dia=find_date(page)
                # print("DIA completed")
                new_row = pd.DataFrame({
                    'Title': [title],
                    'Date In Article': [dia],
                    'Main Text': [extracted_text],
                    'URL': [url]
                })

                self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
        except Exception as e:
            new_row = pd.DataFrame({
            'Title': ['FAILED'],
            'Date In Article': ['FAILED'],
            'Main Text': ['FAILED'],
            'URL': [url]
        })
            self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
            print(f"An error occurred while processing {url}: {str(e)}")
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
