import requests
from config.settings import REQUESTS_HEADERS
import pandas as pd
import os
from dotenv import load_dotenv
from utils.helpers import get_unsubscribe_date

load_dotenv()

class RetrieveSequenceUnsubscribers:
    def __init__(self, sequence_id):
        self.sequence_id = sequence_id
        self.base_url = f"https://app.kit.com/internal/sequences/{sequence_id}/subscriptions"
        self.dataframe = pd.DataFrame()
        self.has_next_page = True
        self.start_cursor = None
        self.end_cursor = None


def get_subscribers_fields(subscriber_id):
    """
    ARGS: subscriber_id
    Returns All tags for a subscriber. Pretty simple, huh?
    """
    url = "https://app.kit.com" + f"/subscribers/{subscriber_id}"
    headers = {
            'Accept': 'application/json',
    }

    response = requests.get(url = url, headers = REQUESTS_HEADERS)

    with open("response.txt", "w", encoding="utf-8") as f:        
        f.write(response.text)

    return  get_unsubscribe_date(response.text)

print(get_subscribers_fields(3907157729))