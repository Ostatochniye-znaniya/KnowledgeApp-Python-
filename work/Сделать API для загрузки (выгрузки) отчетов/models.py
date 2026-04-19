from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import declarative_base, Mapped, MappedColumn, DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = MappedColumn(primary_key = True)
    discipline_id: Mapped[int] = MappedColumn(ForeignKey("disciplines.id"))
    teacher_id: Mapped[int] = MappedColumn(ForeignKey("users.id"))
    file_path: Mapped[str] = MappedColumn(String(255))
    is_correct: Mapped[bool] = MappedColumn(Boolean)
    done_in_paper_form: Mapped[bool] = MappedColumn(Boolean)
    done_in_electronic_form: Mapped[bool] = MappedColumn(Boolean)
    all_done: Mapped[bool] = MappedColumn(Boolean)
    semester_id: Mapped[int] = MappedColumn(Integer)

    teacher: Mapped["Users"] = relationship(back_populates="reports")
    discipline: Mapped["Disciplines"] = relationship(back_populates="reports")

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = MappedColumn(primary_key = True)
    name: Mapped[str] = MappedColumn(String(255))
    email: Mapped[str] = MappedColumn(String(255))
    password: Mapped[str] = MappedColumn(String(255))
    role_id: Mapped[int] = MappedColumn(Integer)
    status_id: Mapped[int] = MappedColumn(Integer)
    faculty_id: Mapped[int] = MappedColumn(Integer)

    reports: Mapped[list["Reports"]] = relationship(back_populates="teacher")
    disciplines: Mapped[list["Disciplines"]] = relationship(back_populates="teacher")

class Disciplines(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = MappedColumn(primary_key = True)
    name: Mapped[str] = MappedColumn(String(255))
    responsible_teacher_id: Mapped[int] = MappedColumn(ForeignKey("users.id"))

    teacher: Mapped["Users"] = relationship(back_populates="disciplines")
    reports: Mapped[list["Reports"]] = relationship(back_populates="discipline")