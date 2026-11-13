from flask import Flask, render_template_string

app = Flask(__name__)

technologies = [
    {"name": "Python", "description": "Язык программирования"},
    {"name": "Flask", "description": "Веб-фреймворк"},
    {"name": "FastAPI", "description": "Фреймворк для создания API"},
]

PAGE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Таблица технологий</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #555; padding: 10px; }
        th { background: #e8eef5; }
    </style>
</head>
<body>
    <h1>Технологии веб-программирования</h1>
    <table>
        <thead><tr><th>Название</th><th>Описание</th></tr></thead>
        <tbody>
        {% for item in technologies %}
            <tr><td>{{ item.name }}</td><td>{{ item.description }}</td></tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""


@app.get("/")
def index() -> str:
    """Формирует HTML-таблицу из списка данных."""
    return render_template_string(PAGE, technologies=technologies)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
