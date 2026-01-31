import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd

load_dotenv()

class GoogleSheetsSubmitter:
    def __init__(self, credentials, spreadsheet_id, tab_name):
        self.credentials = credentials
        self.spreadsheet_id = spreadsheet_id
        self.tab_name = tab_name

    def write_stats_as_column(self, df):
        """
        Writes the DataFrame to the next available column in Google Sheets.
        """
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet = service.spreadsheets()

        header_range = f"{self.tab_name}!A1:Z1"
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id, 
            range=header_range
        ).execute()
        
        existing_headers = result.get('values', [[]])[0]
        next_col_index = len(existing_headers) + 1
        
        col_letter = chr(64 + next_col_index) 

        date_header = df.columns[0]
        column_values = [date_header] + df[date_header].tolist()
        
        values_to_write = [[val] for val in column_values]
        range_to_write = f"{self.tab_name}!{col_letter}1"

        sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_to_write,
            valueInputOption="USER_ENTERED",
            body={"values": values_to_write}
        ).execute()

        print(f"[INFO] Stats for {date_header} successfully written to Column {col_letter}.")