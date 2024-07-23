import time
import pandas as pd
# Importing files
from LinkExtractorModule import *
from CleaningModule import *
from ContentExtractorModule import WebsiteDataExtractor



# nytimes_extractor = NYTimesArticleExtractor("https://www.nytimes.com/section/business", './csvs/NYTimes/InitialHrefNYTimesBusinessArticles.csv',300)
# nytimes_extractor.extract_article_urls()
if __name__ == "__main__":

    # folder = './csvs/FoxNews/'

    # start_time = time.time()

    # genericExtraction= GenericArticleExtractor("https://www.foxbusiness.com/")
    # URL_array = genericExtraction.extract_article_urls()
    # print("Extracted URLs")
    # print(len(URL_array))
    # print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    # fox_cleaner = FoxNewsCleaner(folder,"https://www.foxbusiness.com")
    # URL_array_df = fox_cleaner.clean(URL_array)
    # print("!!!!STEP 2 COMPLETED!!!!")
    # # URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')

    
    # extractor = WebsiteDataExtractor(URL_array_df[:5])
    # new_df = extractor.process_df()
    # print(new_df[:5])
    # end_time=time.time()
    # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # elapsed_time = end_time - start_time

    folder = './csvs/CNN/'

    start_time = time.time()

    genericExtraction= GenericArticleExtractor("https://www.cnn.com/business")
    URL_array = genericExtraction.extract_article_urls()
    print("Extracted URLs")
    print(len(URL_array))
    print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    cnn_cleaner = CNNCleaner(folder,"https://www.cnn.com/business")
    URL_array_df = cnn_cleaner.clean(URL_array)
    URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')
    print("!!!!STEP 2 COMPLETED!!!!")
    

    
    extractor = WebsiteDataExtractor(URL_array_df[:5])
    new_df = extractor.process_df()
    print(new_df)
    end_time=time.time()
    print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    elapsed_time = end_time - start_time

    # Print the result
    print(f"Execution time: {elapsed_time:.2f} seconds")