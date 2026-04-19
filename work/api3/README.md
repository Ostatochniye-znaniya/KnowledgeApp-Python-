# Discipline Check API  
Backend‑проект для получения списка дисциплин, доступных группе в рамках активной проверки.  
Реализовано на **FastAPI**, **SQLAlchemy**, **SQLite**.

---

##  Функционал

API предоставляет метод:

```
GET /api/groups/{group_id}/disciplines
```

Он возвращает список дисциплин, которые:

- назначены указанной группе
- входят в активную проверку (Check.status = "Active")
- отмечены в таблицах связей `GroupDiscipline` и `CheckDiscipline`

---

##  Стек технологий

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy**
- **SQLite**
- **Pydantic v2**

---

##  Структура проекта

```
discipline_check/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── api.py
├── seed.py       # (опционально) скрипт создания тестовых данных
│
└── requirements.txt
```

---

##  Установка и запуск проекта

### 1. Клонируйте проект или создайте папку:

```bash
git clone <repo>
cd discipline_check
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
```

### 3. Активируйте окружение

PowerShell:

```bash
.venv\Scriptsactivate
```

Если появится ошибка:

```bash
Set-ExecutionPolicy RemoteSigned
```

### 4. Установите зависимости

```bash
pip install -r requirements.txt
```

Если файла нет:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

---

##  Создание базы данных

SQLite создаётся автоматически при первом запуске, но нужно сформировать таблицы:

В `main.py` уже есть:

```python
Base.metadata.create_all(bind=engine)
```

Это создаёт файлы БД автоматически.

---

##  (Опционально) Добавление тестовых данных

Можно создать данные в базе, выполнив:

```bash
python seed.py
```

Если файла нет, его можно создать так:

```python
from database import SessionLocal
import models

db = SessionLocal()

# test group
g = models.Group(name="ИС-21")
db.add(g)
db.commit()

# disciplines
d1 = models.Discipline(name="Математика")
d2 = models.Discipline(name="Программирование")
db.add_all([d1, d2])
db.commit()

# active check
chk = models.Check(status="Active")
db.add(chk)
db.commit()

# relations
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d1.id))
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d2.id))

db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d1.id))
db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d2.id))

db.commit()
db.close()

print("Test data inserted!")
```

---

##  Запуск сервера

```bash
python -m uvicorn main:app --reload
```

Сервер будет доступен по адресу:

```
http://127.0.0.1:8000
```

---

##  Документация API

После запуска API документация доступна по адресу:

 **http://127.0.0.1:8000/docs**

Можно выполнить запрос прямо из браузера.

---

##  Пример запроса

```
GET http://127.0.0.1:8000/api/groups/1/disciplines
```

### Пример ответа:

```json
[
  { "id": 1, "name": "Математика" },
  { "id": 2, "name": "Программирование" }
]
```

---


Проект реализует:

- Получение дисциплин для группы
- Фильтрация по активной проверке
- Корректная структура проекта
- Полная работоспособность локально
- Возможность интеграции в будущую систему

---


