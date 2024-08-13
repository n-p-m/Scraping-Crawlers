import json
import pandas as pd
import csv

def read_json(file_path):
    with open(file_path, 'r') as jsonfile:
        return json.load(jsonfile)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as jsonfile:
        json_str = jsonfile.read()
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"First 100 characters of the file: {json_str[:100]}")
        raise

def compare_data(json_data, csv_data):
    mismatches = []

    for id, entry in json_data.items():
        json_name = entry.get('Name', '')
        json_org = entry.get('Organization', '')
        
        # Find matching row in CSV data
        csv_row = next((row for row in csv_data 
                        if f"{row.get('First name', '')}|{row.get('Last name', '')}" == json_name 
                        and row.get('employment_organization', '') == json_org), None)
        
        if csv_row is None:
            mismatches.append({
                'JSON_ID': id,
                'JSON_Name': json_name,
                'JSON_Organization': json_org,
                'Mismatch_Type': 'No matching entry in CSV'
            })
        else:
            csv_id = csv_row.get('id', '')
            if id != csv_id:
                mismatches.append({
                    'JSON_ID': id,
                    'CSV_ID': csv_id,
                    'Name': json_name,
                    'Organization': json_org,
                    'Mismatch_Type': 'ID mismatch'
                })

    # Check for entries in CSV that are not in JSON
    for row in csv_data:
        csv_name = f"{row.get('First name', '')}|{row.get('Last name', '')}"
        csv_org = row.get('employment_organization', '')
        csv_id = row.get('id', '')

        if not any(entry.get('Name') == csv_name and entry.get('Organization') == csv_org for entry in json_data.values()):
            mismatches.append({
                'CSV_ID': csv_id,
                'CSV_Name': csv_name,
                'CSV_Organization': csv_org,
                'Mismatch_Type': 'No matching entry in JSON'
            })

    return mismatches

# Main execution
json_file_path = 'Checkingindex.py'
csv_file_path = 'forbes_2024_full_list.csv'

# Read JSON data
json_data = read_json(json_file_path)

# Read CSV data
csv_data = read_csv(csv_file_path)

# Compare data
mismatches = compare_data(json_data, csv_data)

# Print mismatches
if mismatches:
    print("Mismatches found:")
    for mismatch in mismatches:
        print(mismatch)
else:
    print("No mismatches found.")

# Optionally, save mismatches to a CSV file
if mismatches:
    mismatches_df = pd.DataFrame(mismatches)
    mismatches_df.to_csv('mismatches.csv', index=False)
    print("Mismatches saved to 'mismatches.csv'")