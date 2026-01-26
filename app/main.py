from fastapi import FastAPI
from app.config import settings
from app.services.groq.connection import test_groq_connection, test_chat_groq_connection
from app.services.elasticsearch.connection import test_elasticsearch_connection
from app.services.redis.connection import test_redis_connection
from app.services.postgres.connection import test_postgres_connection

app = FastAPI()

@app.get("/test")
def test_connections():
   return {

        "groq_chat" : test_chat_groq_connection(),
        "elasticsearch" : test_elasticsearch_connection(),
        "redis" : test_redis_connection(),
        "postgres" : test_postgres_connection()
    }