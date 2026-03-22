# app.py
from flask import Flask, request, jsonify
from models import db, Report  # db = SQLAlchemy()


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
