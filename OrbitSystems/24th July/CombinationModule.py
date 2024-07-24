import time
import pandas as pd
# Importing files
from LinkExtractorModule import *
from CleaningModule import *
from ContentExtractorModule import WebsiteDataExtractor
import json


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

    # folder = './csvs/CNN/'

    # start_time = time.time()

    # genericExtraction= GenericArticleExtractor("https://www.cnn.com/business")
    # URL_array = genericExtraction.extract_article_urls()
    # print("Extracted URLs")
    # print(len(URL_array))
    # print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    # cnn_cleaner = CNNCleaner(folder,"https://www.cnn.com/business")
    # URL_array_df = cnn_cleaner.clean(URL_array)
    # URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')
    # print("!!!!STEP 2 COMPLETED!!!!")
    

    
    # extractor = WebsiteDataExtractor(URL_array_df[:5])
    # new_df = extractor.process_df()
    # print(new_df)
    # end_time=time.time()
    # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # elapsed_time = end_time - start_time

    # # Print the result
    # print(f"Execution time: {elapsed_time:.2f} seconds")


    # folder = './csvs/NYTimes/'

    # start_time = time.time()

    # genericExtraction= GenericArticleExtractor("https://www.nytimes.com/section/business")
    # URL_array = genericExtraction.extract_article_urls()
    # print("Extracted URLs")
    # print(URL_array)
    # print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    # nytimes_cleaner = NYTimesCleaner(folder,"https://www.nytimes.com")
    # URL_array_df = nytimes_cleaner.clean(URL_array)
    # # URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')
    # print("!!!!STEP 2 COMPLETED!!!!")
    

    
    # extractor = WebsiteDataExtractor(URL_array_df)
    # new_df = extractor.process_df()
    # new_df.to_csv(folder + 'FinalCheckingURLS.csv', index=False, encoding='utf-8')
    # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    # folder = './csvs/Fierce/'

    # # start_time = time.time()

    # genericExtraction= GenericArticleExtractor("https://www.fiercehealthcare.com/")
    # URL_array = genericExtraction.extract_article_urls()
    # print("Extracted URLs")
    # print("Number of URLS"+ str(len(URL_array)))
    # print(URL_array)
    # print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    # fierce_cleaner = FierceCleaner(folder,"https://www.fiercehealthcare.com")
    # URL_array_df = fierce_cleaner.clean(URL_array)
    # URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')
    # print("!!!!STEP 2 COMPLETED!!!!")
    
    # extractor = WebsiteDataExtractor(URL_array_df)
    # new_df = extractor.process_df()
    # new_df.to_csv(folder + 'FinalCheckingURLS.csv', index=False, encoding='utf-8')
    # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    



    # end_time=time.time()
    # elapsed_time = end_time - start_time

    # # Print the result
    # print(f"Execution time: {elapsed_time:.2f} seconds")

    '''
    For this section, I think my IP is blocked

        folder = './csvs/ModernHealtcare/'

        start_time = time.time()

        genericExtraction= GenericArticleExtractor("https://www.modernhealthcare.com")
        URL_array = genericExtraction.extract_article_urls()
        print("Extracted URLs")
        print("Number of URLS"+ str(len(URL_array)))
        print(URL_array)
        print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        # fierce_cleaner = FierceCleaner(folder,"https://www.fiercehealthcare.com")
        # URL_array_df = fierce_cleaner.clean(URL_array)
        # URL_array_df.to_csv( folder + 'CheckingURLS.csv', index=False, encoding='utf-8')
        # print("!!!!STEP 2 COMPLETED!!!!")
        
        # extractor = WebsiteDataExtractor(URL_array_df)
        # new_df = extractor.process_df()
        # new_df.to_csv(folder + 'FinalCheckingURLS.csv', index=False, encoding='utf-8')
        # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        



        end_time=time.time()
        elapsed_time = end_time - start_time

        # Print the result
        print(f"Execution time: {elapsed_time:.2f} seconds")
    '''
#######################HealthcareDive######################

    domains=[('https://www.nytimes.com/section/business','https://www.nytimes.com'),
             ('https://www.cnn.com/business','https://www.cnn.com'),
             ('https://www.foxbusiness.com/','https://www.foxbusiness.com'),
             ('https://www.fiercehealthcare.com/','https://www.fiercehealthcare.com'),
             ('https://www.healthcaredive.com/','https://www.healthcaredive.com'),
             ('https://www.modernhealthcare.com/','https://www.modernhealthcare.com')]    

    folder = './csvs/CNN/'

    index=1

    extractionURL, domainURL = domains[index]

    start_time = time.time()


    print("!!!!!!!!!!! Starting STEP 1 !!!!!!!!!!!!!!!!!!")
    genericExtraction= GenericArticleExtractor(extractionURL)
    URL_array = genericExtraction.extract_article_urls()
    # print("Extracted URLs")
    # print("Number of URLS"+ str(len(URL_array)))
    # print(URL_array)
    # URL_array.to_csv( folder + 'InitialHref.csv', index=False, encoding='utf-8')
    print("!!!!!!!!!!!!!!!!!STEP 1 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    print("!!!!!!!!!!! Starting STEP 2 !!!!!!!!!!!!!!!!!!")

    hcd_cleaner = GenericCleaner(folder,domainURL)
    URL_array_df = hcd_cleaner.clean(URL_array)
    URL_array_df.to_csv( folder + 'CheckingUrlsAfterCleaning.csv', index=False, encoding='utf-8')
    print("!!!!STEP 2 COMPLETED!!!!")
    

    ########### DEFINING THE JSON OBJECT ################
 
    


#     URLS_TO_EXTRACT=["https://www.foodbusinessnews.net/articles/26339-vital-farms-expanding-footprint-to-indiana",
# "https://www.qsrmagazine.com/story/100k-incentive-spurs-qdobas-franchise-expansion-amid-economic-pressures/",
# "https://www.restaurantbusinessonline.com/technology/mad-mobile-maker-cake-pos-lands-50m-funding",
# "https://www.qsrmagazine.com/story/popeyes-and-tim-hortons-parent-unveils-45m-investment-to-build-in-china/",
# "https://www.foodbusinessnews.net/articles/26386-house-of-raeford-acquiring-tyson-foods-poultry-plant",
# "https://www.healthcaredive.com/news/walmart-health-shut-down/714671/",
# "https://www.informationweek.com/it-infrastructure/cognizant-to-acquire-belcan-in-1-3b-deal-to-boost-r-d",
# "https://www.computerworld.com/article/2515643/sai-group-buys-get-well-aims-to-use-ai-for-better-patient-engagement.html",
# "https://www.geekwire.com/2024/levelten-lands-65m-to-expand-its-clean-energy-marketplaces-services-and-geographic-reach/",
# "https://techcrunch.com/2024/07/17/deepfake-detecting-firm-pindrop-lands-100m-loan-to-grow-its-offerings/"]
    

#     URL_array_df = pd.DataFrame(URLS_TO_EXTRACT, columns=['URL'])

    articles_json = {

        'id' : index,
        'url' : extractionURL,
        'count_of_articles' : len(URL_array_df),
        'articles' : []

    }

    print("!!!!!!!!!!! Starting STEP 3 !!!!!!!!!!!!!!!!!!")

    extractor = WebsiteDataExtractor(URL_array_df[:20])
    new_df = extractor.process_df()
    new_df.to_csv(folder + 'FinalCheckingURLS.csv', index=False, encoding='utf-8')
    print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    ######### Adding articles to the parent JSON #############
    for index, row in new_df.iterrows():
        article = {
            'id': index+1,
            'title': row['Title'],
            'article': row['Main Text'],
            'date': row['Date In Article'],
            'URL': row['URL']
        }
        articles_json['articles'].append(article)
    

    json_string = json.dumps(articles_json, indent=2)
    print(json_string)

    # file_path=
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, 'articles.txt')


    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_string)

    
    end_time=time.time()
    elapsed_time = end_time - start_time

    # Print the result
    print(f"Execution time: {elapsed_time:.2f} seconds")