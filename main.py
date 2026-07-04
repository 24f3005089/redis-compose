from fastapi import FastAPI
import redis
import os

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/hit/{key}")
def hit(key: str):
    count = redis_client.incr(key)
    return {
        "key": key,
        "count": count
    }

@app.get("/count/{key}")
def count(key: str):
    value = redis_client.get(key)

    return {
        "key": key,
        "count": int(value) if value else 0
    }

@app.get("/healthz")
def health():
    try:
        redis_client.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except:
        return {
            "status": "error",
            "redis": "down"
        }
