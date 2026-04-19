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