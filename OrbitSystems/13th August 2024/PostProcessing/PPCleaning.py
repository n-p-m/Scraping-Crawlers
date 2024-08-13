# import json
# import itertools

# def has_word_before_pipe(name):
#     parts = name.split("|")
#     return len(parts) > 1 and parts[0].strip() != ""

# def is_valid_title(title):
#     invalid_titles = [
#         "Just a moment...",
#         "Access to this page has been denied",
#         "Access Denied"
#     ]
#     return title not in invalid_titles

# try:
#     # Parse the JSON data
#     with open('updated_json_file.json', 'r') as file:
#         data = json.load(file)
    
#     print(f"Successfully loaded JSON data. Total entries: {len(data)}")

#     # Dictionaries to store the separated data
#     null_date_data = {}
#     company_data = {}
#     valid_data = {}
#     title_error_data = {}

#     # Counters
#     null_date_count = 0
#     company_count = 0
#     invalid_title_count = 0

#     # Iterate through each entry
#     for key, entry in itertools.islice(data.items(), len(data)):
#         if 'articles' not in entry:
#             print(f"Warning: 'articles' key not found in entry {key}")
#             continue
        
#         if 'Name' not in entry:
#             print(f"Warning: 'Name' key not found in entry {key}")
#             continue

#         null_articles = []
#         non_null_articles = []
        
#         for article in entry['articles']:
#             if 'date' not in article:
#                 print(f"Warning: 'date' key not found in article for entry {key}")
#                 continue
            
#             if article["date"] is None or article["date"] == "FAILED":
#                 null_articles.append(article)
#                 null_date_count += 1
#             else:
#                 non_null_articles.append(article)

#         # Step 1: Save entries with null dates
#         if null_articles:
#             null_date_data[key] = entry.copy()
#             null_date_data[key]['articles'] = null_articles

#         # Proceed with entries that have non-null dates
#         if non_null_articles:
#             # Step 2: Check if there's a word before "|" in the Name field
#             if has_word_before_pipe(entry['Name']):
#                 valid_articles = []
#                 invalid_articles = []
#                 for article in non_null_articles:
#                     if 'title' in article and is_valid_title(article['title']):
#                         valid_articles.append(article)
#                     else:
#                         invalid_articles.append(article)
#                         invalid_title_count += 1
                
#                 if valid_articles:
#                     valid_data[key] = entry.copy()
#                     valid_data[key]['articles'] = valid_articles
                
#                 if invalid_articles:
#                     title_error_data[key] = entry.copy()
#                     title_error_data[key]['articles'] = invalid_articles
#             else:
#                 company_data[key] = entry.copy()
#                 company_data[key]['articles'] = non_null_articles
#                 company_count += 1

#     print(f"Number of articles with null dates: {null_date_count}")
#     print(f"Number of entries categorized as companies: {company_count}")
#     print(f"Number of articles removed due to invalid titles: {invalid_title_count}")
#     print(f"Entries in null_date_data: {len(null_date_data)}")
#     print(f"Entries in company_data: {len(company_data)}")
#     print(f"Entries in valid_data: {len(valid_data)}")
#     print(f"Entries in title_error_data: {len(title_error_data)}")

#     # Save the results to files
#     with open('Step_1_null_date_data.json', 'w') as f:
#         json.dump(null_date_data, f, indent=2)
#     print("Saved Step_1_null_date_data.json")

#     with open('Step_2_company_data.json', 'w') as f:
#         json.dump(company_data, f, indent=2)
#     print("Saved Step_2_company_data.json")

#     with open('Step_3_valid_data.json', 'w') as f:
#         json.dump(valid_data, f, indent=2)
#     print("Saved Step_3_valid_data.json")

#     with open('STEP_3_title_error.json', 'w') as f:
#         json.dump(title_error_data, f, indent=2)
#     print("Saved STEP_3_title_error.json")

# except json.JSONDecodeError as e:
#     print(f"Error decoding JSON: {e}")
# except FileNotFoundError:
#     print("Error: 'Forbes_POI.json' file not found")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")




import json
import itertools

def has_word_before_pipe(name):
    parts = name.split("|")
    return len(parts) > 1 and parts[0].strip() != ""

def is_valid_title(title):
    invalid_titles = [
        "Just a moment...",
        "Access to this page has been denied",
        "Access Denied"
    ]
    return title not in invalid_titles

try:
    # Parse the JSON data
    with open('updated_json_file.json', 'r') as file:
        data = json.load(file)
    
    print(f"Successfully loaded JSON data. Total entries: {len(data)}")

    # Dictionaries to store the separated data
    null_date_data = {}
    company_data = {}
    valid_data = {}
    title_error_data = {}

    # Counters
    null_date_count = 0
    company_count = 0
    invalid_title_count = 0

    # Iterate through each entry
    for key, entry in itertools.islice(data.items(), len(data)):
        if 'articles' not in entry:
            print(f"Warning: 'articles' key not found in entry {key}")
            continue
        
        if 'Name' not in entry:
            print(f"Warning: 'Name' key not found in entry {key}")
            continue

        null_articles = []
        non_null_articles = []
        
        for article in entry['articles']:
            if 'date' not in article:
                print(f"Warning: 'date' key not found in article for entry {key}")
                continue
            
            if article["date"] is None or article["date"] == "FAILED":
                null_articles.append(article)
                null_date_count += 1
            else:
                non_null_articles.append(article)

        # Step 1: Save entries with null dates
        if null_articles:
            null_date_data[key] = entry.copy()
            null_date_data[key]['articles'] = null_articles

        # Proceed with entries that have non-null dates
        if non_null_articles:
            # Step 2: Apply title filter
            valid_articles = []
            invalid_articles = []
            for article in non_null_articles:
                if 'title' in article and is_valid_title(article['title']):
                    valid_articles.append(article)
                else:
                    invalid_articles.append(article)
                    invalid_title_count += 1
            
            # Step 3: Check if there's a word before "|" in the Name field
            if has_word_before_pipe(entry['Name']):
                if valid_articles:
                    valid_data[key] = entry.copy()
                    valid_data[key]['articles'] = valid_articles
                
                if invalid_articles:
                    title_error_data[key] = entry.copy()
                    title_error_data[key]['articles'] = invalid_articles
            else:
                if valid_articles:
                    company_data[key] = entry.copy()
                    company_data[key]['articles'] = valid_articles
                    company_count += 1
                
                if invalid_articles:
                    title_error_data[key] = entry.copy()
                    title_error_data[key]['articles'] = invalid_articles

    print(f"Number of articles with null dates: {null_date_count}")
    print(f"Number of entries categorized as companies: {company_count}")
    print(f"Number of articles removed due to invalid titles: {invalid_title_count}")
    print(f"Entries in null_date_data: {len(null_date_data)}")
    print(f"Entries in company_data: {len(company_data)}")
    print(f"Entries in valid_data: {len(valid_data)}")
    print(f"Entries in title_error_data: {len(title_error_data)}")

    # Save the results to files
    with open('Step_1_null_date_data.json', 'w') as f:
        json.dump(null_date_data, f, indent=2)
    print("Saved Step_1_null_date_data.json")

    with open('Step_2_title_error.json', 'w') as f:
        json.dump(title_error_data, f, indent=2)
    print("Saved Step_2_title_error.json")

    with open('Step_3_company_data.json', 'w') as f:
        json.dump(company_data, f, indent=2)
    print("Saved Step_3_company_data.json")

    with open('Step_3_valid_data.json', 'w') as f:
        json.dump(valid_data, f, indent=2)
    print("Saved Step_3_valid_data.json")

except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except FileNotFoundError:
    print("Error: 'updated_json_file.json' file not found")
except Exception as e:
    print(f"An unexpected error occurred: {e}")