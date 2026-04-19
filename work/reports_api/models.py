from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, DeclarativeBase, relationship, mapped_column

class Base(DeclarativeBase):
    pass

class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key = True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    file_path: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    done_in_paper_form: Mapped[bool] = mapped_column(Boolean)
    done_in_electronic_form: Mapped[bool] = mapped_column(Boolean)
    all_done: Mapped[bool] = mapped_column(Boolean)
    semester_id: Mapped[int] = mapped_column(Integer)

    teacher: Mapped["Users"] = relationship(back_populates="reports")
    discipline: Mapped["Disciplines"] = relationship(back_populates="reports")

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(Integer)
    status_id: Mapped[int] = mapped_column(Integer)
    faculty_id: Mapped[int] = mapped_column(Integer)

    reports: Mapped[list["Reports"]] = relationship(back_populates="teacher")
    disciplines: Mapped[list["Disciplines"]] = relationship(back_populates="teacher")

class Disciplines(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(255))
    responsible_teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    teacher: Mapped["Users"] = relationship(back_populates="disciplines")
    reports: Mapped[list["Reports"]] = relationship(back_populates="discipline")