#todo : добавить fk на оба поля 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Report(db.Model):
    __tablename__ = 'Report'
    report_id = db.Column(db.Integer, primary_key=True)   
    discipline_id = db.Column(db.Integer, nullable=False)                                      
    teacher_id = db.Column(db.Integer, nullable=False) 
    
    file_path = db.Column(db.String(100))
    is_correct = db.Column(db.Boolean)
    result_of_attestation = db.Column(db.Text, nullable=True)
    
    done_in_paper_form = db.Column(db.Boolean, default=False)
    done_in_electronic_form = db.Column(db.Boolean, default=False)
    all_done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'discipline_id': self.discipline_id,
            'teacher_id': self.teacher_id,
            'file_path': self.file_path,
            'is_correct': self.is_correct,
            'result_of_attestation': self.result_of_attestation,
            'done_in_paper_form': self.done_in_paper_form,
            'done_in_electronic_form': self.done_in_electronic_form,
            'all_done': self.all_done,
        }
