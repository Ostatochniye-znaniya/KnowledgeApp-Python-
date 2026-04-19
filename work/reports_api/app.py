from config import Config
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from models import Base, Users, Reports, Disciplines


app = Flask(__name__)

engine = create_engine(
    Config.db_url, 
    echo = True)

Session = sessionmaker(bind = engine)
session = Session()

Base.metadata.create_all(engine)
session.commit()

@app.route('/', methods = ['GET'])
def index():
    return "api для отчетов"


@app.route('/reports', methods = ['GET', 'POST'])
def reports():
    if request.method == "GET":
        result = session.query(Reports).all()
        return [Reports.to_dict(x) for x in result]
    
    if request.method == "POST":
        data = request.get_json()
        try:
            new_report = Reports(
                report_id = data.get("report_id"),
                discipline_id = data.get("discipline_id"),
                teacher_id = data.get("teacher_id"),
                file_path = data.get("file_path"),
                is_correct = data.get("is_correct"),
                done_in_paper_form = data.get("done_in_paper_form"),
                done_in_electronic_form = data.get("done_in_electronic_form"),
                all_done = data.get("all_done"),
                semester_id = data.get("semester_id")
            )

            session.add(new_report)
            session.commit()
            return {'status':'done'}
        except ValueError:
            return 'Error'

@app.route('/reports/done', methods = ['GET'])
def done():
    result = session.query(Reports).filter(Reports.all_done == True)
    return [Reports.to_dict(x) for x in result]


@app.route('/reports/<int:rep_id>', methods = ["GET", "PATCH"])
def get_report(rep_id):
    if request.method == "GET":
        result = session.query(Reports).filter(Reports.report_id == rep_id)
        return [Reports.to_dict(x) for x in result]
    if request.method == "PATCH":
        data = request.get_json()
        report = session.get(Reports, rep_id)
        if not report:
            return jsonify({"error": "Report not found"}), 404
        try:
            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)
            session.commit()
            return jsonify(report.to_dict())
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 400
        
        