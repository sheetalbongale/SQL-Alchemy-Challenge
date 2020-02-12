from flask import Flask , jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime as dt
#######################################################
#                 Database Setup
#######################################################
