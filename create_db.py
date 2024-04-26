import asyncio

from database.models import create_tables, drop_tables

if __name__ == "__main__":
    asyncio.run(create_tables())

# if __name__ == "__main__":
#     asyncio.run(drop_tables())