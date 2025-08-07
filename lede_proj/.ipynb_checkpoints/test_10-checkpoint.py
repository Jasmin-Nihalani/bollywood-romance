import pandas as pd
import requests
from urllib.parse import quote

# Load your Excel file
df = pd.read_excel("/Users/Jasmin.Nihalani/Desktop/imdb_records.xlsx")

# Take only the first 10 films for testing
df_sample = df.head(10)

# Updated function with expanded keyword check
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

        return None  # No valid result
    except Exception as e:
        print(f"Error processing '{title}' ({year}): {e}")
        return None

# Apply the function to your sample
df_sample["wikipedia_url"] = df_sample.apply(lambda row: get_wikipedia_url(row["title"], row["year"]), axis=1)

# Save to CSV
df_sample.to_csv("/Users/Jasmin.Nihalani/Desktop/imdb_wiki_test_10.csv", index=False)
print("✅ Saved test results to imdb_wiki_test_10.csv on your Desktop")
