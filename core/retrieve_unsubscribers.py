from config.settings import REQUESTS_HEADERS
import pandas as pd
import os
from dotenv import load_dotenv
from utils.helpers import parse_unsubscribe_date
import asyncio, aiohttp
from utils.spreadsheet_submitter import GoogleSheetsSubmitter
from google.oauth2.service_account import Credentials

load_dotenv()

class RetrieveSequenceUnsubscribers:
    def __init__(self, sequence_id, destination_tab):
        self.sequence_id = sequence_id
        self.base_url = f"https://app.kit.com/internal/sequences/{sequence_id}/subscriptions?"
        self.params = f"state=cancelled&query=&include_total_count=true"
        self.headers = REQUESTS_HEADERS
        self.df = pd.DataFrame()
        self.tasks = []
        self.destination_tab = destination_tab


    async def get_unsubscriber_timestamp(self, session, subscriber_id):
            url = "https://app.kit.com" + f"/subscribers/{subscriber_id}"
            async with session.get(url = url, headers = self.headers) as response:
                html = await response.text()
                return parse_unsubscribe_date(html)

    async def plan_sequence_scraping(self):
            total_unsubs = None
            current_planning_cursor = None
            all_records = []
            async with aiohttp.ClientSession(headers=self.headers) as session:
                
                async def fire_initial_request(session):
                    async with session.get(url = self.base_url + self.params) as response:
                        data = await response.json()
                        pagination = data['pagination']
                        total_unsubs_val = pagination['total_count']
                        initial_fetch_cursor = pagination['end_cursor'] if pagination.get('has_next_page') else None
                        
                        records = data['records']
                        tasks = [self.get_unsubscriber_timestamp(session, r['subscriber']['id']) for r in records]
                        timestamps = await asyncio.gather(*tasks)

                        for record, ts in zip(records, timestamps):
                            if ts:
                                record['subscriber']['unsubscribed_at'] = ts.isoformat() if hasattr(ts, 'isoformat') else ts
                            else:
                                record['subscriber']['unsubscribed_at'] = None
                                
                            all_records.append(record)

                        return initial_fetch_cursor, total_unsubs_val
                
                current_planning_cursor, total_unsubs = await fire_initial_request(session)

                async def fetch_unsubscribers(session, active_cursor, records_list):
                    while active_cursor is not None:
                        async with session.get(url=self.base_url + f"after={active_cursor}&" + self.params) as response:
                            data = await response.json()
                            pagination = data['pagination']
                            
                            records = data['records']
                            tasks = [self.get_unsubscriber_timestamp(session, r['subscriber']['id']) for r in records]
                            timestamps = await asyncio.gather(*tasks)

                            for record, ts in zip(records, timestamps):
                                record['subscriber']['unsubscribed_at'] = ts
                                records_list.append(record)
                            
                            print(len(records_list))

                            active_cursor = pagination['end_cursor'] if pagination.get('has_next_page') else None
                            print(f"scraping cursor {active_cursor}")
                                        
                    self.df = pd.json_normalize(records_list, sep='_')
                    return self.df
                
                self.df = await fetch_unsubscribers(session, active_cursor=current_planning_cursor, records_list=all_records)
                
                if self.df.shape[0] == total_unsubs:
                    print(f"Successfully scraped {total_unsubs} records. The numbers reconcile. GJ!")
                return self.df
            

    def submit_to_spreadsheets(self):
        if self.df.empty:
            print("No data found to submit.")
            return

        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_file(creds_path, scopes=scopes)
        
        submitter = GoogleSheetsSubmitter(
            credentials= credentials,
            spreadsheet_id=os.getenv("GOOGLE_SPREADSHEET_ID"),
            tab_name=self.destination_tab
        )
        
        status = submitter.write_dataframe(self.df)
        if status == 200:
             print(f"Submitted to {self.destination_tab}!")

if __name__ == "__main__":
    handler = RetrieveSequenceUnsubscribers(2614399, destination_tab="Unsubscribers: Approved Email 4")
    asyncio.run(handler.plan_sequence_scraping())
    handler.submit_to_spreadsheets()


