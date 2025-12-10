import os
from redis.asyncio import Redis
# config settings for redis and postgres!
class RedisConfig:
    HOST = os.getenv('REDIS_HOST', 'localhost')
    PASSWORD = os.getenv('REDIS_PASSWORD', None)
    PORT = int(os.getenv('REDIS_PORT', 6379))
    CLIENT = Redis(host=HOST, port=PORT, decode_responses=True)

        

class PostgresConfig:
    USER = os.getenv('POSTGRES_USER', 'postgres')
    DB = os.getenv('POSTGRES_DB', 'XposedOrNot')
    HOST = os.getenv ('POSTGRES_HOST', 'localhost')
    PORT = os.getenv('POSTGRES_PORT', '5432')
    PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.DB}"
        )


class Config:
    REDIS = RedisConfig()
    POSTGRES = PostgresConfig()
    a = 50

config = Config()
