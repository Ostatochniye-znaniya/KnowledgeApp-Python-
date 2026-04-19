from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    disciplines = relationship("GroupDiscipline", back_populates="group")


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Check(Base):
    __tablename__ = "checks"
    id = Column(Integer, primary_key=True, index=True)
    check_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    disciplines = relationship("CheckDiscipline", back_populates="check")


class GroupDiscipline(Base):
    __tablename__ = "group_disciplines"
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), primary_key=True)

    group = relationship("Group", back_populates="disciplines")
    discipline = relationship("Discipline")


class CheckDiscipline(Base):
    __tablename__ = "check_disciplines"
    check_id = Column(Integer, ForeignKey("checks.id"), primary_key=True)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), primary_key=True)

    check = relationship("Check", back_populates="disciplines")
    discipline = relationship("Discipline")


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)

    group_id = Column(Integer, ForeignKey("groups.id"))
    discipline_id_1 = Column(Integer, ForeignKey("disciplines.id"))
    discipline_id_2 = Column(Integer, ForeignKey("disciplines.id"))

    is_own_department_1 = Column(Integer)  # 1 — своя, 0 — чужая
    is_own_department_2 = Column(Integer)

    group = relationship("Group")
    discipline1 = relationship("Discipline", foreign_keys=[discipline_id_1])
    discipline2 = relationship("Discipline", foreign_keys=[discipline_id_2])