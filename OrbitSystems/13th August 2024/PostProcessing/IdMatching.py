import csv
import json

# Step 1: Read CSV and create mapping
id_mapping = {}
with open('forbes_2024_full_list.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        first_name = row['first_name'] if row['first_name'] != 'null'  else ''
        last_name = row['last_name'] if row['last_name']!='null' else ''
        full_name = f"{first_name}|{last_name}"
        org = row['employment_organization'] if row['employment_organization']!='null'  else ''
        new_id = row['id']  # Assuming the CSV has an 'id' column
        id_mapping[(full_name, org)] = new_id

# Step 2: Read JSON
with open('combined_forbes.json', 'r') as json_file:
    data = json.load(json_file)

# Step 3: Update JSON with new IDs
updated_data = {}
no_match_messages = []

for csv_name_org, new_id in id_mapping.items():
    csv_name, csv_org = csv_name_org
    
    # Find matching entry in JSON
    for old_id, entry in data.items():
        json_name = entry['Name']
        json_org = entry['Organization']
        
        # if json_name == csv_name and json_org == csv_org:
        if json_name == csv_name:

            # Update the entry's ID
            entry['id'] = int(new_id)
            
            # Add to updated data with new ID as key
            updated_data[new_id] = entry
            break
    else:
        no_match_messages.append(f"No match found in JSON for Name: '{csv_name}', Organization: '{csv_org}'")

# Step 4: Write updated JSON back to file
with open('updated_json_file.json', 'w') as json_file:
    json.dump(updated_data, json_file, indent=2)

with open('not_extracted_during_scraping.txt', 'w') as txt_file:
    for message in no_match_messages:
        txt_file.write(message + '\n')

print("JSON file has been updated with new IDs.")