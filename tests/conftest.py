import asyncio
import sys

# This setting will apply to all tests automatically
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
