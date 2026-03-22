# app.py
from flask import Flask, request, jsonify
from models import db, Report


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2008@localhost:5432/reports_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

REPORTS = {}
CHANGEABLE_FIELDS = ("discipline_id", "teacher_id", "file_path", "is_correct", "result_of_attestation")

@app.route('/')
def index():
    return "api для отчетов"

@app.route('/report', methods=["GET", "POST"])
def report():
    if request.method == "GET":
        reports = Report.query.all()
        return jsonify([
            {
                "report_id": r.report_id,
                "discipline_id": r.discipline_id,
                "teacher_id": r.teacher_id,
                "file_path": r.file_path,
                "is_correct": r.is_correct,
                "result_of_attestation": r.result_of_attestation
            }
            for r in reports
        ])
    
    if request.method == "POST":
        data = request.get_json()
        new_report = Report(
            # report_id = data.get("report_id"),
            discipline_id=data.get("discipline_id"),
            teacher_id=data.get("teacher_id"),
            file_path=data.get("file_path"),
            is_correct=data.get("is_correct", False),
            result_of_attestation=data.get("result_of_attestation")
        )

        db.session.add(new_report)
        db.session.commit()
        return jsonify({"message": "Report created", "id": new_report.report_id}), 201
    
# @app.route('/done', methods = ["GET"])                                                                УТОЧНИТЬ ПО ПОЛЮ СТАТУС
# def to_sign():
#     res = []
#     for i in REPORTS:
#         if REPORTS[i]["status"] in ("valid", "to be signed"):
#             REPORTS[i]["status"] = "to be signed"
#             res.append(REPORTS[i])
#     return {"готовые к подписи отчеты": res}
                                                                     
@app.route('/report/<int:id>', methods = ["GET", "PATCH"])            
def get_report(id):
    report = Report.query.get(id)
    if request.method == "GET":
        try:
            return report.to_dict()

        except KeyError:
            return "отчета с введенным id не найдено"
        
    if request.method == "PATCH":
        data = request.get_json()
        if data is None:
            return {"error": "empty json"}, 400
        
        log = []
        for field, value in data.items():
            if field in CHANGEABLE_FIELDS:
                if hasattr(report, field):
                    setattr(report, field, value)
                else:
                    log.append(f'{field} - атрибут не существует')
            else:
                log.append(f'{field} - поле не в списке изменяемых')
        
        db.session.add(report)
        db.session.commit()
        
        return {
            "message": "отчет обновлен",
            "warnings": log if log else None,
            "report": report.to_dict()
        }
