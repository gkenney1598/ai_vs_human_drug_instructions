import requests
from bs4 import BeautifulSoup

base = "https://medlineplus.gov/druginfo/meds/"
headers = {"User-Agent": "Mozilla/5.0"}

drug_texts = []

keys = ["a606008", "a601105"]

for key in keys:
    url = base + key + ".html"
    print("Scraping:", url)

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Failed:", key)
        continue

    soup = BeautifulSoup(r.text, "html.parser")

    # main content block
    container = soup.find("article")
    if not container:
        continue

    text = ""

    paragraphs = [p.get_text(" ", strip=True) for p in container.find_all("div", "section-body")] #go by section body not by paragraph
    header = [h.get_text(" ", strip=True) for h in container.find_all("div", "section-title")]
    for i in range(len(header)):
        text += header[i] + "\n"
        text += paragraphs[i] + "\n"

    drug_texts.append({
        "key": key,
        "url": url,
        "text": text
    })

print("\n Scraped", print(drug_texts), "drugs.")
