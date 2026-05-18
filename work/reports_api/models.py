from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, DeclarativeBase, relationship, mapped_column
from typing import List

class Base(DeclarativeBase):
    pass

class Reports(Base):
    __tablename__ = "reports"

    report_id: Mapped[int] = mapped_column(primary_key = True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.discipline_id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    file_path: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    done_in_paper_form: Mapped[bool] = mapped_column(Boolean)
    done_in_electronic_form: Mapped[bool] = mapped_column(Boolean)
    all_done: Mapped[bool] = mapped_column(Boolean)
    semester_id: Mapped[int] = mapped_column(Integer)

    teacher: Mapped["Users"] = relationship(back_populates="reports")
    discipline: Mapped["Disciplines"] = relationship(back_populates="reports")
    def to_dict(self):
        return {
        column.name: getattr(self, column.name)
        for column in self.__table__.columns
    }

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(Integer)
    status_id: Mapped[int] = mapped_column(Integer)
    faculty_id: Mapped[int] = mapped_column(Integer)

    reports: Mapped[list["Reports"]] = relationship(back_populates="teacher")
    disciplines: Mapped[list["Disciplines"]] = relationship(back_populates="teacher")

    def to_dict(self):
        return {
        column.name: getattr(self, column.name)
        for column in self.__table__.columns
    }

class Faculties(Base):
    __tablename__ = "faculties"
    faculty_id: Mapped[int] = mapped_column(primary_key=True)
    faculty_name: Mapped[str] = mapped_column(String(255))
    
    departments: Mapped[List["Departments"]] = relationship(back_populates="faculty")


class Departments(Base):
    __tablename__ = "departments"
    department_id: Mapped[int] = mapped_column(primary_key=True)
    department_name: Mapped[str] = mapped_column(String(255))
    faculty_id: Mapped[int] = mapped_column(ForeignKey('faculties.faculty_id'))
    
    disciplines: Mapped[List["Disciplines"]] = relationship(back_populates="department")
    faculty: Mapped["Faculties"] = relationship(back_populates="departments")
    study_programs: Mapped[List["StudyProgram"]] = relationship(back_populates="department")

class StudyProgram(Base):
    __tablename__ = "StudyPrograms"
    program_id: Mapped[int] = mapped_column(primary_key=True)
    program_name: Mapped[str] = mapped_column(String(255))
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.department_id'))
    cypher_of_direction: Mapped[str] = mapped_column(String(255))

    department: Mapped["Departments"] = relationship(back_populates="study_programs")
    groups: Mapped[List["Group"]] = relationship(back_populates="program")

class Group(Base):
    __tablename__ = "groups"
    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[int] = mapped_column(Integer)

    study_program_id: Mapped[int] = mapped_column(ForeignKey('StudyPrograms.program_id'))

    program: Mapped["StudyProgram"] = relationship(back_populates="groups")

class Disciplines(Base):
    __tablename__ = "disciplines"

    discipline_id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(255))
    responsible_teacher_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.department_id"))

    teacher: Mapped["Users"] = relationship(back_populates="disciplines")
    reports: Mapped[list["Reports"]] = relationship(back_populates="discipline")
    department: Mapped["Departments"] = relationship(back_populates="disciplines")
    
    def to_dict(self):
        return {
        column.name: getattr(self, column.name)
        for column in self.__table__.columns
    }