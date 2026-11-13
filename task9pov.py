from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    URL,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)

database_path = Path(__file__).with_name("lab6.sqlite3")
engine = create_engine(URL.create("sqlite", database=str(database_path)))

metadata = MetaData()
students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("group_name", String(30), nullable=False),
)


class StudentData(BaseModel):
    """Имя и группа студента."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    group_name: str = Field(min_length=1, max_length=30)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Создаёт таблицу при запуске сервера."""
    metadata.create_all(engine)
    yield
    engine.dispose()


app = FastAPI(title="Студенты", lifespan=lifespan)


@app.get("/")
@app.get("/students")
def get_students() -> list[dict[str, int | str]]:
    """Читает список студентов из SQLite."""
    with engine.connect() as connection:
        rows = connection.execute(select(students).order_by(students.c.id))
        return [dict(row) for row in rows.mappings()]


@app.post("/students", status_code=201)
def add_student(data: StudentData) -> dict[str, int | str]:
    """Добавляет студента в SQLite."""
    with engine.begin() as connection:
        result = connection.execute(
            students.insert().values(
                name=data.name,
                group_name=data.group_name,
            )
        )
        primary_key = result.inserted_primary_key
        if primary_key is None:
            raise RuntimeError("Не удалось получить ID студента")

        student_id = primary_key[0]

    return {
        "id": student_id,
        "name": data.name,
        "group_name": data.group_name,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8004)
