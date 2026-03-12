from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == "GET":                                                            #получить/вернуть запрос
        ...
    if request.method == "POST":
        ...


@app.route('/report_error', methods = ["GET, POST"])
def report_error():                                                                        #выкинуть ошибку о неверном заполнении
    ...

@app.route('/done', methods = ["POST"])
def signed():
    ...                                                                                 #повесить флаг что готово к печати
