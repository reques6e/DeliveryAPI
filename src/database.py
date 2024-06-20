import aiosqlite


class DataBase:
    def __init__(self) -> None:
        self.db_path = 'db.db'

    async def table_create(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS info (
                    name TEXT,
                    description TEXT,
                    logo TEXT
                )
            ''')
            await db.commit()

    async def get_description_info(self) -> str:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT description FROM info LIMIT 1
            ''')
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None