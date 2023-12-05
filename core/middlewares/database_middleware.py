from typing import Dict, Any, Callable, Awaitable
from aiogram.types import Message
from aiogram import BaseMiddleware
from psycopg_pool import AsyncConnectionPool

from core.utils.dbconnect import UserDatabase, ReceptionDatabase

class UsersDatabaseMiddleware(BaseMiddleware):
    def __init__(self, connector: AsyncConnectionPool):
        super().__init__()
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        async with self.connector.connection() as connect:
            data['request'] = UserDatabase(connect)
            return await handler(event, data)

class ReceptionDatabaseMiddleware(BaseMiddleware):
    def __init__(self, connector: AsyncConnectionPool):
        super().__init__()
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ):
        async with self.connector.connection() as connect:
            data['reception'] = ReceptionDatabase(connect)
            return await handler(event, data)