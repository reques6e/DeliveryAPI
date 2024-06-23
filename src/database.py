import aiosqlite

from typing import Optional, Union

from auth.models import UserStructure
from cities.models import CityStructure


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

            await db.execute('''
                CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    age INTEGER,
                    password TEXT,
                    admin INTEGER DEFAULT 0,
                    block INTEGER DEFAULT 0,
                    user_group TEXT,
                    city INTEGER,
                    address TEXT,
                    phone INTEGER,
                    reg_date INTEGER,
                    passport TEXT,
                    token TEXT
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
        
    async def user_create(
        self, 
        data: UserStructure
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO users (id, username, age, password, admin, block, user_group, city, address, phone, reg_date, passport, token)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.id,
                data.username,
                data.age,
                data.password,
                data.admin,
                data.block,
                data.user_group,
                data.city,
                data.address,
                data.phone,
                data.reg_date,
                data.passport,
                data.token
            ))
            await db.commit()

            return True
        
    async def user_info(
        self,
        id: int
    ) -> Union[UserStructure, bool]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM users WHERE id = ?', (id,))
            row = await cursor.fetchone()

        if row:
            return UserStructure(
                id=row[0],
                username=row[1],
                age=row[2],
                password=row[3],
                admin=row[4],
                block=row[5],
                user_group=row[6],
                city=row[7],
                address=row[8],
                phone=row[9],
                reg_date=row[10],
                passport=row[11],
                token=row[12]
            )
        return None
    
    async def user_delete(
        self,
        id: int,
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                    DELETE FROM users WHERE id = ?
                ''', (id,)
            )

            await db.commit()

            return True
         
    async def cities_get(
        self
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id, name, description FROM cities')
            rows = await cursor.fetchall()

            if rows:
                cities = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in rows]
                
                return cities
            
            return None
    
    async def city_get(
        self,
        id: int
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM cities WHERE id = ?', (id,))
            
            if cursor:
                return await cursor.fetchone()
            
            return None
        
    async def city_create(
        self,
        data: CityStructure
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO cities (id, username, description)
                VALUES (?, ?, ?)
            ''', (
                data.id,
                data.name,
                data.description
            ))
            await db.commit()

            return True
        
    async def city_delete(
        self,
        id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                    DELETE FROM cities WHERE id = ?
                ''', (id,)
            )
            await db.commit()

            return True
        
if __name__ == '__main__':
    import asyncio

    db = DataBase()

    print(asyncio.run(db.city_get(555)))