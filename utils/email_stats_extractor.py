from bs4 import BeautifulSoup
import re

def extract_email_stats(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    stats = {}
    
    sequence_name_element = soup.find('h3', class_='preview_subject')
    if sequence_name_element:
        stats['sequence_name'] = sequence_name_element.get_text(strip=True)
    
    all_report_stats = soup.find_all('div', class_='report-stat')
    
    for stat_div in all_report_stats:
        text = stat_div.get_text(strip=True)
        if 'Sends' in text:
            number = re.search(r'(\d[\d,]*)', text)
            if number:
                stats['total_sent'] = int(number.group(1).replace(',', ''))
        elif 'Open Rate' in text:
            number = re.search(r'([\d.]+)%', text)
            if number:
                stats['open_rate'] = float(number.group(1))
        elif 'Click Rate' in text:
            number = re.search(r'([\d.]+)%', text)
            if number:
                stats['click_rate'] = float(number.group(1))
    
    small_stats = soup.find_all('div', class_='report-stat--small')
    for stat_div in small_stats:
        text = stat_div.get_text(strip=True)
        if 'Unsubscribes' in text:
            number = re.search(r'(\d+)', text)
            if number:
                stats['unsubscribes'] = int(number.group(1))
    
    return stats