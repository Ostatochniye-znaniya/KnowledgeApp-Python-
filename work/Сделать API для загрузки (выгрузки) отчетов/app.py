from flask import Flask, request, redirect, url_for


app = Flask(__name__)

REPORTS = {}
SPECIALTIES = ()
PROGRAMS = ()
PROFESSORS = []
GROUPS = ()


@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == "GET":                                                            #получить/вернуть запрос
        ...
    if request.method == "POST":
        report = request.form.get("data")
        check = report.speciality in SPECIALTIES and report.program in PROGRAMS \
        and report.professor in PROFESSORS and request.group in GROUPS

        if check:
            REPORTS[report["id"]] = report
        else:
            return redirect(url_for('report_error'))
                                                                      
@app.route('/report_error', methods = ["GET, POST"])
def report_error():                                                                        #выкинуть ошибку о неверном заполнении
    ...

@app.route('/done', methods = ["POST"])
def signed():
    ...                                                                                 #повесить флаг что готово к печати
