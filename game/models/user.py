from ..database.db import db
import sqlalchemy as sa
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(40), unique=True, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    OTP = sa.Column(sa.String(8), nullable=False)
    wins = sa.Column(sa.Integer)
    wins_as_hunter = sa.Column(sa.Integer)
    games_played = sa.Column(sa.Integer)
    avatar_url = sa.Column(sa.String)

