import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Hello API")


@app.get("/")
async def hello() -> dict[str, str]:
    """Возвращает приветствие в формате JSON."""
    return {"message": "Hello, FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
