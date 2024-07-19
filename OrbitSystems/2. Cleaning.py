# import pandas as pd



# def cleaning(filename):
#     df= pd.read_csv(filename+".csv",encoding='utf-8')
    
#     # Removing any URL's which doesn't follow a format


    
#     # Removing any duplicate rows
#     df.drop_duplicates(inplace=True)

#     # Save rows with empty titles in a separate CSV
#     no_title_df = df[df['Title'].str.strip() == '']
#     no_title_df.to_csv("NoTitleButURL.csv", index=False, encoding='utf-8')

#     # Remove rows with empty titles from the original dataframe
#     df = df[df['Title'].str.strip() != '']

#     # When there are two rows with same URL, we consider longest title
#     df = df.loc[df.groupby('URL').apply(lambda x: x['Title'].str.len().idxmax())]
    
#     #Strippping leading and trailing whitespaces
#     df['Title'] = df['Title'].str.strip()


#     df.to_csv(filename+"_cleaned_Without_TitleFilter"+".csv", index=False, encoding='utf-8')

#     #Below is the code to remove rows with less than 2 words in sentence.
#     df_4words = df[df['Title'].str.split().str.len() > 3]

#     df_4words.to_csv(filename+"_cleaned_WithMoreThan3Words"+".csv", index=False, encoding='utf-8')

#     df_lessthan3words = df[df['Title'].str.split().str.len() <= 3]

#     df_lessthan3words.to_csv(filename+"_cleaned_WithLessThan4Words"+".csv", encoding='utf-8', index=False)

# import pandas as pd
# import re


# folder_to_save='./csvs/'

# def cleaning(filename):
#     df = pd.read_csv(folder_to_save + filename + ".csv", encoding='utf-8')
    
#     initial_count = len(df)
#     print(f"Initial number of rows: {initial_count}")

#     # Count and remove URLs that don't start with https, http, //, or www
#     pattern = r'^(https?://|//|www\.)'
#     invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#     invalid_url_count = len(invalid_urls)
#     df = df[df['URL'].str.match(pattern, case=False)]
#     print(f"Number of rows with invalid URLs removed: {invalid_url_count}")

#     # Removing any duplicate rows
#     duplicates_count = df.duplicated().sum()
#     df.drop_duplicates(inplace=True)
#     print(f"Number of duplicate rows removed: {duplicates_count}")

#     # Save rows with empty titles in a separate CSV
#     no_title_df = df[df['Title'].str.strip() == '']
#     no_title_count = len(no_title_df)
#     no_title_df.to_csv(folder_to_save+"NoTitleButURL.csv", index=False, encoding='utf-8')
#     print(f"Number of rows with no title: {no_title_count}")

#     # Remove rows with empty titles from the original dataframe
#     df = df[df['Title'].str.strip() != '']

#     # When there are two rows with same URL, we consider longest title
#     before_longest_title = len(df)
#     df = df.loc[df.groupby('URL').apply(lambda x: x['Title'].str.len().idxmax())]
#     longest_title_removed = before_longest_title - len(df)
#     print(f"Number of rows removed due to longest title selection: {longest_title_removed}")

#     # Stripping leading and trailing whitespaces
#     df['Title'] = df['Title'].str.strip()

#     df.to_csv(folder_to_save+ filename + "_cleaned_Without_TitleFilter" + ".csv", index=False, encoding='utf-8')

#     # Below is the code to remove rows with less than 4 words in sentence.
#     df_4words = df[df['Title'].str.split().str.len() > 3]
#     df_4words.to_csv(folder_to_save + filename + "_cleaned_WithMoreThan3Words" + ".csv", index=False, encoding='utf-8')

#     df_lessthan4words = df[df['Title'].str.split().str.len() <= 3]
#     lessthan4words_count = len(df_lessthan4words)
#     df_lessthan4words.to_csv(folder_to_save+ filename + "_cleaned_WithLessThan4Words" + ".csv", encoding='utf-8', index=False)
#     print(f"Number of rows with less than 4 words in title: {lessthan4words_count}")

#     final_count = len(df_4words)+no_title_count
#     print(f"Final number of rows(which is only url's with more than 4 words and empty sentences.): {final_count}")
#     print(f"Total rows removed: {initial_count - final_count}")

#     # return invalid_url_count

# # Example usage
# cleaning("InitialHrefFoxNewsBusinessArticles")
"""


------------------------VERSION 1 ----------------
WORKING!!!


"""
# import pandas as pd
# import re
# from datetime import datetime

# folder_to_save='./csvs/CNN/'

# def cleaning(filename):
#     # Open a text file to write the log
#     log_filename = f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#     with open(folder_to_save+ log_filename, 'w') as log_file:
#         def log(message):
#             print(message)
#             log_file.write(message + '\n')

#         df = pd.read_csv( folder_to_save + filename + ".csv", encoding='utf-8')
        
#         initial_count = len(df)
#         log(f"Initial number of rows: {initial_count}")

#         # Count and remove URLs that don't start with https, http, //, or www
#         pattern = r'^(https?://|//|www\.)'
#         invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
#         invalid_url_count = len(invalid_urls)
#         df = df[df['URL'].str.match(pattern, case=False)]
#         log(f"Number of rows with invalid URLs removed: {invalid_url_count}")

#         # Removing any duplicate rows
#         duplicates_count = df.duplicated().sum()
#         df.drop_duplicates(inplace=True)
#         log(f"Number of duplicate rows removed: {duplicates_count}")

#         # Save rows with empty titles in a separate CSV
#         no_title_df = df[df['Title'].str.strip() == '']
#         no_title_count = len(no_title_df)
#         no_title_df.to_csv(folder_to_save+ "NoTitleButURL.csv", index=False, encoding='utf-8')
#         log(f"Number of rows with no title: {no_title_count}")

#         # Remove rows with empty titles from the original dataframe
#         df = df[df['Title'].str.strip() != '']

#         # # When there are two rows with same URL, we consider longest title
#         # before_longest_title = len(df)
#         # df = df.loc[df.groupby('URL').apply(lambda x: x['Title'].str.len().idxmax())]
#         # longest_title_removed = before_longest_title - len(df)
#         # log(f"Number of rows removed due to longest title selection: {longest_title_removed}")


#         # When there are two or more rows with the same URL, concatenate their titles
#         before_concat = len(df)
#         df = df.groupby('URL').agg({
#             'Title': lambda x: ' | '.join(x.drop_duplicates()),
#             'URL': 'first'  # Keep the URL (it's the same for all rows in the group)
#         }).reset_index(drop=True)
#         rows_concat = before_concat - len(df)
#         log(f"Number of rows concatenated due to same URL: {rows_concat}")

#         # Stripping leading and trailing whitespaces
#         df['Title'] = df['Title'].str.strip()

#         df.to_csv(folder_to_save + filename + "_cleaned_Without_TitleFilter" + ".csv", index=False, encoding='utf-8')

#         # Below is the code to remove rows with less than 4 words in sentence.
#         df_4words = df[df['Title'].str.split().str.len() > 3]
#         df_4words.to_csv(folder_to_save+filename + "_cleaned_WithMoreThan3Words" + ".csv", index=False, encoding='utf-8')
#         log(f"Number of rows with more than 3 words in title: {len(df_4words)}")

#         df_lessthan4words = df[df['Title'].str.split().str.len() <= 3]
#         lessthan4words_count = len(df_lessthan4words)
#         df_lessthan4words.to_csv(folder_to_save+filename + "_cleaned_WithLessThan4Words" + ".csv", encoding='utf-8', index=False)
#         log(f"Number of rows with less than 4 words in title: {lessthan4words_count}")

#         final_count = len(df_4words)+no_title_count
#         log(f"Final number of rows(which is only url's with more than 4 words and empty sentences.): {final_count}")
#         log(f"Total rows removed: {initial_count - final_count}")

#         df_Extraction_of_Info=pd.concat([df_4words,no_title_df])
#         df_Extraction_of_Info.to_csv(folder_to_save+filename + "_Extraction_of_Info" + ".csv", encoding='utf-8', index=False)
#     # return invalid_url_count

# # Example usage
# cleaning("InitialHrefCNNNewsBusinessArticles")
# # print(f"Log file has been created: {log_filename}")



"""


------------------------VERSION 2 ----------------

OOPS IMPLEMENTATION


"""

import pandas as pd
import re
from datetime import datetime
from abc import ABC, abstractmethod

class DataCleaner(ABC):
    def __init__(self, folder_to_save):
        self.folder_to_save = folder_to_save

    @abstractmethod
    def remove_invalid_urls(self, df):
        pass

    def clean(self, filename):
        self.create_log_file()
        
        df = pd.read_csv(self.folder_to_save + filename + ".csv", encoding='utf-8')
        
        initial_count = len(df)
        self.log(f"Initial number of rows: {initial_count}")

        df = self.remove_invalid_urls(df)
        df = self.remove_duplicates(df)
        df = self.concatenate_titles(df)
        df = self.strip_whitespace(df)
        no_title_df = self.handle_empty_titles(df)

        self.save_dataframe(df, filename + "_cleaned_Without_TitleFilter")

        df_4words, df_lessthan4words = self.filter_by_word_count(df)
        self.save_dataframe(df_4words, filename + "_cleaned_WithMoreThan3Words")
        self.save_dataframe(df_lessthan4words, filename + "_cleaned_WithLessThan4Words")

        final_count = len(df_4words) + len(no_title_df)
        self.log(f"Final number of rows: {final_count}")
        self.log(f"Total rows removed: {initial_count - final_count}")

        # Log the sizes of dataframes before concatenation
        self.log(f"Number of rows in df_4words: {len(df_4words)}")
        self.log(f"Number of rows in no_title_df: {len(no_title_df)}")

        df_Extraction_of_Info = pd.concat([df_4words, no_title_df], ignore_index=True)
        
        # Log the size of the concatenated dataframe
        self.log(f"Number of rows in df_Extraction_of_Info after concatenation: {len(df_Extraction_of_Info)}")

        self.save_dataframe(df_Extraction_of_Info, filename + "_Extraction_of_Info")
        self.close_log_file()

    def log(self, message):
        print(message)
        self.log_file.write(message + '\n')

    def create_log_file(self):
        log_filename = f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.log_file = open(self.folder_to_save + log_filename, 'w')

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
        pattern = r'^(https?://|//|www\.)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        total=len(df)
        self.log(f"Number of rows with invalid URLs: {invalid_url_count} and passing-> {total-invalid_url_count}")
        return df

class FoxNewsCleaner(DataCleaner):
    def remove_invalid_urls(self, df):
        # First, handle URLs starting with '//'
        df.loc[df['URL'].str.startswith('//', na=False), 'URL'] = 'https:' + df.loc[df['URL'].str.startswith('//', na=False), 'URL']

        # Now check for valid URLs
        pattern = r'^(https?://|www\.)'
        invalid_urls = df[~df['URL'].str.match(pattern, case=False)]
        invalid_url_count = len(invalid_urls)
        df = df[df['URL'].str.match(pattern, case=False)]
        df.to_csv(self.folder_to_save + "AfterConvertingInvalidURLs.csv", index=False, encoding='utf-8')
        self.log(f"Number of rows with invalid URLs : {invalid_url_count}")
        self.log(f"Number of URLs updated from '//' to 'https://': {sum(df['URL'].str.startswith('https://', na=False))}")
        
        return df

# # Example usage
# cnn_cleaner = CNNCleaner('./csvs/CNN/')
# cnn_cleaner.clean("InitialHrefCNNNewsBusinessArticles")

fox_cleaner = FoxNewsCleaner('./csvs/FoxNews/')
fox_cleaner.clean("InitialHrefFoxNewsBusinessArticles")