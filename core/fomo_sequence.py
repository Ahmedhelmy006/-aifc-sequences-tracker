import pandas as pd
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

from config.settings import *
from core.email_stats_fetcher import fetch_email_stats
from utils.spreadsheet_submitter import GoogleSheetsSubmitter # Adjusted name to class

load_dotenv()

async def fomo_main():
    targets = [
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_1_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_2_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_3_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_4_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_5_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_6_ID),
        (FOMO_SEQUENCE_ID, FOMO_SEQUENCE_EMAIL_7_ID),

    ]
    
    tasks = [fetch_email_stats(seq_id, email_id) for seq_id, email_id in targets]
    results = await asyncio.gather(*tasks)
    
    mapping = {
        'masterclass replay [expires in 48 hours]': 'Email 1',
        'Your advantage is here': 'Email 2',
        'Your $8,594 bonus expires in 48 hours': 'Email 3',
        'Traditional CFO or AI CFO (you choose)': 'Email 4',
        'This is your last day to become an AI CFO': 'Email 5',
        '⌛ The AI window is open, but only for 6 more hours': 'Email 6',
        "Your final chance to become an AI CFO - 180 minutes left": 'Email 7'
    }

    processed_rows = []
    current_date = datetime.today().strftime('%d/%m/%y')

    for res in results:
        if not res: continue
        
        email_num = mapping.get(res['sequence_name'], "Unknown")
        total_opens = round((res['open_rate'] / 100) * res['total_sent'])/100
        total_clicked = round((res['click_rate'] / 100) * res['total_sent'])/100

        processed_rows.extend([
            {"Metric": f"{email_num} Name", current_date: res['sequence_name']},
            {"Metric": f"{email_num} Total Sends", current_date: res['total_sent']},
            {"Metric": f"{email_num} Open Rate", current_date: f"{res['open_rate']}%"},
            {"Metric": f"{email_num} Click Rate", current_date: f"{res['click_rate']}%"},
            {"Metric": f"{email_num} Unsubscribes", current_date: res['unsubscribes']},
            {"Metric": f"{email_num} Total Opens", current_date: total_opens},
            {"Metric": f"{email_num} Total Clicked", current_date: total_clicked},
            {"Metric": " ", current_date: " "} 
        ])

    final_df = pd.DataFrame(processed_rows).set_index("Metric")

    
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(creds_path, scopes=scopes)

    submitter = GoogleSheetsSubmitter(credentials, os.getenv("GOOGLE_SPREADSHEET_ID"), "FOMO Sequence")
    submitter.write_stats_as_column(final_df)
    
    return final_df

