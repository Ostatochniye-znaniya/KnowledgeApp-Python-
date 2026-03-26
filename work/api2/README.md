
# **Group Status API**

**API‑сервис на FastAPI** для управления статусами групп с использованием **SQLite** и **SQLAlchemy**.  
Проект разработан в рамках задания:
 **Реализовать метод, принимающий массив данных (id + status) и сохраняющий/обновляющий статусы групп в базе данных.**

---
## **Цель проекта**
Создать REST API, которое позволяет:
-  Принимать массив групп и их статусов  
-  Обновлять статус уже существующих групп  
-  Автоматически создавать группы, если их ещё нет в БД  
-  Получать список всех групп  

---
## **Стек технологий**
| Технология   | Описание |
|--------------|----------|
| **FastAPI**  | Высокопроизводительный фреймворк для API |
| **SQLAlchemy** | ORM для работы с базами данных |
| **SQLite** | Локальная лёгковесная база данных |
| **Pydantic** | Валидация входных данных |

---
## **Требования**
- Python **3.10+** (проект тестировался на Python 3.13)
- pip

---
## **Установка и запуск**
### 1 Клонирование проекта
```bash
cd path/to/project
```

### 2 Создание виртуального окружения
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
echo source venv/bin/activate
```

### 3 Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4 Запуск приложения
```bash
python -m uvicorn main:app --reload
```
Приложение будет доступно по адресу: **http://localhost:8000**

###  Документация API
- Swagger UI → **http://localhost:8000/docs**
- ReDoc → **http://localhost:8000/redoc**

---
##  **API Endpoints**
###  GET /groups
Получить список всех групп.
```json
[
  {"id": 1, "status": "active"},
  {"id": 2, "status": "inactive"}
]
```

###  POST /update-status
Обновить или создать группы.
```json
[
  {"id": 1, "status": "active"},
  {"id": 2, "status": "pending"}
]
```
Ответ:
```json
{"message": "Statuses updated successfully"}
```

---
##  **Структура проекта**
```
project/
├── main.py
├── models.py
├── database.py
├── requirements.txt
└── test.db
```

---
##  **Описание файлов**
- **main.py** — маршруты и логика API
- **models.py** — модель Group
- **database.py** — подключение к БД
- **requirements.txt** — зависимости

---
##  **Особенности проекта**
- ✔ Автоматическое создание таблиц
- ✔ Валидация входных данных
- ✔ Один endpoint для создания/обновления
- ✔ PostgreSQL можно легко подключить
- ✔ Swagger документация встроена

---
##  **Примеры использования**
### cURL
```bash
curl -X GET "http://localhost:8000/groups"

curl -X POST "http://localhost:8000/update-status"   -H "Content-Type: application/json"   -d '[{"id":1,"status":"active"},{"id":2,"status":"pending"}]'
```

### Python
```python
import requests
print(requests.get("http://localhost:8000/groups").json())
print(requests.post("http://localhost:8000/update-status", json=[{"id":1,"status":"active"}]).json())
```

