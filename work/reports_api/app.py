from config import Config
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from models import Base, Disciplines, Reports, Departments, StudyProgram, Group


app = Flask(__name__)

engine = create_engine(
    Config.db_url)

Session = sessionmaker(bind = engine)
session = Session()

Base.metadata.create_all(engine)
session.commit()

@app.route('/', methods = ['GET', 'POST'])
def index():
    return "api для отчетов"


@app.route('/reports', methods=['GET'])
def reports():
    if request.method == "GET":
        teacher_id = request.args.get('teacher_id')
        group_number = request.args.get('group_number')
        discipline_id = request.args.get('discipline_id')

        query = session.query(Reports)
        query = query.filter(Reports.is_correct == False)

        if teacher_id:
            query = query.filter(Reports.teacher_id == teacher_id)
        if discipline_id:
            query = query.filter(Reports.discipline_id == discipline_id)
        if group_number:
            query = (
                query
                .join(Disciplines, Reports.discipline_id == Disciplines.discipline_id)
                .join(Departments, Disciplines.department_id == Departments.department_id)
                .join(StudyProgram, Departments.department_id == StudyProgram.department_id)
                .join(Group, StudyProgram.program_id == Group.study_program_id)
                .filter(Group.group_number == group_number)
            )

        results = query.all()
        return [r.to_dict() for r in results]
    
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

@app.route('/report_schema', methods = ["GET"])
def get_report_schema():
    return {
        "report_id": "int",
        "discipline_id": "int",
        "teacher_id": "int",
        "file_path": "str",
        "is_correct": "bool",
        "done_in_paper_form": "bool",
        "done_in_electronic_form": "bool",
        "all_done": "bool",
        "semester_id": "int"
    }
