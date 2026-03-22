import requests

data = {
# "report_id": 1,
"discipline_id": 2,
"teacher_id": 2,
"file_path": "C:/User/reports/report5.txt",
"is_correct":True,
"result_of_attestation": True,                                       
}

requests.post(
"http://127.0.0.1:5000/report",
json=data
)

# requests.patch(
# "http://127.0.0.1:5000/report/01",
# json={
#     "professor" : "Black"
# }
# )