import time
import pandas as pd
# Importing files
from LinkExtractorModule import *
from CleaningModule import *
from ContentExtractorModule import WebsiteDataExtractor
import json
from logging_config import logger




if __name__ == "__main__":

    domains=[('https://www.nytimes.com/section/business','https://www.nytimes.com', 'nytimes'),
             ('https://www.cnn.com/business','https://www.cnn.com', 'cnn'),
             ('https://www.foxbusiness.com/','https://www.foxbusiness.com', 'foxbusiness'),
             ('https://www.fiercehealthcare.com/','https://www.fiercehealthcare.com', 'fiercehealthcare'),
             ('https://www.healthcaredive.com/','https://www.healthcaredive.com', 'healthcaredive'),
             ('https://www.modernhealthcare.com/','https://www.modernhealthcare.com', 'modernhealthcare'),]    

    folder = './testing/'

    index=0

    extractionURL, domainURL, domainName = domains[index]

    start_time = time.time()


    # print("!!!!!!!!!!! Starting STEP 1 !!!!!!!!!!!!!!!!!!")


    genericExtraction= GenericArticleExtractor(extractionURL)
    genericExtraction.logger.info("STARTING STEP 1")
    URL_array = genericExtraction.extract_article_urls()
    genericExtraction.logger.info("STEP 1 COMPLETED")

    # print("Extracted URLs")
    # print("Number of URLS"+ str(len(URL_array)))
    # print(URL_array)
    # URL_array.to_csv( folder + 'InitialHref.csv', index=False, encoding='utf-8')


    hcd_cleaner = GenericCleaner(folder, domainURL)
    hcd_cleaner.logger.info("Starting STEP 2")
    URL_array_df = hcd_cleaner.clean(URL_array)
    hcd_cleaner.logger.info("STEP 2 COMPLETED")
    # print(URL_array_df.to_csv(folder + 'CleanedURLS.csv', index=False, encoding='utf-8'))

    articles_json = {

        'id' : index,
        'url' : extractionURL,
        'count_of_articles' : len(URL_array_df),
        'articles' : []

    }

    # print("!!!!!!!!!!! Starting STEP 3 !!!!!!!!!!!!!!!!!!")

    extractor = WebsiteDataExtractor(URL_array_df)
    extractor.logger.info("Starting STEP 3")
    new_df, status_df = extractor.process_df()
    extractor.logger.info("STEP 3 COMPLETED")
    # print(new_df)
    # print("!!!!!!!!status below")
    # print(status_df)
    # # new_df.to_csv(folder + 'FinalCheckingURLS.csv', index=False, encoding='utf-8')
    # # print("!!!!!!!!!!!!!!!!!STEP 3 COMPLETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    ######### Adding articles to the parent JSON #############
    for index, row in new_df.iterrows():
        article = {
            'id': index,
            'title': row['Title'],
            'article': row['Main Text'],
            'date': row['Date In Article'],
            'URL': row['URL']
        }
        # logger.info(f"Adding articles to the JSON")
        articles_json['articles'].append(article)
        
    logger.info(f"Added articles to the JSON")
    

    json_string = json.dumps(articles_json, indent=2)
    # print(json_string)
    logger.info("Writing the JSON object to JSON file")
    # file_path=
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f'{domainName}_articles.json')


    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_string)

    logger.info("JSON object written to JSON file")
    
    end_time=time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Execution time: {elapsed_time:.2f} seconds")
    # Print the result
    # print(f"Execution time: {elapsed_time:.2f} seconds")

    logger.info("Process completed successfully")



    
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
