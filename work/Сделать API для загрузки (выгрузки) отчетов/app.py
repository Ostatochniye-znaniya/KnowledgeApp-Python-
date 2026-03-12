from flask import Flask, request, redirect, url_for


app = Flask(__name__)

REPORTS = {}
SPECIALTIES = ("CS",)                                               #тестовые значения
PROGRAMS = ("AI",)
PROFESSORS = ["Ivanov",]
GROUPS = ("A101",)


@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == "GET":                                                            #получить/вернуть запрос
        return REPORTS
    if request.method == "POST":
        report_obj = request.json
        check = report_obj["speciality"] in SPECIALTIES and report_obj["program"] in PROGRAMS \
        and report_obj["professor"] in PROFESSORS and report_obj["group"] in GROUPS

        if check:
            REPORTS[report_obj["id"]] = report_obj
            print(REPORTS)
            return REPORTS
        else:
            return REPORTS
                                                                      
@app.route('/report_error', methods = ["GET"])
def report_error():
    ...

@app.route('/done', methods = ["GET"])
def signed():
    ...                                                                                 #повесить флаг что готово к печати
