"""


------------------------VERSION 2 ----------------

OOPS IMPLEMENTATION


"""

import pandas as pd
import re
from datetime import datetime
from abc import ABC, abstractmethod
import time


class DataCleaner(ABC):
    def __init__(self, folder,domain):
        self.domain=domain
        self.folder=folder

    @abstractmethod
    def remove_invalid_urls(self, df):
        pass

    @abstractmethod
    def add_domain(self, df):
        pass

    def clean(self, URL_array):
        self.create_log_file()
        
        # df = pd.read_csv(self.folder_to_save + filename + ".csv", encoding='utf-8')
        df=pd.DataFrame(URL_array,columns=['URL'])
        initial_count = len(df)
        self.log(f"Initial number of rows: {initial_count}")

        df = self.remove_invalid_urls(df)
        df = self.add_domain(df)
        df = self.remove_duplicates(df)
        # df = self.concatenate_titles(df)
        # df = self.strip_whitespace(df)
        # no_title_df = self.handle_empty_titles(df)

        # self.save_dataframe(df, filename + "_cleaned_Without_TitleFilter")

        # df_4words, df_lessthan4words = self.filter_by_word_count(df)
        # self.save_dataframe(df_4words, filename + "_cleaned_WithMoreThan3Words")
        # self.save_dataframe(df_lessthan4words, filename + "_cleaned_WithLessThan4Words")

        # final_count = len(df_4words) + len(no_title_df)
        # self.log(f"Final number of rows: {final_count}")
        # self.log(f"Total rows removed: {initial_count - final_count}")

        # # Log the sizes of dataframes before concatenation
        # self.log(f"Number of rows in df_4words: {len(df_4words)}")
        # self.log(f"Number of rows in no_title_df: {len(no_title_df)}")

        # df_Extraction_of_Info = pd.concat([df_4words, no_title_df], ignore_index=True)
        
        # # Log the size of the concatenated dataframe
        # self.log(f"Number of rows in df_Extraction_of_Info after concatenation: {len(df_Extraction_of_Info)}")

        # self.save_dataframe(df, filename + "_Extraction_of_Info")
        self.close_log_file()
        return df

    def log(self, message):
        print(message)
        self.log_file.write(message + '\n')

    def create_log_file(self):
        log_filename = f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.log_file = open(self.folder + log_filename, 'w')

    def close_log_file(self):
        self.log_file.close()

    def remove_duplicates(self, df):
        duplicates_count = df.duplicated().sum()
        # total_so_far = len(df)
        df.drop_duplicates(inplace=True)
        # self.log(f"Total_so_far: {total_so_far}")
        self.log(f"Number of duplicate rows: {duplicates_count}")
        return df

    def handle_empty_titles(self, df):
        no_title_df = df[df['Title'].str.strip() == '']
        no_title_count = len(no_title_df)
        self.save_dataframe(no_title_df, "NoTitleButURL")
        # print(f"length of no_title_df {len(no_title_df)}")
        self.log(f"Number of rows with no title: {no_title_count}")
        # df = df[df['Title'].str.strip() == '']
        # print(f"length of df of only empty titles {len(df)}")
        return no_title_df

    def concatenate_titles(self, df):
        before_concat = len(df)
        df = df.groupby('URL').agg({
            'Title': lambda x: ' | '.join(x.drop_duplicates()),
            'URL': 'first'
        }).reset_index(drop=True)
        rows_concat = before_concat - len(df)
        # self.log(f"Total_so_far: {before_concat}")
        self.log(f"Number of rows concatenated due to same URL: {rows_concat}")
        return df

    def strip_whitespace(self, df):
        df['Title'] = df['Title'].str.strip()
        return df

    def filter_by_word_count(self, df):
        df_4words = df[df['Title'].str.split().str.len() > 3]
        df_lessthan4words = df[df['Title'].str.split().str.len() <= 3]
        self.log(f"Number of rows with more than 3 words in title: {len(df_4words)}")
        self.log(f"Number of rows with less than 4 words in title: {len(df_lessthan4words)}")
        return df_4words, df_lessthan4words

    def save_dataframe(self, df, filename):
        df.to_csv(self.folder_to_save + filename + ".csv", index=False, encoding='utf-8')

class CNNCleaner(DataCleaner):
    def remove_invalid_urls(self, df):
        pattern = r'^(https://|/)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        total=len(df)
        self.log(f"Number of rows with invalid URLs: {invalid_url_count} and passing-> {total-invalid_url_count}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/'
        slash_urls_count = df['URL'].str.startswith('/').sum()
        
        # Add domain to URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
        self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
        return df

class FoxNewsCleaner(DataCleaner):
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '//'
        df.loc[df['URL'].str.startswith('//', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('//', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|//)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        self.log(f"Number of URLs updated from '//' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/'
        slash_urls_count = df['URL'].str.startswith('//').sum()
        
        # Add domain to URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('//') else x)
        
        self.log(f"Added domain to {slash_urls_count} URLs starting with '//'")
        return df


class NYTimesCleaner(DataCleaner):
    # NOTE in NYTimes, most articles are relative path which starts with '/'
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '//'
        # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|/)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/'
        slash_urls_count = df['URL'].str.startswith('/').sum()
        
        # Add domain to URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
        self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
        return df
    
class FierceCleaner(DataCleaner):
    # NOTE in NYTimes, most articles are relative path which starts with '/'
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '//'
        # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|/)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/'
        slash_urls_count = df['URL'].str.startswith('/').sum()
        
        # Add domain to URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
        self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
        return df
    
class HealthcareDiveCleaner(DataCleaner):
    # NOTE in NYTimes, most articles are relative path which starts with '/'
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '/'
        # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|/)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/'
        slash_urls_count = df['URL'].str.startswith('/').sum()
        
        # Add domain to URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
        self.log(f"Added domain to {slash_urls_count} URLs starting with '/'")
        return df
    

class GenericCleaner(DataCleaner):
    # NOTE in NYTimes, most articles are relative path which starts with '/'
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '//'
        # df.loc[df['URL'].str.startswith('/', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('/', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|/|//)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        # df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        # print(invalid_urls)
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        # self.log(f"Number of URLs updated from '/' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        return df
    
    def add_domain(self, df):
        # Count URLs starting with '/' and '//'
        slash_urls_count = df['URL'].str.startswith('/').sum()
        double_slash_urls_count = df['URL'].str.startswith('//').sum()
        
        # # Determine which format is more common
        # if slash_urls_count >= double_slash_urls_count:
        #     # If '/' is more common or equal, update URLs starting with '/'
        #     df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        #     update_message = f"Added domain to {slash_urls_count} URLs starting with '/'"
        # else:
        #     # If '//' is more common, update URLs starting with '//'
        #     df['URL'] = df['URL'].apply(lambda x: self.domain + x[1:] if x.startswith('//') else x)
        #     update_message = f"Updated {double_slash_urls_count} URLs starting with '//'"
        
        # Remove '//' from URLs starting with '//'
        df['URL'] = df['URL'].apply(lambda x: x[2:] if x.startswith('//') else x)

        """In Foxbusiness, after removing //, we see that its mostly URL with WWW which are articles."""

        df['URL'] = df['URL'].apply(lambda x: "https://" + x if x.startswith('www') else x)

        # Update URLs starting with '/'
        df['URL'] = df['URL'].apply(lambda x: self.domain + x if x.startswith('/') else x)
        
                
                
        df.to_csv(self.folder + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')

        # self.log(update_message)
        self.log(f"URLs starting with '/': {slash_urls_count}")
        self.log(f"URLs starting with '//': {double_slash_urls_count}")
        
        return df