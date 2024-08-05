import pandas as pd
import re
from datetime import datetime
from abc import ABC, abstractmethod
import time
# from logging_config import logger
import logging
import os

class DataCleaner(ABC):
    def __init__(self, folder, domain):
        self.domain = domain
        self.folder = folder
        self.logger = logging.getLogger(self.__class__.__name__)
        # self.logger = self.setup_logger()

    # def setup_logger(self):
    #     logger = logging.getLogger(self.__class__.__name__)
    #     logger.setLevel(logging.DEBUG)

    #     # Create logs directory if it doesn't exist
    #     log_dir = os.path.join(self.folder, 'logs')
    #     os.makedirs(log_dir, exist_ok=True)

    #     # File handler
    #     file_handler = logging.FileHandler(os.path.join(log_dir, f'{self.__class__.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'))
    #     file_handler.setLevel(logging.DEBUG)

    #     # Console handler
    #     console_handler = logging.StreamHandler()
    #     console_handler.setLevel(logging.INFO)

    #     # Create formatter and add it to the handlers
    #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #     file_handler.setFormatter(formatter)
    #     console_handler.setFormatter(formatter)

    #     # Add the handlers to the logger
    #     logger.addHandler(file_handler)
    #     logger.addHandler(console_handler)

    #     return logger

    @abstractmethod
    def remove_invalid_urls(self, df):
        pass

    @abstractmethod
    def add_domain(self, df):
        pass

    def clean(self, URL_array):
        self.logger.info("Starting cleaning process")
        
        df = pd.DataFrame(URL_array, columns=['URL'])
        df['Status']=''
        
        initial_count = len(df)
        self.logger.info(f"Initial number of rows: {initial_count}")

        # df.to_csv(os.path.join(self.folder, "InitialHref.csv"), index=False, encoding='utf-8')
        df = self.remove_invalid_urls(df)
        df = self.add_domain(df)
        df = self.remove_duplicates(df)
       
        self.logger.info("Cleaning process completed")
        # return df
        df= df.reset_index(drop=True)
        return df

    def remove_duplicates(self, df):
        duplicates_count = df.duplicated().sum()
        df.drop_duplicates(inplace=True)
        self.logger.info(f"Number of duplicate rows removed: {duplicates_count}")
        return df


class GenericCleaner(DataCleaner):
    def remove_invalid_urls(self, df):
        pattern = r'^(https?://|/|//)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        self.logger.info(f"Number of rows with invalid URLs: {invalid_url_count}")
        return df
    
    def add_domain(self, df):
        slash_urls_count = df['URL'].str.startswith('/').sum()
        double_slash_urls_count = df['URL'].str.startswith('//').sum()
        
        df['URL'] = df['URL'].apply(lambda x: x[2:] if x.startswith('//') else x)
        df['URL'] = df['URL'].apply(lambda x: "https://" + x if x.startswith('www') else x)
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
        # df.to_csv(os.path.join(self.folder, "AfterConvertingInvalidURLs.csv"), index=False, encoding='utf-8')
        self.logger.info(f"URLs starting with '/': {slash_urls_count}")
        self.logger.info(f"URLs starting with '//': {double_slash_urls_count}")
        self.logger.info("Saved 'AfterConvertingInvalidURLs.csv'")
        
        return df
    

    # def handle_empty_titles(self, df):
    #     no_title_df = df[df['Title'].str.strip() == '']
    #     no_title_count = len(no_title_df)
    #     self.save_dataframe(no_title_df, "NoTitleButURL")
    #     self.logger.info(f"Number of rows with no title: {no_title_count}")
    #     return no_title_df

    # def concatenate_titles(self, df):
    #     before_concat = len(df)
    #     df = df.groupby('URL').agg({
    #         'Title': lambda x: ' | '.join(x.drop_duplicates()),
    #         'URL': 'first'
    #     }).reset_index(drop=True)
    #     rows_concat = before_concat - len(df)
    #     self.logger.info(f"Number of rows concatenated due to same URL: {rows_concat}")
    #     return df

    # def strip_whitespace(self, df):
    #     df['Title'] = df['Title'].str.strip()
    #     self.logger.debug("Whitespace stripped from Title column")
    #     return df

    # def save_dataframe(self, df, filename):
    #     df.to_csv(os.path.join(self.folder, f"{filename}.csv"), index=False, encoding='utf-8')
    #     self.logger.info(f"Saved dataframe to {filename}.csv")

# class CNNCleaner(DataCleaner):
#     def remove_invalid_urls(self, df):
#         pattern = r'^(https://|/)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         total = len(df)
#         self.logger.info(f"Number of rows with invalid URLs: {invalid_url_count}, valid URLs: {total}")
#         return df
    
#     def add_domain(self, df):
#         slash_urls_count = df['URL'].str.startswith('/').sum()
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
#         self.logger.info(f"Added domain to {slash_urls_count} URLs starting with '/'")
#         return df

# class FoxNewsCleaner(DataCleaner):
#     def remove_invalid_urls(self, df):
#         df.loc[df['URL'].str.startswith('//', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('//', na=False), 'URL']
#         pattern = r'^(https?://|//)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         self.logger.info(f"Number of rows with invalid URLs: {invalid_url_count}")
#         self.logger.info(f"Number of URLs updated from '//' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         slash_urls_count = df['URL'].str.startswith('//').sum()
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('//') else x)
#         self.logger.info(f"Added domain to {slash_urls_count} URLs starting with '//'")
#         return df

# Similar modifications for NYTimesCleaner, FierceCleaner, HealthcareDiveCleaner...





#######################  OLD WORKING CODE WITH NO LOGGING  ############################
# import pandas as pd
# import re
# from datetime import datetime
# from abc import ABC, abstractmethod
# import time


# class DataCleaner(ABC):
#     def __init__(self, folder,domain):
#         self.domain=domain
#         self.folder=folder

#     @abstractmethod
#     def remove_invalid_urls(self, df):
#         pass

#     @abstractmethod
#     def add_domain(self, df):
#         pass

#     def clean(self, URL_array):
#         self.create_log_file()
        
#         # df = pd.read_csv(self.folder_to_save + filename + ".csv", encoding='utf-8')
#         df=pd.DataFrame(URL_array,columns=['URL'])
#         initial_count = len(df)
#         self.log(f"Initial number of rows: {initial_count}")

#         df = self.remove_invalid_urls(df)
#         df = self.add_domain(df)
#         df = self.remove_duplicates(df)
       
#         self.close_log_file()
#         return df

#     def log(self, message):
#         print(message)
#         self.log_file.write(message + '\n')

#     def create_log_file(self):
#         log_filename = f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#         self.log_file = open(self.folder + log_filename, 'w')

#     def close_log_file(self):
#         self.log_file.close()

#     def remove_duplicates(self, df):
#         duplicates_count = df.duplicated().sum()
#         # total_so_far = len(df)
#         df.drop_duplicates(inplace=True)
#         # self.log(f"Total_so_far: {total_so_far}")
#         self.log(f"Number of duplicate rows: {duplicates_count}")
#         return df

#     def handle_empty_titles(self, df):
#         no_title_df = df[df['Title'].str.strip() == '']
#         no_title_count = len(no_title_df)
#         self.save_dataframe(no_title_df, "NoTitleButURL")
#         # print(f"length of no_title_df {len(no_title_df)}")
#         self.log(f"Number of rows with no title: {no_title_count}")
#         # df = df[df['Title'].str.strip() == '']
#         # print(f"length of df of only empty titles {len(df)}")
#         return no_title_df

#     def concatenate_titles(self, df):
#         before_concat = len(df)
#         df = df.groupby('URL').agg({
#             'Title': lambda x: ' | '.join(x.drop_duplicates()),
#             'URL': 'first'
#         }).reset_index(drop=True)
#         rows_concat = before_concat - len(df)
#         # self.log(f"Total_so_far: {before_concat}")
#         self.log(f"Number of rows concatenated due to same URL: {rows_concat}")
#         return df

#     def strip_whitespace(self, df):
#         df['Title'] = df['Title'].str.strip()
#         return df

# class CNNCleaner(DataCleaner):
#     def remove_invalid_urls(self, df):
#         pattern = r'^(https://|/)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         total=len(df)
#         self.log(f"Number of rows with invalid URLs: {invalid_url_count} and passing-> {total-invalid_url_count}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/'
#         slash_urls_count = df['URL'].str.startswith('/').sum()
        
#         # Add domain to URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
#         self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
#         return df

# class FoxNewsCleaner(DataCleaner):
#     def remove_invalid_urls(self, df):
#         # First, handle URLs starting with '//'
#         df.loc[df['URL'].str.startswith('//', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('//', na=False), 'URL']

#         # Now check for valid URLs
#         pattern = r'^(https?://|//)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
#         self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
#         self.log(f"Number of URLs updated from '//' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/'
#         slash_urls_count = df['URL'].str.startswith('//').sum()
        
#         # Add domain to URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('//') else x)
        
#         self.log(f"Added domain to {slash_urls_count} URLs starting with '//'")
#         return df


# class NYTimesCleaner(DataCleaner):
#     # NOTE in NYTimes, most articles are relative path which starts with '/'
#     def remove_invalid_urls(self, df):
#         # First, handle URLs starting with '//'
#         # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

#         # Now check for valid URLs
#         pattern = r'^(https?://|/)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
#         self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
#         self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/'
#         slash_urls_count = df['URL'].str.startswith('/').sum()
        
#         # Add domain to URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
#         self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
#         return df
    
# class FierceCleaner(DataCleaner):
#     # NOTE in NYTimes, most articles are relative path which starts with '/'
#     def remove_invalid_urls(self, df):
#         # First, handle URLs starting with '//'
#         # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

#         # Now check for valid URLs
#         pattern = r'^(https?://|/)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
#         self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
#         self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/'
#         slash_urls_count = df['URL'].str.startswith('/').sum()
        
#         # Add domain to URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
#         self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
#         return df
    
# class HealthcareDiveCleaner(DataCleaner):
#     # NOTE in NYTimes, most articles are relative path which starts with '/'
#     def remove_invalid_urls(self, df):
#         # First, handle URLs starting with '/'
#         # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

#         # Now check for valid URLs
#         pattern = r'^(https?://|/)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
#         self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
#         self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/'
#         slash_urls_count = df['URL'].str.startswith('/').sum()
        
#         # Add domain to URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
#         self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
#         return df
    

# class GenericCleaner(DataCleaner):
#     # NOTE in NYTimes, most articles are relative path which starts with '/'
#     def remove_invalid_urls(self, df):
#         # First, handle URLs starting with '//'
#         # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

#         # Now check for valid URLs
#         pattern = r'^(https?://|/|//)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
#         # print(invalid_urls)
#         self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
#         # self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
#         return df
    
#     def add_domain(self, df):
#         # Count URLs starting with '/' and '//'
#         slash_urls_count = df['URL'].str.startswith('/').sum()
#         double_slash_urls_count = df['URL'].str.startswith('//').sum()
        
#         df['URL'] = df['URL'].apply(lambda x: x[2:] if x.startswith('//') else x)

#         """In Foxbusiness, after removing //, we see that its mostly URL with WWW which are articles."""

#         df['URL'] = df['URL'].apply(lambda x: "https://" + x if x.startswith('www') else x)

#         # Update URLs starting with '/'
#         df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
                
                
#         df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')

#         # self.log(update_message)
#         self.log(f"URLs starting with '/': {slash_urls_count}")
#         self.log(f"URLs starting with '//': {double_slash_urls_count}")
        
#         return df