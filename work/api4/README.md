# Discipline Check API

Backend‑проект на **FastAPI + SQLAlchemy + SQLite**, предназначенный для:

 получения доступных дисциплин для конкретной группы в рамках активной проверки
 сохранения выбора дисциплин (две дисциплины + проверка «своя/чужая кафедра»)
 получения всех сохранённых выборов

Проект полностью локальный и готов для интеграции в будущую систему.

---

#  Функциональность

## 1. Получение доступных дисциплин
```
GET /api/groups/{group_id}/disciplines
```
Возвращает список дисциплин, доступных для указанной группы в рамках **активной проверки**.

## 2. Сохранение выбора дисциплин
```
POST /api/choices
```
Принимает:
- ID группы
- ID дисциплины 1
- ID дисциплины 2
- «своя/чужая кафедра» для каждой дисциплины

Сохраняет выбор в таблице `choices`.

## 3. Получение всех выборов
```
GET /api/choices
```
Возвращает список всех записей в таблице `choices`.

---

#  Стек 

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy ORM**
- **SQLite**
- **Pydantic v2**

---

#  Структура проекта

```
api_project/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── api.py
├── seed.py
├── README.md
└── requirements.txt
```

---

#  Установка и запуск

## 1. Создать виртуальное окружение
```powershell
python -m venv venv
```

## 2. Активировать окружение
PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Если появится ошибка про запрет выполнения скриптов:
```powershell
Set-ExecutionPolicy RemoteSigned
```
Выбрать **A** (Yes to all).

## 3. Установить зависимости
```powershell
pip install -r requirements.txt
```
Если файла нет:
```powershell
pip install fastapi uvicorn sqlalchemy pydantic
```

---

#  Инициализация базы данных

SQLite создаётся автоматически при запуске приложения.

Но перед этим желательно заполнить тестовые данные:
```powershell
python seed.py
```

---

#  Запуск сервера

```powershell
python -m uvicorn main:app --reload
```

Сервер запустится по адресу:
```
http://127.0.0.1:8000
```

Swagger документация:
```
http://127.0.0.1:8000/docs
```

---

#  Тестовые запросы

## 1. Получение доступных дисциплин
```
GET /api/groups/1/disciplines
```
Пример ответа:
```json
[
  { "id": 1, "name": "Математика" },
  { "id": 2, "name": "Программирование" }
]
```

## 2. Сохранение выбора
```
POST /api/choices
```
Body:
```json
{
  "group_id": 1,
  "discipline_id_1": 1,
  "discipline_id_2": 2,
  "is_own_department_1": true,
  "is_own_department_2": false
}
```
Ответ:
```json
{
  "id": 1,
  "group_id": 1,
  "discipline_id_1": 1,
  "discipline_id_2": 2,
  "is_own_department_1": true,
  "is_own_department_2": false
}
```

## 3. Получение всех выборов
```
GET /api/choices
```
Ответ (пример):
```json
[
  {
    "id": 1,
    "group_id": 1,
    "discipline_id_1": 1,
    "discipline_id_2": 2,
    "is_own_department_1": true,
    "is_own_department_2": false
  }
]
```

---


API реализует:
- получение доступных дисциплин
- сохранение выбора (2 дисциплины + проверка кафедры)
- просмотр всех выборов
- структура чистая, легко расширяемая

---

