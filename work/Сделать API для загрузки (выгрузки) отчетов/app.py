from flask import Flask, request, redirect, url_for


app = Flask(__name__)

REPORTS = {}
SPECIALTIES = ("CS","SWE")                                               #тестовые значения
PROGRAMS = ("AI","WEB")
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
        report_obj = request.json

        checks = {
            "speciality": report_obj["speciality"] in SPECIALTIES,
            "program": report_obj["program"] in PROGRAMS,
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

            REPORTS[report_obj["id"]] = report_obj
            return REPORTS
        else:
            err_lst = []
            for k, v in checks.items():
                print(k,v)
                if v == False:
                    err_lst.append(f'{k} нет в списке')
            return err_lst
                                                                       
@app.route('/report_error', methods = ["GET"])
def report_error():
    ...

@app.route('/done', methods = ["GET"])
def signed():
    ...                                                                                 #повесить флаг что готово к печати
