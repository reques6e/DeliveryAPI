import aiosqlite

from typing import Optional, Union

from pages.auth.models import UserStructure, UserUpdate
from pages.city.models import CityStructure, CityUpdate
from pages.point.models import PointStructure, PointUpdate
from pages.order.models import OrderStructure, OrderUpdate


class DataBase:
    def __init__(self) -> None:
        self.db_path = 'src/database/db.db'

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
                CREATE TABLE IF NOT EXISTS point (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    city_id INTEGER
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

            await db.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    city_id INTEGER,
                    point_id INTEGER,
                    description TEXT,
                    img TEXT,
                    date INTEGER,
                    active INTEGER
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
                return [{'id': row[0], 'name': row[1], 'description': row[2]} for row in rows]
                            
            return None
    
    async def city_get(
        self,
        id: int
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id, name, description FROM cities WHERE id = ?', (id,))
            row = await cursor.fetchone()

            if row:
                return [{'id': row[0], 'name': row[1], 'description': row[2]}]
            
            return None
        
    async def city_create(
        self,
        data: CityStructure
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO cities (id, name, description)
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

    async def point_get(
        self,
        id: int
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM point WHERE id = ?', (id,))
            
            row = await cursor.fetchone()
            if row:
                return [{'id': row[0], 'name': row[1], 'description': row[2], 'city_id': row[3]}]
            
            return None
         
    async def points_get(
        self
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id, name, description, city_id FROM point')
            rows = await cursor.fetchall()

            if rows:
                return [{'id': row[0], 'name': row[1], 'description': row[2], 'city_id': row[3]} for row in rows]
                            
            return None
        
    async def point_create(
        self,
        data: PointStructure
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO point (id, name, description, city_id)
                VALUES (?, ?, ?, ?)
            ''', (
                data.id,
                data.name,
                data.description,
                data.city_id
            ))
            await db.commit()

            return True
    
    async def point_delete(
        self,
        id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                    DELETE FROM point WHERE id = ?
                ''', (id,)
            )
            await db.commit()

            return True
        
    async def find_point_by_city(
        self,
        city_id: int
    ) -> Union[bool, None]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id FROM point WHERE city_id = ?', (city_id,))
            
            rows = await cursor.fetchall()
            
            if rows:
                return rows
            
            return None

    async def get_users_by_city(
        self,
        city_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id FROM users WHERE city = ?', (city_id,))
            
            rows = await cursor.fetchall()
            
            if rows:
                return rows
            
            return None

    async def update_city_in_users(
        self,
        old_city_id: int,
        new_city_id: int
    ) -> Union[bool, None]:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE users SET city = ? WHERE city = ?', (new_city_id, old_city_id))
            
            await db.commit()
            
            return True   
        
    async def point_update(
        self, 
        data: PointUpdate
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            update_data = data.dict(exclude_unset=True)
            id = data.id
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])

            values = list(update_data.values())
            values.append(id)

            await db.execute(
                f"UPDATE point SET {set_clause} WHERE id = ?", values)
            await db.commit()

            return True
        
    async def city_update(
        self, 
        data: CityUpdate
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            update_data = data.dict(exclude_unset=True)
            id = data.id
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])

            values = list(update_data.values())
            values.append(id)

            await db.execute(
                f"UPDATE cities SET {set_clause} WHERE id = ?", values)
            await db.commit()

            return True

    async def auth_get(
        self
    ):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id, username, age, password, admin, block, user_group, city, address, phone, reg_date, passport, token FROM users')
            rows = await cursor.fetchall()

            if rows:
                return [{'id': row[0], 'username': row[1], 'age': row[2], 'password': row[3], 'admin': row[4], 'block': row[5], 'user_group': row[6], 'city': row[7], 'address': row[8], 'phone': row[9], 'reg_date': row[10], 'passport': row[11], 'token': row[12]} for row in rows]
                                
            return None

        
    async def auth_update(
        self, 
        data: UserUpdate
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            update_data = data.dict(exclude_unset=True)
            id = data.id
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])

            values = list(update_data.values())
            values.append(id)

            await db.execute(
                f"UPDATE users SET {set_clause} WHERE id = ?", values)
            await db.commit()

            return True

    async def order_get(
        self,
        id: int
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM orders WHERE id = ?', (id,))
            
            row = await cursor.fetchone()
            if row:
                return [{'id': row[0], 'city_id': row[1], 'point_id': row[2], 'description': row[3], 'img': row[4], 'date': row[5], 'active': row[6]}]
            
            return None

    async def orders_get(
        self
    ): 
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id, city_id, point_id, description, img, date, active FROM orders')
            rows = await cursor.fetchall()

            if rows:
                return [{'id': row[0], 'city_id': row[1], 'point_id': row[2], 'description': row[3], 'img': row[4], 'date': row[5], 'active': row[6]} for row in rows]
                            
            return None
                     
    async def order_create(
        self,
        data: OrderStructure
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO orders (id, city_id, point_id, description, img, date, active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.id,
                data.city_id,
                data.point_id,
                data.description,
                data.img,
                data.date,
                data.active
            ))
            await db.commit()

            return True

    async def order_update(
        self, 
        data: OrderUpdate
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            update_data = data.dict(exclude_unset=True)
            id = data.id
            set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])

            values = list(update_data.values())
            values.append(id)

            await db.execute(
                f"UPDATE orders SET {set_clause} WHERE id = ?", values)
            await db.commit()

            return True
                
    async def order_delete(
        self,
        id: int,
    ) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                    DELETE FROM orders WHERE id = ?
                ''', (id,)
            )

            await db.commit()

            return True
        
    async def get_orders_by_city(
        self,
        city_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id FROM orders WHERE city_id = ?', (city_id,))
            
            rows = await cursor.fetchall()
            
            if rows:
                return rows
            
            return None
        
    async def get_orders_by_point(
        self,
        point_id: int
    ):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT id FROM orders WHERE point_id = ?', (point_id,))
            
            rows = await cursor.fetchall()
            
            if rows:
                return rows
            
            return None