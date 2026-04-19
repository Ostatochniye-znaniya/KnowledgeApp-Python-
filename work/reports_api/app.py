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

Base.metadata.create_all(engine)

@app.route('/', methods = ['GET'])
def index():
    return "api для отчетов"
