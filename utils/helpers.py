from bs4 import BeautifulSoup
from datetime import datetime

def parse_unsubscribe_date(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    em = soup.find('em', string=lambda t: t and 'Unsubscribed on' in t)
    if not em:
        return None
    
    row = em.find_parent('tr')
    # get the LAST td with class nowrap (the date column, not the first one)
    date_td = row.find_all('td', class_='nowrap')[-1]
    date_span = date_td.find('span', title=True)
    if not date_span:
        return None
    title = date_span['title'].replace(' EST', '').replace(' EDT', '').replace('am', 'AM').replace('pm', 'PM')
    return datetime.strptime(title, "%b %d, %Y at %I:%M%p")
    #return datetime.strptime(date_span['title'], "%b %d, %Y at %I:%M%p %Z")