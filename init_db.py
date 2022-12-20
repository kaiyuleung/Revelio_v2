from game import db
from game import app
from game.models.user import User
from werkzeug.security import generate_password_hash
from tool import get_random_string, get_random_avatar

users = [
    { 
        'username': "s", 
        'email': "s@s.com",
        'password': "s", 
        'wins': 4,
        'wins_as_hunter': 3,
        'games_played': 10
    },
    { 
        'username': "kai", 
        'email': "kyl1g16.ecs@gmail.com",
        'password': "kaitheguy", 
        'wins': 96,
        'wins_as_hunter': 70,
        'games_played': 100
    },
    { 
        'username': "ocr", 
        'email': "oscr1998@outlook.com",
        'password': "oliwiththetrolley", 
        'wins': 98,
        'wins_as_hunter': 88,
        'games_played': 100
    },
    { 
        'username': "thamiem", 
        'email': "thamiem2000@gmail.com",
        'password': "thamiemwiththeskincareroutine", 
        'wins': 45,
        'wins_as_hunter': 1,
        'games_played': 100
    },
    { 
        'username': "matt", 
        'email': "matthieuchan96@gmail.com",
        'password': "mattwiththehat", 
        'wins': 66,
        'wins_as_hunter': 24,
        'games_played': 66
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for user in users:
        db.session.add(User(
            username = user['username'],
            email = user['email'], 
            password = generate_password_hash(user["password"], method='sha256'),
            OTP = get_random_string(),
            wins = user['wins'],
            wins_as_hunter = user['wins_as_hunter'],
            games_played = user['games_played'],
            avatar_url = get_random_avatar(),
        ))
    db.session.commit()
