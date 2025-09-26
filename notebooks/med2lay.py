import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

def get_medlineplus_definition(term):
    """Fetch a clean layman-friendly definition from MedlinePlus."""
    url = f"https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term={term}"
    response = requests.get(url)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    for doc in root.findall(".//document"):
        summary = doc.findtext("content[@name='FullSummary']")
        if summary:
            clean_text = BeautifulSoup(summary, "html.parser").get_text(" ", strip=True)
            # Limit to first 2 sentences for readability
            sentences = clean_text.split(".")
            return ".".join(sentences[:2]).strip()
    return None

# Load your existing short dictionary
with open("med2lay.json", "r") as f:
    med2lay = json.load(f)

# Add "detailed" definitions from MedlinePlus
for term in med2lay.keys():
    detailed = get_medlineplus_definition(term)
    if detailed:
        med2lay[term]["detailed"] = detailed
    else:
        med2lay[term]["detailed"] = med2lay[term]["short"]  # fallback

# Save updated dictionary
with open("med2lay.json", "w") as f:
    json.dump(med2lay, f, indent=2)

print("Updated med2lay.json with detailed definitions\n\n")

print("Here are the med to layman terms: ", med2lay)

print("Saved med2lay.json with", len(med2lay), "terms\n\n")

print(json.dumps(med2lay, indent=2))
