from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class Server:
    host: str
    user: str
    password: str
    db_name: str

@dataclass
class Settings:
    bots: Bots
    server: Server

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        Bots(
            bot_token=env.str('API_TOKEN'),
            admin_id=env.str('ADMIN_ID')
        ),
        Server(
            host=env.str('HOST'),
            user=env.str('DBUSER'),
            password=env.str('PASSWORD'),
            db_name=env.str('DBNAME')
        )
    )

settings = get_settings('config')
print(settings)