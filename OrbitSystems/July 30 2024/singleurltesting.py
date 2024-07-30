# from urllib.request import urlopen
# from bs4 import BeautifulSoup
 
# # target url
# url = 'https://www.geeksforgeeks.org/'
 
# # using the BeautifulSoup module
# soup = BeautifulSoup(urlopen(url))
 
# # displaying the title
# print("Title of the website is : ")
# print (soup.title.get_text())

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import extraction
import requests
# target url
url = 'https://www.cnn.com/2024/07/26/politics/trump-netanyahu-meeting-mar-a-lago/index.html'
 

start=time.time()
# using the BeautifulSoup module
soup = BeautifulSoup(urlopen(url))
 
# displaying the title
print("Title of the website is : ")
print (soup.title.get_text())
print("Time taken: ", time.time()-start)


start = time.time()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

page = requests.get(url, headers=headers).text
title= extraction.Extractor().extract(page, source_url=url).title

# displaying the title
print("Title of the website is : ") 
print (title)
print("Time taken: ", time.time()-start)
