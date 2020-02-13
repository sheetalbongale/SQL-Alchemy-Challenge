from flask import Flask , jsonify, resuest, render_template
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
import datetime as dt
#######################################################
#                 Database Setup
#######################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Resources/hawaii.sqlite"
db = SQLAlchemy(app)