# #This script extracts all the URLs from a given
# # webpage using the BeautifulSoup library.

# from bs4 import BeautifulSoup
# import requests
# import csv 
# import pandas as pd

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

# def extract_article_urls(url):
#     # Send a GET request to the URL
#     response = requests.get(url, headers=headers)
    
#     # If the GET request is successful, the status code will be 200
#     if response.status_code == 200:
#         print("Inside 200")
#         # Get the content of the response
#         page_content = response.content
        
#         # Create a BeautifulSoup object and specify the parser
#         soup = BeautifulSoup(page_content, 'html.parser')
        
#         # Find all the anchor tags
#         anchor_tags = soup.find_all('a')

#         with open('articles.csv', 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             # Write the header
#             writer.writerow(["Title", "URL"])
#             # Write the data
#             for tag in anchor_tags:
#                 if tag.get('href'):
#                     writer.writerow([tag.text, tag.get('href')])

#         cleaning("articles")
#         # print(anchor_tags)
#         # Extract and return the href attribute (URL) from the anchor tags
#         # Filter out any URLs that are None or not articles
#         # return [(tag.text,tag.get('href')) for tag in anchor_tags if tag.get('href')]




# def cleaning(filename):
#     df= pd.read_csv(filename+".csv")
#     # Removing any duplicate rows/columns
#     df.drop_duplicates(inplace=True)

#     # Removing any rows where the title is missing
#     df =df[df['Title'].str.strip() != '']    
    
#     # Group by URL and keep the row with the longest title for each URL
#     # df['Title_Length'] = df['Title'].str.len()
#     # df = df.loc[df.groupby('URL')[df['Title'].str.len()].idxmax()]
#     df = df.loc[df.groupby('URL').apply(lambda x: x['Title'].str.len().idxmax())]

#     # Removing any leading or trailing whitespaces
#     df['Title'] = df['Title'].str.strip()

#     df.to_csv(filename+"_cleaned"+".csv", index=False)



# # Test the function
# url = "https://www.foxnews.com/"
# extract_article_urls(url)

# df=pd.read_csv("articles_cleaned.csv")
# print(df[155:165])
"""

--- CURRENT VERSION----


"""
# from bs4 import BeautifulSoup
# import requests
# import csv 
# import os
# import pandas as pd

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

# def extract_article_urls(url):
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         page_content = response.content
#         soup = BeautifulSoup(page_content, 'html.parser')
#         anchor_tags = soup.find_all('a')

#         csv_path = './csvs/CNN/InitialHrefCNNNewsBusinessArticles.csv'
        
#         # Create directory if it doesn't exist
#         os.makedirs(os.path.dirname(csv_path), exist_ok=True)

#         # Check if file exists to determine whether to write headers
#         file_exists = os.path.isfile(csv_path)

#         with open(csv_path, 'a', newline='', encoding='utf-8') as file:
#             fieldnames = ["Title", "URL"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
            
#             if not file_exists:
#                 writer.writeheader()  # Write header if file doesn't exist

#             for tag in anchor_tags:
#                 if tag.get('href'):
#                     writer.writerow({"Title": tag.text, "URL": tag.get('href')})

#         print(f"Data has been written to {csv_path}")

# url = "https://www.cnn.com/business"
# extract_article_urls(url)

from bs4 import BeautifulSoup
import requests
import csv 
import os
import pandas as pd
from abc import ABC, abstractmethod

class ArticleExtractor(ABC):
    def __init__(self, url, csv_path):
        self.url = url
        self.csv_path = csv_path
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

    def extract_article_urls(self):
        response = self.get_response()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = self.parse_articles(soup)
            self.write_to_csv(articles)
            print(f"Data has been written to {self.csv_path}")

    def get_response(self):
        return requests.get(self.url, headers=self.headers)

    @abstractmethod
    def parse_articles(self, soup):
        pass

    def write_to_csv(self, articles):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        file_exists = os.path.isfile(self.csv_path)

        with open(self.csv_path, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ["Title", "URL"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()

            for article in articles:
                writer.writerow(article)

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

# Usage
cnn_extractor = CNNArticleExtractor("https://www.cnn.com/business", './csvs/CNN/InitialHrefCNNNewsBusinessArticles.csv')
cnn_extractor.extract_article_urls()

# For Fox News, you would create a similar class and implement its parsing logic
# fox_extractor = FoxNewsArticleExtractor("https://www.foxnews.com/business", './csvs/FoxNews/InitialHrefFoxNewsBusinessArticles.csv')
# fox_extractor.extract_article_urls()
