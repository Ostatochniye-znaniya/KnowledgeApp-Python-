from config import Config
from flask import Flask, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from models import Base, Disciplines, Reports, Departments, StudyProgram, Group


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = Config.MAX_FILE_SIZE
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

ALLOWED_MIMETYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/reports/<int:rep_id>/upload', methods=["POST"])
def upload_report(rep_id):
    teacher_id = request.form.get("teacher_id")

    if not teacher_id:
        return jsonify({"error": "teacher_id is required"}), 400

    try:
        teacher_id = int(teacher_id)
    except ValueError:
        return jsonify({"error": "teacher_id must be int"}), 400

    report = session.get(Reports, rep_id)

    if not report:
        return jsonify({"error": "Report not found"}), 404

    if report.teacher_id != teacher_id:
        return jsonify({"error": "This report is not for this teacher"}), 403

    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "File name is empty"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Wrong file extension"}), 400

    if file.mimetype not in ALLOWED_MIMETYPES:
        return jsonify({"error": "Wrong file type"}), 400

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > Config.MAX_FILE_SIZE:
        return jsonify({"error": "File is too large"}), 400

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    old_name = secure_filename(file.filename)
    extension = old_name.rsplit(".", 1)[1].lower()

    new_name = f"report_{rep_id}_{uuid.uuid4().hex}.{extension}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, new_name)

    file.save(save_path)

    report.file_path = save_path
    report.done_in_electronic_form = True

    if report.done_in_paper_form and report.done_in_electronic_form:
        report.all_done = True

    session.commit()

    return jsonify({
        "status": "uploaded",
        "report_id": report.report_id,
        "file_path": report.file_path
    }), 201

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
