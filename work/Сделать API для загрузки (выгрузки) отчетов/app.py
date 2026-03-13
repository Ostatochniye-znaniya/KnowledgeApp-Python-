from flask import Flask, request, redirect, url_for


app = Flask(__name__)

REPORTS = {}
CHANGEABLE_FIELDS = ("professor", "group", "students", )
SPECIALTY_PROGRAMS = {"CS":("AI",), "SWE":("WEB",)}                                               #тестовые значения
PROFESSORS = ["Ivanov","Black"]
GROUPS = ("A101","A102")

def validation(object):
    checks = {
            "speciality": object["speciality"] in SPECIALTY_PROGRAMS,
            "program": object["program"] in SPECIALTY_PROGRAMS[object["speciality"]],
            "professor": object["professor"] in PROFESSORS,
            "group": object["group"] in GROUPS
        }

    if False not in checks.values():
        passed_count, failed_count = 0,0
        for i in object["students"]:
            if i["passed"] == True:
                passed_count += 1
            else:
                failed_count += 1
                    
        object["passed_count"] = passed_count
        object["failed_count"] = failed_count

        object["status"] = "valid"
        return "valid"
    
    else:
        err_lst = []
        for k, v in checks.items():
            print(k,v)
            if v == False:
                err_lst.append(f'ошибка {k}')
        object["status"] = "invalid"
        object["errors"] = err_lst
        return err_lst

@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == "GET":                                                             
        return REPORTS
    if request.method == "POST":
        if request.json is None:
            return "JSON пуст."
        
        report_obj = request.get_json()

        if validation(report_obj) == "valid":
            REPORTS[report_obj["id"]] = report_obj
            return "done"
        else:
            REPORTS[report_obj["id"]] = report_obj
            return validation(report_obj)                

@app.route('/done', methods = ["GET"])
def to_sign():
    res = []
    for i in REPORTS:
        if REPORTS[i]["status"] in ("valid", "to be signed"):
            REPORTS[i]["status"] = "to be signed"
            res.append(REPORTS[i])
    return {"готовые к подписи отчеты": res}
                                                                     
@app.route('/report/<int:id>', methods = ["GET", "PATCH"])
def get_report(id):
    if request.method == "GET":
        try:
            return REPORTS[id]
        except KeyError:
            return "отчета с введенным id не найдено"
        
    if request.method == "PATCH":
        if request.json is None:
            return "empty json"
        try:
            log = []
            if REPORTS[id]: 
                new_info = request.json
                for i in new_info.keys():
                    if i in CHANGEABLE_FIELDS:
                        REPORTS[id][i] = new_info[i]
                    else:
                        log.append(f'{i} error')
                print(log)
            return validation(REPORTS[id])
                
        except KeyError:
            return "отчета с введенным id не найдено"
