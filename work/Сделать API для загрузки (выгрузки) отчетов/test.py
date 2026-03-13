import requests

data = {
"id": 1,
"speciality": "CS",
"program": "AI",
"professor": "Ivanov",
"group": "A101",
"students": [
    {
        "name" : "Ivan Petrov",
        "grade": 5,
        "test_grade": 2,
        "passed": False
    },
    {
        "name" : "Oleg Gazanov",
        "grade": 3,
        "test_grade": 3,
        "passed": True
    }
],
"unallowed": 3,
"skipped": 2                                         
}

requests.post(
"http://127.0.0.1:5000/report",
json=data
)

requests.patch(
"http://127.0.0.1:5000/report/01",
json={
    "professor" : "Black"
}
)