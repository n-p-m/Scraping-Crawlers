import json

# Load the first JSON file
with open('Forbes_POI.json', 'r') as f:
    poi_data = json.load(f)

# Find the highest ID in the first JSON
highest_id = max(int(key) for key in poi_data.keys())

# Load the second JSON file
with open('Forbes_U30_Json', 'r') as f:
    u30_data = json.load(f)

# Combine the data
for key, value in u30_data.items():
    highest_id += 1
    new_key = str(highest_id)
    value['id'] = highest_id
    poi_data[new_key] = value

# Save the combined data to a new JSON file
with open('combined_forbes.json', 'w') as f:
    json.dump(poi_data, f, indent=2)

print("Combined JSON file created successfully!")