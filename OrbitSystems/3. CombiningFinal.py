# # import sys
# # from trafilatura import fetch_url, extract
# # import pandas as pd
# # # import csv
# # import requests
# # from htmldate import find_date
# # # import math
# # import extraction
# # def extract_main_text(url):
# #     try:
# #         # Fetch the HTML content
# #         downloaded = fetch_url(url)
        
# #         if downloaded is None:
# #             print(f"Failed to fetch content from {url}")
# #             return None
        
# #         # Extract the main text, excluding comments and tables
# #         main_text = extract(downloaded, 
# #                             include_comments=False, 
# #                             include_tables=False,
# #                             no_fallback=True)  # Using fast mode
        
# #         if main_text:
# #             return main_text.strip()
# #         else:
# #             print(f"No main text could be extracted from {url}")
# #             return None
    
# #     except Exception as e:
# #         print(f"An error occurred while processing {url}: {str(e)}")
# #         return None

# # if __name__ == "__main__":

# #     # Read the CSV file
# #     # csv_file = pd.read_csv('NER Engine Data Prep(Jason).csv')
# #     csv_file = pd.read_csv('articles_cleaned_WithMoreThan3Words.csv')   

# #     new_df = pd.DataFrame(columns=['Link', 'Extracted_Text', 'Date In Article', 'Title'])
    
# #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
      
# #     # Create a new column 'Extracted_Text' initialized with empty strings
# #     # csv_file['Extracted_Text'] = ''
# #     # csv_file['Date In Article'] = ''
# #     # csv_file['Title'] = ''

# #     # Iterate through the URLs
# #     for index, row in csv_file.iterrows():
# #         url = row['URL']
# #         # print("URL->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(url))
# #         # print(type(url), url)

# #         # if url!=float('nan') or str(url)!='nan':
# #         # if not math.isnan(url):
# #         try:
# #             page = requests.get(url, headers=headers).text 

# #             extracted_text = extract_main_text(url) # Extract the main text
                
# #             if extracted_text:
# #                 # print(f"Extracted main text for {url}:")
# #                 # print(extracted_text)
# #                 # Add the extracted text to the 'Extracted_Text' column
# #                 # csv_file.at[index, 'Extracted_Text'] = extracted_text
# #                 # csv_file.at[index,'Date In Article'] = find_date(page)
# #                 # csv_file.at[index,'Title'] = extraction.Extractor().extract(page, source_url=url).title
# #                 new_df = new_df.append({ 'Title': extraction.Extractor().extract(page, source_url=url).title,'Date In Article': find_date(page),'Extracted_Text': extracted_text, 'URL': url},  ignore_index=True)
        
# #         except Exception as e:
# #                 new_df = new_df.append({ 'Title': extraction.Extractor().extract(page, source_url=url).title,'Date In Article': find_date(page),'Extracted_Text': extracted_text, 'URL': url},  ignore_index=True)

# #             print(f"An error occurred while processing {url}: {str(e)}")
# #             continue
# #     else:
# #         print(f"Failed to extract main text for {url}")

# #     # Save the updated DataFrame back to a CSV file
# #     new_df.to_csv('TestingScript.csv', index=False, encoding='utf-8-sig')


# import sys
# from trafilatura import fetch_url, extract
# import pandas as pd
# import requests
# from htmldate import find_date
# import extraction

# def extract_main_text(url):
#     try:
#         downloaded = fetch_url(url)
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

# if __name__ == "__main__":
#     csv_file = pd.read_csv('articles_cleaned_WithMoreThan3Words.csv')
#     new_df = pd.DataFrame(columns=['Title','Main Text', 'Date In Article', 'URL'])
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

#     for index, row in csv_file.iterrows():
#         url = row['URL']
#         if not url.startswith(('http://', 'https://','//')):
#             print(f"Skipping invalid URL: {url}/n")
#             continue
#         try:
#             page = requests.get(url, headers=headers).text
#             extracted_text = extract_main_text(url)
#             if extracted_text:
#                 new_row = pd.DataFrame({
#                     'Title': [extraction.Extractor().extract(page, source_url=url).title],
#                     'Date In Article': [find_date(page)],
#                     'Extracted_Text': [extracted_text],
#                     'URL': [url]
#                 })
#                 new_df = pd.concat([new_df, new_row], ignore_index=True)
#         except Exception as e:
#             new_row = pd.DataFrame({
#                 'Title': ['FAILED'],
#                 'Date In Article': ['FAILED'],
#                 'Extracted_Text': ['FAILED'],
#                 'URL': [url]
#             })
#             new_df = pd.concat([new_df, new_row], ignore_index=True)
#             print(f"An error occurred while processing {index} with {url}: {str(e)}")

#     new_df.to_csv('TestingScript.csv', index=False, encoding='utf-8-sig')

# import sys
# from trafilatura import fetch_url, extract
# import pandas as pd
# # import csv
# import requests
# from htmldate import find_date
# # import math
# import extraction
# def extract_main_text(url):
#     try:
#         # Fetch the HTML content
#         downloaded = fetch_url(url)
        
#         if downloaded is None:
#             print(f"Failed to fetch content from {url}")
#             return None
        
#         # Extract the main text, excluding comments and tables
#         main_text = extract(downloaded, 
#                             include_comments=False, 
#                             include_tables=False,
#                             no_fallback=True)  # Using fast mode
        
#         if main_text:
#             return main_text.strip()
#         else:
#             print(f"No main text could be extracted from {url}")
#             return None
    
#     except Exception as e:
#         print(f"An error occurred while processing {url}: {str(e)}")
#         return None

# if __name__ == "__main__":

#     # Read the CSV file
#     # csv_file = pd.read_csv('NER Engine Data Prep(Jason).csv')
#     csv_file = pd.read_csv('articles_cleaned_WithMoreThan3Words.csv')   

#     new_df = pd.DataFrame(columns=['Link', 'Extracted_Text', 'Date In Article', 'Title'])
    
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
      
#     # Create a new column 'Extracted_Text' initialized with empty strings
#     # csv_file['Extracted_Text'] = ''
#     # csv_file['Date In Article'] = ''
#     # csv_file['Title'] = ''

#     # Iterate through the URLs
#     for index, row in csv_file.iterrows():
#         url = row['URL']
#         # print("URL->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(url))
#         # print(type(url), url)

#         # if url!=float('nan') or str(url)!='nan':
#         # if not math.isnan(url):
#         try:
#             page = requests.get(url, headers=headers).text 

#             extracted_text = extract_main_text(url) # Extract the main text
                
#             if extracted_text:
#                 # print(f"Extracted main text for {url}:")
#                 # print(extracted_text)
#                 # Add the extracted text to the 'Extracted_Text' column
#                 # csv_file.at[index, 'Extracted_Text'] = extracted_text
#                 # csv_file.at[index,'Date In Article'] = find_date(page)
#                 # csv_file.at[index,'Title'] = extraction.Extractor().extract(page, source_url=url).title
#                 new_df = new_df.append({ 'Title': extraction.Extractor().extract(page, source_url=url).title,'Date In Article': find_date(page),'Extracted_Text': extracted_text, 'URL': url},  ignore_index=True)
        
#         except Exception as e:
#                 new_df = new_df.append({ 'Title': extraction.Extractor().extract(page, source_url=url).title,'Date In Article': find_date(page),'Extracted_Text': extracted_text, 'URL': url},  ignore_index=True)

#             print(f"An error occurred while processing {url}: {str(e)}")
#             continue
#     else:
#         print(f"Failed to extract main text for {url}")

#     # Save the updated DataFrame back to a CSV file
#     new_df.to_csv('TestingScript.csv', index=False, encoding='utf-8-sig')

"""

----------------VERSION 2----------------

"""
# import sys
# from trafilatura import fetch_url, extract
# import pandas as pd
# import requests
# from htmldate import find_date
# import extraction

# def extract_main_text(url):
#     try:
#         downloaded = fetch_url(url)
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

# if __name__ == "__main__":
#     csv_file = pd.read_csv('articles_cleaned_WithMoreThan3Words.csv')
#     new_df = pd.DataFrame(columns=['Title','Main Text', 'Date In Article', 'URL'])
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

#     for index, row in csv_file.iterrows():
#         url = row['URL']
#         if not url.startswith(('http://', 'https://','//')):
#             print(f"Skipping invalid URL: {url}/n")
#             continue
#         try:
#             page = requests.get(url, headers=headers).text
#             extracted_text = extract_main_text(url)
#             if extracted_text:
#                 new_row = pd.DataFrame({
#                     'Title': [extraction.Extractor().extract(page, source_url=url).title],
#                     'Date In Article': [find_date(page)],
#                     'Extracted_Text': [extracted_text],
#                     'URL': [url]
#                 })
#                 new_df = pd.concat([new_df, new_row], ignore_index=True)
#         except Exception as e:
#             new_row = pd.DataFrame({
#                 'Title': ['FAILED'],
#                 'Date In Article': ['FAILED'],
#                 'Extracted_Text': ['FAILED'],
#                 'URL': [url]
#             })
#             new_df = pd.concat([new_df, new_row], ignore_index=True)
#             print(f"An error occurred while processing {index} with {url}: {str(e)}")

#     new_df.to_csv('TestingScript.csv', index=False, encoding='utf-8-sig')




"""

----------------VERSION 3----------------
Trying to combine both more than 3 words and empty URL list....

"""

# import sys
# from trafilatura import fetch_url, extract
# import pandas as pd
# import requests
# from htmldate import find_date
# import extraction

# def extract_main_text(url):
#     try:
#         downloaded = fetch_url(url)
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


# if __name__ == "__main__":
#     folder='./csvs/CNN/'
    
#     # csv_file_1 = pd.read_csv(folder+'InitialHrefFoxNewsBusinessArticles_cleaned_WithLessThan4Words.csv')
#     # csv_file_2 = pd.read_csv(folder+'NoTitleButURL.csv')
#     csv_file = pd.read_csv(folder+'InitialHrefCNNNewsBusinessArticles_Extraction_of_Info.csv')
#     new_df = pd.DataFrame(columns=['Title','Main Text', 'Date In Article', 'URL'])
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
#     # csv_file=pd.concat([csv_file_1,csv_file_2], ignore_index=True)

#     for index, row in csv_file.iterrows():
#         url = row['URL']
#         # if not url.startswith(('http://', 'https://','//')):
#         #     print(f"Skipping invalid URL: {url}/n")
#         #     continue
#         if url.startswith('//'):
#             #Ignore first two elements and start from the third element
#             url = "https:"+ url
#         try:
#             page = requests.get(url, headers=headers).text
#             extracted_text = extract_main_text(url)
#             if extracted_text:
#                 new_row = pd.DataFrame({
#                     'Title': [extraction.Extractor().extract(page, source_url=url).title],
#                     'Date In Article': [find_date(page)],
#                     'Main Text': [extracted_text],
#                     'URL': [url]
#                 })
#                 new_df = pd.concat([new_df, new_row], ignore_index=True)
#         except Exception as e:
#             new_row = pd.DataFrame({
#                 'Title': ['FAILED'],
#                 'Date In Article': ['FAILED'],
#                 'Main Text': ['FAILED'],
#                 'URL': [url]
#             })
#             new_df = pd.concat([new_df, new_row], ignore_index=True)
#             print(f"An error occurred while processing {index} with {url}: {str(e)}")

#     new_df.to_csv( folder + 'CNNBusiness.csv', index=False, encoding='utf-8-sig')


"""


----------------VERSION 4----------------

OOPS Implementation


"""


import sys
from trafilatura import fetch_url, extract
import pandas as pd
import requests
from htmldate import find_date
import extraction

class TextExtractor:
    @staticmethod
    def extract_main_text(url):
        try:
            downloaded = fetch_url(url)
            if downloaded is None:
                print(f"Failed to fetch content from {url}")
                return None
            main_text = extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)
            if main_text:
                return main_text.strip()
            else:
                print(f"No main text could be extracted from {url}")
                return None
        except Exception as e:
            print(f"An error occurred while processing {url}: {str(e)}")
            return None

class WebsiteDataExtractor:
    def __init__(self, csv_path, output_folder):
        self.csv_path = csv_path
        self.output_folder = output_folder
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        self.new_df = pd.DataFrame(columns=['Title', 'Main Text', 'Date In Article', 'URL'])

    def process_csv(self):
        csv_file = pd.read_csv(self.csv_path)
        for index, row in csv_file.iterrows():
            # url = self._prepare_url(row['URL'])
            print(f"processing index {index}-> {row['URL']}")
            url = row['URL']
            # if url:
            self._process_url(url)
        self._save_results()

    # def _prepare_url(self, url):
    #     if url.startswith('//'):
    #         return "https:" + url
    #     return url

    def _process_url(self, url):
        print()
        try:
            page = requests.get(url, headers=self.headers).text
            extracted_text = TextExtractor.extract_main_text(url)
            if extracted_text:
                new_row = pd.DataFrame({
                    'Title': [extraction.Extractor().extract(page, source_url=url).title],
                    'Date In Article': [find_date(page)],
                    'Main Text': [extracted_text],
                    'URL': [url]
                })
                self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
        except Exception as e:
            self._handle_extraction_error(url, e)

    def _handle_extraction_error(self, url, error):
        new_row = pd.DataFrame({
            'Title': ['FAILED'],
            'Date In Article': ['FAILED'],
            'Main Text': ['FAILED'],
            'URL': [url]
        })
        self.new_df = pd.concat([self.new_df, new_row], ignore_index=True)
        print(f"An error occurred while processing {url}: {str(error)}")

    def _save_results(self):
        self.new_df.to_csv(f"{self.output_folder}OutputFile.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    folder = './csvs/CNN/'
    csv_path = folder + 'InitialHrefCNNNewsBusinessArticles.csv'
    extractor = WebsiteDataExtractor(csv_path, folder)
    extractor.process_csv()