import pandas as pd
import requests
from urllib.parse import quote
from tqdm import tqdm

# Load your Excel file
df = pd.read_excel("/Users/Jasmin.Nihalani/Desktop/imdb_records.xlsx")

# Define the query function
def get_wikipedia_url(title, year):
    query = f"{title} {year}"
    encoded_query = quote(query)
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&formatversion=2&srsearch={encoded_query}"

    try:
        response = requests.get(api_url)
        data = response.json()
        results = data.get("query", {}).get("search", [])

        for result in results:
            snippet = result.get("snippet", "").lower()
            if "film" in snippet and any(kw in snippet for kw in ["hindi", "indian", "bollywood"]):
                page_title = result["title"]
                wiki_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                return wiki_url

        return None
    except Exception as e:
        print(f"Error processing '{title}' ({year}): {e}")
        return None

# Apply with tqdm progress bar
tqdm.pandas()
df["wikipedia_url"] = df.progress_apply(lambda row: get_wikipedia_url(row["title"], row["year"]), axis=1)

# Save output
df.to_csv("/Users/Jasmin.Nihalani/Desktop/imdb_with_wiki_urls.csv", index=False)
print("✅ Done! File saved to Desktop")
