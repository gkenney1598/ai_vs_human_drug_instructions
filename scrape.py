import requests
import xml.etree.ElementTree as ET

API_URL = "https://wsearch.nlm.nih.gov/ws/query"

params = {
    "db": "drugs",  # tell API we want drug database
    "term": "all"   # return all results
}

# Request data from API
response = requests.get(API_URL, params=params)
xml_content = response.text

# Parse XML
root = ET.fromstring(xml_content)

drug_entries = []

# Loop through all <document> elements
for doc in root.findall("document"):
    name = doc.findtext("name")
    url = doc.findtext("url")

    if url:
        drug_entries.append({
            "name": name,
            "url": url
        })

print("✅ Found", len(drug_entries), "drug entries.")
print("Example:", drug_entries[:5])
