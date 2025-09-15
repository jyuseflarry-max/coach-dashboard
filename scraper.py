import requests
from bs4 import BeautifulSoup
import json

# --- CONFIGURATION ---
# 1. Paste your API key from ScraperAPI here
API_KEY = '1c8e2eca7f716bef87f042756e8b2f64' 

# 2. Add all the team URLs you want to track
urls_to_track = [
    "https://www.maxpreps.com/ia/solon/solon-spartans/basketball/girls/schedule/"
]

# --- SCRIPT LOGIC ---
teams_data = []

for target_url in urls_to_track:
    # Construct the special URL for the ScraperAPI service
    scraperapi_url = f'http://api.scraperapi.com?api_key={'1c8e2eca7f716bef87f042756e8b2f64'}&url={"https://www.maxpreps.com/ia/solon/solon-spartans/basketball/girls/schedule/"}'
    
    print(f"Scraping {target_url}...")
    
    try:
        # The request now goes to ScraperAPI instead of MaxPreps directly
        response = requests.get(scraperapi_url, timeout=60) # Increased timeout for the API
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        team_name_element = soup.find('h1', attrs={'data-testid': 'page-title'})
        team_name = team_name_element.text.strip() if team_name_element else "Team Name Not Found"
        if 'Basketball' in team_name:
            team_name = team_name.split('Basketball')[0].strip()

        record_div = soup.find('div', attrs={'data-testid': 'overall-record'})
        record = record_div.text.strip() if record_div else "Record Not Found"

        if "Not Found" in team_name or "Not Found" in record:
             raise Exception("Failed to find team data on the page.")

        team_info = {
            'teamName': team_name,
            'record': record,
            'sourceUrl': target_url
        }
        teams_data.append(team_info)
        print(f"  > Success: Found {team_name} ({record})")

    except requests.exceptions.RequestException as e:
        print(f"  > Error: Could not fetch URL. {e}")
    except Exception as e:
        print(f"  > Error: Could not parse page. {e}")

with open('data.json', 'w') as f:
    json.dump(teams_data, f, indent=4)

print("\nScraping complete. Data saved to data.json")