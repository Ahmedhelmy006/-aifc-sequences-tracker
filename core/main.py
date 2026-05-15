import sys
import asyncio
from config.settings import *
from core.approved_sequences import approved_main
from core.fomo_sequence import fomo_main
from core.retrieve_unsubscribers import RetrieveSequenceUnsubscribers
from utils.helpers import trigger_webhook

async def unsubscribers_main(mode: str):
    if mode == 'approved':
        for k, v in approved_sequences_unsubs_tabs.items():
            handler = RetrieveSequenceUnsubscribers(
                sequence_id=k, 
                destination_tab=v
            )
            
            await handler.plan_sequence_scraping()
            handler.submit_to_spreadsheets()
        trigger_webhook()
    elif mode == 'fomo':
        handler = RetrieveSequenceUnsubscribers(
            sequence_id=2612710, 
            destination_tab="Unsubscribers: FOMO"
        )
        
        await handler.plan_sequence_scraping()
        handler.submit_to_spreadsheets()
    else:
        print("No Sequence Found with such name. Please check your spillings.")

async def run():
    if len(sys.argv) < 2:
        print("Usage: python -m core.main [approved|fomo]")
        return

    mode = sys.argv[1].lower()
    if mode == "approved":
        await approved_main()
        await unsubscribers_main(mode)

    elif mode == "fomo":
        await fomo_main()
        await unsubscribers_main(mode)

    else:
        print(f"Unknown mode: {mode}")

if __name__ == "__main__":
    asyncio.run(run())