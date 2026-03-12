from flask import Flask, request, redirect, url_for


app = Flask(__name__)

REPORTS = {}
SPECIALTY_PROGRAMS = {"CS":("AI",), "SWE":("WEB",)}                                               #тестовые значения
PROFESSORS = ["Ivanov","Black"]
GROUPS = ("A101","A102")


@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == "GET":                                                            #todo: подправить вывод с счетчиком фейлд и пессд
        return REPORTS
    if request.method == "POST":
        if request.json is None:
            return "JSON пуст."
        
        report_obj = request.json

        checks = {
            "speciality": report_obj["speciality"] in SPECIALTY_PROGRAMS,
            "program": report_obj["program"] in SPECIALTY_PROGRAMS[report_obj["speciality"]],
            "professor":report_obj["professor"] in PROFESSORS,
            "group":report_obj["group"] in GROUPS
        }

        if False not in checks.values():
            passed_count, failed_count = 0,0
            for i in report_obj["students"]:
                if i["passed"] == True:
                    passed_count += 1
                else:
                    failed_count += 1
                    
            report_obj["passed_count"] = passed_count
            report_obj["failed_count"] = failed_count

            report_obj["status"] = "valid"
            REPORTS[report_obj["id"]] = report_obj
            return REPORTS
        else:
            err_lst = []
            for k, v in checks.items():
                print(k,v)
                if v == False:
                    err_lst.append(f'ошибка {k}')
            report_obj["status"] = "invalid"
            report_obj["errors"] = err_lst
            REPORTS[report_obj["id"]] = report_obj
            return err_lst
                                                                       

@app.route('/done', methods = ["GET"])
def to_sign():
    res = []
    for i in REPORTS:
        if REPORTS[i]["status"] in ("valid", "to be signed"):
            REPORTS[i]["status"] = "to be signed"
            res.append(REPORTS[i])
    return {"готовые к подписи отчеты": res}
                                                                     
@app.route('/report/<int:id>', methods = ["GET"])
def get_report(id):
    try:
        return REPORTS[id]
    except KeyError:
        return "отчета с введенным id не существует"