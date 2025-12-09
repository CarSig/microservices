import os
from redis.asyncio import Redis


class RedisConfig:
    HOST = os.getenv('XPOSED_OR_NOT_REDIS_HOST', 'localhost')
    PASSWORD = os.getenv('XPOSED_OR_NOT_REDIS_PASSWORD', None)
    PORT = int(os.getenv('XPOSED_OR_NOT_REDIS_PORT', 6379))
    @property
    def CLIENT(self) -> Redis:
        return Redis(
            host=self.HOST,
            port=self.PORT,
            decode_responses=True
        )

        

class PostgresConfig:
    USER = os.getenv('XPOSED_OR_NOT_POSTGRES_USER', 'postgres')
    DB = os.getenv('XPOSED_OR_NOT_POSTGRES_DB', 'XposedOrNot')
    HOST = os.getenv ('XPOSED_OR_NOT_POSTGRES_HOST', 'localhost')
    PORT = os.getenv('XPOSED_OR_NOT_POSTGRES_PORT', '5432')
    PASSWORD = os.getenv('XPOSED_OR_NOT_POSTGRES_PASSWORD', '')
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.DB}"
        )


class Config:
    REDIS = RedisConfig()
    POSTGRES = PostgresConfig()

config = Config()
