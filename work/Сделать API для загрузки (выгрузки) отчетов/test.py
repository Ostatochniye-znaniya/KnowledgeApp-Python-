import requests

data = {
"id": 1,
"speciality": "CS",
"program": "AI",
"professor": "Ivanov",
"group": "A101"
}

requests.post(
"http://127.0.0.1:5000/report",
json=data
)