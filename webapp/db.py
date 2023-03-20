from flask_sqlalchemy import SQLAlchemy
from typing import Type, cast


db = SQLAlchemy()
Model = cast(Type, db.Model)
