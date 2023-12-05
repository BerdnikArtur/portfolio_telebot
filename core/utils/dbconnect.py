import psycopg_pool
from datetime import datetime, date
import calendar

class UserDatabase:
    # initialization of database for users
    def __init__(self, connector: psycopg_pool.AsyncConnectionPool.connection):
        self.connector = connector

    async def add_user(self, user_name, user_id):
        query = f"INSERT INTO users (user_id, user_name) VALUES ({user_id}, '{user_name}')"
        await self.connector.execute(query)

class ReceptionDatabase:
    #initialization of database for taking receptions
    def __init__(self, connector: psycopg_pool.AsyncConnectionPool.connection):
        self.connector = connector

    async def add_reception(self, datetime, user_id):
        query = f"INSERT INTO receptions (datetime, user_id) VALUES ('{datetime}'::timestamp, {user_id})"
        await self.connector.execute(query)
    
    async def cancel_reception(self, datetime, user_id):
        async with self.connector.cursor() as cur:
            query = f"DELETE FROM receptions WHERE datetime = '{datetime}'::timestamp AND user_id = '{user_id}'"
            await cur.execute(query)

            if cur.rowcount == 0:
                raise Exception('there aren\'t rows within table that can be removed')

    async def get_reception(self, date):
        async with self.connector.cursor() as cur:
            if datetime.now().month > int(date):
                current_year = datetime.now().year + 1
            else:
                current_year = datetime.now().year
            lastday = calendar.monthrange(current_year, int(date))[1]
            min_date = datetime(year=current_year, month=int(date), day=1)
            max_date = datetime(year=current_year, month=int(date), day=lastday)
            query = f"SELECT datetime FROM receptions WHERE datetime >= '{min_date}'::timestamp AND datetime <= '{max_date}'::timestamp"
            await cur.execute(query)
            data = await cur.fetchall()
    
            return data, min_date, max_date
