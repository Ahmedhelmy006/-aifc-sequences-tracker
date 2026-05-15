from bs4 import BeautifulSoup
from datetime import datetime
import re, time, requests, os
from dotenv import load_dotenv

load_dotenv()

def parse_unsubscribe_date(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Search for an <em> tag containing either "Unsubscribed" or "Complained"
    em = soup.find('em', string=re.compile(r'Unsubscribed|Complained', re.I))
    if not em:
        return None
    
    row = em.find_parent('tr')
    all_nowrap_tds = row.find_all('td', class_='nowrap')
    
    if not all_nowrap_tds:
        return None

    # 2. Logic to pick the correct column
    # If it's a complaint, you mentioned the "Opened" date (usually the first nowrap td)
    # If it's an unsubscribe, your original logic used the last nowrap td
    if "Complained" in em.get_text():
        date_td = all_nowrap_tds[0] 
    else:
        date_td = all_nowrap_tds[-1]

    date_span = date_td.find('span', title=True)
    if not date_span:
        return None
    
    # 3. Clean the title string
    # We remove 'Opened ', timezones, and normalize am/pm for strptime
    title = date_span['title']
    title = title.replace('Opened ', '')
    title = title.replace(' EST', '').replace(' EDT', '')
    title = title.replace('am', 'AM').replace('pm', 'PM').strip()
    
    try:
        return datetime.strptime(title, "%b %d, %Y at %I:%M%p")
    except ValueError:
        # Fallback if the format varies slightly
        return None
    
def trigger_webhook():
    print("Sleeping 120 seconds before triggering webhook...")
    try:
        response = requests.post(
            os.getenv("WEBHOOK_URL"),
            json={
                "event": "supabase_insert_complete",
                "table": "kit_subscribers",
                "status": "success"
            }
        )
        response.raise_for_status()
        print(f"Webhook triggered successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger webhook. Error: {e}")