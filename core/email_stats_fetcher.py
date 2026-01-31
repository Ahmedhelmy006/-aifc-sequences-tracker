import aiohttp
import asyncio
from utils.logger import *
from config.settings import REQUESTS_HEADERS
from utils.email_stats_extractor import extract_email_stats
logger = initialize_logger("stats_fetcher")

async def fetch_email_stats(sequence_id, email_id):
    url = f"https://app.kit.com/sequences/{sequence_id}/reports/{email_id}"
    async with aiohttp.ClientSession(headers=REQUESTS_HEADERS) as session:
        async with session.get(url) as response:
            try:
                logger.info(f"Fetching Sequence: {sequence_id}, Email: {email_id}")
                html = await response.text()
                if response.status == 200:
                    logger.info(f"SUCCESS: Retrieved email: {email_id} from sequence: {sequence_id}. Status Code: {response.status}")
                    return extract_email_stats(html)
            except ConnectionError as e:
                logger.error(f"Connection Failed. Error: {e}")
            
            
if __name__ == "__main__":
    print(asyncio.run(fetch_email_stats(2610101, 9348296)))
