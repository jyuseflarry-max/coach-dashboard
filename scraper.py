import requests
from bs4 import BeautifulSoup
import json

# The URL of the team we want to track
urls = [
    "https://www.maxpreps.com/ia/solon/solon-spartans/basketball/girls/schedule/"
]

# A list to hold the data for all teams
teams_data = []

# Headers to make our request look like it's coming from a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Loop through each URL in our list
for url in urls:
    try:
        # Download the HTML content of the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- NEW, MORE ROBUST DATA FINDING ---
        
        # Find the team name from the main heading (more stable)
        team_name_element = soup.find('h1', attrs={'data-testid': 'page-title'})
        # Check if we found the element before getting the text
        team_name = team_name_element.text.strip() if team_name_element else "Team Name Not Found"
        # Clean up the name a bit
        if 'Basketball' in team_name:
            team_name = team_name.split('Basketball')[0].strip()

        # Find the team record
        record_div = soup.find('div', attrs={'data-testid': 'overall-record'})
        # Check if we found the element before getting the text
        record = record_div.text.strip() if record_div else "Record Not Found"

        # Organize the data into a dictionary
        team_info = {
            'teamName': team_name,
            'record': record,
            'sourceUrl': url
        }
        
        # Add this team's data to our list
        teams_data.append(team_info)
        print(f"Successfully scraped data for {team_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
    except Exception as e: # A general catch for other parsing errors
        print(f"An error occurred while parsing {url}: {e}")

# Save the final list of data to a JSON file
with open('data.json', 'w') as f:
    json.dump(teams_data, f, indent=4)

print("\nScraping complete. Data saved to data.json")