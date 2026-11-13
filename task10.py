import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Список задач")


class TaskData(BaseModel):
    """Данные для создания задачи."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)
    completed: bool = False


class Task(TaskData):
    """Задача с идентификатором."""

    id: int


tasks = [Task(id=1, title="Выполнить лабораторную №6")]


@app.get("/")
@app.get("/tasks")
async def get_tasks() -> list[Task]:
    """Возвращает список задач."""
    return tasks


@app.post("/tasks", status_code=201)
async def add_task(data: TaskData) -> Task:
    """Добавляет задачу и возвращает её."""
    task = Task(
        id=len(tasks) + 1,
        title=data.title,
        completed=data.completed,
    )
    tasks.append(task)
    return task


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
