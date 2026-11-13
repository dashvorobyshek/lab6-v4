from itertools import count

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Заметки")


class NoteData(BaseModel):
    """Заголовок и текст заметки."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1)
    text: str = Field(min_length=1)


class Note(NoteData):
    """Заметка с номером."""

    id: int


notes = {
    1: Note(id=1, title="План", text="Проверить лабораторную работу")
}
identifiers = count(2)


@app.get("/")
@app.get("/notes")
async def get_notes() -> list[Note]:
    """Показывает список заметок."""
    return list(notes.values())


@app.post("/notes", status_code=201)
async def add_note(data: NoteData) -> Note:
    """Добавляет новую заметку."""
    note = Note(id=next(identifiers), title=data.title, text=data.text)
    notes[note.id] = note
    return note


@app.put("/notes/{note_id}")
async def edit_note(note_id: int, data: NoteData) -> Note:
    """Заменяет заголовок и текст существующей заметки."""
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    note = Note(id=note_id, title=data.title, text=data.text)
    notes[note_id] = note
    return note


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int) -> dict[str, str]:
    """Удаляет заметку по номеру."""
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    del notes[note_id]
    return {"message": "Заметка удалена"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
