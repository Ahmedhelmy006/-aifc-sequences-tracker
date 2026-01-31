import sys
import asyncio
from core.approved_sequences import approved_main
from core.fomo_sequence import fomo_main




async def run():
    if len(sys.argv) < 2:
        print("Usage: python -m core.main [approved|fomo]")
        return

    mode = sys.argv[1].lower()
    if mode == "approved":
        await approved_main()
    elif mode == "fomo":
        await fomo_main()
    else:
        print(f"Unknown mode: {mode}")

if __name__ == "__main__":
    asyncio.run(run())